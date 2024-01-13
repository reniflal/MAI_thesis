from psychopy.iohub import launchHubServer
from psychopy.core import getTime, wait
from psychopy import visual
from button_box import button_box
import random

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


button_box1 = button_box(window=win)
button_box1.create_all()


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

num_iterations=2

for t in range(1,num_iterations+1):
    win.flip()
    wait(1)


    trial_target = random.randint(1,16)
    textboxloaded.setText("Target(" +str(t)+ ") is Box "+ str(trial_target))
    textboxloaded.draw()
    button_box1.draw_all()

    win.flip()


    stime = getTime()
    time_out = 1000.0
    gaze_time = 2.0
    gaze_in_time = 0
    gaze_out_time = 0
    gazing = False

    while (gaze_out_time-gaze_in_time < gaze_time) and (getTime() - stime < time_out):
        
        gaze_pos = tracker.getPosition()
        print(gaze_pos)
        if(button_box1.check_button_gaze(trial_target,gaze_pos) and gazing==False):
            gazing = True
            gaze_in_time = getTime()
        elif (button_box1.check_button_gaze(trial_target,gaze_pos) and gazing==True):
            gaze_out_time = getTime()
        elif (gazing == True):
            gazing = False

        textboxloaded.draw()
        button_box1.draw_all()
        win.flip()
        wait(0.1)
    print("trial"+str(t)+" ended")



tracker.setRecordingState(False)

# Stop the ioHub Server
io.quit()



