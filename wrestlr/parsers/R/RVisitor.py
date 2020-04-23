# Generated from wrestlr/parsers/R/R.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .RParser import RParser
else:
    from RParser import RParser

# This class defines a complete generic visitor for a parse tree produced by RParser.

class RVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by RParser#prog.
    def visitProg(self, ctx:RParser.ProgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RParser#LiteralHex.
    def visitLiteralHex(self, ctx:RParser.LiteralHexContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RParser#LiteralNan.
    def visitLiteralNan(self, ctx:RParser.LiteralNanContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RParser#FunctionDef.
    def visitFunctionDef(self, ctx:RParser.FunctionDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RParser#WhileStatement.
    def visitWhileStatement(self, ctx:RParser.WhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RParser#Name.
    def visitName(self, ctx:RParser.NameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RParser#IfStatement.
    def visitIfStatement(self, ctx:RParser.IfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RParser#LiteralDbl.
    def visitLiteralDbl(self, ctx:RParser.LiteralDblContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RParser#ForStatement.
    def visitForStatement(self, ctx:RParser.ForStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RParser#LiteralInf.
    def visitLiteralInf(self, ctx:RParser.LiteralInfContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RParser#BinaryOpUser.
    def visitBinaryOpUser(self, ctx:RParser.BinaryOpUserContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RParser#Parentheses.
    def visitParentheses(self, ctx:RParser.ParenthesesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RParser#BinaryOp.
    def visitBinaryOp(self, ctx:RParser.BinaryOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RParser#Call.
    def visitCall(self, ctx:RParser.CallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RParser#LiteralBool.
    def visitLiteralBool(self, ctx:RParser.LiteralBoolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RParser#UnaryOp.
    def visitUnaryOp(self, ctx:RParser.UnaryOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RParser#LiteralStr.
    def visitLiteralStr(self, ctx:RParser.LiteralStrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RParser#LiteralInt.
    def visitLiteralInt(self, ctx:RParser.LiteralIntContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RParser#LiteralNa.
    def visitLiteralNa(self, ctx:RParser.LiteralNaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RParser#BreakStatement.
    def visitBreakStatement(self, ctx:RParser.BreakStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RParser#LiteralComplex.
    def visitLiteralComplex(self, ctx:RParser.LiteralComplexContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RParser#ExprList.
    def visitExprList(self, ctx:RParser.ExprListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RParser#LiteralNull.
    def visitLiteralNull(self, ctx:RParser.LiteralNullContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RParser#NextStatement.
    def visitNextStatement(self, ctx:RParser.NextStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RParser#IndexSingle.
    def visitIndexSingle(self, ctx:RParser.IndexSingleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RParser#IndexMany.
    def visitIndexMany(self, ctx:RParser.IndexManyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RParser#RepeatStatement.
    def visitRepeatStatement(self, ctx:RParser.RepeatStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RParser#exprlist.
    def visitExprlist(self, ctx:RParser.ExprlistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RParser#formlist.
    def visitFormlist(self, ctx:RParser.FormlistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RParser#Param.
    def visitParam(self, ctx:RParser.ParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RParser#ParamKwarg.
    def visitParamKwarg(self, ctx:RParser.ParamKwargContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RParser#LiteralEllipsis1.
    def visitLiteralEllipsis1(self, ctx:RParser.LiteralEllipsis1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RParser#sublist.
    def visitSublist(self, ctx:RParser.SublistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RParser#KwargEmpty.
    def visitKwargEmpty(self, ctx:RParser.KwargEmptyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RParser#Kwarg.
    def visitKwarg(self, ctx:RParser.KwargContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RParser#StrKwargEmpty.
    def visitStrKwargEmpty(self, ctx:RParser.StrKwargEmptyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RParser#StrKwarg.
    def visitStrKwarg(self, ctx:RParser.StrKwargContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RParser#NullKwargEmpty.
    def visitNullKwargEmpty(self, ctx:RParser.NullKwargEmptyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RParser#NullKwarg.
    def visitNullKwarg(self, ctx:RParser.NullKwargContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RParser#LiteralEllipsis2.
    def visitLiteralEllipsis2(self, ctx:RParser.LiteralEllipsis2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RParser#Arg.
    def visitArg(self, ctx:RParser.ArgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RParser#NoMatch.
    def visitNoMatch(self, ctx:RParser.NoMatchContext):
        return self.visitChildren(ctx)



del RParser