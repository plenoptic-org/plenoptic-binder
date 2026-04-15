#!/usr/bin/env python3

import re
import pathlib
import sys

version = sys.argv[1]
nb_file = pathlib.Path(sys.argv[2])
orig_path = sys.argv[3]
if version == "main":
    docs_url = "https://docs.plenoptic.org/docs/branch/main/"
else:
    docs_url = f"https://docs.plenoptic.org/docs/tag/{version}/"
api_url = docs_url + "api/generated/"
nb_url = docs_url + orig_path.split("docs/")[-1].replace(".md", ".html")

nb_txt = nb_file.read_text()

warning = f""":::{{admonition}} Potential rendering issues
:class: important

This notebook has been converted from our documentation and some of the links or visual
elements may not render correctly. See [original notebook online]({nb_url}) if things
look weird.

:::"""

nb_txt = re.sub(r":::{admonition} Run this notebook yourself.*?:::", warning, nb_txt, flags=re.DOTALL)

for sphinx_domain, tilde, match in re.findall(r"({[A-z]+?})`(~?)([a-z-A-Z_\.]+?)`", nb_txt):
    if tilde:
        repl_txt = match.split(".")[-1]
    else:
        repl_txt = match
    if match.startswith("plenoptic"):
        repl_url = f"{api_url}{match}.html"
        nb_txt = nb_txt.replace(f"{sphinx_domain}`{tilde}{match}`", f"[`{repl_txt}`]({repl_url})")
    else:
        nb_txt = nb_txt.replace(f"{sphinx_domain}`{tilde}{match}`", f"`{repl_txt}`")

nb_file.write_text(nb_txt)
