# TODO: don't use module level BINARY_LEVELS like this on classes
from siuba.siu import UNARY_OPS, BINARY_OPS, BINARY_LEVELS, UnaryOp, BinaryOp, FuncArg, MetaArg, symbolic_dispatch, Call, SliceOp

BINARY_OPS["__assign__"] = "="
BINARY_LEVELS["__assign__"] = 6

# util funcs ------------------------------------------------------------------

def name_well_formatted(x):
    if isinstance(x, str) and not (" " in x or "." in x or "%" in x):
        return True

    return False

def create_column_access(obj, attr):
    # would be useful to move into siu
    if name_well_formatted(attr):
        return BinaryOp("__getattr__", obj, attr)

    return BinaryOp("__getitem__", obj, attr)


# hacks to Call Nodes :/ ------------------------------------------------------

def flip_get(d, key, default = None):
    tmp = {v: k for k,v in d.items()}
    return tmp.get(key, default)

# NEED: op -> call node
def call_factory(func, *args, **kwargs):
    method = flip_get(BINARY_OPS, func)
    if method:
        return BinaryOp(method, *args, **kwargs)

    method = flip_get(UNARY_OPS, func)
    if method:
        return UnaryOp(method, *args, **kwargs)

    return Call("__call__", NameArg(func), *args, **kwargs)


class NameArg(Call):
    def __init__(self, func, *args, **kwargs):
        self.func = '__siu_name__'

        if func == '__siu_name__':
            func = args[0]

        self.args = tuple([func])
        self.kwargs = {}

    def __repr__(self):
        name = self.args[0]
        return name if name_well_formatted(name) else "`{}`".format(name)

    def __call__(self, x):
        raise NotImplementedError("Cannot call Name")

class Keyword(Call):
    def __repr__(self):
        fmt = "{args[0]} {func} {args[1]}"
        return fmt.format(func = "=", args = [self.args[0], repr(self.args[1])])

class AssignOp(BinaryOp):
    # TODO: assign could take an environment?!
    def needs_paren(self, x):

        if isinstance(x, BinaryOp):
            sub_lvl = BINARY_LEVELS[x.func]
            # manually make assign lowest precedence
            #level = BINARY_LEVELS[self.func]
            level = 6
            if sub_lvl != 0 and sub_lvl != level:
                return True

FuncArg.__repr__ = lambda self: self.args[0].__qualname__


# how to represent filter and mutate?
#from wrestlr.call_nodes import AssignOp
#from siuba.siu import strip_symbolic, _
#from siuba.dply.vector import row_number
#op1 = AssignOp("__assign__", "a", strip_symbolic(_.x + _.y < 6))  
#op2 = AssignOp("__assign__", "a", strip_symbolic(row_number(_.y) == 2))
