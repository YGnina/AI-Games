from __future__ import absolute_import, division, print_function
import copy, random
from game import Game

from math import inf

MOVES = {0: 'up', 1: 'left', 2: 'down', 3: 'right'}
MAX_PLAYER, CHANCE_PLAYER = 0, 1 
# reach 512 tiles and a score over 5000

# Tree node. To be used to construct a game tree. 
class Node: 
    # Recommended: do not modify this __init__ function
    def __init__(self, state, player_type):
        #self.state = (state[0], state[1])
        self.state = (copy.deepcopy(state[0]), state[1])

        # to store a list of (direction, node) tuples
        self.children = []

        self.player_type = player_type

    # returns whether this is a terminal state (i.e., no children)
    def is_terminal(self):
        #TODO: complete this
        #pass
        return len(self.children) == 0
    

# AI agent. Determine the next move.
class AI:
    # Recommended: do not modify this __init__ function
    def __init__(self, root_state, search_depth=3): 
        self.root = Node(root_state, MAX_PLAYER)
        self.search_depth = search_depth
        self.simulator = Game(*root_state)

    # (Hint) Useful functions: 
    # self.simulator.current_state, self.simulator.set_state, self.simulator.move

    # TODO: build a game tree from the current node up to the given depth
    def build_tree(self, node = None, depth = 0):
        #pass
        if node == None:
            node = self.root

        if depth < 0:
            return
        
        if node.player_type == CHANCE_PLAYER: #Game simulator

            #Place a random tile a 2 in an empty tile - get_open_tiles() returns all empty tiles
            empty_tile = self.simulator.get_open_tiles()
            #self.simulator.set_state(self.simulator.get_state()[0],self.simulator.get_state()[1])
            # self.simulator.set_state(node.state[0],node.state[1])
            #print(self.simulator.get_state()[1])
            # #Child nodes = #empty tiles
            for x,y in empty_tile:
                self.simulator.set_state(node.state[0],node.state[1])
                self.simulator.tile_matrix[x][y] = 2
                child = Node(self.simulator.current_state(),MAX_PLAYER) #child shoud have different player type
                node.children.append(child)
                # print(child)
                self.build_tree(child,depth-1)
                self.simulator.set_state(node.state[0], node.state[1])

            # Likelihood of transition = 1/(#empty tiles) -> chance()

        elif node.player_type == MAX_PLAYER:
            # 4 actions: 0 - up, 1 - left, 2 - down, 3 - right
            for m in MOVES:
                #self.simulator.set_state(self.simulator.get_state()[0],self.simulator.get_state()[1])
                self.simulator.set_state(node.state[0],node.state[1])
                # - Max node can have at most 4 children
                # - Check if action is possible by using move() in game class - Returns True if valid
                if(self.simulator.move(m)):
                    child = Node(self.simulator.current_state(), CHANCE_PLAYER)
                    node.children.append(child)
                    self.build_tree(child, depth-1)

                #     self.simulator.set_state(node.state[0], node.state[1])
                else:
                    node.children.append(Node(self.simulator.current_state(), 2))
                    

                

    def chance(self,node):
        return 1/len(node.children)     
      
    # TODO: expectimax calculation.
    # Return a (best direction, expectimax value) tuple if node is a MAX_PLAYER
    # Return a (None, expectimax value) tuple if node is a CHANCE_PLAYER
    def expectimax(self, node = None):
        # TODO: delete this random choice but make sure the return type of the function is the same
        
        if node.is_terminal():
            # If the node is a terminal node, return its score
            return None, node.state[1]
        
        if node is None:
            node = self.root

        if node.player_type == MAX_PLAYER:
            value = -inf
            direction = 0
            for d,c in enumerate(node.children):    #node.children:
                new_value = max(value, self.expectimax(c)[1])   # max value
                if(new_value != value):
                    value = new_value
                    direction = d   #random.randint(0, 3)    #c[0]
            return direction,value

        elif node.player_type == CHANCE_PLAYER:
            value = 0
            for c in node.children:
                #value = max(value, self.expectimax(c)[1])
                value += self.expectimax(c)[1] * self.chance(node)
                
            return None,value
        else:
            return None,0
       
       # return random.randint(0, 3), 0


    # Return decision at the root
    def compute_decision(self):
        self.build_tree(self.root, self.search_depth)
        direction, _ = self.expectimax(self.root)
        return direction

    # TODO (optional): implement method for extra credits
    def compute_decision_ec(self):
        # return random.randint(0, 3)
        self.build_tree(self.root, self.search_depth)
        direction, _ = self.expectimax(self.root)
        return direction

