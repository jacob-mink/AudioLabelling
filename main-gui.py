import os
from tkinter.filedialog import askdirectory
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from mutagen.id3 import ID3
from tkinter import *
from tkinter.ttk import *
import argparse
import time
import threading

parser = argparse.ArgumentParser('Audio Labelling', description='Tool to label audio files with supplied binary labels')
parser.add_argument('--file', '-f', type=str, required=True, help='Audio file to load for labelling')
parser.add_argument('--output', '-o', type=str, required=True, help='name.csv file to put label,time (s)')
parser.add_argument('--labels', '-l', nargs=2, type=str, default=['Not Angry', 'Angry'], help='Specify alternate names for binary labelling scheme')
args = parser.parse_args()

# variables for labelling
starttime = -1
label_list = []

root = Tk()
root.minsize(200, 100)
    
pygame.mixer.init()
pygame.mixer.music.load(args.file)

v = StringVar()
labeltype = Label(root, textvariable=v)
def updatelabel(label):
    v.set(label)

label = Label(root, text='Audio Labeller')
label.pack()

updatelabel('None')
labeltype.pack()

label_names = args.labels
print(label_names)
def changelabel(event):
    global label_list
    if event.keysym == 'Left':
        updatelabel(label_names[0])
        label_list.append((0, time.time_ns()))
    elif event.keysym == 'Right':
        updatelabel(label_names[1])
        label_list.append((1, time.time_ns()))

progress = Progressbar(root, orient=HORIZONTAL, length=100, mode='determinate')
def wait_for_end(length):
    while pygame.mixer.music.get_busy():
        progress['value'] = (pygame.mixer.music.get_pos() / (1000 * length)) * 100.
        root.update_idletasks()
        pygame.time.wait(10)
    progress['value'] = 100.
    root.unbind('<Left>')
    root.unbind('<Right>')
    updatelabel('None')

def startsong(event):
    global starttime
    global label_list
    label_list = []
    root.bind('<Left>', changelabel)
    root.bind('<Right>', changelabel)
    starttime = time.time_ns()
    pygame.mixer.music.play()
    threading.Thread(target=wait_for_end, args=(pygame.mixer.Sound(args.file).get_length(),)).start()

startbutton = Button(root, text='Start File')
startbutton.pack()
startbutton.bind("<Button-1>", startsong)

progress.pack()

root.mainloop()
print([(l, (t - starttime) / 1e9) for l, t in label_list])

if len(label_list) > 0:
    with open('{}'.format(args.output), 'w+') as f:
        f.write('{}=0,{}=1\n'.format(label_names[0], label_names[1]))
        for l, t in label_list:
            f.write('{},{}\n'.format(l, (t - starttime) / 1e9))