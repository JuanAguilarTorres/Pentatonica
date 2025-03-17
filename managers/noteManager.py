import config.musicTheory as theory

# ---------------------------
# Note Management
# ---------------------------

def get_note_for_row(row, scale_type, root_key):
    index = 15 - row
    octave_offset = (index // 5) * 12
    base_note = 60 + theory.natural_notes[root_key]
    pattern = theory.major_pentatonic if scale_type == "Major" else theory.minor_pentatonic
    return base_note + octave_offset + pattern[index % 5]