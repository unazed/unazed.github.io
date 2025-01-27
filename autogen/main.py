from dataclasses import dataclass, field
from typing import Self

from template import parse_template_spec, TemplateSpec, FOLDER_TEMPLATE_FOLDER

import argparse
import os

from pprint import pprint


@dataclass
class FolderTree:
    name: str
    children: list[Self] = field(default_factory=list)
    template: TemplateSpec | None = None

    def add_child_path(self, path: str) -> None:
        subpaths = path.split(os.path.sep)
        for child in self:
            if child.name == subpaths[0]:
                child.add_child_path(os.path.join(*subpaths[1:]))
                return

        # If no matching children found, create them
        child = FolderTree(name=subpaths[0])
        if subpaths[1:]:
            child.add_child_path(os.path.join(*subpaths[1:]))
        self.children.append(child)

    def __iter__(self):
        yield from self.children


def preprocess_folder_tree(root_directory: str, folder_tree: FolderTree)\
        -> FolderTree:
    abs_path = os.path.join(root_directory, folder_tree.name)
    if os.path.isdir(
            templ_path := os.path.join(abs_path, FOLDER_TEMPLATE_FOLDER)):
        folder_tree.template = parse_template_spec(templ_path)
    for child in folder_tree:
        preprocess_folder_tree(abs_path, child)
    return folder_tree


def derive_hierarchy(folder: str) -> FolderTree:
    root_node = FolderTree(name=".")
    for abs_path, *_ in os.walk(folder):
        relpath = os.path.relpath(abs_path, folder)
        if relpath == ".":
            continue
        if os.path.split(relpath)[-1].startswith("_"):
            continue
        root_node.add_child_path(relpath)
    return root_node


def main(root_directory: str, out_directory: str) -> None:
    hierarchy = preprocess_folder_tree(
            root_directory, derive_hierarchy(root_directory))
    pprint(hierarchy)


if __name__ == "__main__":
    def valid_directory(path: str) -> str:
        if not os.path.exists(path):
            raise argparse.ArgumentTypeError(
                f"directory does not exist: {path!r}")
        if os.path.isfile(path):
            raise argparse.ArgumentTypeError(f"expected directory: {path!r}")
        return path

    parser = argparse.ArgumentParser(
        prog="autogen",
        description="Convert markup files into HTML",
        epilog="Unazed, 2025"
    )
    parser.add_argument("rootdir",
                        help="Root directory of the markdown files",
                        type=valid_directory)
    parser.add_argument("-o", "--distdir", default="./",
                        help="Output directory for auto-generated HTML",
                        type=valid_directory)
    args = parser.parse_args()

    main(args.rootdir, args.distdir)
