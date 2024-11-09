import cv2
import time
import threading
import pyttsx3

# Initialize the TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Adjust the rate of speech

# Define a list of questions with options and correct answer index
questions = [
    {"question": "What is the powerhouse of the cell?", "options": ["Mitochondria", "Heart", "Chlorophyll", "Buttocks"], "correct_answer_index": 0},
    {"question": "Which planet is known as the Red Planet?", "options": ["Venus", "Earth", "Mars", "Jupiter"], "correct_answer_index": 2},
    {"question": "What is the chemical symbol for water?", "options": ["O2", "H2O", "CO2", "NaCl"], "correct_answer_index": 1},
]
option_prefixes = ["A)", "B)", "C)", "D)"]  # Option letters

# Open the video file
cap = cv2.VideoCapture('media/mc_parkour.mp4')

# Initialize question index and timers
current_question_index = 0
display_correct_only = False
show_progress_bar = False
progress_bar_start_time = 0  # Dedicated timer for the progress bar

# Progress bar settings
progress_bar_duration = 5      # Progress bar duration (5 seconds)
progress_bar_width_ratio = 0.4  # 40% of the frame width

def draw_rounded_rectangle(frame, x_start, y_start, width, height, color, radius=10, thickness=-1):
    """Draws a rounded rectangle on the frame."""
    # Draw the central rectangle (without rounded corners)
    cv2.rectangle(frame, (x_start + radius, y_start), (x_start + width - radius, y_start + height), color, thickness)
    
    # Draw circles for rounded edges
    cv2.circle(frame, (x_start + radius, y_start + radius), radius, color, thickness)
    cv2.circle(frame, (x_start + width - radius, y_start + radius), radius, color, thickness)
    cv2.circle(frame, (x_start + radius, y_start + height - radius), radius, color, thickness)
    cv2.circle(frame, (x_start + width - radius, y_start + height - radius), radius, color, thickness)
    
    # Draw rectangles for the straight parts
    cv2.rectangle(frame, (x_start, y_start + radius), (x_start + width, y_start + height - radius), color, thickness)
    return frame

def speak_text(text):
    """Function to speak text using TTS"""
    engine.say(text)
    engine.runAndWait()

def read_question_and_answer():
    """Announces the question, shows progress bar, and reads the answer"""
    global show_progress_bar, display_correct_only, progress_bar_start_time

    # Read the question
    question_data = questions[current_question_index]
    question_text = question_data["question"]
    correct_answer_index = question_data["correct_answer_index"]
    correct_answer_text = f"The correct answer is {questions[current_question_index]['options'][correct_answer_index]}."

    # Speak the question only
    speak_text(question_text)

    # Wait 1 second, then show the progress bar
    time.sleep(1)
    show_progress_bar = True
    progress_bar_start_time = time.time()  # Start the timer for the progress bar

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
    cv2.putText(frame, question_num_text, (x, question_num_y), font, font_scale, outline_color, outline_thickness)  # Black outline
    cv2.putText(frame, question_num_text, (x, question_num_y), font, font_scale, question_color, thickness)  # White text

    # Display question with outline and white color
    question_y = frame_height // 2 - line_height * 2  # Center question and options on screen
    cv2.putText(frame, question_text, (x, question_y), font, font_scale, outline_color, outline_thickness)  # Black outline
    cv2.putText(frame, question_text, (x, question_y), font, font_scale, question_color, thickness)  # White text

    # Display options with prefix letters, outline, and colors
    y = question_y
    for i, option in enumerate(options):
        y += line_height
        if display_correct_only:
            # Show only the correct answer option
            if i == correct_answer_index:
                option_text = f"{option_prefixes[i]} {option}"
                cv2.putText(frame, option_text, (x, y), font, font_scale, outline_color, outline_thickness)
                cv2.putText(frame, option_text, (x, y), font, font_scale, correct_option_color, thickness)
        else:
            # Display all options with yellow color before the reveal
            option_text = f"{option_prefixes[i]} {option}"
            cv2.putText(frame, option_text, (x, y), font, font_scale, outline_color, outline_thickness)
            cv2.putText(frame, option_text, (x, y), font, font_scale, options_color, thickness)

    # Display the progress bar if the flag is set
    if show_progress_bar:
        # Calculate progress bar width (40% of the frame width)
        progress_bar_width = int(frame_width * progress_bar_width_ratio)

        # Calculate the remaining width of the progress bar based on elapsed time
        elapsed_time = time.time() - progress_bar_start_time
        progress = max(0, 1 - (elapsed_time / progress_bar_duration))
        remaining_width = int(progress_bar_width * progress)

        # Position the progress bar slightly below the last option and centered
        bar_height = 20
        bar_x_start = (frame_width - progress_bar_width) // 2  # Center the progress bar
        bar_y_start = y + line_height + 20  # Slightly below the last option

        # Draw the rounded progress bar
        draw_rounded_rectangle(frame, bar_x_start - 2, bar_y_start - 2, progress_bar_width + 4, bar_height + 4, (255, 255, 255), radius=10, thickness=2)  # White border
        draw_rounded_rectangle(frame, bar_x_start, bar_y_start, progress_bar_width, bar_height, (0, 0, 0), radius=10, thickness=-1)  # Black background

        # Draw the red rounded progress bar fill based on remaining width
        if remaining_width > 0:
            draw_rounded_rectangle(frame, bar_x_start, bar_y_start, remaining_width, bar_height, (0, 0, 255), radius=10, thickness=-1)

    # Display the frame
    cv2.imshow('video', frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
