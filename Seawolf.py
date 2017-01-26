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

stack = [{}]
functionMap = {}

class IntLiteral(Node):

    def __init__(self, value):
        self.value = int(value)

    def evaluate(self):
        return self.value

class Variable(Node):

    def __init__(self, value):
        self.value = value

    def evaluate(self):
        if self.value in stack[len(stack) - 1].keys():
            value = stack[len(stack) - 1][self.value]
        else:
            value = stack[0][self.value]
        return value
    
class Assign(Node):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self):
        stack[len(stack) - 1][self.left.value] = self.right.evaluate()

class Print(Node):

    def __init__(self, value):
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
        self.statements = []

    def evaluate(self):
        for l in self.statements:
            result = l.evaluate()
            if isinstance(l, Block) or isinstance(l, If) or isinstance(l, Else):
                if result is not None:
                    return result
            if isinstance(l, Return):
                return result

class Return(Node):

    def __init__(self, value):
        self.value = value

    def evaluate(self):
        return self.value.evaluate()

class If(Node):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self):
        result = None
        if self.left.evaluate():
            self.right.evaluate()
        if result is not None:
            return result

class Else(Node):

    def __init__(self, left, right1, right2):
        self.left = left
        self.right1 = right1
        self.right2 = right2

    def evaluate(self):
        result = None
        if self.left.evaluate():
            result = self.right1.evaluate()
        else:
            result = self.right2.evaluate()
        if result is not None:
            return result

class ProcDef(Node):

    def __init__(self, left, param, right):
        self.left = left
        self.param = param
        self.right = right

    def evaluate(self):
        for i in range(0, len(self.param)):
            self.param[i] = self.param[i].value
        functionMap[self.left.value] = [self.param, self.right]

class ProcedureCall(Node):

    def __init__(self, left, param):
        self.left = left
        self.param = param

    def evaluate(self):
        newMap = {}
        for i in range(0, len(self.param)):
            newMap[functionMap[self.left.value][0][i]] = self.param[i].evaluate()
        stack.append(newMap)
        result = functionMap[self.left.value][1].evaluate()
        stack.pop()
        if result is not None:
            return result
            

class Parser(tpg.Parser):
    """
    token int "\d+" IntLiteral;
    token variable '[A-Za-z][A-Za-z0-9]*' Variable;
    separator space "\s+";
 
    START/a -> $ a = Block() $ ( statement/b $ a.statements.append(b) $)* ;
   
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
