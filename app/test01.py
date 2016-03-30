from psychopy import visual, core, event

# TODO: read config file
# init variables
screen_size = [1366, 768]
max_turns = 10


# create a window WTF testMonitor is
w01 = visual.Window(screen_size, monitor="testMonitor", units="deg", fullscr=True)

# create some stimuli
# grating = visual.GratingStim(win=w01, mask='circle', size=3, pos=[-4, 0], sf=3)
# fixation = visual.GratingStim(win=w01, size=0.2, pos=[0, 0], sf=0, rgb=-1)

img11 = visual.ImageStim(win=w01, image="../pics/1-1.jpg", pos=[-10, -5], size=5)
img12 = visual.ImageStim(win=w01, image="../pics/1-2.jpg", pos=[-10, 5], size=5)
img21 = visual.ImageStim(win=w01, image="../pics/2-1.jpg", pos=[0, -5], size=5)
img22 = visual.ImageStim(win=w01, image="../pics/2-2.jpg", pos=[0, 5], size=5)
img31 = visual.ImageStim(win=w01, image="../pics/3-1.jpg", pos=[10, -5], size=5)
img32 = visual.ImageStim(win=w01, image="../pics/3-2.jpg", pos=[10, 5], size=5)

# start stimuli and update the window
state = 1
turn = 0
while turn < max_turns:
    state_imgs = [visual.ImageStim(win=w01, image="../pics/{0}-1.jpg".format(state), pos=[-5, -12 + state * 6], size=5),
                  visual.ImageStim(win=w01, image="../pics/{0}-2.jpg".format(state), pos=[5, -12 + state * 6], size=5)]
    if state == 1:
        state = 2
    elif state == 2:
        state = 3
    elif state == 3:
        state = 1
        turn += 1
    elif state == -1:  # reward phase
        pass

    # updates
    for img in state_imgs:
        img.draw()
    w01.update()

    if len(event.getKeys()) > 0:
        break
    event.clearEvents()

    core.wait(1)

w01.close()
core.quit()
