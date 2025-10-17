import pygame
import sys
import random
import time
import os

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)
FONT = pygame.font.Font(None, 74)
SMALL_FONT = pygame.font.Font(None, 36)

# Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Reaction Time Tester ⏱️")
clock = pygame.time.Clock()

# Load sound
pygame.mixer.init()
try:
    beep_sound = pygame.mixer.Sound("beep.wav")
except:
    beep_sound = None

# Score file
SCORE_FILE = "best_score.txt"

def get_best_score():
    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, "r") as f:
            try:
                return float(f.read().strip())
            except ValueError:
                return None
    return None

def save_best_score(score):
    with open(SCORE_FILE, "w") as f:
        f.write(str(score))

# Game states
waiting_to_start = True
waiting_for_green = False
green_displayed = False
reaction_time = None
start_time = 0
false_start = False
best_score = get_best_score()

def get_random_delay():
    return random.uniform(2, 5)

def draw_text(text, font, color, y_offset=0):
    render = font.render(text, True, color)
    rect = render.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    screen.blit(render, rect)

def main():
    global waiting_to_start, waiting_for_green, green_displayed, reaction_time, start_time, false_start, best_score

    running = True
    delay = get_random_delay()
    timer_start = None

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if waiting_to_start:
                    waiting_to_start = False
                    waiting_for_green = True
                    timer_start = time.time()
                    delay = get_random_delay()
                    reaction_time = None
                    false_start = False

                elif waiting_for_green:
                    false_start = True
                    waiting_for_green = False

                elif green_displayed:
                    reaction_time = (time.time() - start_time) * 1000  # in ms
                    green_displayed = False
                    waiting_to_start = True
                    if not best_score or reaction_time < best_score:
                        best_score = reaction_time
                        save_best_score(best_score)

        # Logic
        if waiting_for_green:
            screen.fill(RED)
            draw_text("WAIT FOR GREEN!", SMALL_FONT, WHITE)
            if (time.time() - timer_start) >= delay:
                waiting_for_green = False
                green_displayed = True
                start_time = time.time()
                if beep_sound:
                    beep_sound.play()

        elif green_displayed:
            screen.fill(GREEN)
            draw_text("CLICK NOW!", SMALL_FONT, BLACK)

        elif false_start:
            screen.fill(WHITE)
            draw_text("Too soon! ⚠️", FONT, RED)
            draw_text("Click to try again.", SMALL_FONT, BLACK, 60)

        elif reaction_time:
            screen.fill(WHITE)
            draw_text(f"Your Reaction Time: {int(reaction_time)} ms", FONT, BLACK)
            if best_score:
                draw_text(f"Best: {int(best_score)} ms", SMALL_FONT, GREEN, 80)
            draw_text("Click to try again.", SMALL_FONT, BLACK, 130)

        elif waiting_to_start:
            draw_text("Reaction Time Tester ⏱️", FONT, BLACK)
            if best_score:
                draw_text(f"Best: {int(best_score)} ms", SMALL_FONT, GREEN, -60)
            draw_text("Click to Start", SMALL_FONT, BLACK, 60)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
