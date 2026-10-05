# Scanner -- The lexical analyzer for the Scheme printer and interpreter

import sys
import io
from Tokens import *

SPECIAL_INITIAL_CHARS = set("!$%&*/:<=>?^_~")

SPECIAL_SUBSEQUENT_CHARS = set("+-.@")

PECULIAR_IDENTIFIERS = set("+-")

class Scanner:
    def __init__(self, i):
        self.In = i
        self.buf = []
        self.ch_buf = None

    def read(self):
        if self.ch_buf == None:
            return self.In.read(1)
        else:
            ch = self.ch_buf
            self.ch_buf = None
            return ch
    
    def peek(self):
        if self.ch_buf == None:
            self.ch_buf = self.In.read(1)
            return self.ch_buf
        else:
            return self.ch_buf

    @staticmethod
    def isDigit(ch):
        return ch >= '0' and ch <= '9'

    @staticmethod
    def isInitial(ch):
        if ch >= 'A' and ch <= 'Z':
            return True

        if ch >= 'a' and ch <= 'z':
            return True

        if ch in SPECIAL_INITIAL_CHARS:
            return True

        return False

    @staticmethod
    def isSubsequent(ch):
        if Scanner.isInitial(ch):
            return True

        if Scanner.isDigit(ch):
            return True

        if ch in SPECIAL_SUBSEQUENT_CHARS:
            return True

        return False

    @staticmethod
    def isPeculiarIdentifier(ch):
        if ch in PECULIAR_IDENTIFIERS:
            return True

        return False

    def getNextToken(self):
        try:
            # It would be more efficient if we'd maintain our own
            # input buffer for a line and read characters out of that
            # buffer, but reading individual characters from the
            # input stream is easier.
            ch = self.read()

            # TODO: Skip white space and comments

            # Return None on EOF
            if ch == "":
                return None
    
            # Special characters
            elif ch == '\'':
                return Token(TokenType.QUOTE)
            elif ch == '(':
                return Token(TokenType.LPAREN)
            elif ch == ')':
                return Token(TokenType.RPAREN)
            elif ch == '.':
                #  We ignore the special identifier `...'.
                return Token(TokenType.DOT)

            # Boolean constants
            elif ch == '#':
                ch = self.read()

                if ch == 't':
                    return Token(TokenType.TRUE)
                elif ch == 'f':
                    return Token(TokenType.FALSE)
                elif ch == "":
                    sys.stderr.write("Unexpected EOF following #\n")
                    return None
                else:
                    sys.stderr.write("Illegal character '" +
                                     chr(ch) + "' following #\n")
                    return self.getNextToken()

            # String constants
            elif ch == '"':
                self.buf = []
                # TODO: scan a string into the buffer variable buf
    
                while True:
                    ch = self.read()

                    if ch == '"':
                        break

                    if ch == "":
                        sys.stderr.write("Unexpected EOF in string\n")
                        return None

                    self.buf.append(ch)

                return StrToken("".join(self.buf))

            # Integer constants
            elif self.isDigit(ch):
                i = ord(ch) - ord('0')
                # TODO: scan the number and convert it to an integer

                while True:
                    ch = self.peek()

                    if Scanner.isDigit(ch):
                        i = i * 10 + (ord(self.read()) - ord('0'))
                    else:
                        break

                # make sure that the character following the integer
                # is not removed from the input stream
                return IntToken(i)
    
            # Identifiers
            elif self.isInitial(ch):
                # or ch is some other vaid first character
                # for an identifier
                self.buf = [ch]
                # TODO: scan an identifier into the buffer variable buf

                while True:
                    ch = self.peek()

                    if Scanner.isSubsequent(ch):
                        self.buf.append(self.read())
                    else:
                        break

                # make sure that the character following the identifier
                # is not removed from the input stream
                return IdentToken("".join(self.buf).lower())

            elif self.isPeculiarIdentifier(ch):
                return IdentToken(ch.lower())

            # Whitespace
            elif ch.isspace():
                return self.getNextToken()
            
            # Illegal character
            else:
                sys.stderr.write("Illegal input character '" + ch + "'\n")
                return self.getNextToken()

        except IOError:
            sys.stderr.write("IOError: error reading input file\n")
            return None


if __name__ == "__main__":
    scanner = Scanner(sys.stdin)
    tok = scanner.getNextToken()
    tt = tok.getType()
    print(tt)
    if tt == TokenType.INT:
        print(tok.getIntVal())
