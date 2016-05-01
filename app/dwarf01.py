from psychopy import core, event, visual
from model.daw import DawAction, DawState, DawModel

import numpy as np


class DawApp(object):
    """
    simplest task
    """
    def __init__(self, model):
        self.model = model
        self.fixed_stim = None
        self.clock = core.Clock()

    def start_expriment(self, rounds, **kwargs):
        round_num = 1
        history = []
        window = visual.Window(kwargs.get('screen_size', [1366, 768]),
                               color='Black',
                               monitor="testMonitor",
                               units="deg",
                               fullscr=kwargs.get('full_screen', True))
        self.fixed_stim = visual.Circle(win=window, fillColor='White', radius=.5, pos=(0, 0))

        self.show_message_page(window, "Press any key to start.", block=True)
        while round_num <= rounds:
            status, hist = self.start_new_round(window)

            if status == -1:  # quit
                break
            elif status == 0:  # timeout
                self.show_timeout_message(window)
            elif status == 1:  # ok
                pass

            history.append(hist)
            round_num += 1

        window.close()
        return history

    def start_new_round(self, window, **kwargs):
        # log format: [state 0, response time 1, action 1, state 1 , reward 1,
        #              response time 2, action 2, state 2, reward 2, exit status]
        history = {'type': 'trial', 'states': [], 'actions': [], 'response_times': [], 'rewards': []}

        session = self.model.start_new_session()
        state = session.next()
        history['states'].append(state)

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
                    self.draw_fixed_stim()
                    window.update()

                    self.clock.reset()
                    pressed_keys = event.waitKeys(kwargs.get('action_timeout', 1), actions)
                    history['response_times'].append(self.clock.getTime())
                    pressed_keys = [] if pressed_keys is None else pressed_keys
                    event.clearEvents()

                    a = None
                    if 'q' in pressed_keys:
                        history['exit_status'] = 'quit'
                        return -1, history
                    else:
                        for pressed in pressed_keys:
                            if actions.get(pressed, None) is not None:
                                a = actions[pressed]
                                break
                        if a is None:
                            history['exit_status'] = 'timeout'
                            return 0, history

                    if last_action_image is None:
                        last_action_image = imgs[a.index]
                        imgs.remove(last_action_image)
                        self.show_actions_transition(window, imgs, last_action_image, (-5+a.index*10, 0), (0, 6))

                    session.next()
                    state, reward = session.send(a)

                    history['actions'].append(a)
                    history['states'].append(state)
                    history['rewards'].append(reward)

                    actions = {'q': -1}
                    actions.update(self.model.get_legal_actions(state))
                else:
                    self.show_reward_transition(window, [],
                                                self.model.reward_path if reward > 0 else self.model.lost_path,
                                                imgs[a.index], (-5+a.index*10, 0), (0, 6), cycles=40, duration=1)
                    # self.show_reward_transition(window, imgs+[last_action_image],
                    #                             self.model.reward_path if reward > 0 else self.model.lost_path)
                    session.next()
            except StopIteration:
                history['exit_status'] = 'normal'
                return 1, history

    def draw_fixed_stim(self):
            self.fixed_stim.draw()

    def show_message_page(self, window, message, duration=2, block=False, release_key=None):
        visual.TextStim(win=window, text=message, pos=(0, 0), color='White').draw()
        window.update()

        if block:
            event.waitKeys(keyList=None if release_key is None else [release_key])
        else:
            core.wait(duration)

    def show_timeout_message(self, window):
        self.show_message_page(window, "U have 1 second to select an action!", duration=2)

    def show_actions_transition(self, window, stims, target_stim, start_point, end_point, cycles=30):
        counter = 0
        delta = tuple(np.subtract(end_point, start_point) / float(cycles))

        while counter < cycles:
            self.draw_fixed_stim()
            for stim in stims:
                stim.draw()
            target_stim.pos += delta
            target_stim.draw()
            window.update()

            counter += 1

    def show_reward_transition(self, window, stims, image_path, target_stim,
                               start_point, end_point, cycles=30, duration=1):
        counter = 0
        delta = tuple(np.subtract(end_point, start_point) / float(cycles))

        while counter < cycles:
            self.draw_fixed_stim()
            for stim in stims:
                stim.draw()
            target_stim.pos += delta
            target_stim.draw()
            window.update()

            counter += 1

        self.draw_fixed_stim()
        target_stim.draw()
        for stim in stims:
            stim.draw()
        visual.ImageStim(win=window, image=image_path, pos=(0, -5), size=3).draw()
        window.update()
        core.wait(duration)

    @staticmethod
    def quit():
        core.quit()

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

    app = DawApp(model=daw_model)
    myhistory = app.start_expriment(5)
    print myhistory
    app.save_logs(myhistory, "this is a test for logging in simple task")

    app.quit()
