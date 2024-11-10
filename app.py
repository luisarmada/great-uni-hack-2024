from flask import Flask, render_template, request, redirect, url_for, Response
import os
import threading
from video import generate_frames, read_question_and_answer  # Import functions from video.py

app = Flask(__name__)

# Ensure the upload folder exists
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('Home.html')
    # return render_template('index.html')

@app.route('/file', methods=['GET', 'POST'])
def file():
    if request.method == 'POST':
        # Retrieve file and age range from the form
        file = request.files.get('file')
        age_range = request.form.get('age_range')
        
        # # Save the uploaded file if provided
        # if file:
        #     file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        #     file.save(file_path)
        

        threading.Thread(target=read_question_and_answer).start()
        # Render File.html with video_feed=True to display the video feed
        return render_template('File.html', video_feed=True)

    # Render File.html without video feed on GET request
    return render_template('File.html', video_feed=False)

# Route to start the quiz and redirect to the video page
@app.route('/start_quiz', methods=['POST'])
def start_quiz():
    # Start the quiz logic in a separate thread so it runs independently
    threading.Thread(target=read_question_and_answer).start()
    return redirect(url_for('video'))

@app.route('/video')
def video():
     # Renders the old `video.html` page with embedded video stream
     return render_template('video.html')

@app.route('/video_feed')
def video_feed():
    # Route for serving video frames as an HTTP stream
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# --- Old Routes for Index and Video Pages ---
# Uncomment these routes if you want to use the old `index.html` and `video.html` pages.



if __name__ == '__main__':
    app.run(debug=True)
