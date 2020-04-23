from IPython.core.magic import register_cell_magic
from wrestlr import rlang_convert
from wrestlr.ast import Expression
from wrestlr.transformers import TransformExpr

from IPython.core.magic import Magics, magics_class, cell_magic
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring

from hoof import to_symbol

from siuba import siu
@to_symbol.register(siu.Call)
def _to_symbol_call(x):
    return siu.Symbolic(x)


# This is a pure delight and should go in a siu util file / package? ---
from siuba.siu import _, strip_symbolic, Call, BinaryOp

def shift_add_ops(call):
    if not (isinstance(call, BinaryOp) and call.func == "__add__"):
        return call
    
    pipe = unfurl_pipe(call)
    pipe_to_binary(pipe, "__add__")

    if not (isinstance(pipe[0], BinaryOp) and pipe[0].func == "__rshift__"):
        return call
    
    phead, ptail = pipe[0].args
    
    # prepend tail to add ops
    add_ops = BinaryOp(
        "__add__",
        ptail,
        pipe_to_binary(pipe[1:], "__add__")
    )

    # re-connect head and tail
    return BinaryOp(
        "__rshift__",
        phead,
        add_ops
    )


def unfurl_pipe(call):
    crnt_child, target = call, call.func
    pipe = []
    while crnt_child.func == target:
        # since it's a left-to-right parser, a statement like...
        #    python: data %>% verb1 %>% verb2
        #
        #    ast:    %>%(%>%(data, verb1), verb2)
        left, right = crnt_child.args
        if left.func == target:
            pipe.append(right)
        else:
            pipe.extend([right, left])
            break

        crnt_child = left

    return list(reversed(pipe))

def pipe_to_binary(pipe, op):
    import functools
    return functools.reduce(lambda acc, v: BinaryOp(op, acc, v), pipe)


# Magic utils ----

def parse_ast_expressions(cell, start = "prog", transformer = None):
    tree_ast = rlang_convert(cell, start, mode = "ast")

    if isinstance(tree_ast, Expression) and len(tree_ast.expr) > 1:
        entries = tree_ast.expr
    else:
        entries = [tree_ast]

    out = []
    te = TransformExpr() if transformer is None else transformer
    for expr in entries:
        te.reset()
        out.append(te.visit(expr))

    te.reset()
    return out


@magics_class
class WrestlrMagic(Magics):
    default_opts = {}

    @classmethod
    def set_defaults(cls, execute):
        # hacking for now, not sure how to re-configure magic command defaults
        cls.default_opts['execute'] = execute

    # TODO: toggle showing parse tree, R AST w/ to_symbol
    # e.g %%wrestlr -p -m parse -s

    @magic_arguments()
    @argument('-p', '--print', action='store_true', help="print the conversion, rather than replacing code")
    @argument('-m', '--mode', choices={"siuba", "ast", "parser"}, default="siuba", help="parsing mode: ast, parser, or siuba")
    @argument('-d', '--debug', action='store_true', help="whether to make a nice printout for debugging")
    @argument('-b', '--black', action='store_true', help="whether to apply black formatting (only for siuba conversions)")
    @argument('-t', '--transformer', help="variable name for a custom transformer")
    @argument('-s', '--start', default="prog", help="starting rule for parser")
    @argument('-x', '--experimental', action="store_true", help="experimental things")
    @argument('-e', '--execute', action="store_true", help="execute code")
    @cell_magic
    def wrestlr(self, line, cell):
        args = parse_argstring(self.wrestlr, line)

        # get custom transformer from users environment
        if args.transformer:
            transformer = self.shell.user_ns[args.transformer]
        else:
            transformer = None

        if args.mode == "siuba":
            trees = parse_ast_expressions(cell, args.start, transformer)
            #siuba_code = "\n\n".join(out)
        else:
            trees = [rlang_convert(cell, args.start, mode = args.mode)]

        if args.debug:
            symbol = "\n\n".join(repr(to_symbol(entry)) for entry in trees)
            print(symbol)

        if args.experimental:
            transform = shift_add_ops
        else:
            transform = lambda x: x
        
        code = "\n\n".join(repr(transform(entry)) for entry in trees)
        if args.black:
            from black import format_str, FileMode
            code = format_str(code, mode = FileMode())

        if args.print:
            print(code)
        else:
            self.shell.set_next_input(code, replace=True)

        if self.default_opts.get('execute', args.execute):
            self.shell.run_cell(code)

        # self.shell.run_cell(raw_code, store_history=False)
