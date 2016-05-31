import random

from model.daw2 import DawAction, DawState, DawModel2


class ReferenceAgent(object):
    def __init__(self, model, query_round=10):
        self.model = model
        self.query_round = query_round

    def start(self, rounds):
        round_num = 1
        history = []

        while round_num <= rounds:
            status, hist = self.start_new_round()

            if status == -1:  # quit
                break
            elif status == 0:  # timeout
                pass
            elif status == 1:  # ok
                pass
            history.append(hist)

            if round_num % self.query_round == 0:
                # pass
                hist2 = self.calculate_best_image()
                history.append(hist2)
                hist2 = self.calculate_confidence(1)
                history.append(hist2)

            round_num += 1

        return history

    def start_new_round(self):
        history = {'type': 'trial', 'states': [], 'actions': [], 'response_times': [], 'rewards': []}

        session = self.model.start_new_session()
        state = session.next()
        history['states'].append(state)

        actions = {}
        actions.update(self.model.get_legal_actions(state))

        while True:
            try:
                if state not in self.model.terminal_states:
                    a = actions[random.randint(0, len(actions)-1)]

                    session.next()
                    state, reward = session.send(a)

                    history['actions'].append(a)
                    history['states'].append(state)
                    history['rewards'].append(reward)

                    actions = {}
                    actions.update(self.model.get_legal_actions(state))
                else:
                    session.next()
            except StopIteration:
                history['exit_status'] = 'normal'
                return 1, history

    def calculate_best_image(self):
        return {'answer': '3', 'type': 'best image', 'response_time': 1.5133471488952637}
        # pass

    def calculate_confidence(self, best, discretization=6):
        return {'answer': '3', 'type': 'confidence', 'response_time': 0.1643660068511963}
        # pass

    def save_logs(self, logs, description="No description."):
        from datetime import datetime
        from pickle import dump

        now = datetime.now()
        log_file = open('../log/agent-log@'+now.strftime("%Y-%m-%d %H:%M"), 'w')
        dump((description, self.model, logs), log_file)
        log_file.close()


if __name__ == '__main__':
    myactions = [DawAction(name='left', key=0, index=0), DawAction(name='right', key=1, index=1)]
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
    # these 2 have no usage
    myrewards_matrix[mystates[3]] = {}  # reward state(terminal)
    myrewards_matrix[mystates[4]] = {}  # nonreward state(terminal)

    query_round = 100

    daw_model = DawModel2(states=mystates, actions=myactions,
                          initial_states=myinitial_states, terminal_states=myterminal_states,
                          rewards=myrewards_matrix, transitions=mytransitions_matrix,
                          reward_image_path='../data/test01/reward.png',
                          lost_image_path='../data/test01/lost.png',
                          update_round=query_round,
                          initial_rewards=(.3, .3, .3, .8))

    ag = ReferenceAgent(model=daw_model, query_round=query_round)
    myhistory = ag.start(100)
    # print myhistory
    ag.save_logs(myhistory, "test agent")
