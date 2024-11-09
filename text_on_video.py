import cv2
import time

# Define question and options
question = ["What is the powerhouse of the cell?", "Mitochondria", "Heart", "Chlorophyll", "Buttocks"]
option_prefixes = ["A)", "B)", "C)", "D)"]  # Option letters
correct_answer_index = 1  # Correct answer is "Mitochondria"

# Open the video file
cap = cv2.VideoCapture('media/mc_parkour.mp4')

# Define the start time
start_time = time.time()
display_correct_only = False  # Flag to control when only the correct answer is displayed

# Progress bar settings
progress_bar_start_time = 5    # Progress bar appears after 5 seconds
progress_bar_duration = 5      # Progress bar duration (5 seconds, from 5 to 10 seconds)
progress_bar_width_ratio = 0.4  # 40% of the frame width

while True:
    # Capture frames in the video
    ret, frame = cap.read()
    if not ret:
        break  # Exit loop if video ends

    # Calculate the time elapsed
    elapsed_time = time.time() - start_time

    # After 10 seconds, set flag to display only the correct answer
    if elapsed_time > 10:
        display_correct_only = True

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

    # Display question with outline and white color
    y = frame_height // 2 - line_height * 2  # Center question and options on screen
    cv2.putText(frame, question[0], (x, y), font, font_scale, outline_color, outline_thickness)  # Black outline
    cv2.putText(frame, question[0], (x, y), font, font_scale, question_color, thickness)  # White text

    # Display options with prefix letters, outline, and colors
    for i, option in enumerate(question[1:], start=1):
        y += line_height
        if display_correct_only:
            # Show only the correct answer option
            if i == correct_answer_index:
                option_text = f"{option_prefixes[i - 1]} {option}"
                cv2.putText(frame, option_text, (x, y), font, font_scale, outline_color, outline_thickness)
                cv2.putText(frame, option_text, (x, y), font, font_scale, correct_option_color, thickness)
        else:
            # Display all options with yellow color before the reveal
            option_text = f"{option_prefixes[i - 1]} {option}"
            cv2.putText(frame, option_text, (x, y), font, font_scale, outline_color, outline_thickness)
            cv2.putText(frame, option_text, (x, y), font, font_scale, options_color, thickness)

    # Display the progress bar if between 5 and 10 seconds
    if 5 <= elapsed_time <= 10:
        # Calculate progress bar width (40% of the frame width)
        progress_bar_width = int(frame_width * progress_bar_width_ratio)

        # Calculate the remaining width of the progress bar
        remaining_width = int(progress_bar_width * (1 - (elapsed_time - progress_bar_start_time) / progress_bar_duration))

        # Position the progress bar slightly below the last option and centered
        bar_height = 20
        bar_x_start = (frame_width - progress_bar_width) // 2  # Center the progress bar
        bar_y_start = y + line_height + 20  # Slightly below the last option

        # Draw the background of the progress bar (black)
        cv2.rectangle(frame, (bar_x_start, bar_y_start), (bar_x_start + progress_bar_width, bar_y_start + bar_height), (0, 0, 0), -1)

        # Draw the progress bar fill (red) with rounded edges
        bar_color = (0, 0, 255)  # Red color for the progress bar
        cv2.rectangle(frame, (bar_x_start, bar_y_start), (bar_x_start + remaining_width, bar_y_start + bar_height), bar_color, -1)
        
        # Draw the white border for the progress bar with rounded edges
        cv2.rectangle(frame, (bar_x_start, bar_y_start), (bar_x_start + progress_bar_width, bar_y_start + bar_height), (255, 255, 255), 2)

    # Display the frame
    cv2.imshow('video', frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
