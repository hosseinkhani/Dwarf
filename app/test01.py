from psychopy import visual, core, event
import numpy as np


class Model(object):
    LEFT = 0
    RIGHT = 1

    def __init__(self, max_turns):
        self.max_turns = max_turns
        self.turn = 0
        self.state = 0

    def perform_action(self, action):
        if self.state == 0:
            if action == self.LEFT:
                if np.random.uniform() > .7:
                    self.state = 1
                    return 1, 0
                else:
                    self.state = 2
                    return 2, 0
            elif action == self.RIGHT:
                if np.random.uniform() > .7:
                    self.state = 2
                    return 2, 0
                else:
                    self.state = 1
                    return 1, 0
        elif self.state == 1:
            self.turn += 1
            if action == self.LEFT and np.random.uniform() > .8:
                self.state = 0
                return 0, 1
            else:
                self.state = 0
                return 0, 0
        elif self.state == 2:
            self.turn += 1
            if action == self.LEFT and np.random.uniform() > .5:
                self.state = 0
                return 0, 1
            else:
                self.state = 0
                return 0, 0

    def remained_turns(self):
        return self.max_turns - self.turn


# TODO: read config file
# init variables
screen_size = [1366, 768]
max_turns = 10


# create a window WTF testMonitor is
w01 = visual.Window(screen_size, monitor="testMonitor", units="deg", fullscr=True)
m = Model(max_turns)

# start stimuli and update the window
rewards = 0
while m.remained_turns() > 0:
    # update gui
    state_imgs = [visual.ImageStim(win=w01, image="../pics/{0}-1.jpg".format(m.state), pos=[-5, 0], size=5),
                  visual.ImageStim(win=w01, image="../pics/{0}-2.jpg".format(m.state), pos=[5, 0], size=5)]
    for img in state_imgs:
        img.draw()
    w01.update()

    core.wait(1)

    pressed_keys = event.getKeys()
    # print pressed_keys
    if 'q' in pressed_keys:
        break
    event.clearEvents()

    if 'left' in pressed_keys:
        a = Model.LEFT
    elif 'right' in pressed_keys:
        a = Model.RIGHT
    else:
        print 'No input, default to right!'
        a = Model.RIGHT
    s, r = m.perform_action(a)
    rewards += r
print "rewards: {0}".format(rewards)

w01.close()
core.quit()
