from refrence import ReferenceState, ReferenceAction, ReferenceModel
import random


class DawState(ReferenceState):
    def __init__(self, *images_path, **kwargs):
        ReferenceState.__init__(self, **kwargs)
        self.images = images_path

    def __repr__(self):
        if hasattr(self, 'desc'):
            return self.desc
        return ReferenceState.__repr__(self)


class DawAction(ReferenceAction):
    def __init__(self, name, key, index, **kwargs):
        ReferenceAction.__init__(self, **kwargs)
        self.name = name
        self.key = key
        self.index = index

    def __repr__(self):
        return self.name


class DawModel(ReferenceModel):
    def __init__(self, transitions, rewards, actions, states, initial_states, terminal_states=None,
                 reward_image_path=None, lost_image_path=None):
        ReferenceModel.__init__(self, transitions, rewards, actions, states, initial_states, terminal_states)
        self.reward_path = reward_image_path
        self.lost_path = lost_image_path

    # def __repr__(self):
        # return self  # TODO better representation for docs maybe

    def get_legal_actions(self, state):
        return {action.key: action for action in self.transitions[state].keys()}

    def get_all_actions(self):
        return {action.key: action for action in self.actions}

    def is_transition_common(self, first_state, action, next_state):
        return next_state == max(self.transitions[first_state][action].iteritems(), key=lambda x: x[1])[0]

    def is_transition_rare(self, first_state, action, next_state):
        return not self.is_transition_common(first_state, action, next_state)