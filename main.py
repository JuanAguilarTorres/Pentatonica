# Assets and configuration imports
from assets.mapping import instrument_list
import config.constants as constant
# FluidSynth for MIDI synthesis
import fluidsynth
# Managers for drawing, layout, matrix handling, MIDI export, and note mapping
from managers import drawManager
from managers import layoutManager
from managers.matrixManager import MatrixManager
from managers.midiManager import export_to_midi
from managers.noteManager import get_note_for_row
# Standard libraries
import math
import pygame

# ---------------------------
# Initial Dynamic values
# ---------------------------
BPM = 120
layoutManager.bpm_text = str(BPM)
scale_type = "Major"
root_key = "C"
current_instrument_index = 0
instrument_dropdown_visible = False
instrument_column_offset = 0
current_column = 0
current_playing_matrix = 0
active_notes = []

# ---------------------------
# FluidSynth Setup
# ---------------------------
fs = fluidsynth.Synth()
fs.start()
soundfont = "./assets/FluidR3_GM.sf2"
sfid = fs.sfload(soundfont)
# Default instrument: Acoustic Grand Piano (program 0, bank 0)
fs.program_select(0, sfid, 0, 0)

# ---------------------------
# Pygame UI Setup
# ---------------------------
pygame.init()
screen = pygame.display.set_mode((constant.width, constant.height))
pygame.display.set_caption("Pentatonica")
matrix_manager = MatrixManager()

# ---------------------------
# Playback Logic
# ---------------------------

def calculate_step_duration(bpm):
    return int(60000 / (bpm * 4))

step_duration = calculate_step_duration(BPM)
COLUMN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(COLUMN_EVENT, step_duration)

def update_timer():
    global step_duration
    step_duration = calculate_step_duration(BPM)
    pygame.time.set_timer(COLUMN_EVENT, step_duration)

# ---------------------------
# Main Loop
# ---------------------------
print("Pentatonica started.")
clock = pygame.time.Clock()
running = True
while running:
    current_time_ms = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            # Handle matrix navigation clicks
            if drawManager.nav_controls_y <= my <= drawManager.nav_controls_y + constant.matrix_control_height:
                # Check matrix selection buttons
                for i in range(len(matrix_manager.matrices)):
                    if drawManager.get_matrix_button_rect(i).collidepoint((mx, my)):
                        matrix_manager.switch_to_matrix(i)
                        break
                
                # Check add matrix button
                if drawManager.get_add_matrix_button_rect(matrix_manager).collidepoint((mx, my)):
                    matrix_manager.add_matrix()
                
                # Check delete matrix button
                if matrix_manager.can_delete_last_matrix():
                    if drawManager.get_delete_matrix_button_rect(matrix_manager).collidepoint((mx, my)):
                        if current_playing_matrix + 1 == len(matrix_manager.matrices):
                            current_playing_matrix = 0
                            current_column = 0
                        matrix_manager.delete_last_matrix()
                continue

            # When instrument dropdown is visible, check for horizontal scroll first.
            if instrument_dropdown_visible:
                # Compute visible rows.
                if len(instrument_list) > constant.max_dropdown_rows * 2:
                    visible_rows = constant.max_dropdown_rows
                else:
                    visible_rows = math.ceil(len(instrument_list) / 2)
                visible_columns = 2
                total_columns = math.ceil(len(instrument_list) / visible_rows)
                
                # Horizontal scrolling with mouse wheel.
                if event.button in (4, 5):
                    if event.button == 4:
                        instrument_column_offset = max(0, instrument_column_offset - 1)
                    elif event.button == 5:
                        instrument_column_offset = min(total_columns - visible_columns,
                        instrument_column_offset + 1)
                    continue

                dropdown_height = visible_rows * constant.instrument_item_height
                dropdown_width = visible_columns * constant.column_width
                dropdown_x = layoutManager.instrument_button_rect.right
                dropdown_y = layoutManager.instrument_button_rect.bottom - dropdown_height
                dropdown_rect = pygame.Rect(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                if dropdown_rect.collidepoint((mx, my)):
                    rel_x = mx - dropdown_x
                    rel_y = my - dropdown_y
                    col_index_visible = int(rel_x // constant.column_width)
                    actual_col = instrument_column_offset + col_index_visible
                    row_index = int(rel_y // constant.instrument_item_height)
                    index_clicked = row_index + actual_col * visible_rows
                    if index_clicked < len(instrument_list):
                        current_instrument_index = index_clicked
                        fs.program_select(0, sfid, instrument_list[current_instrument_index]["bank"],
                        instrument_list[current_instrument_index]["program"])
                    instrument_dropdown_visible = False
                    continue
                elif layoutManager.instrument_button_rect.collidepoint((mx, my)):
                    instrument_dropdown_visible = False
                    continue
                else:
                    instrument_dropdown_visible = False

            else:
                # Toggle instrument dropdown when clicking the instrument button.
                if layoutManager.instrument_button_rect.collidepoint((mx, my)):
                    instrument_dropdown_visible = True
                    # Reset horizontal offset when opening.
                    instrument_column_offset = 0
                    continue

            # BPM slider handling (Row 1)
            if layoutManager.bpm_slider_visible and layoutManager.slider_rect.collidepoint((mx, my)):
                layoutManager.slider_dragging = True
                relative = (mx - layoutManager.slider_rect.x) / (layoutManager.slider_width - layoutManager.knob_width)
                relative = max(0, min(1, relative))
                BPM = int(layoutManager.min_bpm + relative * (layoutManager.max_bpm - layoutManager.min_bpm))
                layoutManager.bpm_text = str(BPM)
                update_timer()
                continue

            # BPM input box handling (Row 1)
            if layoutManager.bpm_input_rect.collidepoint((mx, my)):
                layoutManager.bpm_input_active = True
                layoutManager.bpm_slider_visible = True
                # Set flag so that the next digit clears previous text.
                layoutManager.clear_bpm_on_next_input = True
            else:
                # If click is inside grid area, toggle grid cell.
                if my < constant.grid_height:
                    col = mx // constant.cell_size
                    row = my // constant.cell_size
                    current_matrix = matrix_manager.get_current_matrix()
                    current_matrix[row][col] = not current_matrix[row][col]
                else:
                    # Control buttons in Row 1 (Major/Minor)
                    if layoutManager.major_button_rect.collidepoint((mx, my)):
                        scale_type = "Major"
                    elif layoutManager.minor_button_rect.collidepoint((mx, my)):
                        scale_type = "Minor"
                    # Control buttons in Row 3 (Export)
                    elif layoutManager.export_button_rect.collidepoint((mx, my)):
                        export_to_midi(matrix_manager, BPM, scale_type, root_key)
                    else:
                        # Key buttons (Row 2)
                        for key, rect in layoutManager.key_button_rects.items():
                            if rect.collidepoint((mx, my)):
                                root_key = key
                        layoutManager.bpm_input_active = False
                        layoutManager.bpm_slider_visible = False

        elif event.type == pygame.MOUSEBUTTONUP:
            layoutManager.slider_dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if layoutManager.slider_dragging and layoutManager.bpm_slider_visible:
                mx, _ = event.pos
                relative = (mx - layoutManager.slider_rect.x) / (layoutManager.slider_width -
                layoutManager.knob_width)
                relative = max(0, min(1, relative))
                BPM = int(layoutManager.min_bpm + relative *
                (layoutManager.max_bpm - layoutManager.min_bpm))
                layoutManager.bpm_text = str(BPM)
                update_timer()

        elif event.type == pygame.KEYDOWN and layoutManager.bpm_input_active:
            if event.key == pygame.K_RETURN:
                try:
                    new_bpm = int(layoutManager.bpm_text)
                    BPM = max(min(new_bpm,
                    layoutManager.max_bpm), layoutManager.min_bpm)
                except ValueError:
                    BPM = 120
                    layoutManager.bpm_text = "120"
                update_timer()
                layoutManager.bpm_input_active = False
                layoutManager.bpm_slider_visible = False
            elif event.key == pygame.K_BACKSPACE:
                layoutManager.bpm_text = layoutManager.bpm_text[:-1]
            elif event.unicode.isdigit():
                if layoutManager.clear_bpm_on_next_input:
                    layoutManager.bpm_text = event.unicode
                    layoutManager.clear_bpm_on_next_input = False
                else:
                    layoutManager.bpm_text += event.unicode

        elif event.type == COLUMN_EVENT:
            # Play notes from current column of current playing matrix
            current_matrix = matrix_manager.matrices[current_playing_matrix]
            for row in range(constant.grid_rows):
                if current_matrix[row][current_column]:
                    note = get_note_for_row(row, scale_type, root_key)
                    fs.noteon(0, note, 100)
                    active_notes.append((note, current_time_ms))
            
            # Update column and matrix
            current_column += 1
            if current_column >= constant.grid_cols:
                current_column = 0
                current_playing_matrix += 1
                if current_playing_matrix >= len(matrix_manager.matrices):
                    current_playing_matrix = 0
    
    # Clear screen and draw grid
    screen.fill((0, 0, 0))
    current_matrix = matrix_manager.get_current_matrix()
    for row in range(constant.grid_rows):
        for col in range(constant.grid_cols):
            rect = pygame.Rect(col * constant.cell_size, row * constant.cell_size,
            constant.cell_size, constant.cell_size)
            cell_color = (0, 255, 0) if current_matrix[row][col] else (50, 50, 50)
            if col == current_column and matrix_manager.current_matrix_index == current_playing_matrix:
                cell_color = (0, 200, 200) if current_matrix[row][col] else (100, 100, 100)
            pygame.draw.rect(screen, cell_color, rect)
            pygame.draw.rect(screen, (30, 30, 30), rect, 1)
    
    # Draw control area background
    pygame.draw.rect(screen, (30, 30, 30), (0, constant.grid_height, constant.width,
    constant.control_height + constant.matrix_control_height))    
    
    # ---------------------------
    # Draw Row 1: Matrix Navigation controls
    # ---------------------------
    drawManager.draw_matrix_navigation(screen, layoutManager.font, matrix_manager)

    # ---------------------------
    # Draw Row 2: Major/Minor and BPM controls
    # ---------------------------
    drawManager.draw_button(screen, layoutManager.major_button_rect,
    layoutManager.font, "Major", active=(scale_type=="Major"))
    drawManager.draw_button(screen, layoutManager.minor_button_rect,
    layoutManager.font, "Minor", active=(scale_type=="Minor"))
    
    # Draw BPM slider if visible
    if layoutManager.bpm_slider_visible:
        pygame.draw.rect(screen, (80, 80, 80), layoutManager.slider_rect)
        pygame.draw.rect(screen, (255, 255, 255), layoutManager.slider_rect, 2)
        knob_x = layoutManager.slider_rect.x + ((BPM - layoutManager.min_bpm) /
        (layoutManager.max_bpm - layoutManager.min_bpm)) * (layoutManager.slider_width - layoutManager.knob_width)
        knob_rect = pygame.Rect(knob_x, layoutManager.slider_rect.y, layoutManager.knob_width,
        layoutManager.slider_rect.height)
        pygame.draw.rect(screen, (200, 200, 0), knob_rect)
    
    # Draw BPM label and input box
    screen.blit(layoutManager.bpm_label_surf, layoutManager.bpm_label_rect)
    box_color = (150, 150, 150) if layoutManager.bpm_input_active else (100, 100, 100)
    pygame.draw.rect(screen, box_color, layoutManager.bpm_input_rect)
    pygame.draw.rect(screen, (255, 255, 255), layoutManager.bpm_input_rect, 2)
    bpm_surf = layoutManager.font.render(layoutManager.bpm_text, True, (255, 255, 255))
    bpm_rect_draw = bpm_surf.get_rect(center=layoutManager.bpm_input_rect.center)
    screen.blit(bpm_surf, bpm_rect_draw)
    
    # ---------------------------
    # Draw Row 3: Key buttons
    # ---------------------------
    for key, rect in layoutManager.key_button_rects.items():
        drawManager.draw_button(screen, rect, layoutManager.font, key, active=(key == root_key))
    
    # ---------------------------
    # Draw Row 4: Instrument and Export buttons
    # ---------------------------
    inst_name = instrument_list[current_instrument_index]["name"]
    if len(inst_name) > 14:
        inst_name = inst_name[:14] + "..."
    drawManager.draw_button(screen, layoutManager.instrument_button_rect,
    layoutManager.font, inst_name)
    drawManager.draw_button(screen, layoutManager.export_button_rect,
    layoutManager.font, "Export to MIDI")
    
    # Draw instrument dropdown if visible
    if instrument_dropdown_visible:
        if len(instrument_list) > constant.max_dropdown_rows * 2:
            visible_rows = constant.max_dropdown_rows
        else:
            visible_rows = math.ceil(len(instrument_list) / 2)
        visible_columns = 2
        total_columns = math.ceil(len(instrument_list) / visible_rows)
        dropdown_height = visible_rows * constant.instrument_item_height
        dropdown_width = visible_columns * constant.column_width
        dropdown_x = layoutManager.instrument_button_rect.right
        dropdown_y = layoutManager.instrument_button_rect.bottom - dropdown_height
        dropdown_rect = pygame.Rect(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
        pygame.draw.rect(screen, (50, 50, 50), dropdown_rect)
        pygame.draw.rect(screen, (255, 255, 255), dropdown_rect, 2)
        for col in range(instrument_column_offset, min(instrument_column_offset
        + visible_columns, total_columns)):
            for row in range(visible_rows):
                index = row + col * visible_rows
                if index >= len(instrument_list):
                    break
                item_rect = pygame.Rect(dropdown_x + (col - instrument_column_offset) * constant.column_width,
                                        dropdown_y + row * constant.instrument_item_height,
                                        constant.column_width, constant.instrument_item_height)
                if item_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(screen, (100, 100, 100), item_rect)
                instrument_name = instrument_list[index]["name"]
                if len(instrument_name) > 14:
                    instrument_name = instrument_name[:14] + "..."
                text_surf = layoutManager.font.render(instrument_name, True, (255, 255, 255))
                screen.blit(text_surf, (item_rect.x + 5, item_rect.y +
                (constant.instrument_item_height - text_surf.get_height()) // 2))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
fs.delete()
print("Pentatonica closed.")