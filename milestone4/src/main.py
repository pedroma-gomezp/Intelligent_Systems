#!/usr/bin/env python
# -*- coding: utf-8 -*-
"Usage: python {0} <node> <latMin> <longMin> <latMax> <longMax> <objetive_node1>...<objetive_nodeN>"

from State import State
from Node_Tree import Node_Tree
from Node_Map import Node_Map
from State_Space import State_Space
from Problem import Problem
from auxiliary_functions import Searching_Strategies
import sys
import heapq

if len(sys.argv) < 7:
    print(__doc__.format(__file__))
    sys.exit(0)

def search(problem, strategy, max_depth=10000, incr_depth=1):
        
    current_depth = incr_depth
    solution = None
       
    while not solution and current_depth <= max_depth:
        solution = bounded_search(problem, strategy, current_depth)
        current_depth = current_depth + incr_depth

    return solution


def bounded_search(problem, strategy, max_depth=10000):

    frontier = []
    initial_node = Node_Tree(problem.initial_state)
    heapq.heappush(frontier, initial_node)
    solution = False

    while not solution and len(frontier) <> 0:
        current_node = heapq.heappop(frontier)

        if problem.isGoal(current_node.state):
            solution = True

        else:
            successors_list = problem.state_space.getSuccessors(current_node.state, problem.hash_table)
            successor_nodes = create_nodes(successors_list, current_node, max_depth, strategy)

            for node in successor_nodes:
                heapq.heappush(frontier, node)
   
    if solution:
        create_solution(current_node)
        return True
    else:
        return None 
    


def create_nodes(successors_list, parent_node, max_depth, strategy): #en este metodo pasa la magia

    successor_nodes = []
        
    for succ in successors_list:

       state = succ[1]              
       cost = parent_node.cost + succ[2]
       street = succ[0]
       depth = parent_node.depth + 1
       parent = parent_node
       value = 0

       if strategy == Searching_Strategies.BFS:
           value = depth

       elif strategy == Searching_Strategies.DFS:
           value = -depth

       elif strategy == Searching_Strategies.DLS:
            value = -depth

       elif strategy == Searching_Strategies.IDS:
           value = -depth

       elif strategy == Searching_Strategies.UC:
           value = cost

       current_succesor = Node_Tree(state, cost, street, depth, parent, value)                 

       successor_nodes.append(current_succesor)

    return successor_nodes
        


def create_solution(final_node):
    """ This method will write the obtained path onto a file
    """

    current_node = final_node
    stack = [current_node]

    while current_node.parent is not None:
        stack.append(current_node.parent)
        current_node = current_node.parent

    output_file = 'output/path.gpx'
    print "Path generated on " + output_file
    with open(output_file, 'w+') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<gpx version="1.0">\n\t<name>Example gpx</name>\n\t\t<trk><name>Route</name><number>1</number><trkseg>\n')
        while (len(stack)>0):
            f.write(stack.pop().toGPX())
        f.write('\t</trkseg></trk>\n</gpx>')


if __name__ == "__main__":

    print "Looking for nodes " + str(sys.argv[6:])

    initial_state = State(Node_Map(sys.argv[1]), sys.argv[6:])

    boundary_coordinates = (sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])

    problem = Problem(State_Space(boundary_coordinates), initial_state)

    problem.build_hash_table()

    path = search(problem, Searching_Strategies.UC)

    sys.exit(0)
