#!/usr/bin/env python3
"""Used by check_versions.yml workflow to find supported python versions."""

import re
import sys

import tomllib

with open(sys.argv[1], "rb") as f:
    plenoptic_toml = tomllib.load(f)
with open(sys.argv[2], "rb") as f:
    binder_toml = tomllib.load(f)

# this is a dictionary
binder_deps = {}
binder_extras = {}
for k, v in binder_toml["packages"].items():
    if isinstance(v, str):
        binder_deps[k] = v
    else:
        if "extras" in v:
            binder_extras[k] = v["extras"]
        binder_deps[k] = v["version"]


plenoptic_deps = plenoptic_toml["project"]["dependencies"]
plenoptic_deps += plenoptic_toml["project"]["optional-dependencies"]["docs"]
plenoptic_deps += plenoptic_toml["project"]["optional-dependencies"]["nb"]

plenoptic_dep_dict = {}
plenoptic_extras = {}
for pkg in plenoptic_deps:
    pkg = pkg.split(">=")
    # for some reason, pipenv replaces underscores with hyphens
    pkg[0] = pkg[0].replace("_", "-")
    if len(pkg) == 1:
        if "[" in pkg[0]:
            pkg, extras = pkg[0].split("[")
            plenoptic_extras[pkg] = extras[:-1].split(",")
        else:
            pkg = pkg[0]
        if re.findall("[0-9]+", pkg):
            raise ValueError("This script only accounts for version floor "
                             "requirements and there's something else here!")
        plenoptic_dep_dict[pkg] = "*"
    else:
        plenoptic_dep_dict[pkg[0]] = ">=" + pkg[1]

# we handle torch separately
binder_deps.pop("torch")
plenoptic_dep_dict.pop("torch")

if binder_deps != plenoptic_dep_dict:
    printed_warnings = []
    for k, v in binder_deps.items():
        if k not in plenoptic_dep_dict:
            print(f"{k} not in plenoptic")
        elif v != plenoptic_dep_dict[k]:
            print(f"{k} versions are different: {v} (Pipfile) and {plenoptic_dep_dict[k]} (plenoptic)")
        printed_warnings.append(k)
    for k, v in plenoptic_dep_dict.items():
        if k not in printed_warnings:
            if k not in binder_deps:
                print(f"{k} not in Pipfile")
            elif v != binder_deps[k]:
                print(f"{k} versions are different: {v} (plenoptic) and {binder_deps[k]} (Pipfile)")
    raise ValueError("Dependencies are different!")

if binder_extras != plenoptic_extras:
    printed_warnings = []
    for k, v in binder_extras.items():
        if k not in plenoptic_extras:
            print(f"{k} not in plenoptic")
        elif v != plenoptic_extras[k]:
            print(f"{k} extras are different: {v} (Pipfile) and {plenoptic_extras[k]} (plenoptic)")
        printed_warnings.append(k)
    for k, v in plenoptic_extras.items():
        if k not in printed_warnings:
            if k not in binder_extras:
                print(f"{k} not in Pipfile")
            elif v != binder_extras[k]:
                print(f"{k} extras are different: {v} (plenoptic) and {binder_extras[k]} (Pipfile)")
    raise ValueError("Dependency extras are different!")
