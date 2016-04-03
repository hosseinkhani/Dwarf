from refrence import ReferenceState, ReferenceAction, ReferenceModel


class DawState(ReferenceState):
    def __init__(self, *images_path, **kwargs):
        ReferenceState.__init__(self, **kwargs)
        self.images = images_path


class DawAction(ReferenceAction):
    def __init__(self, name, **kwargs):
        ReferenceAction.__init__(self, **kwargs)
        self.name = name

    def __repr__(self):
        return self.name


class DawModel(ReferenceModel):
    def __init__(self, transitions, rewards, actions, states, initial_states, terminal_states=None,
                 reward_image_path=None):
        ReferenceModel.__init__(self, transitions, rewards, actions, states, initial_states, terminal_states)
        self.reward_path = reward_image_path


if __name__ == '__main__':
    s = DawState('dic/sl', 'dic/sl', desc="salam")
    a = DawAction('salam')
    print a
