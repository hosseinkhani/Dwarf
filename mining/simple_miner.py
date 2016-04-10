from pickle import load
import numpy as np


class SimpleMiner(object):
    def __init__(self, file_name):
        self.log_description, self.log_model, self.log_data = load(open('../log/'+file_name, 'r'))
        self._reformat_log_data()

    def _reformat_log_data(self):
        """
        convert raw logs to useful format
        """

        new = []

        last_trial = self.log_data[0]
        for i in xrange(1, len(self.log_data)):
            this_trial = self.log_data[i]
            new.append([this_trial[1].index,
                        this_trial[3].desc,
                        this_trial[4].index,
                        this_trial[5],
                        this_trial[6].desc,
                        True if this_trial[1] == last_trial[1] else False])
            last_trial = this_trial

        self.log_data = new


if __name__ == '__main__':
    miner = SimpleMiner('log@2016-04-10 14:18')
    print miner.log_description, miner.log_data