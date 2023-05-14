import copy
import random

from game import Game, states

HIT = 0
STAND = 1
DISCOUNT = 0.95 #This is the gamma value for all value calculations

class Agent:
    def __init__(self):

        # For MC values
        self.MC_values = {} # Dictionary: Store the MC value of each state
        self.S_MC = {}      # Dictionary: Store the sum of returns in each state
        self.N_MC = {}      # Dictionary: Store the number of samples of each state
        # MC_values should be equal to S_MC divided by N_MC on each state (important for passing tests)

        # For TD values
        self.TD_values = {}  # Dictionary: Store the TD value of each state
        self.N_TD = {}       # Dictionary: Store the number of samples of each state

        # For Q-learning values
        self.Q_values = {}   # Dictionary: Store the Q-Learning value of each state and action
        self.N_Q = {}        # Dictionary: Store the number of samples of each state for each action

        # Initialization of the values
        for s in states:
            self.MC_values[s] = 0
            self.S_MC[s] = 0
            self.N_MC[s] = 0
            self.TD_values[s] = 0
            self.N_TD[s] = 0
            self.Q_values[s] = [0,0] # First element is the Q value of "Hit", second element is the Q value of "Stand"
            self.N_Q[s] = [0,0] # First element is the number of visits of "Hit" at state s, second element is the Q value of "Stand" at s

        # Game simulator
        # NOTE: see the comment of `init_cards()` method in `game.py` for description of the initial game states       
        self.simulator = Game()

    # NOTE: do not modify this function
    # This is the fixed policy given to you, for which you need to perform MC and TD policy evaluation. 
    @staticmethod
    def default_policy(state):
        user_sum = state[0]
        user_A_active = state[1]
        actual_user_sum = user_sum + user_A_active * 10
        if actual_user_sum < 14:
            return 0
        else:
            return 1

    # NOTE: do not modify this function
    # This is the fixed learning rate for TD and Q learning. 
    @staticmethod
    def alpha(n):
        return 10.0/(9 + n)
   
    #TODO: Take one step of transition in the game simulator
    #Hint: Take the given action, and return the next state given by the game engine. 
    #Hint: Useful functions: self.simulator.act_hit, self.simulator.act_stand, self.simulator.state 
    #Hint: If a state is terminal ("game_over"), i.e., taking any action from it doesn't lead to any next state, then you can return None
    #Hint: You need the act_hit and act_stand functions in game.py. Note that they are already generating random next cards. 
    #Hint: You can keep track the reward of states with this function as well, e.g., as one of the return values
    #Hint: After this function, you can also define another function that simulates one full trajectory, but it's optional
    def make_one_transition(self, action):
        # If a state is terminal ("game_over"), then you can return None
        if self.simulator.game_over():
            return None, self.simulator.check_reward()
        
        # HIT
        if action == HIT:
            self.simulator.act_hit()
        # STAND
        elif action == STAND:
            self.simulator.act_stand()

        # return the next state given by the game engine
        # and keep track the reward of states
        return self.simulator.state, self.simulator.check_reward()

    # helper funtion that simulates one full trajectory
    def simulate_till_terminal(self):
        trajectory = []
        while not self.simulator.game_over():
            # cur_s = self.simulator.state
            # r = self.simulator.check_reward()
            #trajectory.append(state)
            a = self.default_policy(self.simulator.state)
            trajectory.append((self.simulator.state,self.simulator.check_reward()))
            
            if a == HIT:
                self.simulator.act_hit()
            elif a == STAND:
                self.simulator.act_stand()

        # next_s = self.simulator.state
        # next_s, next_r = self.make_one_transition(a)
        
        trajectory.append((self.simulator.state,self.simulator.check_reward()))

        return trajectory

    # helper funtion
    def reward_to_go(self,trajectory,state):
        reward = 0
        k = 0
        hold = k

        for i in range(len(trajectory)):
            if trajectory[i] == state:
                k = i
        
        while hold<len(trajectory):
            reward += (DISCOUNT**(hold-k))*trajectory[hold][1]
            hold += 1
        return reward

    #TODO: Implement MC policy evaluation
    def MC_run(self, num_simulation, tester=False):

        # Perform num_simulation rounds of simulations in each cycle of the overall game loop
        for simulation in range(num_simulation):

            # Do not modify the following three lines
            if tester:
                self.tester_print(simulation, num_simulation, "MC")
            self.simulator.reset()  # The simulator is already reset for you for each new trajectory

            # TODO
            # Note: Do not reset the simulator again in the rest of this simulation
            # Hint: self.simulator.state gives you the current state of the trajectory
            # Hint: Use the "make_one_transition" function to take steps in the simulator, and keep track of the states
            # Hint: Go through game.py file and figure out which functions will be useful
            # Make sure to update self.MC_values, self.S_MC, self.N_MC for the autograder
            # Don't forget the DISCOUNT

            # s = self.simulator.state
            trajectory = self.simulate_till_terminal()

            for s in trajectory:
                self.S_MC[s[0]] += self.reward_to_go(trajectory,s[0])
                self.N_MC[s[0]] += 1
                
                #self.MC_values = average (G[s])
                self.MC_values[s[0]] = self.S_MC[s[0]]/self.N_MC[s[0]]

    
    #TODO: Implement TD policy evaluation
    def TD_run(self, num_simulation, tester=False):

        # Perform num_simulation rounds of simulations in each cycle of the overall game loop
        for simulation in range(num_simulation):

            # Do not modify the following three lines
            if tester:
                self.tester_print(simulation, num_simulation, "TD")
            self.simulator.reset()

            # TODO
            # Note: Do not reset the simulator again in the rest of this simulation
            # Hint: self.simulator.state gives you the current state of the trajectory
            # Hint: Use the "make_one_transition" function to take steps in the simulator, and keep track of the states
            # Hint: Go through game.py file and figure out which functions will be useful
            # Hint: The learning rate alpha is given by "self.alpha(...)"
            # Make sure to update self.TD_values and self.N_TD for the autograder
            # Don't forget the DISCOUNT

            cur_s = self.simulator.state
            cur_r = self.simulator.check_reward()

            while cur_s is not None:
                a = self.default_policy(cur_s)
                next_s, next_r = self.make_one_transition(a)
                

                # if next_s is NULL, then TD_V[next_s]=0
                if next_s is None:
                    self.TD_values[next_s] = 0
                    
                self.TD_values[cur_s] += self.alpha(self.N_TD[cur_s]) * (cur_r + 
                            DISCOUNT * self.TD_values[next_s] - self.TD_values[cur_s])

                self.N_TD[cur_s] += 1
                cur_s = next_s
                cur_r = next_r

                
    #TODO: Implement Q-learning
    def Q_run(self, num_simulation, tester=False, epsilon=0.4):

        # Perform num_simulation rounds of simulations in each cycle of the overall game loop
        for simulation in range(num_simulation):

            # Do not modify the following three lines
            if tester:
                self.tester_print(simulation, num_simulation, "Q")
            self.simulator.reset()

            # TODO
            # Note: Do not reset the simulator again in the rest of this simulation
            # Hint: self.simulator.state gives you the current state of the trajectory
            # Hint: Use the "make_one_transition" function to take steps in the simulator, and keep track of the states
            # Hint: Go through game.py file and figure out which functions will be useful
            # Hint: The learning rate alpha is given by "self.alpha(...)"
            # Hint: Implement epsilon-greedy method in "self.pick_action(...)"
            # Important: When calling pick_action, use the given parameter epsilon=0.4 to match the autograder
            # Make sure to update self.Q_values, self.N_Q for the autograder
            # Don't forget the DISCOUNT

            # DISCOUNT = gamma
            cur_s = self.simulator.state
            cur_r = self.simulator.check_reward()

            while cur_s is not None:
                # pick action according to epsilon-greedy
                a = self.pick_action(cur_s, epsilon)
                next_s,next_r= self.make_one_transition(a)
                
                if next_s == None:
                    # if it's null, Q[next_s][next_a] = 0 for every next_a
                    self.Q_values[next_s] = [0, 0]

                self.Q_values[cur_s][a] += self.alpha(self.N_Q[cur_s][a]) * (cur_r + 
                                    DISCOUNT*max(self.Q_values[next_s][0],self.Q_values[next_s][1]) - self.Q_values[cur_s][a])

                self.N_Q[cur_s][a] += 1
                cur_s = next_s
                cur_r = next_r


    #TODO: Implement epsilon-greedy policy
    def pick_action(self, s, epsilon):
        # TODO: Replace the following random value with an action following the epsilon-greedy strategy
        # return random.randint(0, 1)
        if random.random() < epsilon:
            return random.randint(0, 1)
        else:
            if self.Q_values[s][0] > self.Q_values[s][1]:
                return 0
            else:
                return 1 


    ####Do not modify anything below this line####

    #Note: do not modify
    def autoplay_decision(self, state):
        hitQ, standQ = self.Q_values[state][HIT], self.Q_values[state][STAND]
        if hitQ > standQ:
            return HIT
        if standQ > hitQ:
            return STAND
        return HIT #Before Q-learning takes effect, just always HIT

    # NOTE: do not modify
    def save(self, filename):
        with open(filename, "w") as file:
            for table in [self.MC_values, self.TD_values, self.Q_values, self.S_MC, self.N_MC, self.N_TD, self.N_Q]:
                for key in table:
                    key_str = str(key).replace(" ", "")
                    entry_str = str(table[key]).replace(" ", "")
                    file.write(f"{key_str} {entry_str}\n")
                file.write("\n")

    # NOTE: do not modify
    def load(self, filename):
        with open(filename) as file:
            text = file.read()
            MC_values_text, TD_values_text, Q_values_text, S_MC_text, N_MC_text, NTD_text, NQ_text, _  = text.split("\n\n")
            
            def extract_key(key_str):
                return tuple([int(x) for x in key_str[1:-1].split(",")])
            
            for table, text in zip(
                [self.MC_values, self.TD_values, self.Q_values, self.S_MC, self.N_MC, self.N_TD, self.N_Q], 
                [MC_values_text, TD_values_text, Q_values_text, S_MC_text, N_MC_text, NTD_text, NQ_text]
            ):
                for line in text.split("\n"):
                    key_str, entry_str = line.split(" ")
                    key = extract_key(key_str)
                    table[key] = eval(entry_str)

    # NOTE: do not modify
    @staticmethod
    def tester_print(i, n, name):
        print(f"\r  {name} {i + 1}/{n}", end="")
        if i == n - 1:
            print()
