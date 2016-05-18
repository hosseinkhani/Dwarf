import random

from daw import DawState, DawAction, DawModel


class DawModel2(DawModel):
    def __init__(self, transitions, rewards, actions, states, initial_states, terminal_states=None,
                 reward_image_path=None, lost_image_path=None, update_round=10, initial_rewards=None):
        DawModel.__init__(self, transitions, rewards, actions, states, initial_states, terminal_states)
        self.reward_path = reward_image_path
        self.lost_path = lost_image_path

        self.rewards_history = []
        self.update_round = update_round
        self.update_counter = 1
        self.initial_rewards = initial_rewards

    def start_new_session(self, initial_state=None):
        if self.update_counter % self.update_round == 1:
            self.update_model()
        # else:
        self.update_counter += 1

        return DawModel.start_new_session(self, initial_state)

    def update_model(self, reward_probabilities=None):
        self.update_counter = 1
        if reward_probabilities is None:
            rp = list(self.initial_rewards)
        else:
            rp = list(reward_probabilities)
        random.shuffle(rp)

        for i in range(len(rp)):
            self.transitions[self.states[1+i/2]][self.actions[i % 2]][self.states[3]] = rp[i]
            self.transitions[self.states[1+i/2]][self.actions[i % 2]][self.states[4]] = 1-rp[i]

        # TODO maybe not the best way
        self.rewards_history.append([self.transitions[self.states[1]][self.actions[0]][self.states[3]],
                                     self.transitions[self.states[1]][self.actions[1]][self.states[3]],
                                     self.transitions[self.states[2]][self.actions[0]][self.states[3]],
                                     self.transitions[self.states[2]][self.actions[1]][self.states[3]]])
        print self.rewards_history[-1], len(self.rewards_history)
