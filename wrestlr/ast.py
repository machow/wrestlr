# Visualizing raw parse tree in console, by hijacking Symbolic repr -----------
from siuba.siu import Symbolic, Call

def dump_context(node):
    """Return a parse tree as a simple dictionary."""
    start = getattr(node, 'start', None) or node.symbol
    stop  = getattr(node, 'stop', None) or node.symbol

    children = getattr(node, 'children', tuple())
    return dict(
            name = node.__class__.__name__.replace("Context", ""),
            text = node.getText(),
            line_info = {
                "col_start": start.start,
                "line_start": start.line,
                "col_end": stop.stop,
                "line_end": stop.line,
                },
            children = tuple(map(dump_context, children))
            )

class SimplifyVisitor:
    """Visitor for converting a dumped parse tree into siu Calls.

    This is essentially for getting the nice Symbolic representation.
    """
    def __init__(self, show_terminal = False):
        self.show_terminal = show_terminal

    def visit(self, node):
        method_name = 'visit_' + node['name']
        f_visit = getattr(self, method_name, self.generic_visit)

        return f_visit(node)
    def generic_visit(self, node):
        children = node.get('children', tuple())

        func = node['name']
        args = tuple(map(self.visit, children))
        kwargs =  {}

        return Call(func, *args, **kwargs)

    def visit_TerminalNodeImpl(self, node):
        if self.show_terminal:
            return Call(node['name'], node['text'])

        return node['text']

    def visit_Literal(self, node):
        child = node['children'][0]
        if (len(node['children']) == 1
            and child['name'] == "TerminalNodeImpl"
            ):
            # pull literal off of terminal node
            return child['text']

        return self.generic_visit(node)


# AST shaping -----------------------------------------------------------------

from hoof import Hoof, AntlrAst
import antlr4
#from .parsers.R import Visitor as RVisitor

rlang = Hoof("wrestlr.parsers.R")


class Unshaped(AntlrAst):
    _fields = ('arr',)

    def __init__(self, arr=tuple(), _ctx=None):
        self.arr = arr
        self._ctx = _ctx

class BinaryOp(AntlrAst):
    _fields = ('op', 'expr')

class BinaryOpUser(BinaryOp):
    _rules = "BinaryOpUser"
    _remap = None

class UnaryOp(AntlrAst):
    _fields = ('op', 'expr')

class Expression(AntlrAst):
    _fields = ('expr',)

class Name(AntlrAst):
    _fields = ('val',)
    _remap = ('ID->val',)
    _rules = "Name"

class SubList(AntlrAst):
    _fields = ('sub',)
    _rules = "Sublist"
    _remap = None

class Parentheses(AntlrAst):
    _fields = ('expr',)
    _rules = "Parentheses"
    _remap = None

class Kwarg(AntlrAst):
    _fields = ('name', 'val') 
    _remap = ('ID->name', 'expr->val')
    _rules = "Kwarg"


# Function Defs ----

class FunctionDef(AntlrAst):
    _fields = ('formlist', 'expr')
    _remap = None
    _rules = "FunctionDef"

class Param(AntlrAst):
    _fields = ('name',)
    _rules = "Param"
    _remap = ["ID->name"]

class ParamKwarg(Param):
    _fields = ('name', 'value')
    _rules = "ParamKwarg"
    _remap = ["ID->name"]


# Calls ----

class CallOp(AntlrAst):
    _fields = ('expr', 'sublist')
    #_remap = ('expr->op',)

class IndexMany(CallOp): pass
class IndexSingle(CallOp): pass


# Literal type hierarchy ----

# TODO: double-check R is.* checks
class Literal(AntlrAst):
    _fields = ('val', )

    _literal_registry = []

    @classmethod
    def _from_token(cls, ctx):
        return cls(ctx.children[0].getText())
    
    @classmethod
    def _bind_all(cls, Visitor):
        for kls in cls._literal_registry:
            visitor = kls._create_visitor()
            setattr(Visitor, "visitLiteral" + kls.__name__, visitor)

    @classmethod
    def _create_visitor(node_cls):
        def visitor(visitor, ctx):
            return node_cls._from_token(ctx)

        return visitor

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._literal_registry.append(cls)

class Number(Literal): pass

# Literal types ----

class Str(Literal):
    @classmethod
    def _from_token(cls, ctx):
        val = ctx.children[0].getText()
        if val.startswith("`"):
            # `x` is a name in R's AST, it's just often handled like string 
            # by $ implementations.
            return Name(val[1:-1])

        return Str(val)

class Hex(Literal): pass

class Int(Number): pass
class Dbl(Number): pass
class Complex(Number): pass
class Inf(Number): pass
class Nan(Number): pass

class Null(Literal): pass
class Na(Literal): pass

class Bool(Literal): pass

class Ellipsis(Literal): pass

#class Literal(AntlrAst):
#    def __init__(self, val):
#        self.val = val
#    _fields = ('val',)

class AstVisitor(rlang.Visitor):
    # TODO: move into antlr-ast ----
    def visitChildren(self, node, predicate=None):
        result = self.defaultResult()
        n = node.getChildCount()
        for i in range(n):
            if not self.shouldVisitNextChild(node, result):
                return

            c = node.getChild(i)
            if predicate and not predicate(c): continue

            childResult = c.accept(self)
            result = self.aggregateResult(result, childResult)

        return self.result_to_ast(node, tuple(result))

    @staticmethod
    def result_to_ast(node, result):
        if len(result) == 1: return result[0]
        elif len(result) == 0: return None
        elif all(isinstance(res, str) for res in result): return " ".join(result)
        elif all(isinstance(res, AntlrAst) and not isinstance(res, Unshaped) for res in result): return result
        else: return Unshaped(result, _ctx=node)

    def defaultResult(self):
        return list()

    def aggregateResult(self, aggregate, nextResult):
        aggregate.append(nextResult)
        return aggregate


    # AntlrAst visit methods ----
    def visitSublist(self, ctx):
        return self.visitChildren(ctx, lambda c: not isinstance(c, antlr4.TerminalNode))

    def visitNoMatch(self, ctx):
        return []

    def visitArg(self, ctx):
        return self.visitChildren(ctx)

    def visitTerminal(self, ctx):
        return ctx.getText()

    def visitLiteralInt(self, ctx):
        return int(ctx.getText())


    rlang.register("Prog", Expression)
    rlang.register("BinaryOp", BinaryOp)
    rlang.register("UnaryOp", UnaryOp)
    rlang.register("Call", CallOp)
    rlang.register("IndexSingle", IndexSingle)
    rlang.register("IndexMany", IndexMany)
    rlang.register(Parentheses)
    rlang.register(Name)
    rlang.register(Kwarg)
    rlang.register(BinaryOpUser)
    rlang.register(FunctionDef)
    rlang.register(Param)
    rlang.register(ParamKwarg)
    # TODO: should either visit token using hoof, or add multiple rules to class
    rlang.register("LiteralEllipsis1", Ellipsis)
    rlang.register("LiteralEllipsis2", Ellipsis)
    
Literal._bind_all(AstVisitor)
rlang.bind(AstVisitor)
