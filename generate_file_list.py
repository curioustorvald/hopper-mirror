#!/usr/bin/env python3
import glob
import sys


def parse_hopper_file(path):
    name = None
    version = None
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n").rstrip("\r")
            if ":" not in line:
                continue
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()
            if key == "HopperPackageName":
                name = value
            elif key == "HopperPackageVersion":
                version = value
    if name is None:
        raise ValueError(f"{path}: missing HopperPackageName")
    if version is None:
        raise ValueError(f"{path}: missing HopperPackageVersion")
    return name, version


def main():
    entries = []
    seen = {}
    for path in sorted(glob.glob("**/*.hop.per", recursive=True)):
        name, version = parse_hopper_file(path)
        key = (name, version)
        if key in seen:
            sys.exit(
                f"error: duplicate package {name} {version} "
                f"in {seen[key]} and {path}"
            )
        seen[key] = path
        entries.append(f"{name},{version},{path}")

    with open("filelist", "w", encoding="utf-8") as f:
        for entry in entries:
            f.write(entry + "\n")


if __name__ == "__main__":
    main()
