from psychopy import core, event, visual
from model.daw import DawAction, DawState, DawModel
from dwarf01 import DawApp


class DawApp2(DawApp):
    """
    DawApp task + best image choice
    """
    def __init__(self, model, query_round=2, fixed_point_path=None):
        DawApp.__init__(self, model, fixed_point_path)
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
                               fullscr=True)

        self.fixed_stim = visual.ImageStim(win=window, image=self.fixed_point_path, pos=(0, 0), size=1) \
            if self.fixed_point_path is not None else None
        self.show_message_page(window, "Press any key to start.", block=True, release_key=None)
        while round_num <= rounds:
            status, hist = self.start_new_round(window)

            if round_num % self.query_round == 0:
                hist2 = self.show_best_image_page(window, reward_images)
                history.append(hist2)

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

    def show_best_image_page(self, window, imgs_path):
        history = {'type': 'best image'}

        visual.TextStim(win=window, text="which one is better?", pos=(0, 4), color='White').draw()
        for i in xrange(len(imgs_path)):
            visual.ImageStim(win=window, image=imgs_path[i], pos=(-12+i*8, 0), size=5).draw()
            visual.TextStim(win=window, text=str(i), pos=(-12+i*8, -3), color='White').draw()
        window.update()

        self.clock.reset()
        keys = event.waitKeys(keyList=[str(i) for i in range(len(imgs_path))])
        history['response_time'] = self.clock.getTime()
        history['answer'] = keys[0]

        return history


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

    app = DawApp2(model=daw_model, query_round=2, fixed_point_path='../data/test01/fixed.png')
    myhistory = app.start_expriment(5)
    print myhistory
    app.save_logs(myhistory, "dawapp2 log sample")

    app.quit()
