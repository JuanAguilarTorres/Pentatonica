import config.constants as constant
import pygame

# ---------------------------
# Define Layout Rows
# ---------------------------
# Row 1: Top control row (Major/Minor buttons and BPM controls)
row1_y = constant.grid_height + constant.matrix_control_height + 10
# Row 2: Keys row
row2_y = constant.grid_height + constant.matrix_control_height + 60
# Row 3: Instrument and Export buttons
row3_y = constant.grid_height + constant.matrix_control_height + 110

# ---------------------------
# BPM Input and Slider Setup (Row 1 - Right side)
# ---------------------------
bpm_text = "Value"
bpm_input_active = False
bpm_slider_visible = False
# This flag ensures the BPM field is cleared only on the first numeric input.
clear_bpm_on_next_input = False

bpm_input_width = 80
slider_width = 200
slider_height = 20
gap = 5
min_bpm = 60
max_bpm = 240
knob_width = 10
slider_dragging = False

# Pre-render BPM label
pygame.font.init()
font = pygame.font.SysFont(None, 24)
bpm_label_surf = font.render("BPM", True, (255, 255, 255))
bpm_label_width = bpm_label_surf.get_width()

# Right-align the BPM controls in row 1.
group_width = slider_width + gap + bpm_label_width + gap + bpm_input_width
right_margin = 10
group_right = constant.grid_width - right_margin
slider_x = group_right - group_width

slider_rect = pygame.Rect(slider_x, row1_y + (40 - slider_height) // 2, slider_width, slider_height)
bpm_label_rect = bpm_label_surf.get_rect()
bpm_label_rect.topleft = (slider_rect.right + gap, row1_y + (40 - bpm_label_rect.height) // 2)
bpm_input_rect = pygame.Rect(bpm_label_rect.right + gap, row1_y, bpm_input_width, 40)

# ---------------------------
# Other Control Buttons
# ---------------------------
major_button_rect = pygame.Rect(10, row1_y, 100, 40)
minor_button_rect = pygame.Rect(120, row1_y, 100, 40)

# Keys row setup (Row 2)
keys = ["C", "D", "E", "F", "G", "A", "B"]
key_button_width = 50
key_button_height = 30
key_spacing = 10
total_keys_width = len(keys) * key_button_width + (len(keys) - 1) * key_spacing
key_start_x = (constant.width - total_keys_width) // 2
key_button_rects = {}
for i, k in enumerate(keys):
    rect = pygame.Rect(key_start_x + i * (key_button_width + key_spacing), row2_y,
    key_button_width, key_button_height)
    key_button_rects[k] = rect

# Row 3: Instrument and Export buttons
# Make the instrument button wider to fit all instrument names.
instrument_button_rect = pygame.Rect(10, row3_y, 250, 40)
export_button_rect = pygame.Rect(instrument_button_rect.right + 10, row3_y, 120, 40)