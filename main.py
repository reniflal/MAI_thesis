from psychopy.iohub import launchHubServer
from psychopy.core import getTime, wait
from psychopy import visual
from button_box import button_box
import random
import serial
from psychopy import logging, data, core, event
import yaml
from collections import deque
import keyboard

import sys
import os


recalibrated = False #global variable
# Get the absolute path of the parent directory of the current file (main.py)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Append the path of the subfolder to the system path
subfolder_path = os.path.join(current_dir, 'pyequipmentlib_d/src/equipment/')
sys.path.append(subfolder_path)
from marker  import get_marker


user = "_renif_"
exp_num = "check"
exp_type = "trial_"
log_folder_name = user+exp_type+exp_num
num_iterations=25 #experiment interations
press_for_next = False

win = visual.Window(size=(1280, 720),pos=(0,0),allowGUI=True, monitor='testMonitor', units='pix', screen=0, color=(-0.2, -0.2, -0.2), fullscr=True, colorSpace='rgb')
with get_marker('stimtracker',win) as marker:

    time_out = 60.0 #iteration timeout
    gaze_time = 2.0 #gaze time needed to select
    select_time = 0.5
    window_size = 10 # rolling average window for gaze positions
    if window_size <= 0:
            raise ValueError("Window size must be a positive integer.")



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
    log_file_path = "logs" + log_folder_name
    if not os.path.exists(log_file_path):
        os.makedirs(log_file_path)

    clock = core.Clock()


    win.flip()

    # Get the eye tracker device.
    tracker = io.devices.tracker
    # run eyetracker calibration
    r = tracker.runSetupProcedure()

    def wait_till_see_textbox(window_queuex, window_queuey):
        next_box = visual.Rect( win=win, name="next", fillColor=button_box1.color_two, lineColor=button_box1.color_one,  size=button_box1.size,
                                    pos=(0,400), opacity=1)
        text_next = visual.TextStim(win=win, text='Next', color='black', height=20, pos=(0,400))
        
        next_box.draw()
        text_next.draw()
        win.flip()
        not_looked = True
        # window_queuex = deque(maxlen=window_size)
        # window_queuey = deque(maxlen=window_size)
        while(not_looked):
            gaze_pos_temp = tracker.getPosition()
            if(not isinstance(gaze_pos_temp,list)):
                continue
            if((gaze_pos_temp ==None)):
                continue
            window_queuex.append(gaze_pos_temp[0])
            window_queuey.append(gaze_pos_temp[1])
            gaze_pos = gaze_pos_temp
            if len(window_queuex) == window_size:
                gaze_pos[0] = sum(window_queuex)/window_size
                gaze_pos[1] = sum(window_queuey)/window_size
            else:
                gaze_pos = gaze_pos_temp
            
            next_box.draw()
            text_next.draw()
            visual.Circle(win, pos=(gaze_pos[0],gaze_pos[1]), radius=10, fillColor='red').draw()
            win.flip()
            if(next_box.contains(gaze_pos)):
                not_looked = False

        

    def exit_program():
        print("exiting program")
        win.close()  # Close the PsychoPy window
        sys.exit(1)

    keyboard.add_hotkey('ctrl+shift+e', exit_program)
    # Check for and print any eye tracker events received...
    tracker.setRecordingState(True)

    wait(1)
    window_queue0 = deque(maxlen=window_size)
    window_queue1 = deque(maxlen=window_size)
    g_str_prev = 0
    for t in range(1,num_iterations+1):
        button_box1.create_all()
        win.flip()
        wait(1)
        log_file_name = "log"+str(t)+".txt"
        log_file = open(os.path.join(log_file_path,log_file_name), 'w')
        log_file.write('Time\tGazeX\tGazeY\tTrial\tTarget\tGazing\n')  # Writing header

        trial_target = random.randint(1,16)
        textboxloaded.setText("Target(" +str(t)+ ") is Box "+ str(trial_target))
        textboxloaded.draw()
        button_box1.draw_all()
        # Set marker value to 1 - start of trial
        marker.send(1) 
        # print("marker 1")
        win.flip()
        log_file.write(f'{clock.getTime()}\txx\txx\txx\txx\txx\n')

        stime = getTime()
        
        gaze_in_time = 0
        gaze_out_time = 0
        gazing = False
        non_target_gazing = False
        
        while (gaze_out_time-gaze_in_time < gaze_time) and (getTime() - stime < time_out):  

            gaze_pos_temp = tracker.getPosition()
            if(not isinstance(gaze_pos_temp,list)):
                continue
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
            g_str = button_box1.which_button_gaze(gaze_pos)
            
            if(g_str_prev!=0 and g_str!=g_str_prev and g_str_prev!=trial_target):
                # Set marker value to 5 - out of non-target box
                marker.send(5)
                # print("marker 5")
                if(g_str_prev!=0):
                    button_box1.update_button_color(g_str_prev,button_box1.color_one)

            if(g_str==trial_target  and gazing==False):
                # Set marker value to 2 - into target box
                marker.send(2) 
                # print("marker 2")
                gazing = True
                gaze_in_time = getTime()
                button_box1.update_button_color(trial_target,button_box1.color_four)
            elif (g_str==trial_target and gazing==True):
                gaze_out_time = getTime()
                button_box1.update_button_color(trial_target,button_box1.color_four)
            elif (gazing == True):
                gazing = False
                # Set marker value to 3 - out of target box
                marker.send(3) 
                # print("marker 3")
                button_box1.update_button_color(trial_target,button_box1.color_one)





            if(g_str!=0 and g_str!=trial_target and g_str!=g_str_prev):
                # Set marker value to 4 - into non-target box
                marker.send(4) 
                # print("marker 4")
                if(g_str_prev!=0):
                    button_box1.update_button_color(g_str_prev,button_box1.color_one)
                button_box1.update_button_color(g_str,button_box1.color_four)

            
            
            g_str_prev = g_str
            log_file.write(f'{clock.getTime()}\t{gaze_pos[0]}\t{gaze_pos[1]}\t{t}\t{trial_target}\t{g_str}\n')
            textboxloaded.draw()
            button_box1.draw_all()
            win.flip()
            wait(0.05)

        # Set marker value to 6
        marker.send(6) 
        # print("marker 6")
        button_box1.update_button_color(trial_target,button_box1.color_three)
        button_box1.draw_all()
        win.flip()
        log_file.write(f'{clock.getTime()}\tyy\tyy\tyy\tyy\tyy\n')
        wait(select_time)
        button_box1.update_button_color(trial_target,button_box1.color_one)
        print("trial"+str(t)+" ended")
        # Set marker value to 7
        marker.send(7) 
        # print("marker 7")
        win.flip()
        log_file.write(f'{clock.getTime()}\tzz\tzz\tzz\tzz\tzz\n')
        if(press_for_next):
            keyboard.wait('n')
        else:
            wait_till_see_textbox(window_queue0,window_queue1)




    tracker.setRecordingState(False)
    # Stop the ioHub Server
    io.quit()
    log_file.close()



