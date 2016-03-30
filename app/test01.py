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
DATA_PATH = "../data/test01"

# create a window WTF testMonitor is
w01 = visual.Window(screen_size, monitor="testMonitor", units="deg", fullscr=True)
m = Model(max_turns)

# start stimuli and update the window
rewards = 0
reward_img = visual.ImageStim(win=w01, image=DATA_PATH+"/reward.jpg".format(m.state), pos=[0, -6], size=2)
last_img = None
while m.remained_turns() > 0:
    if m.state == 0:
        last_img = None

    # update gui
    state_imgs = [visual.ImageStim(win=w01, image=DATA_PATH+"/{0}-1.jpg".format(m.state), pos=[-5, -2], size=5),
                  visual.ImageStim(win=w01, image=DATA_PATH+"/{0}-2.jpg".format(m.state), pos=[5, -2], size=5)]
    reward_res = visual.TextStim(win=w01, text="cumulative reward: {0}".format(rewards), pos=[-5, 8], color='Black')
    turn_res = visual.TextStim(win=w01, text="turn number: {0}".format(m.turn), pos=[-6, 9], color='Black')
    for img in state_imgs:
        img.draw()
    if last_img is not None:
        last_img.draw()
    reward_res.draw()
    turn_res.draw()
    w01.update()

    pressed_keys = event.waitKeys(2, ['right', 'left', 'q'])
    pressed_keys = [] if pressed_keys is None else pressed_keys

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
    if m.state == 0:
        last_img = state_imgs[0] if a == Model.LEFT else state_imgs[1]
        last_img.setPos([0, 4])

    s, r = m.perform_action(a)
    rewards += r

    # show reward taken
    if r > 0:
        reward_res = visual.TextStim(win=w01, text="cumulative reward: {0}".format(rewards), pos=[-5, 8], color='Black')
        for img in state_imgs:
            img.draw()
        last_img.draw()
        reward_img.draw()
        reward_res.draw()
        turn_res.draw()
        w01.update()
        core.wait(1)

print "rewards: {0}".format(rewards)

w01.close()
core.quit()
