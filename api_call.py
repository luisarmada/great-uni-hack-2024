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

lengthQuiz = "5"
prompt = "You are a professor tasked with creating a multiple-choice" + lengthQuiz + "question quiz for students, using only the image provided. Questions should be under 15 words. Do not preface the question with its number. The quiz must be formatted in this way: A question is printed. Four options are printed. The correct option is printed. The next question is printed. Given first question “question1”, with possible answers A, B, C, D, with A being correct, followed by the second question “question2” here is the correct exact example output: question 1 A B C D A question 2. You can also use true or false questions, only if it is relevant. If doing this, you must follow the same rules of the formatting. Return only the quiz, after printing BEGINQUIZ. At the end of the quiz, print ENDQUIZ"

# response = client.chat.completions.create(
#   model="gpt-4o-mini",
#   messages=[
#     {
#       "role": "user",
#       "content": [
#         {"type": "text", "text": prompt},
#         {


#           "type": "image_url",
#           "image_url": {
#             "url": f"data:image/jpeg;base64,{base64_image}"
#           },
#         },
#       ],
#     }
#   ],
#   max_tokens=300,
# )


# quiz = response.choices[0]

quiz = "Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content='BEGINQUIZ  \nWhat is propositional logic?  \nA system of simple statements  \nA complex mathematical theory  \nA programming language  \nA historical event  \nA  \n\nWhat do propositions represent?  \nOnly true statements  \nOnly false statements  \nStatements that are either true or false  \nNon-logical statements  \nC  \n\nWhat are logical connectives used for?  \nTo form complex propositions  \nTo divide numbers  \nTo differentiate between integers  \nTo prove theorems  \nA  \n\nTrue or False: All propositions can be true at the same time.  \nTrue  \nFalse  \nC  \n\nWhich normal forms are discussed in the chapter?  \nOnly conjunction  \nOnly disjunction  \nConjunctive and disjunctive  \nNone of the above  \nC  \nENDQUIZ', refusal=None, role='assistant', audio=None, function_call=None, tool_calls=None))"
print(quiz)

quizWords = quiz.split()
start = quizWords.index("BEGINQUIZ")
end = quizWords.index("ENDQUIZ")

justQuizWords = []
for i in range(len(quizWords)):
  if i > start and i < end:
    justQuizWords.append(i)

print(justQuizWords)