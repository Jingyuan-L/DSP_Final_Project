# Tk_demo_02_buttons.py
# TKinter demo
# Play a sinusoid using Pyaudio. Use buttons to adjust the frequency.

import tkinter as Tk
import pyaudio
import struct
import numpy as np
from math import sin, cos, pi
from scipy import signal

chords = [[130.81, 164.81, 196, 261.63, 329.63],
          [146.83, 174.61, 220, 293.66, 349.23],
          [164.81, 196, 246.94, 311.13, 392],
          [174.61, 220, 261.63, 349.23, 440],
          [196, 246.94, 293.66, 392, 493.88],
          [220, 261.63, 329.63, 440, 523.25]]

BLOCKLEN   = 64        # Number of frames per block
WIDTH       = 2         # Bytes per sample
CHANNELS    = 1         # Mono
RATE        = 8000      # Frames per second
MAXVALUE = 2**15-1  # Maximum allowed output signal value (because WIDTH = 2)

# Karplus-Strong paramters
K = 0.93
N = 64

# Define input signal
T = 2.0 # time duration (seconds)

# Parameters
Ta = 2      # Decay time (seconds)
fk = chords[0]  # Frequency (Hz)
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
states = np.zeros((5, ORDER))
x = np.zeros((5, BLOCKLEN))
y = np.zeros((5, BLOCKLEN))
buffer = np.zeros((5, BLOCKLEN))

CONTINUE = True
KEYPRESS = -1

def my_function(event):
    global KEYPRESS
    print('You pressed ' + event.char)
    if event.char == 'a':
      KEYPRESS = 0
    elif event.char == 's':
        KEYPRESS = 1
    elif event.char == 'd':
        KEYPRESS = 2
    elif event.char == 'f':
        KEYPRESS = 3
    elif event.char == ' ':
        KEYPRESS = 4


def fun_chord(chord='C'):
    global fk
    global r
    global om
    global a
    global b

    if chord == 'C':
        fk = chords[0]
    elif chord == 'Dm':
        fk = chords[1]
    elif chord == 'Em':
        fk = chords[2]
    elif chord == 'F':
        fk = chords[3]
    elif chord == 'G':
        fk = chords[4]
    elif chord == 'Am':
        fk = chords[5]

    print(chord, fk)
    # Pole radius and angle
    r = 0.01 ** (1.0 / (Ta * RATE))  # 0.01 for 1 percent amplitude
    om = [2.0 * pi * float(f) / RATE for f in fk]
    print(om)

    # Filter coefficients (second-order IIR)
    a = [[1, -2 * r * cos(omi), r ** 2] for omi in om]
    print(a)
    b = [[r * sin(omi)] for omi in om]
    print(b)

def fun_quit():
    global CONTINUE
    print('Good bye')
    CONTINUE = False


# Define TK root
root = Tk.Tk()

# Define widgets
Label_1 = Tk.Label(root, text='Guitar Chord Simulator')
Label_chord = Tk.Label(root, text='Choose chord(In C Major) ')
B_C = Tk.Button(root, text=' C  ', command=lambda: fun_chord(chord='C'))
B_Dm = Tk.Button(root, text='Dm', command=lambda: fun_chord(chord='Dm'))
B_Em = Tk.Button(root, text='Em', command=lambda: fun_chord(chord='Em'))
B_F = Tk.Button(root, text=' F  ', command=lambda: fun_chord(chord='F'))
B_G = Tk.Button(root, text=' G  ', command=lambda: fun_chord(chord='G'))
B_Am = Tk.Button(root, text='Am', command=lambda: fun_chord(chord='Am'))
Label_pluck = Tk.Label(root, text='Press a, s, d, f and space on the keyboard to play notes of the chord.')
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

output_block = [0] * BLOCKLEN  # create 1D array
theta = 0

i = 0
while CONTINUE:
    root.update()

    if KEYPRESS != -1 and CONTINUE:
        i = KEYPRESS
        x[i][0] = 10000.0

    # print(b[i], a[i])
    for k in range(len(y)):
        [y[k], states[k]] = signal.lfilter(b[k], a[k], x[k], zi=states[k])
    # print(y[i])

    if KEYPRESS != -1 and CONTINUE:
        buffer[i] = y[i]
    else:
        for k in range(len(y)):
            for j in range(N):
                y[k][j] = K * 0.5 * (buffer[k][j] + buffer[k][(j+1) % N])
                buffer[k][j] = y[k][j]

    # print(buffer)

    x[i][0] = 0.0
    KEYPRESS = -1

    total = np.zeros((1, BLOCKLEN))
    for k in range(len(y[0])):
        total[0][k] = sum([y[j][k] for j in range(len(y))])

    total = np.clip(total.astype(int), -MAXVALUE, MAXVALUE)  # Clipping

    binary_data = struct.pack('h' * BLOCKLEN, *map(int, total[0]))    # Convert to binary binary data
    stream.write(binary_data, BLOCKLEN)               # Write binary binary data to audio output


# Close audio stream
stream.stop_stream()
stream.close()
p.terminate()
