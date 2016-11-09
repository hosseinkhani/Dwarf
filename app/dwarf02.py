from psychopy import core, event, visual
from model.daw import DawAction, DawState, DawModel
from dwarf01 import DawApp

import numpy as np


class DawApp2(DawApp):
    """
    DawApp task + best image choice
    """
    def __init__(self, model, query_round=10):
        DawApp.__init__(self, model)
        self.query_round = query_round

    def start_expriment(self, rounds, **kwargs):
        tmp_states = set(self.model.initial_states)
        tmp_states.update(set(self.model.terminal_states))
        intermediate_states = [s for s in self.model.states if s not in tmp_states]
        reward_images = [path for state in intermediate_states for path in state.images]
        del tmp_states, intermediate_states

        round_num = 1
        history = []

        window = visual.Window(kwargs.get('screen_size', [1366, 768]),
                               color='Black',
                               monitor="testMonitor",
                               units="deg",
                               fullscr=kwargs.get('full_screen', True))

        self.fixed_stim = visual.Circle(win=window, fillColor='White', radius=.3, pos=(0, 0))

        self.show_message_page(window, "Press any key to start.", block=True, release_key=None)
        while round_num <= rounds:
            status, hist = self.start_new_round(window, **kwargs)

            if status == -1:  # quit
                break
            elif status == 0:  # timeout
                self.show_timeout_message(window)
            elif status == 1:  # ok
                pass
            history.append(hist)

            if round_num % self.query_round == 0:
                print 'conf ---------------'
                hist2 = self.show_best_image_page(window, reward_images)
                history.append(hist2)
                hist2 = self.show_confidence_page(window, kwargs.get('discretization', 5))
                history.append(hist2)

            round_num += 1

        window.close()
        return history

    def show_best_image_page(self, window, imgs_path):
        history = {'type': 'best image'}

        visual.TextStim(win=window, text="which one is better?", pos=(0, 4), color='White').draw()
        for i in xrange(len(imgs_path)):
            visual.ImageStim(win=window, image=imgs_path[i], pos=(-12+i*8, 0), size=5).draw()
            visual.TextStim(win=window, text=str(i+1), pos=(-12+i*8, -3), color='White').draw()
        window.update()

        self.clock.reset()
        keys = event.waitKeys(keyList=[str(i+1) for i in range(len(imgs_path))])
        history['response_time'] = self.clock.getTime()
        history['answer'] = keys[0]

        return history

    def show_confidence_page(self, window, discretization=5):
        history = {'type': 'confidence'}

        visual.TextStim(win=window, text="choose one due to your confidence?", pos=(0, 4), color='White').draw()
        for i in xrange(discretization):
            visual.TextStim(win=window, text=str(i+1), pos=(-10+i*(float(20)/(discretization-1)), -3), color='White').draw()
        window.update()

        self.clock.reset()
        keys = event.waitKeys(keyList=[str(i+1) for i in range(discretization)])
        history['response_time'] = self.clock.getTime()
        history['answer'] = keys[0]

        return history


if __name__ == '__main__':
    myactions = [DawAction(name='left', key='lshift', index=0), DawAction(name='right', key='rshift', index=1)]
    mystates = [DawState('../data/test01/0-1.jpg', '../data/test01/0-2.jpg', desc='im first one', index=-1),
                DawState('../data/test01/1-1.jpg', '../data/test01/1-2.jpg', desc='im left one', index=0),
                DawState('../data/test01/2-1.jpg', '../data/test01/2-2.jpg', desc='im right one', index=2),
                DawState(desc='im final state', index=-1)]

    myinitial_states = {mystates[0]}

    myterminal_states = {mystates[3]}

    mytransitions_matrix = dict()
    mytransitions_matrix[mystates[0]] = {  # first state
        myactions[0]: {mystates[1]: .7, mystates[2]: .3},  # left action
        myactions[1]: {mystates[1]: .3, mystates[2]: .7}  # right action
    }
    mytransitions_matrix[mystates[1]] = {  # left state
        myactions[0]: {mystates[3]: 1.},  # left action
        myactions[1]: {mystates[3]: 1.}  # right action
    }
    mytransitions_matrix[mystates[2]] = {  # right state
        myactions[0]: {mystates[3]: 1.},  # left action
        myactions[1]: {mystates[3]: 1.}  # right action
    }
    # this has no use
    mytransitions_matrix[mystates[3]] = {}  # reward state(terminal)

    probs = np.random.uniform(size=4)

    def myrewards_function(**kwargs):
        if kwargs['current_state'].index == -1:
            return 0.

        reward = 1. if probs[kwargs['current_state'].index+kwargs['action'].index] > np.random.uniform() else 0.

        for i in range(4):
            p = .025 * np.random.randn()
            while probs[i]+p > .8 or probs[i]+p < .2:
                p = .025 * np.random.randn()
            probs[i] += p

        return reward

    query_round = 3

    daw_model = DawModel(states=mystates, actions=myactions,
                         initial_states=myinitial_states, terminal_states=myterminal_states,
                         rewards=myrewards_function, transitions=mytransitions_matrix,
                         reward_image_path='../data/test01/reward.png',
                         lost_image_path='../data/test01/lost.png')

    app = DawApp2(model=daw_model, query_round=query_round)

    # app.start_expriment(3*query_round, screen_size=[800, 600], full_screen=False)  # warm up
    # app.start_expriment(2*query_round, discretization=6)  # warm up

    # daw_model.rewards_history = []
    myhistory = app.start_expriment(3*query_round, discretization=6)
    print myhistory
    # app.save_logs(myhistory, "my log sample")

    app.quit()
