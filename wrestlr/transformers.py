from ast import NodeTransformer, iter_fields
from wrestlr.ast import AntlrAst, BinaryOp

class Pipe(AntlrAst):

    _fields = ('op', 'args')


# convert binary ops to pipes -------------------------------------------------

class Pipeify(NodeTransformer):
    def visit(self, node):
        if not isinstance(node, AntlrAst):
            return node

        return super().visit(node)

    def visit_BinaryOp(self, node):
        #Pipe(["mtcars", "filter(...)", "mutate(...)"])
        left, right = node.expr
        if (node.op == "%>%"
            and isinstance(left, BinaryOp)
            and left.op == "%>%"
            ):
            return Pipe("%>%", self.unfurl_pipe(node))

        return self.generic_visit(node)

        
    def unfurl_pipe(self, node):
        crnt_child = node
        pipe = []
        while crnt_child.op == "%>%":
            # since it's a left-to-right parser, a statement like...
            #    python: data %>% verb1 %>% verb2
            #
            #    ast:    %>%(%>%(data, verb1), verb2)
            left, right = crnt_child.expr
            if isinstance(left, BinaryOp) and left.op == "%>%":
                pipe.append(self.visit(right))
            else:
                pipe.extend([self.visit(right), self.visit(left)])
                break

            crnt_child = left

        return list(reversed(pipe))
                


# transform an R expression into siuba syntax ---------------------------------
from wrestlr import call_nodes as cn
from wrestlr import ast as wast
from functools import reduce
import math

# TODO: if we return custom calls for these, can keep from needing these as dep
from numpy import nan
from pandas import NA

OP_TO_SIUBA = {
        "%>%": ">>",
        "$": "[",
        "[[": "[",
        "::": ".",
        ":::": ".",
        }

def convert_r_name(x):
    if "." in x:
        return x.replace(".", "_")

    return x

def bare_name(x):
    if isinstance(x, cn.NameArg):
        return x.args[0]
    if isinstance(x, str):
        return x
    raise TypeError("Don't know how to get string from type: %s" %type(x))

def escape_keywords(x):
    import keyword
    if x in keyword.kwlist:
        return x + "_"

    return x

class TransformExpr(NodeTransformer):
    # TODO: should error if an AST node would make it out
    """
    from wrestlr.transformers import TransformExpr
    from wrestlr import ast 
    code = '''
            mtcars %>%
              filter(cyl == 6) %>%
              mutate(avg_hp = mean(hp))
            '''
    tree = ast.rlang.parse(code, "prog")
    tree2 = TransformExpr().visit(tree)
    """

    nse_verbs = [
            'select', 'mutate', 'filter', 'arrange', 'summarize', '..NSE..',
            'group_by', 'ungroup', 'nest', 'unnest', 'count', "top_n",
            ]
    method_calls = {"NSE_method": "NSE_method"}

    def __init__(self, nse_verbs = None, method_calls = None):
        self.in_nse_verb = False
        self.in_pipe = False

        self.nse_verbs = self.nse_verbs if nse_verbs is None else nse_verbs
        self.method_calls = self.method_calls if method_calls is None else method_calls

    def reset(self):
        self.in_nse_verb = False
        self.in_pipe = False
    
    def visit(self, node):
        if not isinstance(node, AntlrAst):
            # literal, default is to escape. eg b -> _.b
            return node
        
        return super().visit(node)

    def visit_Parentheses(self, node):
        return self.visit(node.expr)


    # Ops, Calls, and NSE ----------

    def visit_Pipe(self, node):
        node_op = OP_TO_SIUBA.get(node.op, node.op)

        orig_in_pipe = self.in_pipe
        self.in_pipe = True

        child_nodes = map(self.visit, node.args)
        bin_ops = reduce(lambda acc, v: cn.call_factory(node_op, acc, v), child_nodes)

        self.in_pipe = orig_in_pipe

        return list(bin_ops)

    def visit_BinaryOp(self, node):
        left, right = node.expr

        # do not escape lhs for an assignment
        if node.op in {"=", "<-"}:
            return cn.AssignOp("__assign__", self.no_escape(left), self.visit(right))
        
        if node.op == "$":
            if isinstance(left, wast.Name) and self.in_nse_verb and left.val == ".data":
                # special dplyr .data$hp usage
                return self.visit(right)

            if isinstance(right, wast.Str):
                # eg mtcars$"hp", or mtcars$`hp`
                return cn.create_column_access(self.visit(left), self.no_escape(right))

            if isinstance(right, wast.Name):
                # eg mtcars$hp
                return cn.create_column_access(self.visit(left), right.val)

        # R's array creation infix syntax
        if node.op == ":":
            # Otherwise: essentially range function 
            if self.in_nse_verb:
                # in NSE is used for selection. Use siuba's select syntax.
                # eg select(a:c) -> select(_[_.a:_.c])
                slice_op = cn.SliceOp("__siu_slice__", *map(self.str_or_visit, node.expr))
                return cn.BinaryOp("__getitem__", cn.MetaArg("_"), slice_op)

            return cn.Call("__call__", cn.NameArg("range"), *map(self.visit, node.expr))

        node_op = OP_TO_SIUBA.get(node.op, node.op)
        return cn.call_factory(self.no_escape(node_op), *map(self.visit, node.expr))


    def visit_BinaryOpUser(self, node):

        if node.op == "%>%":
            orig_in_pipe = self.in_pipe
            self.in_pipe = True

            res = cn.BinaryOp("__rshift__", *map(self.visit, node.expr))

            self.in_pipe = orig_in_pipe
            return res
        
        node_op = escape_keywords(node.op.strip("%"))
        user_op = cn.BinaryOp("__getattr__", cn.NameArg("user_op"), node_op)

        return cn.Call("__call__", user_op, *map(self.visit, node.expr))
    
    def visit_IndexSingle(self, node):
        # Note: because we gave these their own AST nodes, this doesn't process
        #       cases like `[[`(mtcars, 1, "hp")`, which is probably okay.
        sublist = node.sublist if isinstance(node.sublist, (list, tuple)) else [node.sublist]
        return cn.BinaryOp("__getitem__", self.visit(node.expr), *map(self.visit, sublist))

    def visit_IndexMany(self, node):
        return self.visit_IndexSingle(node)

    def visit_UnaryOp(self, node):
        if node.op == "~":
            return node._get_text()
        
        return cn.call_factory(self.no_escape(node.op), self.visit(node.expr))
    
    def visit_Name(self, node):
        # TODO: once it's clear all bare name objects are using the Name node,
        #       this should be the only place using the visit_literal logic
        if self.in_nse_verb:
            return self.escape_name(node.val)

        return cn.NameArg(node.val)
    
    def visit_Kwarg(self, node):
        return cn.Keyword("__siu_keyword__", node.name, self.visit(node.val))

    def visit_CallOp(self, node):
        # assumes we don't need to visit the Call's op
        # but this would fail for (function(a) {})(1). Probably not an issue
        sublist = node.sublist if isinstance(node.sublist, (list, tuple)) else [node.sublist]
        v_expr = self.no_escape(node.expr)

        # TODO: use context manager to set in_dplyr_verb
        orig_in_dplyr = self.in_nse_verb

        # check if we are calling an nse verb, but default to false for cases
        # like 1(), or (a + b)()
        # TODO: handle dplyr::mutate()
        try:
            _name = bare_name(v_expr)
            is_nse_verb = _name in self.nse_verbs

            # maybe return ggplot call instead ----
            if _name == "aes":
                return self.visit_ggplot_aes(node)
            elif _name == "theme":
                return self.visit_ggplot_theme(node)
            elif _name.endswith("_join"):
                print("visiting two table")
                return self.visit_two_table_verb(node)

        except TypeError:
            is_nse_verb = False

        if is_nse_verb:
            self.in_nse_verb = True

        # create call ----
        call = cn.Call(
                "__call__",
                v_expr,
                *self.visit_call_args(sublist, is_nse_verb)
                )

        self.in_nse_verb = orig_in_dplyr

        # convert certain calls to methods (eg mean(a) -> a.mean() ----
        # TODO: shouldn't be done in transformer, by by siu.CallTreeLocal.
        #       easier to think about the result of this visitor as returning
        #       a python-esque declaration of "what" they were doing, and
        #       CallTreeLocal's job as executing on that declaration
        try:
            call_str = bare_name(call.args[0])
            meth_str = self.method_calls.get(call_str)
        except:
            meth_str = None
        if meth_str and self.in_nse_verb and len(call.args) > 1:
            # mean(a) -> a.mean(). Not robust to eg mean(x = 1)

            return cn.Call(
                    '__call__',
                    cn.BinaryOp('__getattr__', call.args[1], meth_str),
                    *call.args[2:],
                    **call.kwargs
                    )

        return call

    def visit_ggplot_aes(self, node):
        # TODO: this line duplicated in a few places
        sublist = node.sublist if isinstance(node.sublist, (list, tuple)) else [node.sublist]

        return cn.Call(
                "__call__",
                self.no_escape(node.expr),
                *[child._get_text() for child in sublist]
                )

    def visit_ggplot_theme(self, node):
        # Convert theme(axis.x.text = ...) to use axis_x_text
        sublist = node.sublist if isinstance(node.sublist, (list, tuple)) else [node.sublist]

        all_args = []
        for arg in sublist:
            if isinstance(arg, wast.Kwarg):
                all_args.append(wast.Kwarg(convert_r_name(arg.name), arg.val))
            else:
                all_args.append(arg)

        return cn.Call("__call__", self.no_escape(node.expr), *map(self.visit, all_args))

    def visit_two_table_verb(self, node):
        sublist = node.sublist if isinstance(node.sublist, (list, tuple)) else [node.sublist]

        orig_in_nse = self.in_nse_verb
        self.in_nse_verb = True
        res =  call = cn.Call(
                "__call__",
                self.no_escape(node.expr),
                cn.MetaArg("_"),
                self.no_escape(sublist[0]),                 # note: fails for inner_join()
                *self.visit_call_args(sublist[1:], True)
                )
        self.in_nse_verb = orig_in_nse

        return res


    
    def visit_Expression(self, node):
        # TODO: this holds all statements, testing with a single one
        if len(node.expr) > 1:
            raise NotImplementedError("Cannot parse multiple expressions")

        return self.visit(node.expr[0])

    def visit_call_args(self, sublist, is_nse_verb):
        if not len(sublist):
            return []

        orig_in_pipe = self.in_pipe
        self.in_pipe = False

        arg0_peak = self.visit(sublist[0])

        if is_nse_verb and not orig_in_pipe and not isinstance(arg0_peak, cn.Keyword):
            # don't escape first argument of eg mutate(data, hp)
            res = [self.no_escape(sublist[0]), *map(self.visit, sublist[1:])]
        else:
            res = list(map(self.visit, sublist))

        self.in_pipe = orig_in_pipe
        return res


    @staticmethod
    def escape_name(attr):
        obj = cn.MetaArg("_")
        return cn.create_column_access(obj, attr)
        #    
        #return cn.BinaryOp("__getattr__", obj, attr)

    def str_or_visit(self, node):
        if isinstance(node, (wast.Str, wast.Name)):
            return node.val

        return self.visit(node)

    def no_escape(self, node):
        """Visits node as if it is not in a NSE verb."""
        orig_in_dplyr = self.in_nse_verb
        self.in_nse_verb = False
        res = self.visit(node)
        self.in_nse_verb = orig_in_dplyr

        return res
    
    # Literal Conversions  ----------
    def visit_Int(self, node):
        return int(node.val)
    
    def visit_Str(self, node):
        stripped = node.val[1:-1]

        return stripped

    def visit_Bool(self, node):
        return True if node.val == "TRUE" else False

    def visit_Dbl(self, node):
        return float(node.val)

    def visit_Complex(self, node):
        # e.g. R: 1i -> python: 1j
        # In both languages statements like 3 + 2i are binops `+`(3, complex(2))
        return complex(0, int(node.val[:-1]))

    def visit_Null(self, node):
        return None

    def visit_Inf(self, node):
        return math.inf

    def visit_Nan(self, node):
        return nan

    def visit_Na(self, node):
        return NA

    def visit_Ellipsis(self, node):
        # just return string for now...
        return '...'
