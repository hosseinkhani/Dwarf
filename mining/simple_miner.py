from pickle import load
import numpy as np


class SimpleMiner(object):
    """
    simple log manipulation
    no manipulate yet
    """

    def __init__(self, file_name):
        self.log_description, self.log_model, self.log_data = load(open('../log/'+file_name, 'r'))

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
    print miner.log_description
    print miner.log_data
    print miner.log_model.rewards_history
