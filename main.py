# HW3
#Due Date: 03/13/2021, 11:59PM

"""                                   
### Collaboration Statement:
             
"""

class Node:
    def __init__(self, value):
        self.value = value  
        self.next = None 
    
    def __str__(self):
        return "Node({})".format(self.value) 

    __repr__ = __str__
                          
#=============================================== Part I ==============================================
class Stack:
    '''
        >>> x=Stack()
        >>> x.pop()
        >>> x.push(2)
        >>> x.push(4)
        >>> x.push(6)
        >>> x
        Top:Node(6)
        Stack:
        6
        4
        2
        >>> x.pop()
        6
        >>> x
        Top:Node(4)
        Stack:
        4
        2
        >>> len(x)
        2
        >>> x.peek()
        4
    '''
    def __init__(self):
        self.top = None
    
    def __str__(self):
        temp=self.top
        out=[]
        while temp:
            out.append(str(temp.value))
            temp=temp.next
        out='\n'.join(out)
        return ('Top:{}\nStack:\n{}'.format(self.top,out))
    __repr__=__str__

    def isEmpty(self):
        if self.top == None:
          return True

    def __len__(self): 
        if self.isEmpty():
          return 0
        else:
          counter = 1
          current = self.top
          while current.next != None:
            counter += 1
            current = current.next
          return counter

    def push(self,value):
        nn = Node(value)
        nn.next = self.top
        self.top = nn
  
    def pop(self):
        if self.isEmpty():
          return None
        else:
          returnedValue = self.top.value
          self.top = self.top.next
          return returnedValue

    def peek(self):
      if self.isEmpty():
        return None
      else:
        return self.top.value

class Calculator:
    def __init__(self):
        self.__expr = None

    @property
    def getExpr(self):
        return self.__expr

    def setExpr(self, new_expr):
        if isinstance(new_expr, str):
            self.__expr=new_expr
        else:
            print('setExpr error: Invalid expression')
            return None

    def _isNumber(self, txt):
        '''
            >>> x=Calculator()
            >>> x._isNumber(' 2.560 ')
            True
            >>> x._isNumber('7 56')
            False
            >>> x._isNumber('2.56p')
            False
        '''
        try:
          float(txt)
        except:
          return False
        return True

    def goodParenthesis(self,txt):
      """
      This method isolates the parenthesis in a list and pushes them into a stack 
      where from there if its an open parenthesis we push it into the stack and if
      its a close parenthesis we pop out of the stack if the stack ends empty they 
      are good parenthesis if it is not empty there is an error with the parenthesis
      """
      s1 = Stack()
      parenthesis = [i for i in txt.split(' ') if i ==')' or i =="("]
      for paren in parenthesis:
        if paren == "(":
          s1.push(paren)
        elif paren == ')':
          value = s1.pop()
          if value == None:
            return False
      if s1.isEmpty():
        return True
      else:
        return False

    def goodEquation(self,txt):
      """
      This is my error checking function and it isolates all of the terms and operators
      from there we check if its a single numerical value, if it is we return True if not false
      from then on out we have to make sure the first and last values in a list are numerical
      values and they alternate with a valid operator in between and we do this using a stack.
      We go through and check for alternating until we hit the next element being None and then we
      check to make sure its a numerical value
      """
      txtList = txt.split(' ')
      txtList = [i for i in txtList if i != "("  and i != ")" and i != ""]
      s1 = Stack()
      if not self.goodParenthesis(txt):
        return False
      for value in txtList:
        s1.push(value)
      if not self._isNumber(s1.peek()):
        return False
      while s1.top.next != None:
        current = s1.peek()
        if not self._isNumber(current) and current not in "+-/^*":
          return False
        elif self._isNumber(current) and self._isNumber(s1.top.next.value):
          return False
        elif current in "+-/^*" and s1.top.next.value in "+-/^*":
          return False
        else:
          s1.pop()
      if self._isNumber(s1.peek()):
        return True
      else:
        return False

    def getPrecidence(self,value):
      """
      I decided to use a function to hold the precidence and this is the function that I call.
      """
      if value == None or value == '(':
        return 0
      elif value == '+' or value == '-':
        return 2
      elif value == '*' or value == '/':
        return 3
      elif value == '^':
        return 4

    def _getPostfix(self, txt):
        '''
            Required: _getPostfix must create and use a Stack for expression processing
            >>> x=Calculator()
            >>> x._getPostfix('2 ^ 4')
            '2.0 4.0 ^'
            >>> x._getPostfix('2')
            '2.0'
            >>> x._getPostfix('2.1 * 5 + 3 ^ 2 + 1 + 4.45')
            '2.1 5.0 * 3.0 2.0 ^ + 1.0 + 4.45 +'
            >>> x._getPostfix('2 * 5.34 + 3 ^ 2 + 1 + 4')
            '2.0 5.34 * 3.0 2.0 ^ + 1.0 + 4.0 +'
            >>> x._getPostfix('2.1 * 5 + 3 ^ 2 + 1 + 4')
            '2.1 5.0 * 3.0 2.0 ^ + 1.0 + 4.0 +'
            >>> x._getPostfix('( 2.5 )')
            '2.5'
            >>> x._getPostfix ('( ( 2 ) )')
            '2.0'
            >>> x._getPostfix ('2 * ( ( 5 + -3 ) ^ 2 + ( 1 + 4 ) )')
            '2.0 5.0 -3.0 + 2.0 ^ 1.0 4.0 + + *'
            >>> x._getPostfix ('( 2 * ( ( 5 + 3 ) ^ 2 + ( 1 + 4 ) ) )')
            '2.0 5.0 3.0 + 2.0 ^ 1.0 4.0 + + *'
            >>> x._getPostfix ('( ( 2 * ( ( 5 + 3 ) ^ 2 + ( 1 + 4 ) ) ) )')
            '2.0 5.0 3.0 + 2.0 ^ 1.0 4.0 + + *'
            >>> x._getPostfix('2 * ( -5 + 3 ) ^ 2 + ( 1 + 4 )')
            '2.0 -5.0 3.0 + 2.0 ^ * 1.0 4.0 + +'

            # In invalid expressions, you might print an error message, but code must return None, adjust doctest accordingly
            # If you are veryfing the expression in calculate before passing to postfix, this cases are not necessary
            >>> x._getPostfix('2 * 5 + 3 ^ + -2 + 1 + 4')
            >>> x._getPostfix('2 * 5 + 3 ^ - 2 + 1 + 4')
            >>> x._getPostfix('2    5')
            >>> x._getPostfix('25 +')
            >>> x._getPostfix(' 2 * ( 5 + 3 ) ^ 2 + ( 1 + 4 ')
            >>> x._getPostfix(' 2 * ( 5 + 3 ) ^ 2 + ) 1 + 4 (')
            >>> x._getPostfix('2 * 5% + 3 ^ + -2 + 1 + 4')
        '''
        # YOUR CODE STARTS HERE
        """
        For this function first we split the string at spaces getting rid of any
        unnecesary spaces. then we check to make sure its a good equation using the 
        method self.goodEquation that we defined above. From there we go through every
        character and check if its a number and if it is, it is added to the postfix list
        if not we go through and check the precedence of the operator with ( and ^ always
        being pushed in. if its a ) we keep popping until we hit the subsequent (. Finally
        if it is any other arithimtic opererator we check its precidence if it has a higher precidence
        we push it into the stack, if it does not we pop until it is greater than the current stack 
        top.
        """
        postfixStack = Stack()  # method must use postfixStack to compute the postfix expression
        listedValues = [i for i in txt.split(' ') if i != '']
        postfix = []
        if not self.goodEquation(txt):
          return None
        for character in listedValues:
          if self._isNumber(character):
            postfix.append(str(float(character)))
          else:
            if postfixStack.isEmpty() or character == '(' or character == "^":
              postfixStack.push(character)
            elif character == ')':
              while postfixStack.top.value != '(':
                postfix.append(postfixStack.pop())
              postfixStack.pop()
            elif self.getPrecidence(character) > self.getPrecidence(postfixStack.top.value):
              postfixStack.push(character)
            elif self.getPrecidence(character) <= self.getPrecidence(postfixStack.top.value):
              while self.getPrecidence(postfixStack.peek()) >= self.getPrecidence(character):
                postfix.append(postfixStack.pop())
              postfixStack.push(character)
        while postfixStack.top:
          postfix.append(postfixStack.pop())
        return " ".join(postfix)
        
    @property
    def calculate(self):
        '''
            Required: calculate must call postfix
                      calculate must create and use a Stack to compute the final result as shown in the video lecture
            >>> x=Calculator()
            >>> x.setExpr('4 + 3 - 2')
            >>> x.calculate
            5.0
            >>> x.setExpr('-2 + 3.5')
            >>> x.calculate
            1.5
            >>> x.setExpr('4 + 3.65 - 2 / 2')
            >>> x.calculate
            6.65
            >>> x.setExpr('23 / 12 - 223 + 5.25 * 4 * 3423')
            >>> x.calculate
            71661.91666666667
            >>> x.setExpr(' 2 - 3 * 4')
            >>> x.calculate
            -10.0
            >>> x.setExpr('7 ^ 2 ^ 3')
            >>> x.calculate
            5764801.0
            >>> x.setExpr(' 3 * ( ( ( 10 - 2 * 3 ) ) )')
            >>> x.calculate
            12.0
            >>> x.setExpr('8 / 4 * ( 3 - 2.45 * ( 4 - 2 ^ 3 ) ) + 3')
            >>> x.calculate
            28.6
            >>> x.setExpr('2 * ( 4 + 2 * ( 5 - 3 ^ 2 ) + 1 ) + 4')
            >>> x.calculate
            -2.0
            >>> x.setExpr(' 2.5 + 3 * ( 2 + ( 3.0 ) * ( 5 ^ 2 - 2 * 3 ^ ( 2 ) ) * ( 4 ) ) * ( 2 / 8 + 2 * ( 3 - 1 / 3 ) ) - 2 / 3 ^ 2')
            >>> x.calculate
            1442.7777777777778
            >>> x.setExpr(" 4 + + 3 + 2") 
            >>> x.calculate
            >>> x.setExpr("4  3 + 2")
            >>> x.calculate
            >>> x.setExpr('( 2 ) * 10 - 3 * ( 2 - 3 * 2 ) )')
            >>> x.calculate
            >>> x.setExpr('( 2 ) * 10 - 3 * / ( 2 - 3 * 2 )')
            >>> x.calculate
            >>> x.setExpr(' ) 2 ( * 10 - 3 * ( 2 - 3 * 2 ) ')
            >>> x.calculate

            # For extra credit only. If not attemped, these cases must return None
            >>> x.setExpr('( 3.5 ) ( 15 )') 
            >>> x.calculate
            >>> x.setExpr('3 ( 5 ) - 15 + 85 ( 12 )') 
            >>> x.calculate
            >>> x.setExpr("( -2 / 6 ) + ( 5 ( ( 9.4 ) ) )") 
            >>> x.calculate
        '''
        """
        if its not a good equation we return None or else we make a stack, and we push
        numeric values into the stack and then when we hit an operator we pop two values from 
        the stack and person the operation on them subsequently pushing the calculated value
        back into the stack until the end where we pop from the stack the final value.
        """
        if not isinstance(self.__expr,str) or len(self.__expr)<=0:
            print("Argument error in calculate")
            return None
        if not self.goodEquation(self.__expr.strip(' ')):
          return None
        calcStack = Stack()   # method must use calcStack to compute the  expression
        postfix = self._getPostfix(self.__expr).split(' ')
        for char in postfix:
          if self._isNumber(char):
            calcStack.push(char)
          elif char in '+-/^*':
            firstTerm = float(calcStack.pop())
            secondTerm = float(calcStack.pop())
            if char == '+':
              calcStack.push(firstTerm + secondTerm)
            elif char == '-':
              calcStack.push(secondTerm-firstTerm)
            elif char == "*":
              calcStack.push(firstTerm*secondTerm)
            elif char == "/":
              calcStack.push(secondTerm/firstTerm)
            elif char == "^":
              calcStack.push(secondTerm**firstTerm)
        return calcStack.pop()
class AdvancedCalculator:
    '''
        >>> C = AdvancedCalculator()
        >>> C.states == {}
        True
        >>> C.setExpression('a = 5;b = 7 + a;a = 7;c = a + b;c = a * 0;return c')
        >>> C.calculateExpressions() == {'a = 5': {'a': 5.0}, 'b = 7 + a': {'a': 5.0, 'b': 12.0}, 'a = 7': {'a': 7.0, 'b': 12.0}, 'c = a + b': {'a': 7.0, 'b': 12.0, 'c': 19.0}, 'c = a * 0': {'a': 7.0, 'b': 12.0, 'c': 0.0}, '_return_': 0.0}
        True
        >>> C.states == {'a': 7.0, 'b': 12.0, 'c': 0.0}
        True
        >>> C.setExpression('x1 = 5;x2 = 7 * ( x1 - 1 );x1 = x2 - x1;return x2 + x1 ^ 3')
        >>> C.states == {}
        True
        >>> C.calculateExpressions() == {'x1 = 5': {'x1': 5.0}, 'x2 = 7 * ( x1 - 1 )': {'x1': 5.0, 'x2': 28.0}, 'x1 = x2 - x1': {'x1': 23.0, 'x2': 28.0}, '_return_': 12195.0}
        True
        >>> print(C.calculateExpressions())
        {'x1 = 5': {'x1': 5.0}, 'x2 = 7 * ( x1 - 1 )': {'x1': 5.0, 'x2': 28.0}, 'x1 = x2 - x1': {'x1': 23.0, 'x2': 28.0}, '_return_': 12195.0}
        >>> C.states == {'x1': 23.0, 'x2': 28.0}
        True
        >>> C.setExpression('x1 = 5 * 5 + 97;x2 = 7 * ( x1 / 2 );x1 = x2 * 7 / x1;return x1 * ( x2 - 5 )')
        >>> C.calculateExpressions() == {'x1 = 5 * 5 + 97': {'x1': 122.0}, 'x2 = 7 * ( x1 / 2 )': {'x1': 122.0, 'x2': 427.0}, 'x1 = x2 * 7 / x1': {'x1': 24.5, 'x2': 427.0}, '_return_': 10339.0}
        True
        >>> C.states == {'x1': 24.5, 'x2': 427.0}
        True
        >>> C.setExpression('A = 1;B = A + 9;C = A + B;A = 20;D = A + B + C;return D - A')
        >>> C.calculateExpressions() == {'A = 1': {'A': 1.0}, 'B = A + 9': {'A': 1.0, 'B': 10.0}, 'C = A + B': {'A': 1.0, 'B': 10.0, 'C': 11.0}, 'A = 20': {'A': 20.0, 'B': 10.0, 'C': 11.0}, 'D = A + B + C': {'A': 20.0, 'B': 10.0, 'C': 11.0, 'D': 41.0}, '_return_': 21.0}
        True
        >>> C.states == {'A': 20.0, 'B': 10.0, 'C': 11.0, 'D': 41.0}
        True
        >>> C.setExpression('A = 1;B = A + 9;2C = A + B;A = 20;D = A + B + C;return D + A')
        >>> C.calculateExpressions() is None
        True
        >>> C.states == {}
        True
    '''
    def __init__(self):
        self.expressions = ''
        self.states = {}

    def setExpression(self, expression):
        self.expressions = expression
        self.states = {}

    def _isVariable(self, word):
        '''
            >>> C = AdvancedCalculator()
            >>> C._isVariable('volume')
            True
            >>> C._isVariable('4volume')
            False
            >>> C._isVariable('volume2')
            True
            >>> C._isVariable('vol%2')
            False
        '''
        """
        simple function checks to make sure the first letter is a letter
        and subsequent characters are alphanumeric
        """
        if isinstance(word,str) and word[0].isalpha():
          for letter in word:
            if letter.isalnum():
              continue
            else:
              return False
          return True
        else:
          return False
    def isNumber(self,value):
      try:
        float(value)
        return True
      except:
        return False

    def _replaceVariables(self, expr):
        '''
            >>> C = AdvancedCalculator()
            >>> C.states = {'x1': 23.0, 'x2': 28.0}
            >>> C._replaceVariables('1')
            '1'
            >>> C._replaceVariables('105 + x')
            >>> C._replaceVariables('7 * ( x1 - 1 )')
            '7 * ( 23.0 - 1 )'
            >>> C._replaceVariables('x2 - x1')
            '28.0 - 23.0'
        '''
        """
        This function uses recursion to replace all the variables.
        Fist we make a list spliting at spaces. The first if statement
        is checking if the list is empty as it should be and if its not it
        returns false because this is making sure there are no undefined variables. The elif statement
        is the base case which will return the final string because there are no more var in the expr
        that are in the states. Then finally the else statement will keep being hit replacing the current
        variables by adding them to a new cleaned list. I implemented this in this manor so when 
        we have variables inside of variables we always break them down to the point where it is 
        just numerical values.
        """
        expr = expr.split(' ')
        if [x for x in expr if not self.isNumber(x) and self._isVariable(x) and x not in self.states]:
          return None
        elif not [var for var in expr if var in self.states]:
          return " ".join(expr)
        else:
          cleaned =[]
          for var in expr:
            if var in self.states:
              cleaned.append(str(self.states[var]))
            else:
              cleaned.append(str(var))
          return self._replaceVariables(" ".join(cleaned))

    def calculateExpressions(self):
        """
        This function splits the components of the equation at semi colons and then
        breaks those up into the variables and the return statement. Fot the variables we go through
        and if it is a valid variable we set the calcObj exp to the replaces version and then we calculate
        the value and copy the states into the returned dictionary. If the any of the variables are not right we 
        rreturn None. Finally we calculate the returned value using the calcObj we add it to the returned
        dict and return it
        """
        self.states = {}
        returned_dict = {}
        calcObj = Calculator()
        components = self.expressions.split(';')
        variables = components[:-1]
        return_statement = components[-1][7:]
        for variable in variables:
          variableComponents = variable.split(' = ')
          if self._isVariable(variableComponents[0]) != False:
            calcObj.setExpr(self._replaceVariables(variableComponents[1]))
            self.states[variableComponents[0]] = float(calcObj.calculate)
            returned_dict[variable] = self.states.copy()
          else:
            self.states = {}
            return None
        noVariableForm = self._replaceVariables(return_statement)
        calcObj.setExpr(noVariableForm)
        returned_dict['_return_'] = float(calcObj.calculate)
        return returned_dict