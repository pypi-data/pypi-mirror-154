import dis
from importlib.machinery import ExtensionFileLoader, SourceFileLoader
from pathlib import Path


def _patch_function(func, new_code, new_names):
    func.__code__ = func.__code__.replace(co_code=new_code, co_names=new_names)


def _no_mypyc_for_black(cls, fullname, path):
    if fullname.startswith("black.") or fullname == "black":
        path = Path(path)
        name = path.name
        path = path.with_name(f"{name[:name.find('.')]}.py")
        return SourceFileLoader(fullname, str(path))
    return object.__new__(cls)


def patch_black():
    ExtensionFileLoader.__new__ = _no_mypyc_for_black  # there is no way back
    from black import Line, linegen, lines, patched_main, syms, token
    from black.nodes import is_one_sequence_between
    from blib2to3.pytree import Leaf

    def bracket_clone(self) -> Line:
        if (
            not self.magic_trailing_comma
            or (not self.is_def and not self.is_decorator)
            or self.leaves[-1] != self.magic_trailing_comma
        ):
            magic_trailing_comma = None
        else:
            haystack = "".join(str(leaf) for leaf in self.leaves)
            needle = "".join(str(leaf) for leaf in self.magic_trailing_comma.parent.leaves())
            if needle in haystack:
                magic_trailing_comma = self.magic_trailing_comma
            else:
                magic_trailing_comma = None
        return Line(
            mode=self.mode,
            depth=self.depth,
            magic_trailing_comma=magic_trailing_comma,
        )

    def has_magic_trailing_comma_patch(self, closing: Leaf) -> bool:
        if (
            (self.is_def or self.is_decorator)
            and closing.opening_bracket is not None
            and not is_one_sequence_between(
                closing.opening_bracket,
                closing,
                self.leaves,
            )
        ):
            return True

        if closing.opening_bracket is None:
            return False

        # if already multiline, set multiline
        parent = self.leaves[-1].parent
        if parent.type not in (syms.arglist, syms.typedargslist):
            return False
        line = 0
        distinct_lines = 0
        for child in parent.children:
            if child.type == token.COMMA:
                if child.lineno != line:
                    line = child.lineno
                    distinct_lines += 1
        if distinct_lines <= 1:
            if line == closing.lineno:
                self.remove_trailing_comma()
            return False

        return True

    nop = dis.opmap["NOP"]

    Line.bracket_clone = bracket_clone
    Line.has_magic_trailing_comma_patch = has_magic_trailing_comma_patch

    func = linegen.bracket_split_build_line
    code = func.__code__
    ops = bytearray(code.co_code)
    assert ops[:2] == bytes(
        [dis.opmap["LOAD_GLOBAL"], code.co_names.index("Line")],
    ), "patch failed for bracket_split_build_line"
    ops[:6] = [
        dis.opmap["LOAD_FAST"],
        code.co_varnames.index("original"),
        dis.opmap["LOAD_METHOD"],
        len(code.co_names),
        dis.opmap["CALL_METHOD"],
        0,
    ]
    ops[6:14] = [nop] * (14 - 6)
    _patch_function(func, bytes(ops), code.co_names + ("bracket_clone",))

    func = lines.Line.has_magic_trailing_comma
    code = func.__code__
    ops = bytearray(code.co_code)
    pattern = bytes(
        [
            dis.opmap["LOAD_FAST"],
            code.co_varnames.index("self"),
            dis.opmap["LOAD_ATTR"],
            code.co_names.index("is_import"),
            dis.opmap["POP_JUMP_IF_FALSE"],
        ],
    )
    pos = ops.find(pattern)
    assert pos >= 0, "patch failed for has_magic_trailing_comma"
    pos += len(pattern) + 5
    patch = [
        dis.opmap["LOAD_FAST"],
        code.co_varnames.index("self"),
        dis.opmap["LOAD_METHOD"],
        len(code.co_names),
        dis.opmap["LOAD_FAST"],
        code.co_varnames.index("closing"),
        dis.opmap["CALL_METHOD"],
        1,
        dis.opmap["RETURN_VALUE"],
    ]
    ops[pos : pos + len(patch)] = patch  # noqa: E203
    ops = ops[: pos + len(patch)]
    _patch_function(func, bytes(ops), code.co_names + ("has_magic_trailing_comma_patch",))

    return patched_main


def main():
    patch_black()()


if __name__ == "__main__":
    main()
