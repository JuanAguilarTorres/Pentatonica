import config.constants as constant
from datetime import datetime
from managers.noteManager import get_note_for_row
import mido
from mido import Message, MidiFile, MidiTrack, MetaMessage
import os
import time
import random

# ---------------------------
# MIDI Management
# ---------------------------
def export_to_midi(matrix_manager, BPM, scale_type, root_key):
    mid = MidiFile(ticks_per_beat=480)
    track = MidiTrack()
    mid.tracks.append(track)
    tempo = mido.bpm2tempo(BPM)
    track.append(MetaMessage('set_tempo', tempo=tempo, time=0))
    
    ticks_per_step = mid.ticks_per_beat // 4
    note_duration_ticks = int((constant.note_length_ms / 60000) * BPM * mid.ticks_per_beat)
    
    events = []
    total_cols = constant.grid_cols * len(matrix_manager.matrices)
    
    for matrix_index, matrix in enumerate(matrix_manager.matrices):
        offset = matrix_index * constant.grid_cols
        for col in range(constant.grid_cols):
            t_start = (offset + col) * ticks_per_step
            for row in range(constant.grid_rows):
                if matrix[row][col]:
                    note = get_note_for_row(row, scale_type, root_key)
                    events.append((t_start, 'note_on', note))
                    events.append((t_start + note_duration_ticks, 'note_off', note))
    
    events.sort(key=lambda e: (e[0], 0 if e[1]=='note_on' else 1))
    
    current_time = 0
    for event in events:
        delta = event[0] - current_time
        current_time = event[0]
        if event[1] == 'note_on':
            track.append(Message('note_on', note=event[2], velocity=100, time=delta))
        else:
            track.append(Message('note_off', note=event[2], velocity=100, time=delta))
    
    os.makedirs("exports", exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d")
    rand_num = random.randint(1000, 9999)
    filename = os.path.join("exports", f"export{date_str}{rand_num}.mid")
    mid.save(filename)
    print("Exported to MIDI:", filename)