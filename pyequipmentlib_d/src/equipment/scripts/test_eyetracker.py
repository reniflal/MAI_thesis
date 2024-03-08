#!/usr/bin/env python
import click
import numpy as np
import psychopy.core as core
from equipment.eyetracker import get_eye_tracker, get_eye_trackers
from psychopy import event, monitors, visual
from psychopy.visual import TextStim, Window

FILT_TIME = 0.2


@click.command()
@click.option(
    "--monitor",
    "-m",
    type=click.Choice(monitors.getAllMonitors()),
    help="Monitor ID (see PsychoPY MonitorCenter).",
    required=True,
    default=None,
)
@click.option("--tracker", "-t", type=str, help="Eye tracker device")
@click.option(
    "--io-config",
    "-io",
    type=click.Choice(get_eye_trackers()),
    help="Path to a PsychoPy iohub config .yml file.",
    default=None,
)
def main_cli(monitor, tracker, io_config):
    monitor = monitors.Monitor(monitor)
    win = Window(
        size=monitor.getSizePix(),
        monitor=monitor,
        fullscr=True,
        units="deg",
    )
    win.recordFrameIntervals = True

    event.globalKeys.add(
        key="q",
        modifiers=["ctrl", "alt"],
        func=core.quit,
        name="shutdown",
    )

    with get_eye_tracker(tracker, win, 'test_eyetracker',  io_config=io_config) as eye_tracker:

        def calibrate_and_record():
            eye_tracker.runSetupProcedure()
            eye_tracker.setRecordingState(True)

        event.globalKeys.add(
            key="c",
            modifiers=["ctrl", "alt"],
            func=calibrate_and_record,
            name="shutdown",
        )
        eye_tracker.setRecordingState(True)
        instructions = TextStim(
            win,
            "Ctrl+Alt+q: quit \n Ctrl+Alt+c: calibrate",
            pos=[0, -8],
            color="black",
            autoDraw=True,
        )
        gaze = TextStim(win, "+", color="white", autoDraw=True)
        gaze_filt = TextStim(win, "+", color="black", autoDraw=True)
        fixation = TextStim(win, "+", color="blue", autoDraw=True)
        filt_len = int(FILT_TIME / win.refreshThreshold)
        filt = np.zeros((2, filt_len))
        while True:
            instructions.draw()
            fixation.draw()
            gaze_pos = eye_tracker.getPosition()
            if gaze_pos is not None:
                filt[:, :-1] = filt[:, 1:]
                filt[:, -1] = gaze_pos
            gaze.pos = gaze_pos
            gaze_filt.pos = np.mean(filt, axis=1)
            win.flip()


if __name__ == "__main__":
    main_cli()
