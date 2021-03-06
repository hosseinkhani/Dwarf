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
            return 'b'
        if label == '1':
            return 'g'
        if label == '2':
            return 'r'
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

    def draw_bar(self, ax, mu, sigma, ind, label=None, width=.3):
        sigma = math.sqrt(sigma)

        if label is None:
            return ax.bar(ind, mu, width, yerr=sigma)
        else:
            return ax.bar(ind, mu, width, yerr=sigma,
                          color=self.label_to_color(label), label=label, ecolor='k')


        # add some text for labels, title and axes ticks
        # ax.set_ylabel('Scores')
        # ax.set_title('Scores by group and gender')
        # ax.set_xticks(ind + width)
        # ax.set_xticklabels(('G1', 'G2', 'G3', 'G4', 'G5'))

        # for rect in rects1:
        # height = rect.get_height()
        # ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
        #         '%d' % int(height),
        #         ha='center', va='bottom')

    def draw_legend(self, ax, plots, loc=3):
        l = ax.legend(handles=plots, loc=loc)
        l.draggable(state=True)

    def write_selected(self, ax, num, confidence):
        ax.set_title('{num} selected with confidence {confidence}'.format(num=num, confidence=confidence))

    def draw_results(self, qs, best, confidence, real_mu):
        fig = plt.figure()
        fig.suptitle("best action index is {real_best}".format(real_best=real_mu.index(max(real_mu))))
        ax = fig.add_subplot(111)
        ax.grid(True)

        # self.draw_gaussian(ax, best, 1.0/(10*confidence))
        plots = []

        for i in range(4):
            if len(qs[i]) == 0:
                continue

            mu = sum(qs[i]) / float(len(qs[i]))
            sigma = sum([((d-real_mu[i])**2)/(len(qs[i])**2) for d in qs[i]])
            # sigma = sum([((d-mu)**2)/((len(qs[i]))**.5) for d in qs[i]])

            print 'mu: ', mu, 'sigma: ', sigma

            # plots.append(self.draw_gaussian(ax, mu, sigma, str(i)))
            plots.append(self.draw_bar(ax, mu, sigma, i, str(i)))
        self.write_selected(ax, best, confidence)
        self.draw_legend(ax, plots)

        plt.draw()

        self.fig_num += 1

    def show_qvalues_confidence(self):
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
                print 'qvalues', qs

                miner.draw_results(qs, best, int(hist['answer']), miner.log_model.rewards_history[c])

                # raw_input("next?")
                c += 1
                best = -1
                qs = [[] for i in range(4)]
            elif hist['type'] == 'best image':
                print '#'*10, 'figure:', c+1
                best = int(hist['answer'])-1
                print 'best', best


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

    # miner = SimpleMiner('agent-log@2016-06-01 16:43')
    miner = SimpleMiner('agent-log@2016-06-01 16:52')
    print miner.log_description
    # print miner.log_data
    print len(miner.log_model.rewards_history), miner.log_model.rewards_history
    miner.show_qvalues_confidence()

    # exit: exit button for each window
    plt.ioff()
    plt.show()

    # exit: all windows by pressing enter
    # raw_input("press enter to exit all windows?")
