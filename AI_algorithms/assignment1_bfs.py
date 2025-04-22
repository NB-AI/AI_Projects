"""
Assignment 01 - BFS
"""


from .. problem import Problem
from .. datastructures.queue import Queue


# please ignore this
def get_solver_mapping():
    return dict(bfs=BFS)


class BFS(object):
    # TODO, exercise 1:
    # - implement Breadth First Search (BFS)
    # - use 'problem.get_start_node()' to get the node with the start state
    # - use 'problem.is_end(node)' to check whether 'node' is the node with the end state
    # - use a set() to store already visited nodes
    # - use the 'queue' datastructure that is already imported as the 'fringe'/ the 'frontier'
    # - use 'problem.successors(node)' to get a list of nodes containing successor states
    def solve(self, problem: Problem): # I called the successors also children (like in a tree) out of habit



        start_node = problem.get_start_node()
        call_queue_class = Queue()
        already_visited = []

        if start_node.parent != None:
            parent_unimportant = start_node.parent

            list_children = problem.successors(parent_unimportant) # get all children of the parent of the starting node into a list
            start_node_done = False
            for ele in list_children: # the result of the loop shall be a queuce which is up to date for the start node
                if ele == start_node and ele.state not in already_visited:
                    call_queue_class.put(ele)
                    already_visited.append(ele.state)
                    start_node_done = True
                if start_node_done == True and ele.state not in already_visited: # append the queue of one full rest level after the starting node
                    call_queue_class.put(ele)
                    already_visited.append(ele.state)
                # also append the queue by the chidlren of siblings which are left from the start node:
                if start_node_done == False and len(problem.successors(ele))>0 and ele.state not in already_visited: # then append the queue by the next_level nodes of the left start node's siblings
                    for child_of_left_sibling in problem.successors(ele):
                        if child_of_left_sibling.state not in already_visited:
                            call_queue_class.put(child_of_left_sibling)
                            already_visited.append(child_of_left_sibling.state)

        else: # starting node has no parent --> then it also has no sibilings --> queue only consists of the starting node at first
            call_queue_class.put(start_node)
            already_visited.append(start_node.state)



        # now we have generated a current queue. Now it is time to look at the single nodes in the queue:
        # you have always to look at the first element of the queue. Is it the searched one? Also delete the first element and
        # append the queue by the children of the node.
        # Queue will be empty when there is no child (last level) for any node anymore.

        while call_queue_class.has_elements() == True: # process of searching at most finished when no element in queue anymore
            first_node_in_queue = call_queue_class.get() # get and delete the first node in the queue
            if problem.is_end(first_node_in_queue) == True:
                return first_node_in_queue
            elif len(problem.successors(first_node_in_queue))>0:
                list_children_first_node = problem.successors(first_node_in_queue) # get list of children of the first node in queue
                for single_child in list_children_first_node:
                    # each node shall be visited only once. when node was in queue it shall not appear anymore!:
                    if single_child.state not in already_visited:
                        call_queue_class.put(single_child) # append the queue by the children of the node which is deleted from the queue
                        already_visited.append(single_child.state)
        return False # False is returned when the searched node was not found in the tree


    """
     visited = []
            current = problem.get_start_node()
            fringe = []
    
            while not problem.is_end(current) == True:
                visited.append(current.state)
    
                for child in problem.successors(current):
                    if child.state not in visited:
                        fringe.append(child)
                        visited.append(child.state)
                print(len(fringe))
                current = fringe.pop(0)
    
                print(current.state, len(fringe))
    
            return current
    """
