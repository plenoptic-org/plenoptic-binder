#!/usr/bin/env python3
"""Used by check_versions.yml workflow to find supported python versions."""

import sys

import tomllib

with open(sys.argv[1], "rb") as f:
    toml = tomllib.load(f)

print(toml["packages"]["torch"]["version"])
