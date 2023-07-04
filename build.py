#!/usr/bin/env python3

import argparse
import os
import io
import yaml

def get_bibliographies(path) -> list[str]:
    with io.open(f"{os.path.dirname(path)}/metadata.yaml", "r") as stream:
        metadata = yaml.safe_load(stream)
        return metadata["bibliography"]

def check_prerequisites() -> None | list[str]:
    return None

def _build_single(pandoc: str, source: str, target: str, options: str):
    metadata_file = f"{os.path.dirname(source)}/metadata.yaml"

    if os.path.exists(metadata_file):
        options += f" --metadata-file={metadata_file}"

    return os.system(f"{pandoc} -F pandoc-crossref --citeproc {options} -i {source} -o {target}") 

def _build_folder(pandoc: str, source: str, target: str, options: str):
    return os.system(f"{pandoc} -F pandoc-crossref --citeproc {options} \
    --metadata-file={source}/metadata.yaml -i {source}/*.md -o {target}")

def main(source: str, target: str, options: str = "", docker: bool = False, pandoc: str = "pandoc"):
    if docker:
        pandoc = 'docker run --mount type=bind,source="$(pwd)",target=/var/data --workdir /var/data pandoc/extra'

    if target.split(".")[-1] == "md":
        options += " -s -f gfm"
    if target.split(".")[-1] == "tex":
        options += " -s"

    if os.path.isdir(source):
        return _build_folder(pandoc, source, target, options)
    else:
        return _build_single(pandoc, source, target, options)

if __name__=="__main__":
    parser = argparse.ArgumentParser()         
    parser.add_argument("source")
    parser.add_argument("target")
    parser.add_argument("--options", default="", type=str)
    parser.add_argument("--pandoc", default="pandoc", type=str)
    parser.add_argument("--docker", action="store_true")
    
    missing = check_prerequisites()

    if not missing is None:
        print("Not all prerequisites are met:", missing)

    args = parser.parse_args()

    exit(main(args.source, args.target, args.options, pandoc=args.pandoc, docker=args.docker))
