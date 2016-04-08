from psychopy import core, event, visual
from model.daw import DawAction, DawState, DawModel


class DawApp(object):
    def __init__(self, model):
        self.model = model

    def start_expriment(self, rounds, **kwargs):
        round_num = 1
        history = []
        window = visual.Window(kwargs.get('screen_size', [800, 600]),#[1366, 768]),
                               monitor="testMonitor",
                               units="deg",
                               fullscr=False)

        while round_num <= rounds:
            history.append("start round {0}".format(round_num))
            status, hist = self.start_new_round(window)

            if status == -1:  # quit
                history.extend(hist)
                history.append('quit')
                break
            elif status == 0:  # timeout
                self.show_timeout_message(window)
                history.extend(hist)
                history.append('time out')
            elif status == 1:  # ok
                history.extend(hist)
                history.append('finish')

            round_num += 1

        window.close()
        return history

    def start_new_round(self, window):
        history = []

        session = self.model.start_new_session()
        state = session.next()
        actions = {'q': -1}
        actions.update(self.model.get_legal_actions(state))

        while True:
            try:
                history.append(state.desc)

                if state not in self.model.terminal_states:
                    imgs = []
                    for i in xrange(len(state.images)):
                        imgs.append(visual.ImageStim(win=window, image=state.images[i], pos=[-5+i*10, -2], size=5))
                        imgs[i].draw()
                    window.update()

                    pressed_keys = event.waitKeys(2, actions)
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

                    session.next()
                    state, reward = session.send(a)

                    history.append(a.name)
                    history.append(reward)

                    actions = {'q': -1}
                    actions.update(self.model.get_legal_actions(state))

                    print state.desc, reward
                else:
                    session.next()
            except StopIteration:
                return 1, history

    @staticmethod
    def show_timeout_message(window):
        visual.TextStim(win=window, text="U have 1 second to select an action!", pos=[0, 0], color='Black').draw()
        window.update()
        core.wait(2)

    @staticmethod
    def quit():
        core.quit()


if __name__ == '__main__':
    myactions = [DawAction(name='left', key='left'), DawAction(name='right', key='right')]
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
                     reward_image_path='../data/test01/2-1.jpg')

    app = DawApp(model=daw_model)
    print app.start_expriment(3)
    app.quit()

