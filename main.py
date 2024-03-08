from psychopy.iohub import launchHubServer
from psychopy.core import getTime, wait
from psychopy import visual
from button_box import button_box
import random
import serial
from psychopy import logging, data, core
import yaml
from collections import deque
import keyboard

import sys
import os

# Get the absolute path of the parent directory of the current file (main.py)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Append the path of the subfolder to the system path
subfolder_path = os.path.join(current_dir, 'pyequipmentlib_d/src/equipment/')
sys.path.append(subfolder_path)
from marker  import get_marker
    
win = visual.Window(size=(1280, 720),pos=(0,0),allowGUI=True, monitor='testMonitor', units='pix', screen=0, color=(-0.2, -0.2, -0.2), fullscr=True, colorSpace='rgb')
with get_marker('stimtracker',win) as marker:

    time_out = 60.0 #iteration timeout
    gaze_time = 2.0 #gaze time needed to select
    select_time = 0.5
    window_size = 10 # rolling average window for gaze positions
    num_iterations=2 #experiment interations
    if window_size <= 0:
            raise ValueError("Window size must be a positive integer.")

    # # Set the serial port parameters
    # port = 'COM1'  # Change this to your specific serial port
    # baud_rate = 9600
    # # Open the serial port
    # ser = serial.Serial(port, baud_rate, timeout=1)

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
        pos=(0.0,.75),
        # If the text string length < num rows * num cols in
        # textgrid_shape, how should text be justified?
        #
        grid_horz_justification='center',
        grid_vert_justification='center')


    button_box1 = button_box(window=win)
    button_box1.create_all()
    

    textboxloaded.draw()

    # ioDevice = 'eyetracker.hw.mouse.EyeTracker'
    # ioConfig = {ioDevice: {'name': 'tracker', 'device_number': 0}, 'window': win}
    yaml_file_path = 'tobii_config.yml'
    with open(yaml_file_path, 'r') as file:
        ioConfig = {'eyetracker.hw.tobii.EyeTracker':yaml.safe_load(file), 'window': win}
    io = launchHubServer(**ioConfig)

    

    # Open a data file for logging
    log_file_path = "log.txt"
    log_file = open(log_file_path, 'w')
    log_file.write('Time\tGazeX\tGazeY\tTrial\tTarget\tGazing\n')  # Writing header
    clock = core.Clock()
    

    win.flip()

    # Get the eye tracker device.
    tracker = io.devices.tracker
    # run eyetracker calibration
    r = tracker.runSetupProcedure()
    
    keyboard.add_hotkey('ctrl+shift+c', tracker.runSetupProcedure)
    # Check for and print any eye tracker events received...
    tracker.setRecordingState(True)

    wait(1)
    window_queue0 = deque(maxlen=window_size)
    window_queue1 = deque(maxlen=window_size)

    for t in range(1,num_iterations+1):
        win.flip()
        wait(1)


        trial_target = random.randint(1,16)
        textboxloaded.setText("Target(" +str(t)+ ") is Box "+ str(trial_target))
        textboxloaded.draw()
        button_box1.draw_all()
        # Set marker value to 1 
        marker.send(1) 
        win.flip()
        # ser.write(b'1')


        stime = getTime()
        
        gaze_in_time = 0
        gaze_out_time = 0
        gazing = False
        
        while (gaze_out_time-gaze_in_time < gaze_time) and (getTime() - stime < time_out):  
            gaze_pos_temp = tracker.getPosition()
            # print(gaze_pos)
            if((gaze_pos_temp ==None)):
                continue
            window_queue0.append(gaze_pos_temp[0])
            window_queue1.append(gaze_pos_temp[1])
            
            if len(window_queue0) == window_size:
                gaze_pos[0] = sum(window_queue0)/window_size
                gaze_pos[1] = sum(window_queue1)/window_size
            else:
                gaze_pos = gaze_pos_temp
            visual.Circle(win, pos=(gaze_pos[0],gaze_pos[1]), radius=10, fillColor='red').draw()
            if(button_box1.check_button_gaze(trial_target,gaze_pos) and gazing==False):
                gazing = True
                gaze_in_time = getTime()
                button_box1.update_button_color(trial_target,button_box1.color_two)
            elif (button_box1.check_button_gaze(trial_target,gaze_pos) and gazing==True):
                gaze_out_time = getTime()
                button_box1.update_button_color(trial_target,button_box1.color_two)
            elif (gazing == True):
                gazing = False
                button_box1.update_button_color(trial_target,button_box1.color_one)
            g_str = button_box1.which_button_gaze(gaze_pos)
            log_file.write(f'{clock.getTime()}\t{gaze_pos[0]}\t{gaze_pos[1]}\t{t}\t{trial_target}\t{g_str}\n')
            textboxloaded.draw()
            button_box1.draw_all()
            win.flip()
            wait(0.05)
        # ser.write(b'8')
        # Set marker value to 8
        marker.send(2) 
        button_box1.update_button_color(trial_target,button_box1.color_three)
        button_box1.draw_all()
        win.flip()
        wait(select_time)
        button_box1.update_button_color(trial_target,button_box1.color_one)
        print("trial"+str(t)+" ended")
        # Set marker value to 9
        marker.send(3) 
        win.flip()
        # ser.write(b'9')



    tracker.setRecordingState(False)
    # ser.close()
    # Stop the ioHub Server
    io.quit()
    log_file.close()



