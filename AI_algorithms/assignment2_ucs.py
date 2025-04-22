"""
Assignment 02 - UCS
"""


from .. problem import Problem
from .. datastructures.priority_queue import PriorityQueue


def get_solver_mapping():
    return dict(ucs=UCS)


class UCS(object):
    # TODO, excercise 2:
    # - implement Uniform Cost Search (UCS), a variant of Dijkstra's Graph Search
    # - use the provided PriorityQueue where appropriate
    # - to put items into the PriorityQueue, use 'pq.put(<priority>, <item>)'
    # - to get items out of the PriorityQueue, use 'pq.get()'
    # - store visited nodes in a 'set()'
    def solve(self, problem: Problem):
        pq = PriorityQueue()
        visitor_set = set()
        start_node = problem.get_start_node()
        pq.put(start_node.cost, start_node)
        visitor_set.add(start_node)
        if problem.is_end(start_node):
            return start_node
        first_node = pq.get()

        node_succ = problem.successors(first_node)


        found = False
        while found == False:
            for single_node in node_succ:  # always add all successors to pq when it is not current node itself
                if single_node.cost > 0 and single_node not in visitor_set: # so the single_node is not the starting node; visitor set saves the nodes:
                    # important because identical nodes can differ in their costs and are therefore different here. Identical nodes with same costs
                    # aren't added to the priority queue
                    pq.put(single_node.cost, single_node)
                    visitor_set.add(single_node)

            first_node = pq.get()
            if problem.is_end(first_node):

                return first_node
            else:
                node_succ = problem.successors(first_node)


        

