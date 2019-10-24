from operator import lt, ne, eq, gt


class Constraint(object):
    """A Constraint consists of
    * scope: a tuple of variables
    * condition: a function that can applied to a tuple of values
    for the variables
    """
    def __init__(self, scope, condition):
        self.scope = scope
        self.condition = condition

    def __repr__(self):
        return self.condition.__name__ + str(self.scope)

    def holds(self, assignment):
        """returns the value of Constraint con evaluated in assignment.

        precondition: all variables are assigned in assignment
        """
        return self.condition(*tuple(assignment[v] for v in self.scope))


class CSP(object):
    """A CSP consists of
    * domains, a dictionary that maps each variable to its domain
    * constraints, a list of constraints
    * variables, a set of variables
    * var_to_const, a variable to set of constraints dictionary
    """
    def __init__(self, domains, constraints):
        """domains is a variable:domain dictionary
        constraints is a list of constriants
        """
        self.variables = set(domains)
        self.domains = domains
        self.constraints = constraints
        self.var_to_const = {var:set() for var in self.variables}
        for con in constraints:
            for var in con.scope:
                self.var_to_const[var].add(con)

    def __str__(self):
        """string representation of CSP"""
        return str(self.domains)

    def __repr__(self):
        """more detailed string representation of CSP"""
        return "CSP({}, {})".format(self.domains, [str(c) for c in self.constraints])

    def consistent(self, assignment):
        """assignment is a variable:value dictionary
        returns True if all of the constraints that can be evaluated
                        evaluate to True given assignment.
        """
        return all(con.holds(assignment)
                    for con in self.constraints
                    if all(v in  assignment  for v in con.scope))


def ne_(val):
    """not equal value"""
    # nev = lambda x: x != val   # alternative definition
    # nev = partial(neq,val)     # another alternative definition
    def nev(x):
        return val != x
    nev.__name__ = str(val)+"!="      # name of the function 
    return nev

def is_(val):
    """is a value"""
    # isv = lambda x: x == val   # alternative definition
    # isv = partial(eq,val)      # another alternative definition
    def isv(x):
        return val == x
    isv.__name__ = str(val)+"=="
    return isv

csp0 = CSP(
    {
        'X': {1, 2, 3}, 'Y': {1, 2, 3}, 'Z': {1, 2, 3}
    },
    [
        Constraint(('X', 'Y'), lt),
        Constraint(('Y', 'Z'), lt)
    ]
)

C0 = Constraint(('A', 'B'), lt)
C1 = Constraint(('B',), ne_(2))
C2 = Constraint(('B', 'C'), lt)
csp1 = CSP(
    {'A': {1, 2, 3, 4}, 'B': {1, 2, 3, 4}, 'C': {1, 2, 3, 4}},
    [C0, C1, C2]
)

csp2 = CSP(
    {'A': {1, 2, 3, 4}, 'B': {1, 2, 3, 4}, 'C': {1, 2, 3, 4}, 'D': {1, 2, 3, 4}, 'E': {1, 2, 3, 4}},
    [
        Constraint(('B',), ne_(3)),
        Constraint(('C',), ne_(2)),
        Constraint(('A', 'B'), ne),
        Constraint(('B', 'C'), ne),
        Constraint(('C', 'D'), lt),
        Constraint(('A', 'D'), eq),
        Constraint(('A', 'E'), gt),
        Constraint(('B', 'E'), gt),
        Constraint(('C', 'E'), gt),
        Constraint(('D', 'E'), gt),
        Constraint(('B', 'D'), ne)
    ]
)

csp3 = CSP(
    {'A': {1, 2, 3, 4}, 'B': {1, 2, 3, 4}, 'C': {1, 2, 3, 4}, 'D': {1, 2, 3, 4}, 'E': {1, 2, 3, 4}},
    [
        Constraint(('A','B'), ne),
        Constraint(('A','D'), lt),
        Constraint(('A','E'), lambda a, e: (a - e) % 2 == 1), # A-E is odd
        Constraint(('B','E'), lt),
        Constraint(('D','C'), lt),
        Constraint(('C','E'), ne),
        Constraint(('D','E'), ne)
    ]
)

def adjacent(x, y):
   """True when x and y are adjacent numbers"""
   return abs(x - y) == 1

csp4 = CSP(
    {'A': {1, 2, 3, 4, 5}, 'B': {1, 2, 3, 4, 5}, 'C': {1, 2, 3, 4, 5}, 'D': {1, 2, 3, 4, 5}, 'E': {1, 2, 3, 4, 5}},
    [
        Constraint(('A','B'), adjacent),
        Constraint(('B','C'), adjacent),
        Constraint(('C','D'), adjacent),
        Constraint(('D','E'), adjacent),
        Constraint(('A','C'), ne),
        Constraint(('B','D'), ne),
        Constraint(('C','E'), ne)
    ]
)

def meet_at(p1, p2):
    """returns a function that is true when the words meet at the postions p1, p2
    """
    def meets(w1, w2):
        return w1[p1] == w2[p2]
    meets.__name__ = "meet_at({}, {})".format(p1, p2)
    return meets

crossword1 = CSP(
    {
        'one_across': {'ant', 'big', 'bus', 'car', 'has'},
        'one_down': {'book', 'buys', 'hold', 'lane', 'year'},
        'two_down': {'ginger', 'search', 'symbol', 'syntax'},
        'three_across': {'book', 'buys', 'hold', 'land', 'year'},
        'four_across': {'ant', 'big', 'bus', 'car', 'has'}
    },
    [
        Constraint(('one_across', 'one_down'), meet_at(0, 0)),
        Constraint(('one_across', 'two_down'), meet_at(2, 0)),
        Constraint(('three_across', 'two_down'), meet_at(2, 2)),
        Constraint(('three_across', 'one_down'), meet_at(0, 2)),
        Constraint(('four_across', 'two_down'), meet_at(0, 4))
    ]
)

words = {
    'ant', 'big', 'bus', 'car', 'has','book', 'buys', 'hold',
    'lane', 'year', 'ginger', 'search', 'symbol', 'syntax'
}
           
def is_word(*letters, words=words):
    """is true if the letters concatenated form a word in words"""
    return "".join(letters) in words

letters = [
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
    "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"
]

crossword1d = CSP(
    {
        'p00': letters, 'p10': letters, 'p20': letters,                 # first row
        'p01': letters, 'p21': letters,                                 # second row
        'p02': letters, 'p12': letters, 'p22': letters, 'p32': letters, # third row
        'p03': letters, 'p23': letters,                                 # fourth row
        'p24': letters, 'p34': letters, 'p44': letters,                 # fifth row
        'p25': letters                                                  # sixth row
    },
    [
        Constraint(('p00', 'p10', 'p20'), is_word),                      # 1-across
        Constraint(('p00', 'p01', 'p02', 'p03'), is_word),               # 1-down
        Constraint(('p02', 'p12', 'p22', 'p32'), is_word),               # 3-across
        Constraint(('p20', 'p21', 'p22', 'p23', 'p24', 'p25'), is_word), # 2-down
        Constraint(('p24', 'p34', 'p44'), is_word)                       # 4-across
    ]
)
               
def test(CSP_solver, csp=csp1, solutions=[{'A': 1, 'B': 3, 'C': 4}, {'A': 2, 'B': 3, 'C': 4}]):
    """CSP_solver is a solver that takes a csp and returns a solution
    csp is a constraint satisfaction problem
    solutions is the list of all solutions to csp
    This tests whether the solution returned by CSP_solver is a solution.
    """
    print("Testing csp with", CSP_solver.__doc__)
    sol0 = CSP_solver(csp)
    print("Solution found:", sol0)
    assert sol0 in solutions, "Solution not correct for {}".format(csp)
    print("Passed unit test")
