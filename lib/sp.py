class Search_problem(object):
    """A search problem consists of:
    * a start node
    * a neighbors function that gives the neighbors of a node
    * a specification of a goal
    * a (optional) heuristic function.
    The methods must be overridden to define a search problem."""

    def start_node(self):
        """returns start node"""
        raise NotImplementedError("start_node")   # abstract method
    
    def is_goal(self,node):
        """is True if node is a goal"""
        raise NotImplementedError("is_goal")   # abstract method

    def neighbors(self,node):
        """returns a list of the arcs for the neighbors of node"""
        raise NotImplementedError("neighbors")   # abstract method

    def heuristic(self,n):
        """Gives the heuristic value of node n.
        Returns 0 if not overridden."""
        return 0

class Arc(object):
    """An arc has a from_node and a to_node node and a (non-negative) cost"""
    def __init__(self, from_node, to_node, cost=1, action=None):
        assert cost >= 0, "Cost cannot be negative for {} -> {}, cost: {}".format(from_node, to_node, cost)
        self.from_node = from_node
        self.to_node = to_node
        self.action = action
        self.cost = cost

    def __repr__(self):
        """string representation of an arc"""
        if self.action:
            return '{} --{}--> {}'.format(self.from_node, self.action, self.to_node)
        else:
            return '{} --> {}'.format(self.from_node, self.to_node)

