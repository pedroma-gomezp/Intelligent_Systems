from Node_Map import Node_Map

class State:
    '''Class repressenting a state of our problem'''

    def __init__(self, node_map, objetive_nodes=None):

        if not isinstance(node_map, Node_Map): 
            raise TypeError
        
        if objetive_nodes is None:
            self.objetive_nodes = []

        self.node_map=node_map
        self.objetive_nodes = objetive_nodes

    def __repr__(self):
        return self.node

