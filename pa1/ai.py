from __future__ import print_function
from heapq import * #Hint: Use heappop and heappush

ACTIONS = [(0,1),(1,0),(0,-1),(-1,0)] #up,right,down,left

# to run the test: python main.py -t

class AI:
    def __init__(self, grid, type):
        self.grid = grid
        self.set_type(type)
        self.set_search()

    def set_type(self, type):
        self.final_cost = 0
        self.type = type

    def set_search(self):
        self.final_cost = 0
        self.grid.reset()
        self.finished = False       #not finished
        self.failed = False         #not failed
        self.previous = {}          #no previous

        # Initialization of algorithms goes here
        #  frontier <- start node, explored <- {}
        if self.type == "dfs":
            self.frontier = [self.grid.start]
            self.explored = []

        elif self.type == "bfs":
            #pass
            self.frontier = [self.grid.start]
            self.explored = []
        
        elif self.type == "ucs":
            #pass
            # node ← a node with STATE = problem.INITIAL-STATE, PATH-COST = 0
            # frontier ← a priority queue ordered by PATH-COST, with node as the only element 
            # explored ← an empty set 
            self.frontier = []        # PATH-COST, start node
            heappush(self.frontier,(0, self.grid.start))
            self.explored = []
            self.new_frontier = []

        elif self.type == "astar":
            #pass
            # Total cost = Real cost + Heuristic cost (F=G+H)
            # node ← a node with STATE = problem.INITIAL-STATE, G+H
            # frontier ← a priority queue ordered by G+H, with node as the only element
            # explored ← an empty set
            self.frontier = []     # g+h=f,g,start node
            heappush(self.frontier,(0, 0, self.grid.start))
            self.explored = []
            self.new_frontier = []

    def get_result(self):
        total_cost = 0
        current = self.grid.goal
        while not current == self.grid.start:
            total_cost += self.grid.nodes[current].cost()
            current = self.previous[current]
            self.grid.nodes[current].color_in_path = True #This turns the color of the node to red
        total_cost += self.grid.nodes[current].cost()
        self.final_cost = total_cost

    def make_step(self):
        if self.type == "dfs":
            self.dfs_step()
        elif self.type == "bfs":
            self.bfs_step()
        elif self.type == "ucs":
            self.ucs_step()
        elif self.type == "astar":
            self.astar_step()

    #DFS: BUGGY, fix it first
    def dfs_step(self):
        #empty frontier, no node to be explored
        if not self.frontier:
            self.failed = True
            self.finished = True
            print("no path")
            return
        
        # current node should be the last one in frontier
        current = self.frontier.pop()
        #print(current) ->(15, 19)
                        # (14, 19)
                        # (13, 19)

        #Finishes search if we've found the goal.
        # if current == self.grid.goal:
        #     self.finished = True
        #     return

        # ACTIONS = [(0,1),(1,0),(0,-1),(-1,0)] up,right,down,left
        # find the children of current node and set the color
        children = [(current[0]+a[0], current[1]+a[1]) for a in ACTIONS]
        #print(children) ->[(15, 20), (16, 19), (15, 18), (14, 19)]
                        # [(14, 20), (15, 19), (14, 18), (13, 19)]
                        # [(13, 20), (14, 19), (13, 18), (12, 19)]

        self.grid.nodes[current].color_checked = True
        self.grid.nodes[current].color_frontier = False

        # mark current as explored
        self.explored.append(current)

        for n in children:
            # avoid duplicate
            if n not in self.explored and n not in self.frontier:
            # check the range in case of out of range
                if n[0] in range(self.grid.row_range) and n[1] in range(self.grid.col_range):
                    if not self.grid.nodes[n].puddle:
                            self.previous[n] = current

                            # can't find the goal
                            if n != self.grid.goal:
                                self.frontier.append(n)
                                self.grid.nodes[n].color_frontier = True
                            else:
                                # finished because find the goal
                                self.finished = True

    #Implement BFS here (Don't forget to implement initialization at line 23)
    def bfs_step(self):
        if not self.frontier:
            self.failed = True
            self.finished = True
            print("no path")
            return
        
        # current node should be the first one in frontier
        current = self.frontier.pop(0)
        # find the children of current node and set the color
        children = [(current[0]+a[0], current[1]+a[1]) for a in ACTIONS]
        self.grid.nodes[current].color_checked = True
        self.grid.nodes[current].color_frontier = False

        # add current node to explored
        self.explored.append(current)

        for n in children:
            # avoid duplicate
            if n not in self.explored and n not in self.frontier:
                # check the range in case of out of range
                if n[0] in range(self.grid.row_range) and n[1] in range(self.grid.col_range):
                    if not self.grid.nodes[n].puddle:
                        self.previous[n] = current
                        # can't find the goal
                        if n != self.grid.goal:
                            self.frontier.append(n)
                            self.grid.nodes[n].color_frontier = True
                        else:
                            # finished because find the goal
                            self.finished = True


    #Implement UCS here (Don't forget to implement initialization at line 23)
    def ucs_step(self):
        if not self.frontier:
            self.failed = True
            self.finished = True
            print("no path")
            return
        
        # pop the element with the minimum cost from the frontier by using heap queue
        current = heappop(self.frontier)
        # print(current)    -> (0, (15, 19))
        # print(current[1]) -> (15, 19)
        # print(current[1][0]) -> 15
        # find the children of current node and set the color
        children = [(current[1][0]+a[0], current[1][1]+a[1]) for a in ACTIONS]
        self.grid.nodes[current[1]].color_checked = True
        self.grid.nodes[current[1]].color_frontier = False

        # print(children)

        # add current node to explored
        self.explored.append(current[1])

        for n in children:
            # avoid duplicate
            # check if it is an explored state (ignore), 
            # or has already appeared in the frontier with a lower cost (ignore)
            if n not in self.explored and n not in self.new_frontier:
                # check the range in case of out of range
                if n[0] in range(self.grid.row_range) and n[1] in range(self.grid.col_range):
                    if not self.grid.nodes[n].puddle:
                        # update previous
                        self.previous[n] = current[1]
                        # print(self.previous[n])
                        # can't find the goal
                        if n != self.grid.goal:
                            # self.frontier.append(n)
                            # put the node and updated cost
                            heappush(self.frontier,(self.grid.nodes[n].cost()+current[0],n))
                            # add to new_frontier so that it can be checked
                            self.new_frontier.append(n)
                            self.grid.nodes[n].color_frontier = True
                        else:
                            # finished because find the goal
                            self.finished = True

    
    #Implement Astar here (Don't forget to implement initialization at line 23)
    def astar_step(self):
        if not self.frontier:
            self.failed = True
            self.finished = True
            print("no path")
            return
        
        # current = heappop(self.frontier)
        # print(current) ->(0, 0, (15, 19))
        # print(current[2]) ->(15, 19)

        # g = heappop(self.frontier)
        # f = heappop(self.frontier)
        # current = heappop(self.frontier)
        f,g,current = heappop(self.frontier)

        # print(g,h,current) #-> 0 0 (15, 19)
        
        children = [(current[0]+a[0], current[1]+a[1]) for a in ACTIONS]
        # print(children) ->[(15, 20), (16, 19), (15, 18), (14, 19)]
        self.grid.nodes[current].color_checked = True
        self.grid.nodes[current].color_frontier = False
        self.explored.append(current)

        for n in children:
            # avoid duplicate
            # check if it is an explored state (ignore), 
            # or has already appeared in the frontier with a lower cost (ignore)
            if n not in self.explored and n not in self.new_frontier:
                # check the range in case of out of range
                if n[0] in range(self.grid.row_range) and n[1] in range(self.grid.col_range):
                    if not self.grid.nodes[n].puddle:
                        # update previous
                        self.previous[n] = current
                        # print(self.previous[n])
                        # can't find the goal
                        if n != self.grid.goal:
                            #F=G+H
                            # update values
                            h = f - g
                            new_g = self.grid.nodes[n].cost() + g
                            new_f = new_g + h
                            # new_h = new_f - new_g
                            
                            heappush(self.frontier,(new_f, new_g, n))
                            
                            # add to new_frontier so that it can be checked
                            self.new_frontier.append(n)
                            self.grid.nodes[n].color_frontier = True
                        else:
                            # finished because find the goal
                            self.finished = True

