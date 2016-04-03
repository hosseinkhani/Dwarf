
class DawApp(object):
    def __init__(self, model):
        self.model = model

    def start_expriment(self, rounds):
        round_num = 1
        cumulative_reward = 0
        history = []

        while round_num <= rounds:
            res = self.start_one_round()
            cumulative_reward += res[1]
            history.extend(res[0])

            round_num += 1

    def start_one_round(self):
        rewards = 0
        history = []

        session = self.model.start_new_session()
        while True:
            try:
                session.next()
                res = session.send(0)  # TODO
                print res[0].desc, res[1]
            except StopIteration:
                return history, rewards
