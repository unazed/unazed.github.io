from collections import defaultdict
from dataclasses import dataclass, field
from typing import TypeAlias, NoReturn, Self, Literal, IO

import os


FOLDER_TEMPLATE_FOLDER = "_template"
TEMPL_KEYWORDS = ("import", "export", "else", "end")

PathLike: TypeAlias = str | os.PathLike


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
        raise SyntaxError(
            f"{self.path!r} ({self.line_no}:{self.col_no}): {msg}")

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

    def expect_keyword(self, which: str | None = None, maybe: bool = False)\
            -> str:
        if (kw := self.expect_token(maybe=maybe)) not in TEMPL_KEYWORDS\
                and not maybe:
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
            return TemplateDecl(
                qualifier,
                TemplatePosition(
                    stmt_start_pos,
                    self.file.tell() - stmt_start_pos
                )
            )

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
                self._error(
                    "Expected closing block for import 'else' statement")
            content_position = TemplatePosition(
                content_start_pos,
                len(block_content)
            )
            self.expect_decl(expect_quali="end")
        elif qualifier == "export":
            self.expect_literal("}}")
            content_start_pos = self.file.tell()
            if (block_content := self.read_until("{{")) is None:
                self._error("Expected closing block for export block")
            content_position = TemplatePosition(
                content_start_pos,
                len(block_content)
            )
            self.expect_decl(expect_quali="end")
        else:
            self.expect_literal("}}")

        return TemplateDecl(
            qualifier, name=name,
            stmt_position=TemplatePosition(
                stmt_start_pos,
                self.file.tell() - stmt_start_pos
            ),
            block_position=content_position
        )


def extract_template_positions(path: str) \
        -> dict[Literal["imports"] | Literal["exports"], list[TemplateDecl]]:
    mapping = {"imports": [], "exports": []}
    ctx = TemplateParsingCtx(file=open(path), path=path)
    while (cs := ctx.peek(n=2)):
        if cs == "{{":
            decl = ctx.expect_decl()
            if decl.qualifier == "import":
                mapping["imports"].append(decl)
            elif decl.qualifier == "export":
                mapping["exports"].append(decl)
        ctx.read()
    return mapping


def parse_template_spec(path: str) -> TemplateSpec:
    templ = TemplateSpec()
    for file in os.listdir(path):
        file = os.path.join(path, file)
        if not os.path.isfile(file):
            continue
        for type_, positions in extract_template_positions(file).items():
            getattr(templ, type_)[os.path.basename(file)] = positions
    return templ
