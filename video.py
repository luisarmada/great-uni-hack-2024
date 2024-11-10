# video.py

import cv2
import time
import threading
import pyttsx3
import pygame
from openai import OpenAI
import base64
import os
import re

# Initialize pygame mixer
pygame.mixer.init()

# Initialize OpenAI client
client = OpenAI()

# Path configuration
current_dir = os.getcwd()
image_path = os.path.join(current_dir, "static", "media", "testmaths1.jpg")
sound_path = os.path.join(current_dir, "static", "media", "five_s_timer.mp3")
overlay_image_path = os.path.join(current_dir, "static", "media", "trump.png")

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Prepare API prompt
lengthQuiz = "5"
prompt = (
    "You are a professor tasked with creating a multiple-choice" + lengthQuiz +
    "question quiz for students, using only the image provided. Questions should be under 15 words. "
    "Do not preface the question with its number. The quiz must be formatted in this way: A question is printed, "
    "with the word QUESTION printed before it. Four options are printed, each one with the word OPTION printed before it. "
    "The correct option is printed, with the word CORRECT printed before it. The next question is printed with the word "
    "QUESTION printed before it. Given first question “question1”, with possible answers “aaa”, “bbb” ,  “ccc”, “ddd”, "
    "with “aaa” being correct, followed by the second question “question2” here is the correct exact example output: "
    "QUESTIONquestion 1 OPTIONaaa OPTIONbbb OPTIONccc OPTIONddd CORRECTaaa QUESTIONquestion 2. You can also use true "
    "or false questions, only if it is relevant. If doing this, you must follow the same rules of the formatting. "
    "Return only the quiz, after printing BEGINQUIZ. At the end of the quiz, print ENDQUIZ. Print all text on the same "
    "line. Do not, under any circumstances, print anything on a new line anywhere in your response. No new lines."
)

# Generate quiz using the OpenAI API
def generate_quiz():
    base64_image = encode_image(image_path)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                ],
            }
        ],
        max_tokens=300,
    )
    quiz_str = str(response.choices[0])
    return quiz_str

# Clean quiz text
def clean_quiz_text(raw_quiz_text):
    quiz_content_match = re.search(r"BEGINQUIZ\s*(.*?)\s*ENDQUIZ", raw_quiz_text, re.DOTALL | re.IGNORECASE)
    if quiz_content_match:
        return f"BEGINQUIZ\n{quiz_content_match.group(1).strip()}\nENDQUIZ"
    return ""

# Parse quiz text into structured questions
def parse_quiz_text(quiz_text):
    content_match = re.search(r"BEGINQUIZ\s*(.*?)\s*ENDQUIZ", quiz_text, re.DOTALL | re.IGNORECASE)
    if not content_match:
        return []

    content = content_match.group(1)
    questions_raw = re.findall(r"QUESTION\s*(.*?)\s*(OPTION.*?)(?=CORRECT)", content, re.DOTALL)
    correct_answers = re.findall(r"CORRECT\s*(.*?)\s*(?=QUESTION|$)", content, re.DOTALL)
    
    questions = []
    for idx, (question_text, options_block) in enumerate(questions_raw):
        question_text = question_text.strip()
        options = re.findall(r"OPTION\s*(.*?)\s*(?=OPTION|CORRECT|$)", options_block, re.DOTALL)
        options = [option.strip() for option in options]
        correct_answer_text = correct_answers[idx].strip()
        correct_answer_index = options.index(correct_answer_text) if correct_answer_text in options else None
        questions.append({
            "question": question_text,
            "options": options,
            "correct_answer_index": correct_answer_index
        })

    return questions

# Generate quiz data
raw_quiz_data = generate_quiz()
cleaned_quiz_str = clean_quiz_text(raw_quiz_data)
questions = parse_quiz_text(cleaned_quiz_str)

# Control variables for the quiz
current_question_index = 0
show_progress_bar = False
display_correct_only = False
show_overlay_image = False
progress_bar_start_time = 0
progress_bar_duration = 5

# Load overlay image and set size
overlay_image = cv2.imread(overlay_image_path, -1)
overlay_image = cv2.resize(overlay_image, (250, 200))

# Function to handle TTS
def speak_text(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()

# Function to play the timer sound
def play_timer_sound():
    pygame.mixer.music.load(sound_path)
    pygame.mixer.music.play()

# Main function to handle the quiz flow
def read_question_and_answer():
    global show_progress_bar, display_correct_only, progress_bar_start_time, show_overlay_image, current_question_index

    while current_question_index < len(questions):
        question_data = questions[current_question_index]
        question_text = question_data["question"]
        correct_answer_index = question_data["correct_answer_index"]
        correct_answer_text = question_data["options"][correct_answer_index]

        # Speak question text directly
        show_overlay_image = True
        speak_text(question_text)  # This will block until TTS finishes
        time.sleep(1)  # Small delay after TTS

        # Start the progress bar and play timer sound
        show_overlay_image = False
        show_progress_bar = True
        progress_bar_start_time = time.time()
        play_timer_sound()  # Start timer sound
        time.sleep(progress_bar_duration)

        # Show correct answer and speak it directly
        show_progress_bar = False
        display_correct_only = True
        speak_text(f"The correct answer is {correct_answer_text}")
        time.sleep(1)  # Small delay after TTS

        # Reset flags for next question
        display_correct_only = False
        current_question_index += 1

# Function to draw a rounded rectangle with an optional border
def draw_rounded_rectangle(frame, x_start, y_start, width, height, color, radius=10, thickness=-1):
    cv2.rectangle(frame, (x_start + radius, y_start), (x_start + width - radius, y_start + height), color, thickness)
    cv2.circle(frame, (x_start + radius, y_start + radius), radius, color, thickness)
    cv2.circle(frame, (x_start + width - radius, y_start + radius), radius, color, thickness)
    cv2.circle(frame, (x_start + radius, y_start + height - radius), radius, color, thickness)
    cv2.circle(frame, (x_start + width - radius, y_start + height - radius), radius, color, thickness)
    cv2.rectangle(frame, (x_start, y_start + radius), (x_start + width, y_start + height - radius), color, thickness)
    return frame

# Generate video frames for streaming
def generate_frames():
    global cap, show_progress_bar, display_correct_only, current_question_index, show_overlay_image

    cap = cv2.VideoCapture('static/media/mc_parkour_lq.mp4')
    threading.Thread(target=read_question_and_answer).start()

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        if current_question_index < len(questions):
            question_data = questions[current_question_index]
            question_text = question_data["question"]
            options = question_data["options"]
            correct_answer_index = question_data["correct_answer_index"]

            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            question_color = (255, 255, 255)
            options_color = (0, 255, 255)
            correct_option_color = (0, 255, 0)
            outline_color = (0, 0, 0)
            thickness = 2
            outline_thickness = thickness + 2
            frame_height, frame_width = frame.shape[:2]
            line_height = 40
            x = 50

            question_num_text = f"Question {current_question_index + 1} out of {len(questions)}"
            question_num_y = frame_height // 2 - line_height * 3
            cv2.putText(frame, question_num_text, (x, question_num_y), font, font_scale, outline_color, outline_thickness)
            cv2.putText(frame, question_num_text, (x, question_num_y), font, font_scale, question_color, thickness)

            question_y = frame_height // 2 - line_height * 2
            cv2.putText(frame, question_text, (x, question_y), font, font_scale, outline_color, outline_thickness)
            cv2.putText(frame, question_text, (x, question_y), font, font_scale, question_color, thickness)

            y = question_y
            for i, option in enumerate(options):
                y += line_height
                if display_correct_only and i != correct_answer_index:
                    continue
                option_text = f"{chr(65 + i)}) {option}"
                color = correct_option_color if display_correct_only and i == correct_answer_index else options_color
                cv2.putText(frame, option_text, (x, y), font, font_scale, outline_color, outline_thickness)
                cv2.putText(frame, option_text, (x, y), font, font_scale, color, thickness)

            if show_overlay_image:
                overlay_y = frame_height - overlay_image.shape[0]
                overlay_x = frame_width - overlay_image.shape[1]
                overlay_image_with_alpha(frame, overlay_image, overlay_x, overlay_y)

            if show_progress_bar:
                progress_bar_width_ratio = 0.4
                progress_bar_width = int(frame_width * progress_bar_width_ratio)
                elapsed_time = time.time() - progress_bar_start_time
                progress = max(0, 1 - elapsed_time / progress_bar_duration)
                remaining_width = int(progress_bar_width * progress)
                bar_height = 20
                bar_x_start = (frame_width - progress_bar_width) // 2
                bar_y_start = y + line_height + 20

                draw_rounded_rectangle(frame, bar_x_start - 2, bar_y_start - 2, progress_bar_width + 4, bar_height + 4, (255, 255, 255), radius=10, thickness=2)
                draw_rounded_rectangle(frame, bar_x_start, bar_y_start, progress_bar_width, bar_height, (0, 0, 0), radius=10, thickness=-1)
                if remaining_width > 0:
                    draw_rounded_rectangle(frame, bar_x_start, bar_y_start, remaining_width, bar_height, (0, 0, 255), radius=10, thickness=-1)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

# Helper function to handle overlay image transparency
def overlay_image_with_alpha(background, overlay, x, y):
    overlay_rgb = overlay[..., :3]
    overlay_alpha = overlay[..., 3:] / 255.0
    h, w = overlay_rgb.shape[:2]
    roi = background[y:y+h, x:x+w]
    background[y:y+h, x:x+w] = (overlay_rgb * overlay_alpha + roi * (1 - overlay_alpha)).astype(background.dtype)
