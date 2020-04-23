/*
 [The "BSD licence"]
 Copyright (c) 2013 Terence Parr
 All rights reserved.
 Redistribution and use in source and binary forms, with or without
 modification, are permitted provided that the following conditions
 are met:
 1. Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.
 2. Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in the
    documentation and/or other materials provided with the distribution.
 3. The name of the author may not be used to endorse or promote products
    derived from this software without specific prior written permission.
 THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
 IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
 OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
 IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
 INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
 NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
 THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/

/**
derived from http://svn.r-project.org/R/trunk/src/main/gram.y
http://cran.r-project.org/doc/manuals/R-lang.html#Parser
I'm no R genius but this seems to work.
Requires RFilter.g4 to strip away NL that are really whitespace,
not end-of-command. See TestR.java
Usage:
$ antlr4 R.g4 RFilter.g4
$ javac *.java
$ java TestR sample.R
... prints parse tree ...
*/
grammar R;

prog:   (   expr (';'|NL)*
        |   NL
        )*
        EOF
    ;

/*
expr_or_assign
    :   expr ('<-'|'='|'<<-') expr_or_assign
    |   expr
    ;
*/

expr:   expr '[[' sublist ']' ']'                                # IndexSingle // '[[' follows R's yacc grammar
    |   expr '[' sublist ']'                                     # IndexMany
    |   expr op=('::'|':::') expr                                # BinaryOp
    |   expr op=('$'|'@') expr                                   # BinaryOp
    |   expr NL* '(' sublist NL* ')'                             # Call        // call function  
    |   'function' '(' formlist? ')' expr                        # FunctionDef // define function
    |   <assoc=right> expr op='^' expr                           # BinaryOp
    |   op=('-'|'+') NL* expr                                    # UnaryOp
    |   expr op=':' NL* expr                                     # BinaryOp
    |   expr op=USER_OP NL* expr                                 # BinaryOpUser    // anything wrappedin %: '%' .* '%'
    |   expr op=('*'|'/') NL* expr                               # BinaryOp
    |   expr op=('+'|'-') NL* expr                               # BinaryOp
    |   expr op=('>'|'>='|'<'|'<='|'=='|'!=') NL* expr           # BinaryOp
    |   op='!' NL* expr                                          # UnaryOp
    |   expr op=('&'|'&&') NL* expr                              # BinaryOp
    |   expr op=('|'|'||') NL* expr                              # BinaryOp
    |   op='~' expr                                              # UnaryOp      // TODO: label as formula?
    |   expr op='~' expr                                         # BinaryOp
    |   expr op=('<-'|'<<-'|'='|'->'|'->>'|':=') NL* expr        # BinaryOp
    |   '{' NL* exprlist NL* '}'                                 # ExprList    // compound statement
    |   'if' '(' expr ')' expr                                   # IfStatement
    |   'if' '(' expr ')' expr 'else' expr                       # IfStatement
    |   'for' '(' ID 'in' expr ')' expr                          # ForStatement
    |   'while' '(' expr ')' expr                                # WhileStatement
    |   'repeat' expr                                            # RepeatStatement
    |   op='?' expr                                              # UnaryOp // get help on expr, usually string or ID
    |   'next'                                                   # NextStatement
    |   'break'                                                  # BreakStatement
    |   '(' expr ')'                                             # Parentheses
    |   ID                                                       # Name
    |   STRING                                                   # LiteralStr
    |   HEX                                                      # LiteralHex
    |   INT                                                      # LiteralInt
    |   FLOAT                                                    # LiteralDbl
    |   COMPLEX                                                  # LiteralComplex
    |   'NULL'                                                   # LiteralNull
    |   'NA'                                                     # LiteralNa
    |   'Inf'                                                    # LiteralInf
    |   'NaN'                                                    # LiteralNan
    |   'TRUE'                                                   # LiteralBool
    |   'FALSE'                                                  # LiteralBool
    ;

exprlist
    :   expr ((';'|NL) expr?)*
    |
    ;

formlist : form (',' form)* ;

form:   ID                                                      # Param
    |   ID '=' expr                                             # ParamKwarg
    |   ELLIPSIS                                                # LiteralEllipsis1
    ;

sublist : NL* sub NL* (',' NL* sub)* ;

sub :   ID '='                                                  # KwargEmpty
    |   ID '=' expr                                             # Kwarg
    |   STRING '='                                              # StrKwargEmpty
    |   STRING '=' expr                                         # StrKwarg
    |   'NULL' '='                                              # NullKwargEmpty
    |   'NULL' '=' expr                                         # NullKwarg
    |   ELLIPSIS                                                # LiteralEllipsis2
    |   expr                                                    # Arg
    |                                                           # NoMatch
    ;

HEX :   '0' ('x'|'X') HEXDIGIT+ [Ll]? ;

INT :   DIGIT+ [Ll]? ;

fragment
HEXDIGIT : ('0'..'9'|'a'..'f'|'A'..'F') ;

FLOAT:  DIGIT+ '.' DIGIT* EXP? [Ll]?
    |   DIGIT+ EXP? [Ll]?
    |   '.' DIGIT+ EXP? [Ll]?
    ;
fragment
DIGIT:  '0'..'9' ; 
fragment
EXP :   ('E' | 'e') ('+' | '-')? INT ;

COMPLEX
    :   INT 'i'
    |   FLOAT 'i'
    ;

ELLIPSIS: '...' ;

STRING
    :   '"' ( ESC | ~[\\"] )*? '"'
    |   '\'' ( ESC | ~[\\'] )*? '\''
    |   '`' ( ESC | ~[\\'] )*? '`'
    ;
fragment
ESC :   '\\' [abtnfrv"'\\]
    |   UNICODE_ESCAPE
    |   HEX_ESCAPE
    |   OCTAL_ESCAPE
    ;

fragment
UNICODE_ESCAPE
    :   '\\' 'u' HEXDIGIT HEXDIGIT HEXDIGIT HEXDIGIT
    |   '\\' 'u' '{' HEXDIGIT HEXDIGIT HEXDIGIT HEXDIGIT '}'
    ;

fragment
OCTAL_ESCAPE
    :   '\\' [0-3] [0-7] [0-7]
    |   '\\' [0-7] [0-7]
    |   '\\' [0-7]
    ;

fragment
HEX_ESCAPE
    :   '\\' HEXDIGIT HEXDIGIT?
    ;

ID  : '.' (LETTER|'_'|'.') (LETTER|DIGIT|'_'|'.')*
    | LETTER (LETTER|DIGIT|'_'|'.')*
    | '.'
    ;
    
fragment LETTER  : [a-zA-Z] ;

USER_OP :   '%' .*? '%' ;

COMMENT :   '#' .*? '\r'? '\n' -> type(NL) ;

// Match both UNIX and Windows newlines
NL      :   '\r'? '\n' ;

WS      :   [ \t\u000C]+ -> skip ;
