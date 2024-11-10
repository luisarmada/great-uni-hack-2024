from openai import OpenAI
import base64
import os
import re

current_dir = os.getcwd()

path = current_dir+"/testmaths1.jpg"
client = OpenAI()


def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')
  
base64_image = encode_image(path)

lengthQuiz = "5"
prompt = "You are a linguist tasked with making language more understandable for younger people. Your task is to take the notes provided to you and convert them to what is called ‘brainrot’ language. The following words are commonly used in brainrot language : “skibidi gyatt rizz only in ohio did you pray today livvy dunne rizzing up baby gronk sussy imposter pibby glitch in real life sigma alpha omega male grindset goon cave freddy fazbear smurf cat vs strawberry elephant blud dawg shmlawg ishowspeed a whole bunch of turbulence bro really thinks he's carti literally hitting the griddy the ocky way kai cenat fanum tax garten of banban no edging in class not the mosquito again bussing axel in harlem whopper whopper whopper whopper 1 2 buckle my shoe goofy ahh sin city monday left me broken quirked up goated with the sauce john pork grimace shake kiki do you love me huggy wuggy nathaniel b stare biggest bird omar the referee amogus uncanny wholesome reddit chungus keanu reeves pizza tower zesty poggers kumalala savesta quandale dingle glizzy rose toy ankha zone thug shaker morbin time dj khaled sisyphus shadow wizard money gang ayo the pizza here PLUH nair waxing t-pose family guy funny moments compilation with subway surfers gameplay at the bottom nickeh30 ratio uwu delulu opium bird cg5 mewing fortnite battle pass all my fellas gta 6 backrooms gigachad based cringe kino F in the chat i love lean looksmaxxing gassy social credit xbox live mrbeast kid named finger better caul saul i am a surgeon hit or miss i guess they never miss huh i like ya cut g ice spice we go gym coffin of andy and leyley metal pipe falling.” Ensure you use these words in your produced text. Take the image provided and summarise the information in clear, very concise and valuable bullet points using only the information contained within the image. To get this information, you must extract the text from within the image. Bullet points should not exceed 20 words, save words where possible. For example: “In propositional logic, there are five peas in a pod” would be changed to “goofy aah propositional logic has five peas in a pod uwu.” Prioritise conservation of information over use of brainrot terms, but ensure brainrot terms are still used well - there must be a balance. You must use the brainrot language integrated into the text in each bullet point. In your response to this request, return only the summary bullet points, alongside the text ‘BEGIN’ at the start and ‘END’ at the end. Nothing else is permitted to be said in your response. No newlines are permitted, everything must be on the same line."
response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {
      "role": "user",
      "content": [
        {"type": "text", "text": prompt},
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


quiz = response.choices[0]
print(str(quiz))
quizStr = str(quiz)


def clean_quiz_text(raw_quiz_text):
    # Attempt to find the content strictly between BEGINQUIZ and ENDQUIZ
    quiz_content_match = re.search(r"BEGIN\s*(.*?)\s*END", raw_quiz_text, re.DOTALL | re.IGNORECASE)
    if quiz_content_match:
        # Strip any extra whitespace from extracted content
        return quiz_content_match.group(1).strip()
    return ""

print(clean_quiz_text(quizStr))