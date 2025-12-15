"""
14-post-processing.py - Accessing Events's audio output for post-processing.

The Events framework is essentially an audio material generator. The user will
generally want to have access to the result for future treatments, as in passing
through some reverb or delay.

There are two built-in arguments that help the user to configure the audio output
of the Events object.

- `signal`: A string indicating which attribute of the instrument is its final
            audio output. The Events objects will automatically sum this attribute
            signal from all active instrument instances.
- `outs`: Determine how many channels the Events object output signal will contain.
          This value should match the number of audio streams produced by the
          instrument.

Once these two arguments are defined, the sig() method returns an audio signal that
is the sum of the active instance output signals.

"""

from pyo import *
import random

s = Server().boot()

# A simple custom instrument. Note that the out() method is not called!
class MyInstrument(EventInstrument):
    def __init__(self, **args):
        EventInstrument.__init__(self, **args)
        self.output = LFO(freq=self.freq, sharp=[0.5, 0.6], type=2, mul=self.env)


# Some notes...
scl = EventScale("C", "aeolian", 3, 3, type=2)

# ... then the sequence of events. We are looking for a 2 streams (`outs`)
# signal in the self.output attribute (`signal`) of the instrument.
e = Events(
    instr=MyInstrument,
    degree=EventSlide(scl, segment=3, step=1),
    beat=1 / 4.0,
    db=-12,
    signal="output",
    outs=2, # set to 1 for mono
    attack=0.001,
    decay=0.05,
    sustain=0.7,
    release=0.05,
).play()

# ---------------------
# Tkinter GUI
# ---------------------
import tkinter as tk
root = tk.Tk()
root.title("Laser Harp Simulator")








#20 to 20khz is human hearing. 20 sounds almost inaudible base, probably better starting 100. 10000 sounds like a very high bell but still pleasing.
freq_range = [200, 10000]
# Six random frequencies.
freqs = [random.uniform(freq_range[0], freq_range[1]) for i in range(6)]

# Single trigger (like plucking once)
pluck = Trig()  # fires once

# LFO applied to the decay
decay = Sine(0.1).range(0.01, 0.3)

# Six resonators, one trigger, all frequencies
rezos = ComplexRes(pluck, freqs, decay, mul=5)



chorus = Chorus(rezos, depth=1, feedback=0.25)
#delay = Delay(chorus, delay=1, feedback=0.5)
reverb = WGVerb(chorus , feedback=0.8, cutoff=5000, bal=0.25).out()

# If you want, you can randomly reassign frequencies for the next pluck
def new():
    freqs = [random.uniform(freq_range[0], freq_range[1]) for i in range(6)]
    rezos.freq = freqs
    pluck.play()  # trigger again once


s.start()
#s.gui(locals())
# 
new()

time.sleep(4)
s.stop()
s.shutdown()
exit()
try:
    while True:
       # pass  # or add GPIO/piano loop here
       time.sleep(1)
except KeyboardInterrupt:
    s.stop()
    s.shutdown()