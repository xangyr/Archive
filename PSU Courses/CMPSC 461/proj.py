# author:   Xiangyu Ren
# psu id:   xvr5040@psu.edu
# date:     02/04/2020
# purpose:  grammar for query (SQL)
import sys

# type
# using integers for the type value, use lists to store the keywords and op
INVALID, INT, FLOAT, IDENTIFIER, KEYWORD, OPERATOR, COMMA, EOI = 0, 1, 2, 3, 4, 5, 6, 7
kw_l = ["SELECT", "FROM", "WHERE", "AND"]
op_l = ["=", "<", ">"]
# pattern
digit = "0123456789"
letter = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

# function: tp_string
# take in type, return the type name
def tp_string(tp):
    if tp == INT:
        return "Int"
    elif tp == FLOAT:
        return "Float"
    elif tp == IDENTIFIER:
        return "Identifier"
    elif tp == KEYWORD:
        return "Keyword"
    elif tp == OPERATOR:
        return "Operator"
    elif tp == COMMA:
        return "Comma"
    elif tp == EOI:
        return "EOI"
    return "Invalid"

# class: Token
# input: type, value
class Token:
    # set initial values for self.__tp & self.__val
    # set variables to private
    def __init__(self, tp, value):
        self.__tp = tp
        self.__val = value

    # return self.__tp
    def getType(self):
        return self.__tp

    # return self.__val
    def getValue(self):
        return self.__val

    # override function __repr
    def __repr__(self):
        if self.__tp in [INT, FLOAT, IDENTIFIER]:
            return self.__val
        elif self.__tp == KEYWORD:
            return self.__val
        elif self.__tp == OPERATOR:
            return self.__val
        elif self.__tp == COMMA:
            return ","
        elif self.__tp == EOI:
            return ""
        else:
            return "INVALID"

# class: Lexer
# input: query string
class Lexer:
    # set inits and call nextChar() to get the first char
    def __init__(self, s):
        self.query = s
        self.index = 0
        self.nextChar()

    # function to set self.char and update self.index
    def nextChar(self):
        self.char = self.query[self.index]
        self.index += 1
        return self.char

    '''
    def consumeChar(self, pattern):
        char = self.char
        if self.nextChar() in pattern:
            return char + self.consumeChar(pattern)
        else:
            return char
    '''

    # function to concatenate all chars that follow pattern
    # and return
    def consumeChar(self, pattern):
        r = self.char
        self.nextChar()
        while self.char in pattern:
            r = r + self.char
            self.nextChar()
        return r

    # check if nextChar() == ch
    # return boolean value
    def checkChar(self, ch):
        if self.nextChar() == ch:
            self.nextChar()
            return True
        else:
            return False

    # function: nextToken
    # 1. when meet a space, nextChar()
    # 2. when the first char is alphabet, check the rest
    #       if is letters or digits and not a keyword, Token(ID,...
    #       else, Token(KEYWORD,...
    # 3. when meet a digit, check the rest
    #       if meet a '.' then digits, Token(FLOAT,...
    #       if not '.', Token(INT,...
    #       else, Token(INVALID,...
    # 4. when meet a op, check around chars, if not surround by spaces, Token(OP,...
    # 5. when meet ',', Token(COMMA, ',')
    # 6. when meet '$', Token(EOI, '')
    # 7. else INVALID
    def nextToken(self):
        while True:
            if self.char == ' ':
                self.nextChar()
            elif self.char.isalpha():
                id = self.consumeChar(letter + digit)
                if id not in kw_l:
                    return Token(IDENTIFIER, id)
                else:
                    return Token(KEYWORD, id)
            elif self.char.isdigit():
                num = self.consumeChar(digit)
                if self.char != ".":
                    return Token(INT, num)
                num += self.char
                self.nextChar()
                if self.char.isdigit():
                    num += self.consumeChar(digit)
                    return Token(FLOAT, num)
                else:
                    return Token(INVALID, num)
            elif self.char in op_l:
                op = self.char
                if self.query[self.index] == ' ' or \
                        self.query[self.index-2] == ' ':
                    return Token(INVALID, op)
                self.nextChar()
                return Token(OPERATOR, op)
            elif self.char == ',':
                self.nextChar()
                return Token(COMMA, ",")
            # elif self.char is self.query[-1]:
            elif self.char == '$':
                return Token(EOI, '')
            else:
                self.nextChar()
                return Token(INVALID, self.char)

# class: Parser
# input: query string
class Parser:
    # build object lexer and set the token
    # add '$' to the end of query for helping recognize EOI
    def __init__(self, s):
        self.lexer = Lexer(s + '$')
        self.token = self.lexer.nextToken()

    # run the parser
    def run(self):
        self.query()

    # function to check if the toke type is the type we want
    # if is, update self.token
    # if not, syntax error
    def match(self, tp):
        val = self.token.getValue()
        if self.token.getType() == tp:
            self.token = self.lexer.nextToken()
        else:
            self.tp_error(tp)
        return val

    # function to handle the syntax error
    def tp_error(self, tp):
        print "Syntax error: expecting: " + tp_string(tp) \
              + "; saw: " + tp_string(self.token.getType())
        sys.exit(1)

    # function to handle the invalid keyword input
    def key_error(self, saw, exp):
        print "Keyword invalid: expecting: " + exp \
              + "; saw: " + saw
        sys.exit(1)

    # the start case of the grammar
    # SELECT <IDList> FROM <IDList> [WHERE <CondList>]
    # first match SELECT,
    # then call idlist() for matching,
    # then match FROM,
    # then idlist() again,
    # then use if the determine if has keyword WHERE,
    # if has match and condlist,
    # if no match EOI
    def query(self):
        print "<Query>"
        key = self.match(KEYWORD)
        if key == "SELECT":
            print "\t<Keyword>" + key + "</Keyword>"
        else:
            self.key_error(key, "SELECT")
        self.idlist()
        key = self.match(KEYWORD)
        if key == "FROM":
            print "\t<Keyword>" + key + "</Keyword>"
        else:
            self.key_error(key, "FROM")
        self.idlist()
        if self.token.getValue() == 'WHERE':
            key = self.match(KEYWORD)
            if key == "WHERE":
                print "\t<Keyword>" + key + "</Keyword>"
            else:
                self.key_error(key, "WHERE")
            print "\t<CondList>"
            self.cond()
            while self.token.getType() == KEYWORD and \
                    self.token.getValue() == "AND":
                print "\t\t<Keyword>AND</Keyword>"
                self.token = self.lexer.nextToken()
                self.cond()
            print "\t</CondList>"
        self.match(EOI)
        print "</Query>"

    # function for matching idlist,
    # first match id and use while to see if has other ', id'
    def idlist(self):
        print "\t<IdList>"
        id = self.match(IDENTIFIER)
        print "\t\t<Id>" + id + "</Id>"
        while self.token.getType() == COMMA:
            print "\t\t<Comma>,</Comma>"
            self.token = self.lexer.nextToken()
            id = self.match(IDENTIFIER)
            print "\t\t<Id>" + id + "</Id>"
        print "\t</IdList>"

    # function for matching cond,
    # match id, op, and term sequentially
    def cond(self):
        print "\t\t<Cond>"
        id = self.match(IDENTIFIER)
        print "\t\t\t<Id>" + id + "</Id>"
        op = self.match(OPERATOR)
        print "\t\t\t<Operator>" + op + "</Operator>"
        print "\t\t\t<Term>"
        self.term()
        print "\t\t\t</Term>"
        print "\t\t</Cond>"
    # function for matching terms,
    # use if statements to match id, int, or float
    def term(self):
        if self.token.getType() == IDENTIFIER:
            print "\t\t\t\t<Identifier>" + self.token.getValue() \
                  + "</Identifier>"
        elif self.token.getType() == INT:
            print "\t\t\t\t<Int>" + self.token.getValue() + "</Int>"
        elif self.token.getType() == FLOAT:
            print "\t\t\t\t<Float>" + self.token.getValue() + "</Float>"
        else:
            print "Syntax error: expecting an ID, an int, or a float" \
                  + "; saw:" \
                  + tp_string(self.token.getType())
            sys.exit(1)
        self.token = self.lexer.nextToken()


if __name__ == "__main__":
    ##########################################
    print "Testing the lexer: test 1"
    lex = Lexer("ab12, abdgydf, weihief $")
    tk = lex.nextToken()
    while tk.getType() != EOI:
        print tk
        tk = lex.nextToken()
    print

    print "Testing the lexer: test 2"
    lex = Lexer("x=5.4 AND y<5 AND z>7 $")
    tk = lex.nextToken()
    while tk.getType() != EOI:
        print tk
        tk = lex.nextToken()
    print

    print "Testing the lexer: test 3"
    lex = Lexer("ab12=6.87 AND y>xv AND z=ab $")
    tk = lex.nextToken()
    while tk.getType() != EOI:
        print tk
        tk = lex.nextToken()

    ##########################################
    print "\nTesting the parser: test 1"
    parser = Parser("SELECT C1,C2 FROM T1")
    parser.run()

    print "\nTesting the parser: test 2"
    parser = Parser("SELECT C1,C2 FROM T1 WHERE C1=5.23")
    parser.run()

    print "\nTesting the parser: test 3"
    parser = Parser("SELECT C1,C2 FROM T1 WHERE C1=3 AND C2<C1 AND C3")
    parser.run()
