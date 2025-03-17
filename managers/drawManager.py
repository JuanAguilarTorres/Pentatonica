import config.constants as constant
import pygame

# ---------------------------
# Matrix Navigation Controls
# ---------------------------
nav_button_width = 30
nav_button_height = 30
nav_button_spacing = 5
add_matrix_button_width = 30

# Position the matrix navigation controls above the main control area
nav_controls_y = constant.grid_height

# Calculate positions for matrix navigation buttons
def get_matrix_button_rect(index):
    x = 10 + index * (nav_button_width + nav_button_spacing)
    return pygame.Rect(x, nav_controls_y + 5, nav_button_width, nav_button_height)

def get_add_matrix_button_rect(matrix_manager):
    x = 10 + len(matrix_manager.matrices) * (nav_button_width + nav_button_spacing)
    return pygame.Rect(x, nav_controls_y + 5, add_matrix_button_width, nav_button_height)

def get_delete_matrix_button_rect(matrix_manager):
    x = 10 + (len(matrix_manager.matrices) + 1) * (nav_button_width + nav_button_spacing)
    return pygame.Rect(x, nav_controls_y + 5, nav_button_width, nav_button_height)

# ---------------------------
# Drawing Management
# ---------------------------

def draw_matrix_navigation(screen, font, matrix_manager):
    # Draw matrix buttons
    for i in range(len(matrix_manager.matrices)):
        rect = get_matrix_button_rect(i)
        color = (200, 200, 200) if i == matrix_manager.current_matrix_index else (100, 100, 100)
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, (255, 255, 255), rect, 2)
        text_surf = font.render(str(i + 1), True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)
    
    # Draw add matrix button
    add_rect = get_add_matrix_button_rect(matrix_manager)
    pygame.draw.rect(screen, (100, 100, 100), add_rect)
    pygame.draw.rect(screen, (255, 255, 255), add_rect, 2)
    text_surf = font.render("+", True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=add_rect.center)
    screen.blit(text_surf, text_rect)
    
    # Draw delete matrix button if last matrix can be deleted
    if matrix_manager.can_delete_last_matrix():
        delete_rect = get_delete_matrix_button_rect(matrix_manager)
        pygame.draw.rect(screen, (200, 50, 50), delete_rect)
        pygame.draw.rect(screen, (255, 255, 255), delete_rect, 2)
        text_surf = font.render("x", True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=delete_rect.center)
        screen.blit(text_surf, text_rect)

def draw_button(screen, rect, font, text, active=False):
    if len(text) > 14:
        text = text[:14] + "..."
    color = (200, 200, 200) if active else (100, 100, 100)
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, (255, 255, 255), rect, 2)
    text_surf = font.render(text, True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)
