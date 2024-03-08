# pyequipmentlib

## Installation

This library has been tested on python 3.8

### As a dependency

In the active python virtual/conda environment of your project, execute:

``` sh
pip install git@gitlab.kuleuven.be:compneuro/pyequipmentlib.git#egg=equipment
```

or add it to your requirements.txt

### Standalone

For development or using the test and verification scripts

``` sh
git clone git@gitlab.kuleuven.be:compneuro/pyequipmentlib.git
cd pyequipmentlib
virtualenv .venv
pip install -r build_requirements.txt
pip install -e .
```

### When sending markers over USB to the Cedrus Gen 1 StimTracker

Install the FTDI D2XX Direct drivers from https://ftdichip.com/drivers/d2xx-drivers/

### When using the SR Research Eyelink 1000 Pro eye tracker

For using the Eyelink eye tracker, you need to install the SR Research
SDK:

-   On Windows, MacOS and Ubuntu:
    https://www.sr-support.com/thread-13.html
-   On RHEL-based linux (RHEL, CentOS, Fedora, ...):
    https://centos8.sr-research.com

When you have installed these libraries, you then need to install the
provided python wheels for the python bindings of the SDK:

``` sh
pip install <path to SDK installation>/SampleExperiments/Python/wheels/sr_research_pylink-2.1.1.0-cp38-cp38-<yourplatform>.whl
```

Finally, check if the Eyelink is [correctly set
up](https://gitlab.kuleuven.be/compneuro/lab-documentation/-/wikis/Equipment-manuals/Eyelink-1000-Plus#eyelink-sdk)

### When using the Cedrus StimTracker

## Usage

### Markers

Create a marker instance as follows. The method `marker.send()` sets the
next value to be sent, the marker will actually be sent on the sent on
the next `window.flip()` command.

``` python
from equipment.marker import get_marker
from psychopy.visual import Window

window = Window()

with get_marker('serial') as marker:
    # Set marker value to 10 
    marker.send(10) 
    # Send the marker
    window.flip()
    # Stop sending the marker
    window.flip()
```

The marker is defined whithin a `with` context in order to handle things
like cleanly opening and closing serial, USB or parallell ports, or
continuously drawing a black background in the case of visual markers.
Marker values must be integers larger or equal to 0 and smaller or equal
to 255.

#### Available marker mechanisms

-   `visual`: Send markers as a visual flash to be picked up by the
    Cedrus Stimtracker's photosensor
-   `viewpixx`: Send markers through the VPixx ViewPixx monitor
-   `usb`: Send markers through a USB port
-   `serial`: Send markers through a serial port
-   `parallel`: Send markers through a parallel port

### Eye tracker

#### Monitor setup

The defaults in the eye tracker calibration configuration files are
specified in [degrees ov visual
angle](https://www.psychopy.org/general/units.html#degrees-of-visual-angle).
In order to use this, you must first set up your monitor specification
using

``` sh
python -m psychopy.monitors.MonitorCenter
```

and input your monitors resolution, size and the distance to the screen.
Afterwards, you can use the eye tracker as follows:

#### Using the configuration presets

``` python
from equipment.eyetracker import get_eye_tracker
from psychopy import monitors

monitor = monitor.Monitor("my_monitor_name") # replace with your monitor's name as specified in the MonitorCenter
window = Window(monitor=monitor, size=monitor.getSizePix(),units='deg') 
with get_eye_tracker('tobii', window) as eye_tracker:
    eye_tracker.runSetupProcedure() # setup/calibrate
    eye_tracker.setRecordingState(True) # start recording
    while True:
        gaze_position = eye_tracker.getPosition()
```

`get_eyetracker()` returns an instance of the [psychopy eye tracker
interface](https://www.psychopy.org/api/iohub/device/eyetracker.html)

#### Using a custom configuration

TODO #### Available eye trackers

-   `tobii`
-   `eyelink`

### Test scripts
