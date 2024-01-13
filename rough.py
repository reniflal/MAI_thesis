from psychopy import visual, core, event

# Create a PsychoPy window
win = visual.Window(size=(800, 600), fullscr=False, allowGUI=True, color='black')

# Create ROIs
roi1 = visual.Rect(win, width=100, height=100, pos=(-200, 0), fillColor='red')
roi2 = visual.Rect(win, width=100, height=100, pos=(200, 0), fillColor='blue')

# Instructions
instructions = visual.TextStim(win, text="Look at the red or blue square.\nPress 'q' to quit.")

# Clock for timing
trial_clock = core.Clock()

# Run the experiment
while not event.getKeys(['q']):
    # Start the clock
    trial_clock.reset()

    # Draw stimuli
    roi1.draw()
    roi2.draw()
    instructions.draw()
    win.flip()

    # Check for eye tracker data (replace this with your eye tracker integration)
    gaze_pos = (0, 0)  # Replace with actual gaze position

    # Check if gaze is inside ROI1
    if roi1.contains(gaze_pos):
        roi1.fillColor = 'yellow'  # Change color when gazed
    else:
        roi1.fillColor = 'red'

    # Check if gaze is inside ROI2
    if roi2.contains(gaze_pos):
        roi2.fillColor = 'yellow'  # Change color when gazed
    else:
        roi2.fillColor = 'blue'

    # Draw stimuli with updated colors
    roi1.draw()
    roi2.draw()
    instructions.draw()
    win.flip()

    # Record timesOn and timesOff for ROIs
    times_on_roi1 = []
    times_off_roi1 = []
    times_on_roi2 = []
    times_off_roi2 = []

    # Check if gaze enters or leaves ROI1
    if roi1.contains(gaze_pos):
        times_on_roi1.append(trial_clock.getTime())
    else:
        times_off_roi1.append(trial_clock.getTime())

    # Check if gaze enters or leaves ROI2
    if roi2.contains(gaze_pos):
        times_on_roi2.append(trial_clock.getTime())
    else:
        times_off_roi2.append(trial_clock.getTime())

# Print timesOn and timesOff for ROIs
print("Times On ROI 1:", times_on_roi1)
print("Times Off ROI 1:", times_off_roi1)
print("Times On ROI 2:", times_on_roi2)
print("Times Off ROI 2:", times_off_roi2)

# Close the window
win.close()
core.quit()
