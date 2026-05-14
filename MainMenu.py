import pygame
import sys
import subprocess

def draw_button(screen, text, font, pos, default_color, hover_color):
    mouse_pos = pygame.mouse.get_pos()
    text_surf = font.render(text, True, default_color)
    text_rect = text_surf.get_rect(topleft=pos)
    is_hovering = text_rect.collidepoint(mouse_pos)

    # Change text color when hovering
    color = hover_color if is_hovering else default_color
    text_surf = font.render(text, True, color)

    display_text = text
    if is_hovering:
        display_text = "> " + text

    text_surf = font.render(display_text, True, color)
    screen.blit(text_surf, pos)
    return text_rect, is_hovering

def main_menu():
    pygame.init()
    pygame.mixer.music.load("MainMenuTheme.mp3")
    pygame.mixer.music.play(-1) # -1 Will make it loop forever
    # click_sound = pygame.mixer.Sound("click.wav")
    # click_sound.play()

    # --- Menu Settings ---
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game Launcher")
    
    # Background
    background = pygame.image.load("BackgroundMenu.png").convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    # Font
    font = pygame.font.SysFont("Courier New", 48)
    title_font = pygame.font.SysFont("Courier New", 72)
    
    # Colors
    BG_COLOR = (30, 30, 40)
    TEXT_COLOR = (255, 255, 255)
    
    # Button Rectangles (X, Y, Width, Height)
    play_pos = (60, HEIGHT/2.5)
    quit_pos = (60, HEIGHT/2)

    running = True
    while running:
        # screen.fill(BG_COLOR)
        screen.blit(background, (0, 0))
        
        # Transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        # RGBA
        overlay_color = (0, 0, 0, 200) #0 - 255

        # Polygon points
        cut_polygon = [
            (0, 0), # top left
            (WIDTH/1.3, 0), # top right cut point
            (WIDTH/2, HEIGHT), # bottom left cut point
            (0, HEIGHT) # bottom left
        ]

        # Polygon Outline
        pygame.draw.line(
            screen,
            (180, 60, 60), # RGB color
            (WIDTH/1.3, 0), # Line start x, y
            (WIDTH/2, HEIGHT), # Line end x, y
            3 # Line thickness
        )

        pygame.draw.polygon(overlay, overlay_color, cut_polygon)
        screen.blit(overlay, (0, 0))

        # Draw Title
        title_surf = title_font.render("PESAWAT NGUDUD", True, TEXT_COLOR)
        title_rect = title_surf.get_rect(topleft=(60, HEIGHT//4))
        screen.blit(title_surf, title_rect)
        
        # Draw Buttons
        play_btn, _ = draw_button(
            screen,
            "PLAY",
            font,
            play_pos,
            TEXT_COLOR,
            (255, 60, 60)
        )

        quit_btn, _ = draw_button(
            screen,
            "QUIT",
            font,
            quit_pos,
            TEXT_COLOR,
            (255, 60, 60)
        )

        pygame.display.flip()
        
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # PLAY BUTTON CLICKED
                if play_btn.collidepoint(event.pos):
                    # 1. Quit the menu's pygame instance to free up the screen/audio
                    pygame.quit()
                    
                    # 2. Launch your existing game untouched
                    # Replace "your_game.py" with the exact name of your game file!
                    subprocess.run([sys.executable, "Test_1.py"])
                    
                    # 3. When the game is closed, re-initialize pygame for the menu
                    pygame.init()
                    screen = pygame.display.set_mode((WIDTH, HEIGHT))
                    pygame.display.set_caption("Game Launcher")
                    pygame.mixer.music.load("MainMenuTheme.mp3")
                    pygame.mixer.music.play(-1)

                    # 4. Re-initiallize font (Prevent crash DO NOT REMOVE)
                    font = pygame.font.SysFont("Courier New", 48)
                    title_font = pygame.font.SysFont("Courier New", 72)
                
                # QUIT BUTTON CLICKED
                elif quit_btn.collidepoint(event.pos):
                    running = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main_menu()