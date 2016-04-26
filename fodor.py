import sys
import tpg

class SemanticError(Exception):
    """
    This is the class of the exception that is raised when a semantic error
    occurs.
    """
class Node(object):
    """
    A base class for nodes. Might come in handy in the future.
    """

    def evaluate(self):
        """
        Called on children of Node to evaluate that child.
        """
        raise Exception("Not implemented.")

class VariableMap(Node):

    def __init__(self):
        self.map = {}

variableMap = VariableMap()

class IntLiteral(Node):

    def __init__(self, value):
        self.value = int(value)

    def evaluate(self):
        return self.value

class Variable(Node):

    def __init__(self, value):
        self.value = value;

    def evaluate(self):
        return variableMap[self.value]
    
class Assign(Node):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self):
        variableMap[self.left] = self.right.evaluate()

class Print(Node):

    def __init__(self, value):
        print("Print construction")
        self.value = value

    def evaluate(self):
        print(self.value.evaluate())

class Operation(Node):

    def __init__(self, operate, left, right):
        self.operate = operate
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        return {
            '*': left * right,
            '+': left + right,
            '-': left - right,
            '%': left % right
        }[self.operate]

class Compare(Node):

    def __init__(self, operate, left, right):
        self.operate = operate
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        boolean = {
            '<':left < right,
            '==':left == right
        }[self.operate]
        if boolean:
            return 1
        else:
            return 0
    
# Above: Done
# Below: Work

class Block(Node):

    def __init__(self):
        print("Block construction")
        self.statements = []

    def evaluate(self):
        for l in self.statements:
            l.evaluate()

class Return(Node):

    def __init__(self, value):
        self.value = value

    def evaluate(self):
        return self.value.evaluate()

class Parser(tpg.Parser):
    """
    token int "\d+" IntLiteral;
    token variable '[A-Za-z][A-Za-z0-9]*' Variable;
    separator space "\s+";
 
    START/a -> statement/a ;
   
    statement/a -> ( _func_def/a | block/a | code/a );
   
    block/a -> "\{" $ a = Block() $ ( statement/b $ a.statements.append(b) $ )* "\}";
   
    code/a -> ( _if_else/a | _if/a | lines/a );
    lines/a -> ( _assign/a | _print/a | _return/a | _function/a ) ";" ;
   
    _func_def/a -> variable/v params/n block/b    $ a = ProcDef(v, n, b) $ ;
    _if_else/a -> "if" "\(" expression/e "\)" statement/d "else" statement/s   $ a = Else(e,d,s) $;
    _if/a -> "if" "\(" expression/e "\)" statement/s       $ a = If(e, s) $;
    _assign/a -> expression/a "=(?!=)" expression/b        $ a = Assign(a, b) $ ;
    _print/a -> "print" expression/a                       $ a = Print(a) $ ;
    _return/a -> "return " expression/a                    $ a = Return(a) $ ;
    _function/a -> variable/v param_list/l                 $ a = ProcedureCall(v, l) $ ;
   
    expression/a -> compare/a;
 
    compare/a -> mod/a
    ( "<" mod/b $ a = Compare("<", a, b) $
    | "==" mod/b $ a = Compare("==", a, b) $
    )* ;
    
    mod/a -> addsub/a ( "\%" addsub/b $ a = Operation("%", a, b) $)*;
 
    addsub/a -> muldiv/a
    ( "\+" muldiv/b $ a = Operation("+", a, b) $
    | "\-"  muldiv/b $ a = Operation("-", a, b) $
    )* ;
 
    muldiv/a -> parens/a
    ( "\*" parens/b $ a = Operation("*", a, b) $
    )* ;
   
    parens/a -> _function/a | "\(" expression/a "\)" | literal/a | variable/a;
 
    literal/a -> int/a;
     
    params/a -> "\(" $ a = [] $ ( variable/v $ a.append(v) $ )?
    ( "," variable/v $ a.append(v) $ )*
    "\)"
    ;
   
    param_list/a -> "\(" $ a = [] $ ( expression/e $ a.append(e) $ )?
    ( "," expression/e $ a.append(e) $ )*
    "\)"
    ;
    """

parse = Parser()

try:
    f = open(sys.argv[1], "r")
except(IndexError, IOError):
    f = open("input1.txt", "r")
    
line = f.read()
f.close()

try:
    node = parse(line)

    result = node.evaluate()

except tpg.Error:
    print("SYNTAX ERROR")
        
except SemanticError:
    print("SEMANTIC ERROR")
