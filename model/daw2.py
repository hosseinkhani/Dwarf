import random

from daw import DawState, DawAction, DawModel


class DawModel2(DawModel):
    def __init__(self, transitions, rewards, actions, states, initial_states, terminal_states=None,
                 reward_image_path=None, lost_image_path=None, update_round=10):
        DawModel.__init__(self, transitions, rewards, actions, states, initial_states, terminal_states)
        self.reward_path = reward_image_path
        self.lost_path = lost_image_path

        self.rewards_history = []
        self.update_round = update_round
        self.update_counter = 0

        self.update_model()

    def start_new_session(self, initial_state=None):
        self.update_counter += 1
        if self.update_counter % self.update_round == 0:
            self.update_counter = 0
            self.update_model()

        return DawModel.start_new_session(self, initial_state)

    def update_model(self):
        if bool(random.getrandbits(1)):  # left state goal
            if bool(random.getrandbits(1)):  # left action goal
                self.transitions[self.states[1]][self.actions[0]][self.states[3]] = .7
                self.transitions[self.states[1]][self.actions[0]][self.states[4]] = .3

                self.transitions[self.states[1]][self.actions[1]][self.states[3]] = .3
                self.transitions[self.states[1]][self.actions[1]][self.states[4]] = .7
            else:  # right action goal
                self.transitions[self.states[1]][self.actions[0]][self.states[3]] = .3
                self.transitions[self.states[1]][self.actions[0]][self.states[4]] = .7

                self.transitions[self.states[1]][self.actions[1]][self.states[3]] = .7
                self.transitions[self.states[1]][self.actions[1]][self.states[4]] = .3

            self.transitions[self.states[2]][self.actions[0]][self.states[3]] = .3
            self.transitions[self.states[2]][self.actions[0]][self.states[4]] = .7

            self.transitions[self.states[2]][self.actions[1]][self.states[3]] = .3
            self.transitions[self.states[2]][self.actions[1]][self.states[4]] = .7
        else:  # right state goal
            if bool(random.getrandbits(1)):  # left action goal
                self.transitions[self.states[2]][self.actions[0]][self.states[3]] = .7
                self.transitions[self.states[2]][self.actions[0]][self.states[4]] = .3

                self.transitions[self.states[2]][self.actions[1]][self.states[3]] = .3
                self.transitions[self.states[2]][self.actions[1]][self.states[4]] = .7
            else:  # right action goal
                self.transitions[self.states[2]][self.actions[0]][self.states[3]] = .3
                self.transitions[self.states[2]][self.actions[0]][self.states[4]] = .7

                self.transitions[self.states[2]][self.actions[1]][self.states[3]] = .7
                self.transitions[self.states[2]][self.actions[1]][self.states[4]] = .3

            self.transitions[self.states[1]][self.actions[0]][self.states[3]] = .3
            self.transitions[self.states[1]][self.actions[0]][self.states[4]] = .7

            self.transitions[self.states[1]][self.actions[1]][self.states[3]] = .3
            self.transitions[self.states[1]][self.actions[1]][self.states[4]] = .7

        # TODO maybe not the best way
        self.rewards_history.append([self.transitions[self.states[1]][self.actions[0]][self.states[3]],
                                     self.transitions[self.states[1]][self.actions[1]][self.states[3]],
                                     self.transitions[self.states[2]][self.actions[0]][self.states[3]],
                                     self.transitions[self.states[2]][self.actions[1]][self.states[3]]])
        # print self.rewards_history[-1]