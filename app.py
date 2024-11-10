# app.py

from flask import Flask, render_template, Response, redirect, url_for
import threading
from video import generate_frames, read_question_and_answer  # Import functions from video.py

app = Flask(__name__)

# Route for the main HTML page with the start button
@app.route('/')
def index():
    return render_template('index.html')

# Route to start the quiz and redirect to the video page
@app.route('/start_quiz', methods=['POST'])
def start_quiz():
    # Start the quiz logic in a separate thread so it runs independently
    threading.Thread(target=read_question_and_answer).start()
    return redirect(url_for('video'))

# Route to display the video page
@app.route('/video')
def video():
    return render_template('video.html')

# Route for the MJPEG video stream
@app.route('/video_feed')
def video_feed():
    # Stream video frames generated by `generate_frames`
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)