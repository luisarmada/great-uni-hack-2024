from openai import OpenAI
import base64
import os

current_dir = os.getcwd()

path = current_dir+"/testmaths1.jpg"
client = OpenAI()


def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')
  
base64_image = encode_image(path)

lengthQuiz = "10"

response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {
      "role": "user",
      "content": [
        {"type": "text", "text": "You are a professor tasked with making a " + lengthQuiz + "-question quiz on the text in this image. The quiz should have short questions, not more than 10 words each. You should not provide the answers. The questions should be numbered. Return only the quiz."},
        {


          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
          },
        },
      ],
    }
  ],
  max_tokens=300,
)

print(response.choices[0])