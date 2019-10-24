def yes(ans):
    """returns true if the answer is yes in some form"""
    return ans.lower() in ['yes', 'yes.', 'oui', 'oui.', 'y', 'y.']    # bilingual


class Clause(object):
    """A definite clause"""

    def __init__(self, head, body=[]):
        """clause with atom head and lost of atoms body"""
        self.head = head
        self.body = body

    def __str__(self):
        """returns the string representation of a clause.
        """
        if self.body:
            return self.head + " <- " + " & ".join(self.body) + "."
        else:
            return self.head + "."

        
class Askable(object):
    """An askable atom"""

    def __init__(self, atom):
        """clause with atom head and lost of atoms body"""
        self.atom = atom

    def __str__(self):
        """returns the string representation of a clause."""
        return "askable " + self.atom + "."


from lib.display import Displayable


class KB(Displayable):
    """A knowledge base consists of a set of clauses.
    This also creates a dictionary to give fast access to the clauses with an atom in head.
    """
    def __init__(self, statements=[]):
        self.statements = statements
        self.clauses = [c for c in statements if isinstance(c, Clause)]
        self.askables = [c.atom for c in statements if isinstance(c, Askable)]
        self.atom_to_clauses = {}  # dictionary giving clauses with atom as head
        for c in self.clauses:
            if c.head in self.atom_to_clauses:
                self.atom_to_clauses[c.head].add(c)
            else:
                self.atom_to_clauses[c.head] = {c}

    def clauses_for_atom(self, a):
        """returns set of clauses with atom a as the head"""
        if a in self.atom_to_clauses:
            return self.atom_to_clauses[a]
        else:
            return set()

    def __str__(self):
        """returns a string representation of this knowledge base.
        """
        return '\n'.join([str(c) for c in self.statements])


triv_KB = KB([
    Clause('i_am', ['i_think']),
    Clause('i_think'),
    Clause('i_smell', ['i_exist'])
])
