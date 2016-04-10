from psychopy import core, event, visual
from model.daw import DawAction, DawState, DawModel

import numpy as np


class DawApp(object):
    def __init__(self, model, fixed_point_path=None):
        self.model = model

        if fixed_point_path is not None:
            self.fixed_point_path = fixed_point_path

    def start_expriment(self, rounds, **kwargs):
        round_num = 1
        history = []
        window = visual.Window(kwargs.get('screen_size', [800, 600]),#[1366, 768]),
                               color='Black',
                               monitor="testMonitor",
                               units="deg",
                               fullscr=False)

        DawApp.show_message_page(window, "Press any key to start.", block=True, release_key=None)
        while round_num <= rounds:
            status, hist = self.start_new_round(window)

            if status == -1:  # quit
                hist += ['quit']
                break
            elif status == 0:  # timeout
                hist += ['timeout']
                self.show_timeout_message(window)
            elif status == 1:  # ok
                hist += ['normal']

            history.append(hist)
            round_num += 1

        window.close()
        return history

    def start_new_round(self, window):
        fixed_stim = visual.ImageStim(win=window, image=self.fixed_point_path, pos=(0, 0), size=1) \
            if self.fixed_point_path is not None else None
        history = []
        clock = core.Clock()

        session = self.model.start_new_session()
        state = session.next()
        history.append(state)

        actions = {'q': -1}
        actions.update(self.model.get_legal_actions(state))

        last_action_image = None

        while True:
            try:
                if state not in self.model.terminal_states:
                    imgs = []
                    for i in xrange(len(state.images)):
                        imgs.append(visual.ImageStim(win=window, image=state.images[i], pos=(-5+i*10, 0), size=5))
                        imgs[i].draw()
                    if last_action_image is not None:
                        # last_action_image.pos = (0, 4)
                        last_action_image.draw()
                    if fixed_stim is not None:
                        fixed_stim.draw()
                    window.update()

                    clock.reset()
                    pressed_keys = event.waitKeys(2, actions)
                    history.append(clock.getTime())
                    pressed_keys = [] if pressed_keys is None else pressed_keys
                    event.clearEvents()

                    a = None
                    if 'q' in pressed_keys:
                        return -1, history
                    else:
                        for pressed in pressed_keys:
                            if actions.get(pressed, None) is not None:
                                a = actions[pressed]
                                break
                        if a is None:
                            return 0, history

                    if last_action_image is None:
                        last_action_image = imgs[a.index]
                        imgs.remove(last_action_image)
                        self.show_actions_transition(window, imgs+[fixed_stim],
                                                     last_action_image, (-5+a.index*10, 0), (0, 6))

                    session.next()
                    state, reward = session.send(a)

                    history.append(a)
                    history.append(state)
                    history.append(reward)

                    actions = {'q': -1}
                    actions.update(self.model.get_legal_actions(state))
                else:
                    self.show_reward_transition(window, imgs+[last_action_image]+[fixed_stim],
                                                self.model.reward_path if reward > 0 else self.model.lost_path)
                    session.next()
            except StopIteration:
                return 1, history

    @staticmethod
    def show_message_page(window, message, duration=2, block=False, release_key='space'):
        visual.TextStim(win=window, text=message, pos=[0, 0], color='White').draw()
        window.update()

        if block:
            event.waitKeys(keyList=None if release_key is None else [release_key])
        else:
            core.wait(duration)

    @staticmethod
    def show_timeout_message(window):
        DawApp.show_message_page(window, "U have 1 second to select an action!", duration=2)

    @staticmethod
    def show_actions_transition(window, stims, target_stim, start_point, end_point, cycles=40):
        counter = 0
        delta = tuple(np.subtract(end_point, start_point) / float(cycles))

        while counter < cycles:
            for stim in stims:
                stim.draw()
            target_stim.pos += delta
            target_stim.draw()
            window.update()

            counter += 1

    @staticmethod
    def show_reward_transition(window, stims, image_path):
        for stim in stims:
            stim.draw()
        visual.ImageStim(win=window, image=image_path, pos=(0, -5), size=3).draw()
        window.update()
        core.wait(1)

    @staticmethod
    def quit():
        core.quit()

    @staticmethod
    def format_history(history):
        return history

    def save_logs(self, logs, description="No description."):
        from datetime import datetime
        from pickle import dump

        now = datetime.now()
        log_file = open('../log/log@'+now.strftime("%Y-%m-%d %H:%M"), 'w')
        dump((description, self.model, logs), log_file)
        log_file.close()


if __name__ == '__main__':
    myactions = [DawAction(name='left', key='left', index=0), DawAction(name='right', key='right', index=1)]
    mystates = [DawState('../data/test01/0-1.jpg', '../data/test01/0-2.jpg', desc='im first one'),
                DawState('../data/test01/1-1.jpg', '../data/test01/1-2.jpg', desc='im left one'),
                DawState('../data/test01/2-1.jpg', '../data/test01/2-2.jpg', desc='im right one'),
                DawState(desc='im reward state'),
                DawState(desc='im nonreward state')]

    myinitial_states = {mystates[0]}

    myterminal_states = {mystates[3], mystates[4]}

    mytransitions_matrix = dict()
    mytransitions_matrix[mystates[0]] = {  # first state
        myactions[0]: {mystates[0]: 0, mystates[1]: .7, mystates[2]: .3, mystates[3]: 0, mystates[4]: 0},  # left action
        myactions[1]: {mystates[0]: 0, mystates[1]: .3, mystates[2]: .7, mystates[3]: 0, mystates[4]: 0}  # right action
    }
    mytransitions_matrix[mystates[1]] = {  # left state
        myactions[0]: {mystates[0]: 0, mystates[1]: 0, mystates[2]: 0, mystates[3]: .6, mystates[4]: .4},  # left action
        myactions[1]: {mystates[0]: 0, mystates[1]: 0, mystates[2]: 0, mystates[3]: .1, mystates[4]: .9}  # right action
    }
    mytransitions_matrix[mystates[2]] = {  # right state
        myactions[0]: {mystates[0]: 0, mystates[1]: 0, mystates[2]: 0, mystates[3]: .2, mystates[4]: .8},  # left action
        myactions[1]: {mystates[0]: 0, mystates[1]: 0, mystates[2]: 0, mystates[3]: .4, mystates[4]: .6}  # right action
    }
    # these 2 have no use
    mytransitions_matrix[mystates[3]] = {}  # reward state(terminal)
    mytransitions_matrix[mystates[4]] = {}  # nonreward state(terminal)

    myrewards_matrix = dict()
    myrewards_matrix[mystates[0]] = {  # first state
        myactions[0]: {mystates[0]: 0, mystates[1]: 0, mystates[2]: 0, mystates[3]: 1, mystates[4]: 0},  # left action
        myactions[1]: {mystates[0]: 0, mystates[1]: 0, mystates[2]: 0, mystates[3]: 1, mystates[4]: 0}  # right action
    }
    myrewards_matrix[mystates[1]] = {  # left state
        myactions[0]: {mystates[0]: 0, mystates[1]: 0, mystates[2]: 0, mystates[3]: 1, mystates[4]: 0},  # left action
        myactions[1]: {mystates[0]: 0, mystates[1]: 0, mystates[2]: 0, mystates[3]: 1, mystates[4]: 0}  # right action
    }
    myrewards_matrix[mystates[2]] = {  # right state
        myactions[0]: {mystates[0]: 0, mystates[1]: 0, mystates[2]: 0, mystates[3]: 1, mystates[4]: 0},  # left action
        myactions[1]: {mystates[0]: 0, mystates[1]: 0, mystates[2]: 0, mystates[3]: 1, mystates[4]: 0}  # right action
    }
    # these 2 have no use
    myrewards_matrix[mystates[3]] = {}  # reward state(terminal)
    myrewards_matrix[mystates[4]] = {}  # nonreward state(terminal)

    daw_model = DawModel(states=mystates, actions=myactions,
                         initial_states=myinitial_states, terminal_states=myterminal_states,
                         rewards=myrewards_matrix, transitions=mytransitions_matrix,
                         reward_image_path='../data/test01/reward.png',
                         lost_image_path='../data/test01/lost.png')

    app = DawApp(model=daw_model, fixed_point_path='../data/test01/fixed.png')
    history = app.start_expriment(5)
    for h in history:
        print h
    app.save_logs(history, "this is a test for logging")

    app.quit()
