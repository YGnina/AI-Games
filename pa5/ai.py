from __future__ import print_function
from game import sd_peers, sd_spots, sd_domain_num, init_domains, \
    restrict_domain, SD_DIM, SD_SIZE
import random, copy

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

        assign = []          #σ
        stack = []           #Δ

        while True:
            assign, domains = self.propagate(assign,domains)
            if (0,0) not in assign:
                if self.allAssigned(assign):
                    return self.solution(assign)
                else:
                    assign,x =  self.makeDecision(assign,domains)
                    stack = stack.append(assign,x,domains)
            else:
                if stack == None:
                    return None
                else:
                    assign,domains = self.backtrack(stack)



    # TODO: add any supporting function you need

    # helper function for solve
    def allAssigned(a):
        pass

    def solution(a):
        pass

    # take assignment and domains as parameters
    def propagate(assign,d):
        # while True:
        #     # d = domains, x_i = sd_spots
        #     for x in d:
        #         if d[x] = a:
        #             a = a + {(x,a)}
        pass


    def makeDecision(assign,d):
        # if x in assign:
        #     a = d()
        pass


    def backtrack(s):
        assign,x,domains = s.pop()
        a = assign[x]
        assign.remove((x,a))
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
