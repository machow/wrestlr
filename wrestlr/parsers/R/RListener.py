# Generated from wrestlr/parsers/R/R.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .RParser import RParser
else:
    from RParser import RParser

# This class defines a complete listener for a parse tree produced by RParser.
class RListener(ParseTreeListener):

    # Enter a parse tree produced by RParser#prog.
    def enterProg(self, ctx:RParser.ProgContext):
        pass

    # Exit a parse tree produced by RParser#prog.
    def exitProg(self, ctx:RParser.ProgContext):
        pass


    # Enter a parse tree produced by RParser#LiteralHex.
    def enterLiteralHex(self, ctx:RParser.LiteralHexContext):
        pass

    # Exit a parse tree produced by RParser#LiteralHex.
    def exitLiteralHex(self, ctx:RParser.LiteralHexContext):
        pass


    # Enter a parse tree produced by RParser#LiteralNan.
    def enterLiteralNan(self, ctx:RParser.LiteralNanContext):
        pass

    # Exit a parse tree produced by RParser#LiteralNan.
    def exitLiteralNan(self, ctx:RParser.LiteralNanContext):
        pass


    # Enter a parse tree produced by RParser#FunctionDef.
    def enterFunctionDef(self, ctx:RParser.FunctionDefContext):
        pass

    # Exit a parse tree produced by RParser#FunctionDef.
    def exitFunctionDef(self, ctx:RParser.FunctionDefContext):
        pass


    # Enter a parse tree produced by RParser#WhileStatement.
    def enterWhileStatement(self, ctx:RParser.WhileStatementContext):
        pass

    # Exit a parse tree produced by RParser#WhileStatement.
    def exitWhileStatement(self, ctx:RParser.WhileStatementContext):
        pass


    # Enter a parse tree produced by RParser#Name.
    def enterName(self, ctx:RParser.NameContext):
        pass

    # Exit a parse tree produced by RParser#Name.
    def exitName(self, ctx:RParser.NameContext):
        pass


    # Enter a parse tree produced by RParser#IfStatement.
    def enterIfStatement(self, ctx:RParser.IfStatementContext):
        pass

    # Exit a parse tree produced by RParser#IfStatement.
    def exitIfStatement(self, ctx:RParser.IfStatementContext):
        pass


    # Enter a parse tree produced by RParser#LiteralDbl.
    def enterLiteralDbl(self, ctx:RParser.LiteralDblContext):
        pass

    # Exit a parse tree produced by RParser#LiteralDbl.
    def exitLiteralDbl(self, ctx:RParser.LiteralDblContext):
        pass


    # Enter a parse tree produced by RParser#ForStatement.
    def enterForStatement(self, ctx:RParser.ForStatementContext):
        pass

    # Exit a parse tree produced by RParser#ForStatement.
    def exitForStatement(self, ctx:RParser.ForStatementContext):
        pass


    # Enter a parse tree produced by RParser#LiteralInf.
    def enterLiteralInf(self, ctx:RParser.LiteralInfContext):
        pass

    # Exit a parse tree produced by RParser#LiteralInf.
    def exitLiteralInf(self, ctx:RParser.LiteralInfContext):
        pass


    # Enter a parse tree produced by RParser#BinaryOpUser.
    def enterBinaryOpUser(self, ctx:RParser.BinaryOpUserContext):
        pass

    # Exit a parse tree produced by RParser#BinaryOpUser.
    def exitBinaryOpUser(self, ctx:RParser.BinaryOpUserContext):
        pass


    # Enter a parse tree produced by RParser#Parentheses.
    def enterParentheses(self, ctx:RParser.ParenthesesContext):
        pass

    # Exit a parse tree produced by RParser#Parentheses.
    def exitParentheses(self, ctx:RParser.ParenthesesContext):
        pass


    # Enter a parse tree produced by RParser#BinaryOp.
    def enterBinaryOp(self, ctx:RParser.BinaryOpContext):
        pass

    # Exit a parse tree produced by RParser#BinaryOp.
    def exitBinaryOp(self, ctx:RParser.BinaryOpContext):
        pass


    # Enter a parse tree produced by RParser#Call.
    def enterCall(self, ctx:RParser.CallContext):
        pass

    # Exit a parse tree produced by RParser#Call.
    def exitCall(self, ctx:RParser.CallContext):
        pass


    # Enter a parse tree produced by RParser#LiteralBool.
    def enterLiteralBool(self, ctx:RParser.LiteralBoolContext):
        pass

    # Exit a parse tree produced by RParser#LiteralBool.
    def exitLiteralBool(self, ctx:RParser.LiteralBoolContext):
        pass


    # Enter a parse tree produced by RParser#UnaryOp.
    def enterUnaryOp(self, ctx:RParser.UnaryOpContext):
        pass

    # Exit a parse tree produced by RParser#UnaryOp.
    def exitUnaryOp(self, ctx:RParser.UnaryOpContext):
        pass


    # Enter a parse tree produced by RParser#LiteralStr.
    def enterLiteralStr(self, ctx:RParser.LiteralStrContext):
        pass

    # Exit a parse tree produced by RParser#LiteralStr.
    def exitLiteralStr(self, ctx:RParser.LiteralStrContext):
        pass


    # Enter a parse tree produced by RParser#LiteralInt.
    def enterLiteralInt(self, ctx:RParser.LiteralIntContext):
        pass

    # Exit a parse tree produced by RParser#LiteralInt.
    def exitLiteralInt(self, ctx:RParser.LiteralIntContext):
        pass


    # Enter a parse tree produced by RParser#LiteralNa.
    def enterLiteralNa(self, ctx:RParser.LiteralNaContext):
        pass

    # Exit a parse tree produced by RParser#LiteralNa.
    def exitLiteralNa(self, ctx:RParser.LiteralNaContext):
        pass


    # Enter a parse tree produced by RParser#BreakStatement.
    def enterBreakStatement(self, ctx:RParser.BreakStatementContext):
        pass

    # Exit a parse tree produced by RParser#BreakStatement.
    def exitBreakStatement(self, ctx:RParser.BreakStatementContext):
        pass


    # Enter a parse tree produced by RParser#LiteralComplex.
    def enterLiteralComplex(self, ctx:RParser.LiteralComplexContext):
        pass

    # Exit a parse tree produced by RParser#LiteralComplex.
    def exitLiteralComplex(self, ctx:RParser.LiteralComplexContext):
        pass


    # Enter a parse tree produced by RParser#ExprList.
    def enterExprList(self, ctx:RParser.ExprListContext):
        pass

    # Exit a parse tree produced by RParser#ExprList.
    def exitExprList(self, ctx:RParser.ExprListContext):
        pass


    # Enter a parse tree produced by RParser#LiteralNull.
    def enterLiteralNull(self, ctx:RParser.LiteralNullContext):
        pass

    # Exit a parse tree produced by RParser#LiteralNull.
    def exitLiteralNull(self, ctx:RParser.LiteralNullContext):
        pass


    # Enter a parse tree produced by RParser#NextStatement.
    def enterNextStatement(self, ctx:RParser.NextStatementContext):
        pass

    # Exit a parse tree produced by RParser#NextStatement.
    def exitNextStatement(self, ctx:RParser.NextStatementContext):
        pass


    # Enter a parse tree produced by RParser#IndexSingle.
    def enterIndexSingle(self, ctx:RParser.IndexSingleContext):
        pass

    # Exit a parse tree produced by RParser#IndexSingle.
    def exitIndexSingle(self, ctx:RParser.IndexSingleContext):
        pass


    # Enter a parse tree produced by RParser#IndexMany.
    def enterIndexMany(self, ctx:RParser.IndexManyContext):
        pass

    # Exit a parse tree produced by RParser#IndexMany.
    def exitIndexMany(self, ctx:RParser.IndexManyContext):
        pass


    # Enter a parse tree produced by RParser#RepeatStatement.
    def enterRepeatStatement(self, ctx:RParser.RepeatStatementContext):
        pass

    # Exit a parse tree produced by RParser#RepeatStatement.
    def exitRepeatStatement(self, ctx:RParser.RepeatStatementContext):
        pass


    # Enter a parse tree produced by RParser#exprlist.
    def enterExprlist(self, ctx:RParser.ExprlistContext):
        pass

    # Exit a parse tree produced by RParser#exprlist.
    def exitExprlist(self, ctx:RParser.ExprlistContext):
        pass


    # Enter a parse tree produced by RParser#formlist.
    def enterFormlist(self, ctx:RParser.FormlistContext):
        pass

    # Exit a parse tree produced by RParser#formlist.
    def exitFormlist(self, ctx:RParser.FormlistContext):
        pass


    # Enter a parse tree produced by RParser#Param.
    def enterParam(self, ctx:RParser.ParamContext):
        pass

    # Exit a parse tree produced by RParser#Param.
    def exitParam(self, ctx:RParser.ParamContext):
        pass


    # Enter a parse tree produced by RParser#ParamKwarg.
    def enterParamKwarg(self, ctx:RParser.ParamKwargContext):
        pass

    # Exit a parse tree produced by RParser#ParamKwarg.
    def exitParamKwarg(self, ctx:RParser.ParamKwargContext):
        pass


    # Enter a parse tree produced by RParser#LiteralEllipsis1.
    def enterLiteralEllipsis1(self, ctx:RParser.LiteralEllipsis1Context):
        pass

    # Exit a parse tree produced by RParser#LiteralEllipsis1.
    def exitLiteralEllipsis1(self, ctx:RParser.LiteralEllipsis1Context):
        pass


    # Enter a parse tree produced by RParser#sublist.
    def enterSublist(self, ctx:RParser.SublistContext):
        pass

    # Exit a parse tree produced by RParser#sublist.
    def exitSublist(self, ctx:RParser.SublistContext):
        pass


    # Enter a parse tree produced by RParser#KwargEmpty.
    def enterKwargEmpty(self, ctx:RParser.KwargEmptyContext):
        pass

    # Exit a parse tree produced by RParser#KwargEmpty.
    def exitKwargEmpty(self, ctx:RParser.KwargEmptyContext):
        pass


    # Enter a parse tree produced by RParser#Kwarg.
    def enterKwarg(self, ctx:RParser.KwargContext):
        pass

    # Exit a parse tree produced by RParser#Kwarg.
    def exitKwarg(self, ctx:RParser.KwargContext):
        pass


    # Enter a parse tree produced by RParser#StrKwargEmpty.
    def enterStrKwargEmpty(self, ctx:RParser.StrKwargEmptyContext):
        pass

    # Exit a parse tree produced by RParser#StrKwargEmpty.
    def exitStrKwargEmpty(self, ctx:RParser.StrKwargEmptyContext):
        pass


    # Enter a parse tree produced by RParser#StrKwarg.
    def enterStrKwarg(self, ctx:RParser.StrKwargContext):
        pass

    # Exit a parse tree produced by RParser#StrKwarg.
    def exitStrKwarg(self, ctx:RParser.StrKwargContext):
        pass


    # Enter a parse tree produced by RParser#NullKwargEmpty.
    def enterNullKwargEmpty(self, ctx:RParser.NullKwargEmptyContext):
        pass

    # Exit a parse tree produced by RParser#NullKwargEmpty.
    def exitNullKwargEmpty(self, ctx:RParser.NullKwargEmptyContext):
        pass


    # Enter a parse tree produced by RParser#NullKwarg.
    def enterNullKwarg(self, ctx:RParser.NullKwargContext):
        pass

    # Exit a parse tree produced by RParser#NullKwarg.
    def exitNullKwarg(self, ctx:RParser.NullKwargContext):
        pass


    # Enter a parse tree produced by RParser#LiteralEllipsis2.
    def enterLiteralEllipsis2(self, ctx:RParser.LiteralEllipsis2Context):
        pass

    # Exit a parse tree produced by RParser#LiteralEllipsis2.
    def exitLiteralEllipsis2(self, ctx:RParser.LiteralEllipsis2Context):
        pass


    # Enter a parse tree produced by RParser#Arg.
    def enterArg(self, ctx:RParser.ArgContext):
        pass

    # Exit a parse tree produced by RParser#Arg.
    def exitArg(self, ctx:RParser.ArgContext):
        pass


    # Enter a parse tree produced by RParser#NoMatch.
    def enterNoMatch(self, ctx:RParser.NoMatchContext):
        pass

    # Exit a parse tree produced by RParser#NoMatch.
    def exitNoMatch(self, ctx:RParser.NoMatchContext):
        pass


