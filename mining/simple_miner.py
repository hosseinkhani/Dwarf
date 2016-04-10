from pickle import load
import numpy as np


class SimpleMiner(object):
    def __init__(self, file_name):
        self.log_description, self.log_model, self.log_data = load(open('../log/'+file_name, 'r'))
        self._reformat_log_data()

    def _reformat_log_data(self):
        """
        example of converting raw logs to useful format for mining
        raw format: [state 0, action 1, state 1, reward 1, action 2, state 2, reward 2, exit status]
        new format: [action 1, action 2, state 1, reward, common transition or not, stay or not]
        """
        #
        ind = 0
        while self.log_data[ind][-1] != 'normal':  # skip useless trials
            ind += 1
        last_trial = self.log_data[ind]
        ind += 1

        new_data = []
        while ind < len(self.log_data):
            if self.log_data[ind][-1] == 'normal':  # normal trial
                this_trial = self.log_data[ind]
                new_data.append([this_trial[1].index,
                                 this_trial[4].index,
                                 this_trial[2].desc,
                                 this_trial[6],
                                 self.log_model.is_transition_common(this_trial[0], this_trial[1], this_trial[2]),
                                 True if this_trial[1] == last_trial[1] else False])

                last_trial = this_trial
            else:  # uncompleted trials
                pass
            ind += 1

        self.log_data = new_data


if __name__ == '__main__':
    """
    0 im first one
    1 im left one
    2 im right one
    3 im reward state
    4 im nonreward state
    0 left
    1 right
    """

    miner = SimpleMiner('log@2016-04-10 18:28')
    print miner.log_description
    print miner.log_data