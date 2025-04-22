"""
Assignment 02 - IDS
"""


from .. problem import Problem
from .. datastructures.stack import Stack


# please ignore this
def get_solver_mapping():
    return dict(ids=IDS)

class DLDFS(object):
    def __init__(self, max_depth):
        self.max_depth = max_depth

    # TODO, Exercise 1: implement Depth-Limited Depth First Search (DLDFS)
    # - you can:
    #     - either use the 'Stack()' datastructure for a frontier
    #     - or implement DFS recursively
    #     - if you implement DFS recursively, you use the call stack
    #       as a datastructure for an implicit frontier
    # - DO NOT USE A 'VISITED' SET!

    def solve(self, problem: Problem):

        start_node = problem.get_start_node()
        my_stack = Stack()
        my_list = []

        if problem.is_end(start_node):
            return start_node

        else:
            my_list.append(start_node)
            my_stack.put(start_node.state)

        while len(my_list) > 0:
            first_node = my_list[0]
            my_list = my_list[1:]

            if problem.is_end(first_node) == True:
                return first_node
            elif len(problem.successors(first_node))>0:
                list_children_first_node = problem.successors(first_node)
                for single_child in list_children_first_node:
                    counter = 0
                    for i in my_stack:
                        if i == single_child.state:
                            counter += 1
                    if counter == 0 and single_child.depth <= self.max_depth:
                        my_list.append(single_child)
                        my_stack.put(single_child.state)
        return False # Nothing found on at most the maximal given depth




class IDS(object):

    # TODO, Exercise 1: implement Iterative Deepening Search (IDS)
    # - use the DLDFS implementation from above
    # - start the iterated search at depth == 0
    # - DO NOT USE A 'VISITED' SET
    def solve(self, problem: Problem):
        depth_found = False
        extended_depth = 0
        start_node = problem.get_start_node()

        while depth_found == False:
            call_dldfs = DLDFS(extended_depth)
            last_node = call_dldfs.solve(problem)

            if last_node is False:
                extended_depth += 1

            elif not problem.is_end(last_node):
                extended_depth += 1

            elif problem.is_end(last_node):
                depth_found = True
                return last_node

        return last_node
