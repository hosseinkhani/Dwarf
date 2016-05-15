from pickle import load
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import math



class SimpleMiner(object):
    """
    simple log manipulation
    no manipulate yet
    """

    def __init__(self, file_name):
        self.log_description, self.log_model, self.log_data = load(open('../log/'+file_name, 'r'))
        self.fig_num = 1

        plt.ion()
        plt.show()

    def label_to_color(self, label):
        """
        b : blue.
        g : green.
        r : red.
        c : cyan.
        m : magenta.
        y : yellow.
        k : black.
        w : white.
        """
        if label == '0':
            return 'breen'
        if label == '1':
            return 'glue'
        if label == '2':
            return 'red'
        if label == '3':
            return 'c'

    def draw_gaussian(self, ax, mu, sigma, label=None):
        # fig = plt.figure()
        # fig.suptitle(title)
        # ax = fig.add_subplot(111)

        sigma = math.sqrt(sigma)
        x = np.linspace(mu-3, mu+3, 100)

        if label is None:
            return ax.plot(x, mlab.normpdf(x, mu, sigma))[0]
        else:
            return ax.plot(x, mlab.normpdf(x, mu, sigma), c=self.label_to_color(label), label=label)[0]

    def draw_legend(self, ax, plots, loc=3):
        ax.legend(handles=plots, loc=loc)

    def write_selected(self, ax, num, confidence):
        ax.set_title('{num} selected with confidence {confidence}'.format(num=num, confidence=confidence))

    def draw_results(self, qs, best, confidence, real_mu):
        fig = plt.figure()
        fig.suptitle(str(real_mu.index(.7)))
        ax = fig.add_subplot(111)

        # self.draw_gaussian(ax, best, 1.0/(10*confidence))
        plots = []

        for i in range(4):
            if len(qs[i]) == 0:
                continue

            mu = sum(qs[i]) / float(len(qs[i]))
            sigma = sum([((d-real_mu[i])**2)/((len(qs[i]))**.5) for d in qs[i]])

            print mu, sigma

            plots.append(self.draw_gaussian(ax, mu, sigma))
        self.write_selected(ax, best, confidence)
        self.draw_legend(ax, plots)

        plt.draw()

        self.fig_num += 1

    def show_q_confidence(self):
        c = 0
        best = -1
        qs = [[] for i in range(4)]
        for hist in miner.log_data:
            if hist['type'] == 'trial':
                if hist['exit_status'] != 'normal':
                    continue

                which = 0 if hist['states'][1] == miner.log_model.states[1] else 2
                which += 1 if hist['actions'][1] == miner.log_model.actions[1] else 0
                qs[which].append(hist['rewards'][1])
            elif hist['type'] == 'confidence':
                print 'confidence', hist['answer']
                print qs

                miner.draw_results(qs, best, int(hist['answer']), miner.log_model.rewards_history[c])

                # raw_input("next?")
                c += 1
                best = -1
                qs = [[] for i in range(4)]
            elif hist['type'] == 'best image':
                print 'best', hist['answer']
                best = int(hist['answer'])-1


if __name__ == '__main__':
    """
    0 im first state
    1 im left state
    2 im right state
    3 im reward state
    4 im nonreward state
    #########################
    0 left action
    1 right action
    """

    miner = SimpleMiner('log@2016-05-01 10:15')
    # miner.draw_gaussian(3, 1, 'test')
    print miner.log_description
    # print miner.log_data
    # print len(miner.log_model.rewards_history)
    miner.show_q_confidence()

    raw_input("exit?")
