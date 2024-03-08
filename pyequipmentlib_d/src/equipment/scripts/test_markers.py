#!/usr/bin/env python
import sys
from contextlib import ExitStack

import click
from equipment.marker import get_marker, get_markers
from psychopy import core, event, logging, monitors
from psychopy.visual import TextStim, Window


@click.command()
@click.argument("markers", nargs=-1, type=click.Choice(get_markers()))
@click.option(
    "--monitor",
    "-m",
    type=click.Choice(monitors.getAllMonitors()),
    help="Monitor ID (see PsychoPY MonitorCenter).",
    required=True,
)
def main_cli(markers, monitor):
    monitor = monitors.Monitor(monitor)
    win = Window(
        size=monitor.getSizePix(),
        monitor=monitor,
        fullscr=True,
        allowGUI=False,
        color=[-1,-1,-1],
        waitBlanking=True,
        winType='glfw',
        backendConf=dict(
            refreshHz=250,
            bpc=10,
        )
    )
    win.mouseVisible = False
    win.recordFrameIntervals = True

    event.globalKeys.add(
        key="q",
        modifiers=["ctrl", "alt"],
        func=core.quit,
        name="shutdown",
    )
    #win.winHandle.activate()

    markers = [get_marker(marker, win) for marker in markers]
    with ExitStack() as stack:
        for marker in markers:
            stack.enter_context(marker)

        stim = TextStim(win, autoDraw=True)
        for v in range(256):
            stim.text = f"dec: {v:03}\nbin: {v:08b}"
            for marker in markers:
                marker.send(v)
            for _ in range(int(1 / win.monitorFramePeriod)):

                stim.draw()
                win.flip()

            logging.flush()


if __name__ == "__main__":
    main_cli()
