# Tk_demo_02_buttons.py
# TKinter demo
# Play a sinusoid using Pyaudio. Use buttons to adjust the frequency.

import tkinter as Tk
import pyaudio
import struct
import numpy as np
from math import sin, cos, pi
from scipy import signal

BLOCKLEN   = 64        # Number of frames per block
WIDTH       = 2         # Bytes per sample
CHANNELS    = 1         # Mono
RATE        = 8000      # Frames per second
MAXVALUE = 2**15-1  # Maximum allowed output signal value (because WIDTH = 2)

# Karplus-Strong paramters
K = 0.93
N = 60

# Define input signal
T = 2.0 # time duration (seconds)

# Buffer to store past signal values. Initialize to zero.
buffer = np.random.normal(0, 1, N)   # list of zeros

# Parameters
Ta = 2      # Decay time (seconds)
fk = [2**(k/12) * 440 for k in range(12)]  # Frequency (Hz)
# print(fk)

# Pole radius and angle
r = 0.01**(1.0/(Ta*RATE))       # 0.01 for 1 percent amplitude
om = [2.0 * pi * float(f)/RATE for f in fk]
# print(om)

# Filter coefficients (second-order IIR)
a = [[1, -2*r*cos(omi), r**2] for omi in om]
# print(a)
b = [[r*sin(omi)] for omi in om]
# print(b)
ORDER = 2   # filter order
states = np.zeros((12, ORDER))
x = np.zeros((12, BLOCKLEN))
y = np.zeros((12, BLOCKLEN))

CONTINUE = True
KEYPRESS = ''

def my_function(event):
    global CONTINUE
    global KEYPRESS
    print('You pressed ' + event.char)
    KEYPRESS = event.char


def fun_chord(chord='C'):
    global f1
    print('Up')
    if chord == 'C':
        fk = []



def fun_quit():
    global CONTINUE
    print('Good bye')
    CONTINUE = False


# Define TK root
root = Tk.Tk()

# Define widgets
Label_1 = Tk.Label(root, text='Guitar Simulator')
Label_chord = Tk.Label(root, text='Choose chord(For Key C) ')
B_C = Tk.Button(root, text=' C  ', command=lambda: fun_chord(chord='C'))
B_Dm = Tk.Button(root, text='Dm', command=lambda: fun_chord(chord='Dm'))
B_Em = Tk.Button(root, text='Em', command=lambda: fun_chord(chord='Em'))
B_F = Tk.Button(root, text=' F  ', command=lambda: fun_chord(chord='F'))
B_G = Tk.Button(root, text=' G  ', command=lambda: fun_chord(chord='G'))
B_Am = Tk.Button(root, text='Am', command=lambda: fun_chord(chord='Am'))
Label_pluck = Tk.Label(root, text='Press q,w,e,a,s,d on the keyboard as string 1-6 on guitar to play.')
B_quit = Tk.Button(root, text='Quit', command=fun_quit)

# Place widgets
Label_1.grid(row=0, columnspan=6, pady=5)
Label_chord.grid(row=1, columnspan=6, pady=5)
B_C.grid(row=2, column=0, pady=5)
B_Dm.grid(row=2, column=1, pady=5)
B_Em.grid(row=2, column=2, pady=5)
B_F.grid(row=2, column=3, pady=5)
B_G.grid(row=2, column=4, pady=5)
B_Am.grid(row=2, column=5, pady=5)
Label_pluck.grid(row=3, columnspan=6, pady=5)
B_quit.grid(row=4, columnspan=6, pady=5, ipadx=20)

root.bind("<Key>", my_function)

# Create Pyaudio object
p = pyaudio.PyAudio()
stream = p.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=RATE,
    input=False,
    output=True,
    frames_per_buffer=128)
# specify low frames_per_buffer to reduce latency

BLOCKLEN = 512
output_block = [0] * BLOCKLEN  # create 1D array
theta = 0

i = 0
while CONTINUE:
    root.update()
#
#     if KEYPRESS != '' and CONTINUE:
#         i =  ( ord(KEYPRESS) - ord('a') ) % 12
#         print("The octave of this note is " + str(i+1) )
#         # Some key (not 'q') was pressed
#         x[i][0] = 10000.0
#
#     [y[i], states[i]] = signal.lfilter(b[i], a[i], x[i], zi = states[i])
#     y = K * 0.5 * (buffer[i % N] + buffer[(i + 1) % N])
#     buffer[i % N] = y
#
#
#     x[i][0] = 0.0
#     KEYPRESS = ''
#
#     y[i] = np.clip(y[i].astype(int), -MAXVALUE, MAXVALUE)     # Clipping
#
#     binary_data = struct.pack('h' * BLOCKLEN, *map(int, y[i]));    # Convert to binary binary data
#     stream.write(binary_data, BLOCKLEN)               # Write binary binary data to audio output

print('* Done.')

# Close audio stream
stream.stop_stream()
stream.close()
p.terminate()
