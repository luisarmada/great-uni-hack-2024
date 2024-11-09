import cv2
import time
import threading
import pyttsx3
import pygame

# Initialize the TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Adjust the rate of speech

# Initialize Pygame for audio playback
pygame.mixer.init()

# Define a list of questions with options and correct answer index
questions = [
    {"question": "What is the powerhouse of the cell?", "options": ["Mitochondria", "Heart", "Chlorophyll", "Buttocks"], "correct_answer_index": 0},
    {"question": "Which planet is known as the Red Planet?", "options": ["Venus", "Earth", "Mars", "Jupiter"], "correct_answer_index": 2},
    {"question": "What is the chemical symbol for water?", "options": ["O2", "H2O", "CO2", "NaCl"], "correct_answer_index": 1},
]
option_prefixes = ["A)", "B)", "C)", "D)"]  # Option letters

# Load the overlay image with transparency (using -1 to include the alpha channel)
overlay_image = cv2.imread("media/trump.png", -1)
overlay_height, overlay_width = 200, 250  # Set larger size for the overlay image
overlay_image = cv2.resize(overlay_image, (overlay_width, overlay_height))

# Open the video file
cap = cv2.VideoCapture('media/mc_parkour.mp4')

# Initialize question index and timers
current_question_index = 0
display_correct_only = False
show_progress_bar = False
show_overlay_image = True  # Controls when to show the overlay image
progress_bar_start_time = 0  # Dedicated timer for the progress bar

# Progress bar settings
progress_bar_duration = 5      # Progress bar duration (5 seconds)
progress_bar_width_ratio = 0.4  # 40% of the frame width

def draw_rounded_rectangle(frame, x_start, y_start, width, height, color, radius=10, thickness=-1):
    """Draws a rounded rectangle on the frame."""
    cv2.rectangle(frame, (x_start + radius, y_start), (x_start + width - radius, y_start + height), color, thickness)
    cv2.circle(frame, (x_start + radius, y_start + radius), radius, color, thickness)
    cv2.circle(frame, (x_start + width - radius, y_start + radius), radius, color, thickness)
    cv2.circle(frame, (x_start + radius, y_start + height - radius), radius, color, thickness)
    cv2.circle(frame, (x_start + width - radius, y_start + height - radius), radius, color, thickness)
    cv2.rectangle(frame, (x_start, y_start + radius), (x_start + width, y_start + height - radius), color, thickness)
    return frame

def overlay_image_with_alpha(background, overlay, x, y):
    """Overlay an image with transparency on top of a background image."""
    overlay_rgb = overlay[..., :3]  # Color channels
    overlay_alpha = overlay[..., 3:] / 255.0  # Alpha channel (0-1 range)

    # Define the region of interest (ROI) in the background
    h, w = overlay_rgb.shape[:2]
    roi = background[y:y+h, x:x+w]

    # Blend overlay and background based on alpha channel
    background[y:y+h, x:x+w] = (overlay_rgb * overlay_alpha + roi * (1 - overlay_alpha)).astype(background.dtype)

def speak_text(text):
    """Function to speak text using TTS"""
    engine.say(text)
    engine.runAndWait()

def play_timer_audio():
    """Plays the five-second timer audio"""
    pygame.mixer.music.load("media/five_s_timer.mp3")
    pygame.mixer.music.play()

def read_question_and_answer():
    """Announces the question, shows progress bar, and reads the answer"""
    global show_progress_bar, display_correct_only, progress_bar_start_time, show_overlay_image

    # Read the question
    question_data = questions[current_question_index]
    question_text = question_data["question"]
    correct_answer_index = question_data["correct_answer_index"]
    correct_answer_text = f"The correct answer is {questions[current_question_index]['options'][correct_answer_index]}."

    # Show overlay image and speak the question
    show_overlay_image = True
    speak_text(question_text)

    # Wait 1 second, then show the progress bar and play the timer audio
    time.sleep(1)
    show_progress_bar = True
    show_overlay_image = False  # Hide the overlay image when progress bar starts
    progress_bar_start_time = time.time()  # Start the timer for the progress bar
    threading.Thread(target=play_timer_audio).start()  # Play audio in a separate thread

    # Wait for the progress bar to complete (5 seconds)
    time.sleep(progress_bar_duration)
    show_progress_bar = False

    # Show only the correct answer and read it
    display_correct_only = True
    speak_text(correct_answer_text)

    # Wait 3 seconds before moving to the next question
    time.sleep(3)
    display_correct_only = False
    next_question()

def next_question():
    """Move to the next question and reset variables"""
    global current_question_index
    current_question_index = (current_question_index + 1) % len(questions)
    threading.Thread(target=read_question_and_answer).start()

# Start TTS for the first question
threading.Thread(target=read_question_and_answer).start()

while True:
    # Capture frames in the video
    ret, frame = cap.read()
    if not ret:
        break  # Exit loop if video ends

    # Get the current question and options
    question_data = questions[current_question_index]
    question_text = question_data["question"]
    options = question_data["options"]
    correct_answer_index = question_data["correct_answer_index"]

    # Define font, colors, and outline color
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    question_color = (255, 255, 255)  # White color for the question
    options_color = (0, 255, 255)     # Yellow color for the options
    correct_option_color = (0, 255, 0)  # Green for the correct answer after reveal
    outline_color = (0, 0, 0)         # Black outline color
    thickness = 2
    outline_thickness = thickness + 2  # Slightly thicker for outline effect

    # Calculate position to center the text
    frame_height, frame_width = frame.shape[:2]
    line_height = 40  # Spacing between lines
    x = 50  # Left padding for the text

    # Display "Question x out of y" text above the question
    question_num_text = f"Question {current_question_index + 1} out of {len(questions)}"
    question_num_y = frame_height // 2 - line_height * 3  # Position above the question text
    cv2.putText(frame, question_num_text, (x, question_num_y), font, font_scale, outline_color, outline_thickness)
    cv2.putText(frame, question_num_text, (x, question_num_y), font, font_scale, question_color, thickness)

    # Display question with outline and white color
    question_y = frame_height // 2 - line_height * 2  # Center question and options on screen
    cv2.putText(frame, question_text, (x, question_y), font, font_scale, outline_color, outline_thickness)
    cv2.putText(frame, question_text, (x, question_y), font, font_scale, question_color, thickness)

    # Display options with prefix letters, outline, and colors
    y = question_y
    for i, option in enumerate(options):
        y += line_height
        if display_correct_only:
            if i == correct_answer_index:
                option_text = f"{option_prefixes[i]} {option}"
                cv2.putText(frame, option_text, (x, y), font, font_scale, outline_color, outline_thickness)
                cv2.putText(frame, option_text, (x, y), font, font_scale, correct_option_color, thickness)
        else:
            option_text = f"{option_prefixes[i]} {option}"
            cv2.putText(frame, option_text, (x, y), font, font_scale, outline_color, outline_thickness)
            cv2.putText(frame, option_text, (x, y), font, font_scale, options_color, thickness)

    # Display the overlay image in the bottom-right corner when reading the question
    if show_overlay_image:
        overlay_y = frame_height - overlay_height  # 0-pixel margin from bottom
        overlay_x = frame_width - overlay_width - 10    # 10-pixel margin from right
        overlay_image_with_alpha(frame, overlay_image, overlay_x, overlay_y)

    # Display the progress bar if the flag is set
    if show_progress_bar:
        progress_bar_width = int(frame_width * progress_bar_width_ratio)
        elapsed_time = time.time() - progress_bar_start_time
        progress = max(0, 1 - (elapsed_time / progress_bar_duration))
        remaining_width = int(progress_bar_width * progress)

        bar_height = 20
        bar_x_start = (frame_width - progress_bar_width) // 2
        bar_y_start = y + line_height + 20

        draw_rounded_rectangle(frame, bar_x_start - 2, bar_y_start - 2, progress_bar_width + 4, bar_height + 4, (255, 255, 255), radius=10, thickness=2)
        draw_rounded_rectangle(frame, bar_x_start, bar_y_start, progress_bar_width, bar_height, (0, 0, 0), radius=10, thickness=-1)

        if remaining_width > 0:
            draw_rounded_rectangle(frame, bar_x_start, bar_y_start, remaining_width, bar_height, (0, 0, 255), radius=10, thickness=-1)

    cv2.imshow('video', frame)

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
pygame.mixer.quit()
cv2.destroyAllWindows()
