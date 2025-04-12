import pygame
import csv
import json
import random
import os

# Initialize Pygame and create window
pygame.init()
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flashcard Quiz")
font = pygame.font.Font(None, 32)  # default font, size 32
clock = pygame.time.Clock()

# Colors for convenience
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED   = (200, 0, 0)

# File paths
FLASHCARD_CSV = "flashcards.csv"
DATA_FILE = "user_data.json"

# Load flashcards from CSV
flashcards = []
if os.path.exists(FLASHCARD_CSV):
    with open(FLASHCARD_CSV, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 2:
                question = row[0].strip()
                answer = row[1].strip()
                # Remove wrapping quotes if present
                if question.startswith('"') and question.endswith('"'):
                    question = question[1:-1]
                if answer.startswith('"') and answer.endswith('"'):
                    answer = answer[1:-1]
                flashcards.append((question, answer))
else:
    print(f"Error: {FLASHCARD_CSV} not found.")
    pygame.quit()
    exit()

# Load or initialize user performance data from JSON
user_data = {}
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r') as f:
        try:
            user_data = json.load(f)
        except json.JSONDecodeError:
            user_data = {}
else:
    # If file doesn't exist, we'll create it later when saving
    user_data = {}

# Helper function to save user_data to JSON file
def save_user_data():
    with open(DATA_FILE, 'w') as f:
        json.dump(user_data, f, indent=4)

# Initial state
mode = "NAME"        # modes: "NAME", "QUESTION", "FEEDBACK"
name_input = ""      # to store typed name
answer_input = ""    # to store typed answer for current question
current_question = None
current_answer = None
feedback_message = ""

# Prompt texts
name_prompt = "Enter your name: "
answer_prompt = "Your answer: "

running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Global key controls (works in any mode)
            if event.key == pygame.K_ESCAPE:
                running = False
                continue  # skip other handling
            # Handle input for NAME mode
            if mode == "NAME":
                if event.key == pygame.K_RETURN:  # Enter pressed -> finish name input
                    if name_input.strip() != "":
                        player_name = name_input.strip()
                        # Initialize data for new user if not present
                        if player_name not in user_data:
                            user_data[player_name] = {}
                        # Ensure all flashcards have an entry for this user
                        for q, a in flashcards:
                            if q not in user_data[player_name]:
                                user_data[player_name][q] = {"correct": 0, "wrong": 0}
                        # Move to question mode
                        mode = "QUESTION"
                        # Pick the first question
                        answer_input = ""  # reset answer input
                        # Determine next question based on performance weights
                        stats = user_data[player_name]
                        weights = []
                        for q, a in flashcards:
                            c = stats[q]["correct"]
                            w = stats[q]["wrong"]
                            weight = w - c + 1
                            if weight < 1:
                                weight = 1
                            weights.append(weight)
                        idx = random.choices(range(len(flashcards)), weights=weights, k=1)[0]
                        current_question, current_answer = flashcards[idx]
                    # (If name_input is empty, we stay in NAME mode until a name is entered)
                elif event.key == pygame.K_BACKSPACE:
                    # Remove last character
                    name_input = name_input[:-1]
                else:
                    # Append character to name (ignore special keys)
                    char = event.unicode
                    if char != "":
                        name_input += char
            # Handle input for QUESTION mode (typing the answer)
            elif mode == "QUESTION":
                if event.key == pygame.K_RETURN:  # submit the answer
                    if current_question is not None:
                        user_answer = answer_input.strip()
                        # Check answer (case-insensitive)
                        if user_answer.lower() == current_answer.strip().lower():
                            feedback_message = "Correct! 🙂"
                            # Update stats
                            user_data[player_name][current_question]["correct"] += 1
                        else:
                            feedback_message = f"Incorrect! The correct answer was: {current_answer}"
                            # Update stats
                            user_data[player_name][current_question]["wrong"] += 1
                        # Save updated stats to file
                        save_user_data()
                        # Switch to feedback mode
                        mode = "FEEDBACK"
                        answer_input = ""  # reset answer input for next question
                elif event.key == pygame.K_BACKSPACE:
                    # Remove last char from answer input
                    answer_input = answer_input[:-1]
                else:
                    # Add character to answer input
                    char = event.unicode
                    if char != "":
                        answer_input += char
            # Handle input for FEEDBACK mode (waiting for user to continue)
            elif mode == "FEEDBACK":
                # Any key (or specifically Enter) will continue to next question
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE or event.key == pygame.K_RIGHT:
                    # Choose next flashcard based on updated stats
                    stats = user_data[player_name]
                    weights = []
                    for q, a in flashcards:
                        c = stats[q]["correct"]
                        w = stats[q]["wrong"]
                        weight = w - c + 1
                        if weight < 1:
                            weight = 1
                        weights.append(weight)
                    idx = random.choices(range(len(flashcards)), weights=weights, k=1)[0]
                    current_question, current_answer = flashcards[idx]
                    # Switch back to question mode for the next flashcard
                    mode = "QUESTION"
                    feedback_message = ""  # clear previous feedback

    # Drawing
    screen.fill(WHITE)  # clear screen with white background
    if mode == "NAME":
        # Display name prompt and the current input for name
        prompt_surface = font.render(name_prompt, True, BLACK)
        screen.blit(prompt_surface, (50, 200))
        name_surface = font.render(name_input + "|", True, BLACK)  # '|' as a cursor
        screen.blit(name_surface, (50 + prompt_surface.get_width() + 5, 200))
    elif mode == "QUESTION":
        # Display the current question and answer prompt
        question_text = f"Question: {current_question}"
        question_surf = font.render(question_text, True, BLACK)
        screen.blit(question_surf, (50, 150))
        # Show the answer prompt and current typed answer
        answer_text = answer_prompt + answer_input + "|"
        answer_surf = font.render(answer_text, True, BLACK)
        screen.blit(answer_surf, (50, 200))
    elif mode == "FEEDBACK":
        # Show the question and the feedback message
        question_text = f"Question: {current_question}"
        question_surf = font.render(question_text, True, BLACK)
        screen.blit(question_surf, (50, 150))
        feedback_surf = font.render(feedback_message, True, (0, 0, 255) if feedback_message.startswith("Correct") else RED)
        screen.blit(feedback_surf, (50, 200))
        continue_msg = font.render("Press Enter to continue...", True, BLACK)
        screen.blit(continue_msg, (50, 250))
    # Update the display
    pygame.display.flip()
    clock.tick(30)  # limit to 30 frames per second

# Clean up Pygame on exit
pygame.quit()
