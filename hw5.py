import sys
import tpg

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
    """
    A node representing integer literals.
    """

    def __init__(self, value):
        print("Integer construction: ", value)
        self.value = int(value)

    def evaluate(self):
        return self.value

class RealLiteral(Node):
    """
    A node representing real literals.
    """

    def __init__(self, value):
        print("Real construction: ", value)
        self.value = float(value)

    def evaluate(self):
        return self.value

class BooleanLiteral(Node):
    """
    A node representing boolean literals.
    """

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
    """
    A node representing string literals.
    """

    def __init__(self, value):
        print("String construction:", value);
        temp = str(value)
        self.value = temp[1:len(temp)-1]

    def evaluate(self):
        return self.value

class And(Node):
    """
    A node representing and.
    """

    def __init__(self, left, right):
        print("Operation and ", left.evaluate(), right.evaluate());
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if not isinstance(left, int) or not isinstance(right, int):
            raise SemanticError()
        if left and right:
            return 1
        return 0

class Or(Node):
    """
    A node representing or.
    """

    def __init__(self, left, right):
        print("Operation or ", left.evaluate(), right.evaluate());
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if not isinstance(left, int) or not isinstance(right, int):
            raise SemanticError()
        if left or right:
            return 1
        return 0

class Not(Node):
    """
    A node representing not.
    """

    def __init__(self, left):
        print("Operation not ", left.evaluate());
        self.left = left

    def evaluate(self):
        left = self.left.evaluate()
        if not isinstance(left, int):
            raise SemanticError()
        if left:
            return 0
        return 1

class Add(Node):
    """
    A node representing addition.
    """

    def __init__(self, left, right):
        print("Operation add: ", left.evaluate(), " + ", right.evaluate())
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if isinstance(left, int):
            if not isinstance(right, int):
                raise SemanticError()
        elif isinstance(left, float):
            if not isinstance(right, float):
                raise SemanticError()
        else:
            raise SemanticError()
        return left + right

class Subtract(Node):
    """
    A node representing subtraction.
    """

    def __init__(self, left, right):
        print("Operation subtract ", left.evaluate(), right.evaluate());
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if isinstance(left, int):
            if not isinstance(right, int):
                raise SemanticError()
        elif isinstance(left, float):
            if not isinstance(right, float):
                raise SemanticError()
        else:
            raise SemantcError()
        return left - right

class Multiply(Node):
    """
    A node representing multiplication.
    """

    def __init__(self, left, right):
        print("Operation multiply ", left.evaluate(), right.evaluate());
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if isinstance(left, int):
            if not isinstance(right, int):
                raise SemanticError()
        elif isinstance(left, float):
            if not isinstance(right, float):
                raise SemanticError()
        else:
            raise SemanticError()
        return left * right

class Divide(Node):
    """
    A node representing division.
    """

    def __init__(self, left, right):
        print("Operation divide ", left.evaluate(), right.evaluate());
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if isinstance(left, int):
            if not isinstance(right, int) or right is 0:
                raise SemanticError()
        elif isinstance(left, float):
            if not isinstance(right, float) or right is 0.0:
                raise SemanticError()
        else:
            raise SemanticError()
        return left / right

class FloorDivide(Node):
    """
    A node representing floor divide.
    """

    def __init__(self ,left, right):
        print("Operation floor divide ", left.evaluate(), right.evaluate())
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if isinstance(left, int):
            if not isinstance(right, int) or right is 0:
                raise SemanticError()
        elif isinstance(left, float):
            if not isinstance(right, float) or right is 0.0:
                raise SemanticError()
        else:
            raise SemanticError()
        return left // right

class Power(Node):
    """
    A node representing power.
    """

    def __init__(self, left, right):
        print("Operation power ", left.evaluate(), right.evaluate())
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if not isinstance(left, int) or not isinstance(left, float):
            raise SemanticError()
        if not isinstance(right, int) or not isinstance(right, float):
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
    separator space "\s+";
    
    START/a -> Expression/a;

    Expression/a -> Compare/a;

    Compare/a -> Equals/a;

    Equals/a -> Arrows/a ("==" Arrows/b $ a = Equal(a, b)$
    | "!=" Arrows/b $ a = NotEqual(a, b)$)*;

    Arrows/a -> CompareFact/a ("<" CompareFact/b $ a = Less(a, b)$
    | "<=" CompareFact/b $ a = LessEqual(a, b)$
    | ">" CompareFact/b $ a = Larger(a, b)$
    | ">=" CompareFact/b $ a = LargerEqual(a, b)$)*;

    CompareFact/a -> CompareLiteral/a | "\(" Compare/a "\)";

    CompareLiteral/a -> Boolean/a | string/a;

    Boolean/a -> BooleanAnd/a;
    
    BooleanAnd/a -> BooleanOr/a ("AND" BooleanOr/b $ a = And(a, b)$)*;
    
    BooleanOr/a -> BooleanNot/a ("OR" BooleanNot/b $ a = Or(a, b)$)*;
    
    BooleanNot/a -> BooleanFact/a | "NOT" BooleanFact/a $ a = Not(a)$;

    BooleanFact/a -> BooleanLiteral/a | "\(" Boolean/a "\)";

    BooleanLiteral/a -> boolean/a | Number/a;
    
    Number/a -> Addsub/a;

    Addsub/a -> Muldiv/a("\+" Muldiv/b $ a = Add(a, b)$
    | "-" Muldiv/b $ a = Subtract(a, b)$)*;
    
    Muldiv/a -> Pow/a("\*" Pow/b $ a = Multiply(a, b)$
    | "/" Pow/b $ a = Divide(a, b) $
    | "//" Pow/b $ a = FloorDivide(a, b)$)*;

    Pow/a -> NumberFact/a ("\*\*" NumberFact/b $ a = Power(a, b)$)*;
    
    NumberFact/a -> NumLiteral/a | "\(" Number/a "\)"; 

    NumLiteral/a -> int/a | real/a;
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

# For each line in f
for l in f:
    try:
        # Try to parse the expression.
        node = parse(l)

        # Try to get a result.
        result = node.evaluate()

        # Print the representation of the result.
        print(repr(result))

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

f.close()
