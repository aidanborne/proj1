# Parser -- the parser for the Scheme printer and interpreter
#
# Defines
#
#   class Parser
#
# Parses the language
#
#   exp  ->  ( rest
#         |  #f
#         |  #t
#         |  ' exp
#         |  integer_constant
#         |  string_constant
#         |  identifier
#    rest -> )
#         |  exp+ [. exp] )
#
# and builds a parse tree.  Lists of the form (rest) are further
# `parsed' into regular lists and special forms in the constructor
# for the parse tree node class Cons.  See Cons.parseList() for
# more information.
#
# The parser is implemented as an LL(0) recursive descent parser.
# I.e., parseExp() expects that the first token of an exp has not
# been read yet.  If parseRest() reads the first token of an exp
# before calling parseExp(), that token must be put back so that
# it can be re-read by parseExp() or an alternative version of
# parseExp() must be called.
#
# If EOF is reached (i.e., if the scanner returns None instead of a token),
# the parser returns None instead of a tree.  In case of a parse error, the
# parser discards the offending token (which probably was a DOT
# or an RPAREN) and attempts to continue parsing with the next token.

import sys
from Tokens import TokenType
from Tree import *

class Parser:
    def __init__(self, s):
        self.scanner = s
        self.tok_buf = None

    def parseExp(self):
        # TODO: write code for parsing an exp

        tok = self.nextToken()

        if tok is None:
            return None

        tt = tok.getType()

        if tt == TokenType.QUOTE:
            return self.parseQuote()

        elif tt == TokenType.LPAREN:
            return self.parseRest()

        elif tt == TokenType.TRUE:
            return BoolLit(True)

        elif tt == TokenType.FALSE:
            return BoolLit(False)

        elif tt == TokenType.INT:
            return IntLit(tok.getIntVal())

        elif tt == TokenType.STR:
            return StrLit(tok.getStrVal())

        elif tt == TokenType.IDENT:
            return Ident(tok.getName())

        return None

    def parseQuote(self):
        exp = self.parseExp()

        cons = Ident("quote")
        cdr = Cons(exp, Nil.getInstance())

        return Cons(cons, cdr)

    def parseRest(self):
        tok = self.peekToken()

        if tok.getType() == TokenType.RPAREN:
            self.nextToken()
            return Nil.getInstance()

        car = self.parseExp()

        tok = self.peekToken()

        if tok.getType() == TokenType.DOT:
            self.nextToken()

            cdr = self.parseExp()
            self.expectTokenType(TokenType.RPAREN)
            
            return Cons(car, cdr)

        cdr = self.parseRest()

        return Cons(car, cdr)

    # TODO: Add any additional methods you might need

    def __error(self, msg):
        sys.stderr.write("Parse error: " + msg + "\n")

    def nextToken(self):
        if self.tok_buf is None:
            return self.scanner.getNextToken()

        tok = self.tok_buf
        self.tok_buf = None

        return tok


    def peekToken(self):
        if self.tok_buf:
            return self.tok_buf

        tok = self.scanner.getNextToken()
        self.tok_buf = tok

        return tok

    def expectTokenType(self, tt):
        tok = self.nextToken()

        if tok.getType() == tt:
            return tok

        self.__error("Expected token type " + str(tt) +
                        ", but got " + str(tok.getType()))
        
        return None
