from psychopy.iohub import launchHubServer
from psychopy.core import getTime, wait
from psychopy import visual

win = visual.Window(size=(1280, 720),pos=(0,0),allowGUI=True, monitor='testMonitor', units='pix', screen=0, color=(-0.2, -0.2, -0.2), fullscr=True, colorSpace='rgb')

# A Textbox stim that uses more of the supported graphical features
#
textboxloaded=visual.TextBox(
    window=win,
    text='Starting Experiment',
    font_size=32,
    font_color=[1,1,1],
    border_color=[-1,-1,1], # draw a blue border around stim
    border_stroke_width=4, # border width of 4 pix.
    background_color=[-1,-1,-1], # fill the stim background
    grid_color=[1,-1,-1,0.5], # draw a red line around each
                              # possible letter area,
                              # 50% transparent
    grid_stroke_width=1,  # with a width of 1 pix
    textgrid_shape=[20,2],  # specify area of text box
                            # by the number of cols x
                            # number of rows of text to support
                            # instead of by a screen
                            # units width x height.
    pos=(0.0,.5),
    # If the text string length < num rows * num cols in
    # textgrid_shape, how should text be justified?
    #
    grid_horz_justification='center',
    grid_vert_justification='center')

color_one = 'red'
color_two = 'green'
# Positions of the rectanges.
pos_one = (-100, 0)
pos_two = (100, 0)

rect_one = visual.Rect(
    win=win,
    fillColor=color_one,
    lineColor=color_one, 
    size=100,
    pos=pos_one,
    opacity=1
    )
rect_two = visual.Rect(
    win=win,
    fillColor=color_two,
    lineColor=color_two, 
    size=100,
    pos=pos_two,
    opacity=1
    )


textboxloaded.draw()

ioDevice = 'eyetracker.hw.mouse.EyeTracker'
ioConfig = {ioDevice: {'name': 'tracker', 'device_number': 0}, 'window': win}
io = launchHubServer(**ioConfig)



win.flip()
# Get the eye tracker device.
tracker = io.devices.tracker
# Check for and print any eye tracker events received...
tracker.setRecordingState(True)





wait(1)
textboxloaded.setText("Trial starting")
textboxloaded.draw()
rect_one.draw()
rect_two.draw()

win.flip()
stime = getTime()
while getTime()-stime < 15.0:
    
    gaze_pos = tracker.getPosition()
    print(gaze_pos)
    if rect_one.contains(gaze_pos):
        print("looking into rectangle 1")
    if rect_two.contains(gaze_pos):
        print("looking into rectangle 2")
    textboxloaded.setText("Trial starting " + str(gaze_pos))
    textboxloaded.draw()
    rect_one.draw()
    rect_two.draw()

    win.flip()
    wait(0.1)



tracker.setRecordingState(False)

# Stop the ioHub Server
io.quit()