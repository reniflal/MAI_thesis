import os

from importlib_resources import files
from psychopy.iohub import launchHubServer


def get_eye_trackers():
    return _EYE_TRACKER_DEFAULT_CONF.keys()


def get_eye_tracker(eye_tracker, win, filename, io_config=None):
    if io_config is None:
        io_config = _EYE_TRACKER_DEFAULT_CONF[eye_tracker]
        io_config = files("equipment.io_config").joinpath(io_config)
    return EyeTracker(win, filename, io_config)


class EyeTracker:
    def __init__(self, win, filename, io_config):
        self.win = win
        self.io_config = io_config
        self.filename = filename

    def __enter__(self):
        self._io = launchHubServer(
            experiment_code=self.filename,
            session_code=self.filename,
            window=self.win,
            iohub_config_name=self.io_config,
        )
        if not hasattr(self._io.devices, "tracker"):
            raise OSError("Eye tracker device not found")
        # name = getConfiguration()["name"]
        self._eye_tracker = self._io.devices.tracker
        return self._eye_tracker

    def __exit__(self, exc_type, exc_value, traceback):
        self._eye_tracker.setRecordingState(False)
        self._io.quit()


_EYE_TRACKER_DEFAULT_CONF = dict(
    tobii="tobii_config.yml",
    eyelink="eyelink_config.yml",
)
