from __future__ import print_function
from game import sd_peers, sd_spots, sd_domain_num, init_domains, \
    restrict_domain, SD_DIM, SD_SIZE
import random, copy

conflict = (-1,-1)

class AI:
    def __init__(self):
        pass

    def solve(self, problem):
        domains = init_domains()       #D, x = sd_spots
        restrict_domain(domains, problem) 

        # TODO: implement backtracking search. 

        # # TODO: delete this block ->
        # # Note that the display and test functions in the main file take domains as inputs. 
        # #   So when returning the final solution, make sure to take your assignment function 
        # #   and turn the value into a single element list and return them as a domain map. 
        # for spot in sd_spots:
        #     domains[spot] = [1]
        # return domains
        # # <- TODO: delete this block

        assign = {}          #σ
        stack = []           #Δ

        while True:
            assign, domains = self.propagate(assign,domains)
            if conflict not in assign:
                if self.allAssigned(assign):
                    return self.solution(assign)
                else:
                    assign,x = self.makeDecision(assign,domains)
                    # stack = stack.append(assign,x,domains)
                    # stack.append((assign,x,domains))
                    stack.append((copy.deepcopy(assign),x,copy.deepcopy(domains)))
            else:
                if stack == []:
                    return None
                else:
                    assign,domains = self.backtrack(stack)



    # TODO: add any supporting function you need

    # helper function for solve
    def allAssigned(self,assign):
        # if len(assign) < len(sd_spots):
        #     return False

        for d in sd_spots:
            if d not in assign:
                return False
        return True

    def solution(self,assign):
        s = {}
        for d in assign:
            # s[d] = assign[d]
            s[d] = [assign[d]]
        return s


    # take assignment and domains as parameters
    def propagate(self,assign,domains):
        while True:
            # d = domains, x_i = sd_spots
            # assign = σ
            new_assign = []
            for x in domains:
                # Make assignment if domain becomes singleton
                if len(domains[x])==1 and x not in assign:
                    assign[x] = domains[x][0]
                    # assign = assign + {(x,assign)} 
                    new_assign.append(x)

            # If x has been assigned a value, update its domain
            for x in assign: 
                if len(domains[x])>1:
                    # domains[x].append(assign)
                    # domains[x] = assign[x]
                    domains[x] = [assign[x]]
                    new_assign.append(x)

            for x in domains:
                if len(domains[x]) == 0:
                    assign[conflict] = -1
                    return assign,domains
            
            
            # if there exists i,j such that 
            # ai ∈ D(xi) is not consistent with any aj ∈ D(xj) in C 
            # then D(xi).Remove(ai)
            consist = True

            for i in new_assign:
                for j in sd_peers[i]:
                    if assign[i] in domains[j]:
                        domains[j].remove(assign[i])
                        consist = False
            if consist:
                return assign,domains
    


    def makeDecision(self,assign,domains):
        min_len = float('inf')
        min_x = None
        for x in domains:
            if x not in assign and len(x) < min_len:
                min_len = len(x)
                min_x = x
        assign[min_x] = domains[min_x][0]
        return assign, min_x



    def backtrack(self,stack):
        assign,x,domains = stack.pop()
        a = assign[x]
        # assign.remove((x,a))
        assign.pop(x)
        domains[x].remove(a)

        return assign,domains

 

    #### The following templates are only useful for the EC part #####

    # EC: parses "problem" into a SAT problem
    # of input form to the program 'picoSAT';
    # returns a string usable as input to picoSAT
    # (do not write to file)
    def sat_encode(self, problem):
        text = ""

        # TODO: write CNF specifications to 'text'

        return text

    # EC: takes as input the dictionary mapping 
    # from variables to T/F assignments solved for by picoSAT;
    # returns a domain dictionary of the same form 
    # as returned by solve()
    def sat_decode(self, assignments):
        # TODO: decode 'assignments' into domains
        
        # TODO: delete this ->
        domains = {}
        for spot in sd_spots:
            domains[spot] = [1]
        return domains
        # <- TODO: delete this
