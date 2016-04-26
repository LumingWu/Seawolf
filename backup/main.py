import sys
import tpg

class Variables():
    def __init__(self):
        self.variables = {}
        
    def put(self, key, value):
        print("Putting: ", key, " ", value)
        self.variables[key] = value
        
    def get(self, key):
        print("Getting: ", key, " ", self.variables[key])
        return self.variables[key]

class SemanticError(Exception):
    """
    This is the class of the exception that is raised when a semantic error
    occurs.
    """
    
# These are the nodes of our abstract syntax tree.
class Node(object):
    """
    A base class for nodes. Might come in handy in the future.
    """

    def evaluate(self):
        """
        Called on children of Node to evaluate that child.
        """
        raise Exception("Not implemented.")

class IntLiteral(Node):

    def __init__(self, value):
        print("Integer construction: ", value)
        self.value = int(value)

    def evaluate(self):
        return self.value

class RealLiteral(Node):

    def __init__(self, value):
        print("Real construction: ", value)
        self.value = float(value)

    def evaluate(self):
        return self.value

class BooleanLiteral(Node):

    def __init__(self, value):
        print("Boolean construction: ", value)
        if value[0] == "t":
            self.value = 1
        elif value[0] == "f":
            self.value = 0
        elif int(value):
            self.value = 1
        else:
            self.value = 0

    def evaluate(self):
        return self.value

class StringLiteral(Node):

    def __init__(self, value):
        print("String construction: ", value)
        temp = str(value)
        self.value = temp[1:len(temp)-1]

    def evaluate(self):
        return self.value

class ListLiteral(Node):

    def __init__(self):
        print("List construction: []")
        self.value = []

    def append(self, value):
        print("List append: ", self.value, value.value)
        self.value.append(value)

    def evaluate(self):
        print("List evaluate: ")
        l = []
        for i in self.value:
            l.append(i.evaluate())
        return l

class VariableLiteral(Node):

    def __init__(self, value):
        print("Variable construction: ", value)
        self.value = value

    def evaluate(self):
        print("Variable evaluation: ", self.value)
        return variables.get(self.value)

class Block(Node):

    def __init__(self):
        print("Block construction: ")
        self.block = []

    def evaluate(self):
        print("Block evaluation: ")
        for l in self.block:
            l.evaluate()

    def append(self, node):
        self.block.append(node)

class IF(Node):

    def __init__(self, condition, block1, block2):
        print("If construction:")
        self.condition = condition
        self.block1 = block1
        self.block2 = block2
        
    def evaluate(self):
        if(self.condition.evaluate()):
            self.block1.evaluate()
        else:
            self.block2.evaluate()

class WHILE(Node):

    def __init__(self, condition, block):
        print("While construction")
        self.condition = condition
        self.block = block

    def evaluate(self):
        while self.condition.evaluate():
            self.block.evaluate()

class Print(Node):

    def __init__(self):
        print("Print construction: ")

    def line(self, value):
        print("Print line: ", type(value))
        self.value = value
        
    def evaluate(self):
        print("Console print: ", self.value.evaluate())
        
class Assign(Node):

    def __init__(self, left, right):
        print("Assign construction: ", type(left), type(right))
        self.left = left
        self.right = right

    def evaluate(self):
        if isinstance(self.left, VariableLiteral):
            variables.put(self.left.value, self.right.evaluate())
        else:
            self.left.setValue(self.right.evaluate())
        

class Index(Node):

    def __init__(self, left, right):
        print("Operation index ", type(left), type(right))
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if not ((isinstance(left, str) or isinstance(left, list)) and isinstance(right, int)):
            raise SemanticError
        return left[right]

    def setValue(self, value):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if not ((isinstance(left, str) or isinstance(left, list)) and isinstance(right, int)):
            raise SemanticError
        left[right] = value

class Equal(Node):

    def __init__(self, left, right):
        print("Operation == ", type(left), type(right))
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if left == right:
            return 1
        return 0

class NotEqual(Node):

    def __init__(self, left, right):
        print("Operation != ", type(left), type(right))
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if left != right:
            return 1
        return 0

class Less(Node):

    def __init__(self, left, right):
        print("Operation < ", type(left), type(right))
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if left < right:
            return 1
        return 0
    
class LessEqual(Node):

    def __init__(self, left, right):
        print("Operation <= ", type(left), type(right))
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if left <= right:
            return 1
        return 0
    
class Larger(Node):

    def __init__(self, left, right):
        print("Operation > ", type(left), type(right))
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if left > right:
            return 1
        return 0
    
class LargerEqual(Node):

    def __init__(self, left, right):
        print("Operation >= ", type(left), type(right))
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if left >= right:
            return 1
        return 0

class And(Node):
    
    def __init__(self, left, right):
        print("Operation and ", type(left), type(right))
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if not (isinstance(left, int) and isinstance(right, int)):
            raise SemanticError()
        if left and right:
            return 1
        return 0

class Or(Node):

    def __init__(self, left, right):
        print("Operation or ", type(left), type(right))
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if not (isinstance(left, int) and isinstance(right, int)):
            raise SemanticError()
        if left or right:
            return 1
        return 0

class Not(Node):

    def __init__(self, left):
        print("Operation not ", type(left))
        self.left = left

    def evaluate(self):
        left = self.left.evaluate()
        if not isinstance(left, int):
            raise SemanticError()
        if left:
            return 0
        return 1

class Add(Node):

    def __init__(self, left, right):
        print("Operation add: ", type(left), " + ", type(right))
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if not ((isinstance(left, int) or isinstance(left, float)) and (isinstance(right, int) or isinstance(right, float))) and not (isinstance(left, str) and isinstance(right, str)):
            raise SemanticError()
        return left + right

class Subtract(Node):

    def __init__(self, left, right):
        print("Operation subtract ", type(left), type(right))
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if not (isinstance(left, int) or isinstance(left, float)) and (isinstance(right, int) or isinstance(right, float)):
            raise SemanticError()
        return left - right

class Multiply(Node):

    def __init__(self, left, right):
        print("Operation multiply ", type(left), type(right))
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if not (isinstance(left, int) or isinstance(left, float)) and (isinstance(right, int) or isinstance(right, float)):
            raise SemanticError()
        return left * right

class Divide(Node):

    def __init__(self, left, right):
        print("Operation divide ", type(left), type(right))
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if not (isinstance(left, int) or isinstance(left, float)):
            raise SemanticError()
        if isinstance(right, int):
            if right is 0:
                raise SemanticError()
        elif isinstance(right, float):
            if right is 0.0:
                raise SemanticError()
        else:
            raise SemanticError()
        return left / right

class FloorDivide(Node):
    
    def __init__(self ,left, right):
        print("Operation floor divide ", type(left), type(right))
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if not (isinstance(left, int) or isinstance(left, float)):
            raise SemanticError()
        if isinstance(right, int):
            if right is 0:
                raise SemanticError()
        elif isinstance(right, float):
            if right is 0.0:
                raise SemanticError()
        else:
            raise SemanticError()
        return left // right

class Modulo(Node):

    def __init__(self ,left, right):
        print("Operation modulo ", type(left), type(right))
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if not (isinstance(left, int) or isinstance(left, float)):
            raise SemanticError()
        if isinstance(right, int):
            if right is 0:
                raise SemanticError()
        elif isinstance(right, float):
            if right is 0.0:
                raise SemanticError()
        else:
            raise SemanticError()
        return left % right

class Power(Node):

    def __init__(self, left, right):
        print("Operation power ", type(left), type(right))
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if not (isinstance(left, int) or isinstance(left, float)) and (isinstance(right, int) or isinstance(right, float)):
            raise SemanticError()
        return left ** right
    
# This is the TPG Parser that is responsible for turning our language into
# an abstract syntax tree.
class Parser(tpg.Parser):
    """
    token real "\d*\.\d+|\d+\.\d*" RealLiteral;
    token int "\d+" IntLiteral;
    token boolean "true|false" BooleanLiteral;
    token string "\\"[^\\"]*\\"" StringLiteral;
    token variable "[A-Za-z][A-Za-z0-9_]*" VariableLiteral;
    separator space "\s+";
    
    START/a -> Block/a;

    HighLevelStructure/a -> "if" Return/b (Block/c "else" Block/d $a=IF(b, c, d)$ | Block/c$a=IF(b, c, Block())$)
    | "while" Return/b Block/c $a=WHILE(b, c)$;

    Block/a -> "{"/a$a=Block()$ ((HighLevelStructure/b|Block/b|Expression/b)$a.append(b)$)*  "}";

    Expression/a -> NoReturn/a ";";

    Return/a -> Compare/a;

    Compare/a -> BooleanOr/a;

    BooleanOr/a -> BooleanAnd/a (("or"|"\|\|") BooleanAnd/b $ a = Or(a, b)$)*;
    
    BooleanAnd/a -> Equals/a (("and"|"\&\&") Equals/b $ a = And(a, b)$)*;
    
    Equals/a -> Arrows/a ("==" Arrows/b $ a = Equal(a, b)$
    | "!=" Arrows/b $ a = NotEqual(a, b)$)*;

    Arrows/a -> Not/a ("<=" Not/b $ a = LessEqual(a, b)$
    | "<" Not/b $ a = Less(a, b)$
    |">=" Not/b $ a = LargerEqual(a, b)$
    | ">" Not/b $ a = Larger(a, b)$)*;
    
    Not/a -> BooleanLiteral/a
    | "NOT" BooleanLiteral/a $ a = Not(a)$;

    BooleanLiteral/a -> boolean/a
    | Number/a;
    
    Number/a -> Addsub/a;

    Addsub/a -> Muldiv/a("\+" Muldiv/b $ a = Add(a, b)$
    | "-" Muldiv/b $ a = Subtract(a, b)$)*;
    
    Muldiv/a -> Pow/a("\*" Pow/b $ a = Multiply(a, b)$
    | "/" Pow/b $ a = Divide(a, b) $
    | "//" Pow/b $ a = FloorDivide(a, b)$
    | "%" Pow/b $ a = Modulo(a, b)$)*;

    Pow/a -> Index/a ("\*\*" NumberFact/b $ a = Power(a, b)$)*;
    
    Index/a -> Fact/a ("\\[" Number/b "\\]" $ a = Index(a, b)$)*;
    
    Fact/a -> Literal/a
    | "\(" Return/a "\)";

    Literal/a -> real/a
    | int/a
    | string/a
    | variable/a
    | List/a;
    
    List/a -> "\\[" $a=ListLiteral()$ Return/b $a.append(b)$("," Return/b $a.append(b)$)* "\\]"
    | "\\[\\]"/a $a=ListLiteral()$;
    
    NoReturn/a -> "print" $a=Print()$ Return/b $a.line(b)$ 
    | Return/b "=" Return/c $a=Assign(b, c)$;
    """

# Make an instance of the parser. This acts like a function.
parse = Parser()
# This is the driver code, that reads in lines, deals with errors, and
# prints the output if no error occurs.

# Open the file containing the input.
try:
    f = open(sys.argv[1], "r")
except(IndexError, IOError):
    f = open("input1.txt", "r")

# Read the whole program into one line string.
line = f.read()
f.close()

# Try to initialize varible map
variables = Variables()
try:
    # Try to parse the expression.
    node = parse(line)

    # Try to get a result.
    result = node.evaluate()

    # Print the representation of the result.
    #print(repr(result))

# If an exception is thrown, print the appropriate error.
except tpg.Error:
    print("SYNTAX ERROR")
    # Uncomment the next line to re-raise the syntax error,
    # displaying where it occurs. Comment it for submission.
    # raise
        
except SemanticError:
    print("SEMANTIC ERROR")
    # Uncomment the next line to re-raise the semantic error,
    # displaying where it occurs. Comment it for submission.
    # raise
