import random
from pickle import dump, load


class ReferenceState(object):
    ID = 0

    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

        self.id = ReferenceState.ID
        ReferenceState.ID += 1

    def __index__(self):
        return self.id

    def __eq__(self, other):
        return issubclass(type(other), ReferenceState) and other.id == self.id

    def __hash__(self):
        return self.id


class ReferenceAction(object):
    ID = 0

    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

        self.id = ReferenceAction.ID
        ReferenceAction.ID += 1

    def __index__(self):
        return self.id

    def __eq__(self, other):
        return issubclass(type(other), ReferenceAction) and other.id == self.id

    def __hash__(self):
        return self.id.__hash__()


class ReferenceModel(object):
    def __init__(self, transitions, rewards, actions, states, initial_states, terminal_states=None):
        """
        build an model instance with required parameters for Markove Models
        :param transitions: dict of transitions matrix of model
        :param rewards: dict of rawards matrix of model
        :param actions: list of all actions
        :param states: list of all states
        :param initial_states: initial states of model, set is better than list
        :param terminal_states: terminal states of model, set is better than list
        :return: an instance of Class
        """
        self.transitions = transitions
        self.rewards = rewards
        self.states = states
        self.actions = actions
        self.initial_states = initial_states
        self.terminal_states = terminal_states

    def start_new_session(self, initial_state=None):
        """
        for playing one round in the environment
        :param initial_state: first state to be there, if None a random one selected
        :return: a generator that gets action in each turn and returns (state, reward)
        """
        current_state = initial_state if initial_state is not None else random.sample(self.initial_states, 1)[0]

        yield current_state  # for first state

        while current_state not in self.terminal_states:
            action = yield

            rand = random.random()
            # print '#'*20, current_state, action
            for s, p in self.transitions[current_state][action].iteritems():
                # print s, p, rand
                if rand-p <= 0:
                    break
                rand -= p
            reward = self.rewards(current_state=current_state, action=action, next_state=s) if callable(self.rewards) \
                else self.rewards[current_state][action][s]
            yield s, reward
            current_state = s

    def get_legal_actions(self, state):
        """
        returns list of legal actions at input state
        :param state: state to get legal actions
        :return: list of actions
        """
        if type(self.transitions) == dict:
            return self.transitions[state].keys()
        elif type(self.transitions) == list:
            ans = []
            for action in self.actions:
                if sum(self.transitions[state][action]):
                    ans.append(action)
            return ans
        else:
            raise ValueError("transition must be a 3d list or dict")

    def get_all_actions(self):
        """
        return list of all actions
        :return: list of actions
        """
        return self.actions

    def save(self, file_name, description="No description."):
        """
        save model to a file for later usage
        :param file_name: file to save
        :param description: optional description to add
        """
        log_file = open('../model/'+file_name, 'w')
        dump((description, self), log_file)
        log_file.close()


# if __name__ == '__main__':
#     myactions = [ReferenceAction(name='left'), ReferenceAction(name='right')]
#     mystates = [ReferenceState(desc='im first one'),
#                 ReferenceState(desc='im left one'),
#                 ReferenceState(desc='im right one'),
#                 ReferenceState(desc='im reward state'),
#                 ReferenceState(desc='im noreward state')]
#
#     myinitial_states = {mystates[0]}
#
#     myterminal_states = {mystates[3], mystates[4]}
#
#     mytransitions_matrix = dict()
#     mytransitions_matrix[mystates[0]] = {  # first state
#         myactions[0]: {mystates[0]: 0, mystates[1]: .7, mystates[2]: .3, mystates[3]: 0, mystates[4]: 0},  # left action
#         myactions[1]: {mystates[0]: 0, mystates[1]: .3, mystates[2]: .7, mystates[3]: 0, mystates[4]: 0}  # right action
#     }
#     mytransitions_matrix[mystates[1]] = {  # left state
#         myactions[0]: {mystates[0]: 0, mystates[1]: 0, mystates[2]: 0, mystates[3]: .6, mystates[4]: .4},  # left action
#         myactions[1]: {mystates[0]: 0, mystates[1]: 0, mystates[2]: 0, mystates[3]: .1, mystates[4]: .9}  # right action
#     }
#     mytransitions_matrix[mystates[2]] = {  # right state
#         myactions[0]: {mystates[0]: 0, mystates[1]: 0, mystates[2]: 0, mystates[3]: .2, mystates[4]: .8},  # left action
#         myactions[1]: {mystates[0]: 0, mystates[1]: 0, mystates[2]: 0, mystates[3]: .4, mystates[4]: .6}  # right action
#     }
#     # these 2 have no use
#     mytransitions_matrix[mystates[3]] = {}  # reward state(terminal)
#     mytransitions_matrix[mystates[4]] = {}  # nonreward state(terminal)
#
#     myrewards_matrix = dict()
#     myrewards_matrix[mystates[0]] = {  # first state
#         myactions[0]: {mystates[0]: 0, mystates[1]: 0, mystates[2]: 0, mystates[3]: 1, mystates[4]: 0},  # left action
#         myactions[1]: {mystates[0]: 0, mystates[1]: 0, mystates[2]: 0, mystates[3]: 1, mystates[4]: 0}  # right action
#     }
#     myrewards_matrix[mystates[1]] = {  # left state
#         myactions[0]: {mystates[0]: 0, mystates[1]: 0, mystates[2]: 0, mystates[3]: 1, mystates[4]: 0},  # left action
#         myactions[1]: {mystates[0]: 0, mystates[1]: 0, mystates[2]: 0, mystates[3]: 1, mystates[4]: 0}  # right action
#     }
#     myrewards_matrix[mystates[2]] = {  # right state
#         myactions[0]: {mystates[0]: 0, mystates[1]: 0, mystates[2]: 0, mystates[3]: 1, mystates[4]: 0},  # left action
#         myactions[1]: {mystates[0]: 0, mystates[1]: 0, mystates[2]: 0, mystates[3]: 1, mystates[4]: 0}  # right action
#     }
#     # these 2 have no use
#     myrewards_matrix[mystates[3]] = {}  # reward state(terminal)
#     myrewards_matrix[mystates[4]] = {}  # nonreward state(terminal)
#
#     model = ReferenceModel(states=mystates, actions=myactions,
#                            initial_states=myinitial_states, terminal_states=myterminal_states,
#                            rewards=myrewards_matrix, transitions=mytransitions_matrix)
#     pl = model.start_new_session()
#     s = pl.next()[0]
#     print s.desc
#     pl.next()
#     res = pl.send(myactions[0])
#     print res[0].desc, res[1]
#     pl.next()
#     res = pl.send(myactions[0])
#     print res[0].desc, res[1]
