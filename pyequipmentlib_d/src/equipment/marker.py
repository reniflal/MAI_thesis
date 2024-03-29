from abc import ABC, abstractmethod

import ipdb
import numpy as np
import pyxid
from psychopy import logging
from psychopy.layout import Position
from psychopy.visual import Rect
from serial import Serial


def get_markers():
    return _MARKERS.keys()


def get_marker(marker, win, *args, **kwargs):
    marker = marker.strip().lower()
    if marker not in get_markers():
        raise ValueError(f"marker must be in {get_markers()}")
    return _MARKERS[marker](win, *args, **kwargs)


class Marker(ABC):
    def __init__(
        self,
        win,
    ):
        self.win = win

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    @abstractmethod
    def send(self, value):
        """Log marker with specified value in psychopy log on next window flip"""
        if not type(value) is int or (value < 0) or (value > 255):
            raise ValueError(
                f"value must be a positive integer between 0 and 255, got {value}"
            )
        log_msg = f"MARKER {value} to DEVICE {self.get_device_name()}"
        self.win.logOnFlip(log_msg, logging.EXP)
        return True

    @abstractmethod
    def get_device_name(self):
        pass


class EyeTrackerMarker(Marker):
    def __init__(self, win, eye_tracker, **kwargs):
        self.eye_tracker = eye_tracker
        super().__init__(win, **kwargs)

    def send(self, value):
        """Send marker with specified value to eye tracker on next window flip"""
        super().send(value)

        log_msg = f"MARKER {value}"

        def send_fun():
            self.eye_tracker.sendMessage(log_msg)
            self.eye_tracker.hubClient.sendMessageEvent(text=log_msg)

        self.win.callOnFlip(send_fun)

    def get_device_name(self):
        return self.eye_tracker.getConfiguration()["name"]


class VisualMarker(Marker):
    """Tailored to Cedrus StimTracker photosensor

    From https://cedrus.com/stimtracker/specs.htm

    More information on https://cedrus.com/support/stimtracker_1g/tn1408_onset_visual.htm
    """

    def __init__(self, win, pulse_duration=int(0.1*250), **stim_kwargs):
        super().__init__(win)
        self.pulse_duration = pulse_duration

        left_pix = -self.win.size[0] / 2 + 1
        top_pix = self.win.size[1] / 2 - 1
        stim_kwargs.setdefault("pos", Position([left_pix, top_pix], "pix", win))
        stim_kwargs.setdefault("width", 2.5)  # cm
        stim_kwargs.setdefault("height", 2.5)  # cm
        stim_kwargs.setdefault("units", "cm")
        stim_kwargs.setdefault("lineWidth", 0)
        stim_kwargs.setdefault("lineColor", 0)

        # self.bg_stim = Rect(self.win, fillColor="black", **stim_kwargs)
        self.stim = Rect(self.win, fillColor="black", **stim_kwargs)
        self._win = win

    def send(self, value):
        super().send(value)
        self._draw(value, self.pulse_duration)

    def _draw(self, value, n_frames):
        self._draw_on(value)
        if n_frames == 1:
            self._win.callOnFlip(self._draw_off)
        else:
            self._win.callOnFlip(self._draw, value, n_frames - 1)

    def _draw_on(self, value):
        self.stim.fillColor = "white"

    def _draw_off(self):
        self.stim.fillColor = "black"

    def __enter__(self):
        self.stim.autoDraw = True
        return super().__enter__()

    def __exit__(self, *args):
        self.stim.autoDraw = False
        return super().__exit__(*args)

    def get_device_name(self):
        return "photodiode"


class VIEWPixxMarker(VisualMarker):
    BIT_COLOR_MAP = np.array(
        [
            [0, 2**6, 0],
            [0, 2**4, 0],
            [0, 2**2, 0],
            [0, 2**0, 0],
            [2**6, 0, 0],
            [2**4, 0, 0],
            [2**2, 0, 0],
            [2**0, 0, 0],
        ]
    )

    def __init__(self, win):
        super().__init__(
            win, pulse_duration=1, width=1, height=1, units="pix", colorSpace="rgb255"
        )

    def _draw_on(self, value):
        self.stim.fillColor = self.value2color(value)

    def get_device_name(self):
        return "VIEWPixx/EEG"

    @classmethod
    def value2color(cls, value):
        """Convert a marker value to a color.

        The color conversion maps an integer value < 256 to an
        RGB array, such that, when sent by a ViewPixx monitor in
        VPixx Pixel Mode over a standard DB25 or a NeuroScan
        STIM-to-SCAN (DB25) cable, the marker value read by the NeuroScan
        system represents `value` in binary. More information about pin layout
        and color to pin mapping at https://vpixx.com/vocal/pixelmode and in the
        NeuroScan SynAmps² manual on page 63.
        """
        if value > 255:
            raise ValueError(f"Value ({value}) must be smaller than 256.")
        if value < 0:
            raise ValueError(f"Value ({value}) must be positive.")

        value = bin(value)[2:]
        n_bits = cls.BIT_COLOR_MAP.shape[0]
        value = value.zfill(n_bits)
        value = value[::-1]
        value = np.array(list(value), dtype=int)
        color = value @ cls.BIT_COLOR_MAP
        return color.tolist()


class SerialMarker(Serial, Marker):
    def __init__(self, win, **kwargs):
        """Serial port marker class

        On Windows, use port='0', port='1', ...
        On Mac/Linux, use port = '/dev/ttyS0', port='/dev/ttyS1', ..., or
        port='/dev/ttyUSB0' for USB adapter.
        """

        self.win = win
        self.kwargs = kwargs
        # self.kwargs.setdefault("port", "0")
        self.kwargs.setdefault("port", "/dev/ttyUSB0")
        self.kwargs.setdefault("baudrate", 19200)
        self.kwargs.setdefault("timeout", 1)
        super(SerialMarker, self).__init__(**self.kwargs)

    def get_device_name(self):
        return f"serial port {self.kwargs['port']}"

    def send(self, value):
        super().send(value)

        def _send(value):
            self.write(value)

        self.win.callOnFlip(_send)


class ParallelMarker(Marker):
    def __init__(self, *args):
        raise NotImplementedError


class XID1Marker(Marker):
    """Control the CEDRUS StimTracker Gen 1 throuch the XID version 1 protocol.

    More information at
        * https://github.com/cedrus-opensource/pyxid/tree/pyxid1.0_legacy
        * https://cedrus.com/support/stimtracker_1g/tn1450_st_commands.htm
    """

    def __init__(self, *args, dev=0, pulse_duration=10):
        super().__init__(*args)
        self.dev = dev
        self.pulse_duration = pulse_duration

    def __enter__(self):
        devices = pyxid.get_xid_devices()
        self._dev = devices[self.dev]
        self._dev.set_pulse_duration(self.pulse_duration)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        del self._dev

    def send(self, value):
        super().send(value)

        def _send():
            self._dev.activate_line(bitmask=value, leave_remaining_lines=False)

        self.win.callOnFlip(_send)
        return True

    def get_device_name(self):
        if hasattr(self, "_dev"):
            return "XID1 device: str(self._dev)"
        else:
            return "Uninitialized XID1 device"


_MARKERS = dict(
    viewpixx=VIEWPixxMarker,
    eyetracker=EyeTrackerMarker,
    visual=VisualMarker,
    serial=SerialMarker,
    parallel=ParallelMarker,
    stimtracker=XID1Marker,
)
