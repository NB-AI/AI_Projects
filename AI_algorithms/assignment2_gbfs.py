"""
Assignment 02 - GBFS
"""


import math
from .. problem import Problem
from .. datastructures.priority_queue import PriorityQueue


# please ignore this
def get_solver_mapping():
    return dict(
        gbfs_ec=GBFS_Euclidean,
        gbfs_mh=GBFS_Manhattan
    )


class GBFS(object):
    # TODO, Exercise 2:
    # - implement Greedy Best First Search (GBFS)
    # - use the provided PriorityQueue where appropriate
    # - to put items into the PriorityQueue, use 'pq.put(<priority>, <item>)'
    # - to get items out of the PriorityQueue, use 'pq.get()'
    # - use a 'set()' to store nodes that were already visited
    def solve(self, problem: Problem):
        class_distance = GBFS_Manhattan() # GBFS_Euclidean() # Here choose one of these heuristics!
        pq = PriorityQueue()
        visitor_set = set()
        start_node = problem.get_start_node()
        pq.put(class_distance.heuristic(start_node, problem.get_end_node()), start_node) # here is the only difference to ucs. Use
        # heuristic estimated cost instead of cost for root to current node.
        visitor_set.add(start_node)
        if problem.is_end(start_node):
            return start_node
        first_node = pq.get()

        node_succ = problem.successors(first_node)

        found = False
        while found == False:
            for single_node in node_succ:  # always add all successors to pq when it is not current node itself
                if single_node.cost > 0 and single_node not in visitor_set:  # so the single_node is not the starting node; visitor set saves the nodes:
                    # important because identical nodes can differ in their costs and are therefore different here. Identical nodes with same costs
                    # aren't added to the priority queue
                    pq.put(class_distance.heuristic(single_node, problem.get_end_node()), single_node)
                    visitor_set.add(single_node)

            first_node = pq.get()
            if problem.is_end(first_node):

                return first_node
            else:
                node_succ = problem.successors(first_node)

# this is the GBFS variant with the euclidean distance as a heuristic
# it is registered as a solver with the name 'gbfs_ec'

# please note that in an ideal world, this heuristic should actually be part
# of the problem definition, as it assumes domain knowledge about the structure
# of the problem, and defines a distance to the goal state
class GBFS_Euclidean(GBFS):
    def heuristic(self, current, goal):
        cy, cx = current.state
        gy, gx = goal.state
        return math.sqrt((cy - gy) ** 2 + (cx - gx) ** 2)


# this is the GBFS variant with the manhattan distance as a heuristic
# it is registered as a solver with the name 'gbfs_mh'

# please note that in an ideal world, this heuristic should actually be part
# of the problem definition, as it assumes domain knowledge about the structure
# of the problem, and defines a distance to the goal state
class GBFS_Manhattan(GBFS):
    def heuristic(self, current, goal):
        cy, cx = current.state
        gy, gx = goal.state
        return math.fabs((cy - gy)) + math.fabs(cx - gx)
