from collections import defaultdict
from dataclasses import dataclass, field
from typing import Self, Literal, IO, NoReturn, TypeAlias

import argparse
import json
import os


FOLDER_TEMPLATE_FOLDER = "_template"

TEMPL_KEYWORDS = ("import", "export", "else", "end")

PathLike = str | os.PathLike


@dataclass
class TemplatePosition:
    offset: int
    length: int


@dataclass
class TemplateSpec:
    imports: dict[PathLike, dict[str, TemplatePosition]] \
            = field(default_factory=lambda: defaultdict(dict))
    exports: dict[PathLike, dict[str, TemplatePosition]] \
            = field(default_factory=lambda: defaultdict(dict))


@dataclass
class TemplateDecl:
    qualifier: str
    stmt_position: TemplatePosition
    name: str | None = None
    block_position: TemplatePosition | None = None


@dataclass
class TemplateParsingCtx:
    file: IO
    path: PathLike
    line_no: int = 1
    col_no: int = 0

    def peek(self, offset: int = 0, *, n: int = 1) -> str:
        current_pos = self.file.tell()
        self.file.read(offset)
        data = self.file.read(n)
        self.file.seek(current_pos)
        return data

    def read(self, n: int = 1) -> str:
        cs = self.file.read(n)
        if "\n" not in cs:
            self.col_no += n
            return cs
        self.line_no += cs.count("\n")
        self.col_no = len(cs.split("\n")[-1])
        return cs

    def read_until(self, literal: str) -> str | None:
        res = ""
        while (cs := self.peek(n=len(literal))) and cs != literal:
            res += self.read()
        return res if cs == literal else None

    def _error(self, msg: str) -> NoReturn:
        raise SyntaxError(f"{self.path!r} ({self.line_no}:{self.col_no}): {msg}")

    def expect_whitespace(self, *, maybe: bool = False) -> bool:
        encountered = False
        while (c := self.peek()).isspace():
            encountered = True
            self.read()
        if not encountered and not maybe:
            self._error(f"Expected whitespace, got {c!r}")
        return encountered

    def expect_token(self, *, maybe: bool = False) -> str:
        token = self.peek()

        if not token.isidentifier():
            if maybe:
                return ""
            self._error(f"Expected token, got character {token!r}")
        else:
            self.read()

        while (c := self.peek()):
            if not (token + c).isidentifier():
                break
            token += c
            self.read()

        return token

    def expect_literal(self, s: str) -> None:
        interim = self.read_until(s)
        if interim is None:
            self._error(f"Expected literal {s!r}, found EOF")
        if interim:
            self._error(f"Expected literal {s!r}, found {interim[:16]!r}")
        self.read(len(s))


    def expect_keyword(self, which: str | None = None, maybe: bool = False) -> str:
        if (kw := self.expect_token(maybe=maybe)) not in TEMPL_KEYWORDS and not maybe:
            if which is not None:
                self._error(f"Expected keyword {which!r}, got {kw!r}")
            self._error(f"Expected keyword, got {kw!r}")
        if maybe and not kw:
            return ""
        if which is not None and kw != which:
            self._error(f"Expected keyword {which!r}, got {kw!r}")
        return kw


    def expect_decl(self, *, expect_quali: str | None = None) -> TemplateDecl:
        stmt_start_pos = self.file.tell()

        self.expect_literal("{{")
        self.expect_whitespace(maybe=True)
        qualifier = self.expect_keyword(expect_quali)

        if expect_quali is not None and qualifier != expect_quali:
            self._error(f"Unexpected qualifier {qualifier!r}")

        if qualifier == "end":
            self.expect_whitespace(maybe=True)
            self.expect_literal("}}")
            return TemplateDecl(qualifier,
                    TemplatePosition(stmt_start_pos, self.file.tell() - stmt_start_pos))

        self.expect_whitespace()
        name = self.expect_token()
        self.expect_whitespace(maybe=True)

        content_position = None
        if qualifier == "import" and self.expect_keyword("else", maybe=True):
            # Handle else/end-stmt for imports
            self.expect_whitespace(maybe=True)
            self.expect_literal("}}")
            content_start_pos = self.file.tell()
            if (block_content := self.read_until("{{")) is None:
                self._error("Expected closing block for import 'else' statement")
            content_position = TemplatePosition(content_start_pos, len(block_content))
            self.expect_decl(expect_quali="end")
        elif qualifier == "export":
            self.expect_literal("}}")
            content_start_pos = self.file.tell()
            if (block_content := self.read_until("{{")) is None:
                self._error("Expected closing block for export block")
            content_position = TemplatePosition(content_start_pos, len(block_content))
            self.expect_decl(expect_quali="end")
        else:    
            self.expect_literal("}}")

        return TemplateDecl(qualifier, name=name,
                stmt_position=TemplatePosition(stmt_start_pos, self.file.tell() - stmt_start_pos),
                block_position=content_position)


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


def extract_template_positions(path: str) \
        -> dict[Literal["imports"] | Literal["exports"], list[TemplatePosition]]:
    mapping = {"imports": [], "exports": []}
    ctx = TemplateParsingCtx(file=open(path), path=path)
    while (cs := ctx.peek(n=2)):
        if cs == "{{":
            decl = ctx.expect_decl()
            print(f"Got decl {decl=}")
        ctx.read()
    return mapping


def parse_template_spec(path: str) -> TemplateSpec:
    templ = TemplateSpec()
    for file in os.listdir(path):
        file = os.path.join(path, file)
        if not os.path.isfile(file):
            continue
        for type_, positions in extract_template_positions(file).items():
            getattr(templ, type_)[file] = positions
    return templ


def preprocess_folder_tree(root_directory: str, folder_tree: FolderTree) -> FolderTree:
    abs_path = os.path.join(root_directory, folder_tree.name)
    if os.path.isdir(templ_path := os.path.join(abs_path, FOLDER_TEMPLATE_FOLDER)):
        folder_tree.template = parse_template_spec(templ_path)
    for child in folder_tree:
        preprocess_folder_tree(abs_path, child)


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


if __name__ == "__main__":
    def valid_directory(path: str) -> str:
        if not os.path.exists(path):
            raise argparse.ArgumentTypeError(f"directory does not exist: {path!r}")
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
