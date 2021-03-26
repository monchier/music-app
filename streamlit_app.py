from music21 import *
import streamlit as st
import io
from scipy.io import wavfile
import pretty_midi
import numpy as np


chords = st.text_input("Enter chords")
if not chords:
    st.stop()
s = stream.Stream()
for c in chords.split(" "):
    h = harmony.ChordSymbol(c)
    h.duration.type = 'whole'
    s.append(h)
#sc = scale.PhrygianScale('g')
#x=[s.append(note.Note(sc.pitchFromDegree(i % 11), quarterLength=0.25)) for i in range(60)]
mf = midi.translate.streamToMidiFile(s)
mf.open('midi.mid', 'wb')
mf.write()
mf.close()

midi_data = pretty_midi.PrettyMIDI("midi.mid")
audio_data = midi_data.fluidsynth()
audio_data = np.int16(audio_data / np.max(np.abs(audio_data)) * 32767 * 0.9) # -- Normalize for 16 bit audio https://github.com/jkanner/streamlit-audio/blob/main/helper.py

virtualfile = io.BytesIO()
wavfile.write(virtualfile, 44100, audio_data)

st.audio(virtualfile)
