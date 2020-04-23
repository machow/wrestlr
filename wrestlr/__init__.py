__version__ = "0.0.1"


from .ast import rlang
from .transformers import TransformExpr

def rlang_convert(code, start = "prog", mode = "siuba"):
    if isinstance(code, dict):
        # handle test cases here for now
        ast_tree = rlang.parse(code["src"], start, mode = "ast")
        dst = TransformExpr().visit(ast_tree)
        return {**code, "siuba": dst, "ast": ast_tree}
    if mode in {"ast", "parser"}:
        return rlang.parse(code, start, mode = mode)
    elif mode == "siuba":
        ast_tree = rlang.parse(code, start, mode = "ast")
        return TransformExpr().visit(ast_tree)

    raise ValueError("rlang_convert mode must be one of ast, parser, siuba")


def get_test_case(fname):
    import pkg_resources
    import yaml
    fstream = pkg_resources.resource_stream("wrestlr", "tests/cases/" + fname)
    return yaml.load(fstream, yaml.SafeLoader)


def big_print(d):
    from siuba.siu import Symbolic
    print()
    for k, v in d.items():
        print(k, "--")
        print(v)
        print()

    print("symbol --")
    print(Symbolic(d["siuba"]))


def check_case(fname):
    out = rlang_convert(get_test_case(fname))
    big_print(out)
    return out


def load_ipython_extension(ipython):
    from .magic import WrestlrMagic
    ipython.register_magics(WrestlrMagic)
