import json

class QLearningAgent:
    def __init__(self):
        self.flag = 1
        self.discount_factor = 0.95
        self.alpha = 0.7
        self.alpha_decay = 0.00003
        self.generation = 0
        self.prev_action = 0
        self.prev_state = "0_0_0_0"
        self.moves = []
        self._Qvalues = {} 
        self.max_len = 1000000
        #self.load_qvalues()
    def load_qvalues(self):
        print("Loading Q-table states from json file...")
        try:
            with open("data/_Qvalues_resume.json", "r") as f:
                print(111)
                self._Qvalues = json.load(f)
        except IOError:
            self.init_qvalues(self.prev_state)
    
    def get_max_Qvalue(self, state):
        return max(self._Qvalues[state][0], self._Qvalues[state][1])

    def update(self, state, new_state, action, reward):
        if (self.flag):
            self._Qvalues[state][action] = (1 - self.alpha) * (self._Qvalues[state][action]) + \
            self.alpha * (reward + self.discount_factor * self.get_max_Qvalue(new_state))

    def init_qvalues(self, state):
        if self._Qvalues.get(state) is None:
            self._Qvalues[state] = [0, 0]

    def getAction(self, state):
        if (self.flag):
            self.moves.append((self.prev_state, self.prev_action, state))
            if (len(self.moves) > self.max_len):
                all_moves = list(reversed(self.moves))
                for i in range(self.max_len):
                    state, action, new_state = all_moves[i]
                    self.update(state, new_state, action, 0)
                self.moves = self.moves[self.max_len:]
            self.prev_state = state
        if (self._Qvalues[state][0] >= self._Qvalues[state][1]):
            self.prev_action = 0
        else:
            self.prev_action = 1
        return self.prev_action

    def update_all_Qvalues(self):
        if (self.flag):
            death_flag = 0
            if (int(self.moves[len(self.moves) - 1][2].split("_")[1]) > 120):
                death_flag = 1
            for i in range(len(self.moves) - 1, 0,  -1):
                state, action, new_state = self.moves[i]
                reward = 0
                if (i >= len(self.moves) - 2):
                    reward = -1000
                elif ((death_flag) and action):
                    death_flag = 0
                    reward = -1000
                self.update(state, new_state, action, reward)
            self.moves = []
    def get_x_coordinate(self, x):
        if (x < -40):
            return int(x)
        elif (x < 140):
            return int(x) - (int(x) % 10)
        else:
            return int(x) - (int(x) % 70)
        
    def get_y_coordinate(self, y):
        if (-180 < y < 180):
            return int(y) - (int(y) % 10)
        return int(y) - (int(y) % 60)
    
    def get_state(self, x, y, vel, pipe):
        pipe1 = pipe[0]
        pipe2 = pipe[1]
        if (x - pipe[0]["x"] >= 50):
            pipe1 = pipe[1]
            if (len(pipe) > 2):
                pipe2 = pipe[2]

        x1 = pipe1["x"] - x
        y1 = pipe1["y"] - y

        if (-50 < x1 <= 0):
            y2 = pipe2["y"] - y
        else:
            y2 = 0
        
        x1 = self.get_x_coordinate(x1)
        y1 = self.get_y_coordinate(y1)
        y2 = self.get_y_coordinate(y2)
        state = str(int(x1)) + "_" + str(int(y1)) + "_" + str(int(vel)) 
        self.init_qvalues(state)
        return state

    def save_qvalues(self):
        if self.flag:
            with open("data/_Qvalues_resume.json", "w") as f:
                json.dump(self._Qvalues, f)
