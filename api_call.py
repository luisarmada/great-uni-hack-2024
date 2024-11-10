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
prompt = "You are a professor tasked with creating a multiple-choice" + lengthQuiz + "question quiz for students, using only the image provided. Questions should be under 15 words. Do not preface the question with its number. The quiz must be formatted in this way: A question is printed, with the word QUESTION printed before it. Four options are printed, each one with the word OPTION printed before it. The correct option is printed, with the word CORRECT printed before it. The next question is printed with the word QUESTION printed before it. Given first question “question1”, with possible answers “aaa”, “bbb” ,  “ccc”, “ddd”, with “aaa” being correct, followed by the second question “question2” here is the correct exact example output: QUESTIONquestion 1 OPTIONaaa OPTIONbbb OPTIONccc OPTIONddd CORRECTaaa QUESTIONquestion 2. You can also use true or false questions, only if it is relevant. If doing this, you must follow the same rules of the formatting. Return only the quiz, after printing BEGINQUIZ. At the end of the quiz, print ENDQUIZ. Print all text on the same line. Do not, under any circumstances, print anything on a new line anywhere in your response. No new lines."
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

# quizStr = "Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content='BEGINQUIZ  \nQUESTIONWhat are the two important formal logic systems in computer science?  \nOPTIONPropositional and First-order Logic  \nOPTIONCalculus and Geometry  \nOPTIONAlgebra and Statistics  \nOPTIONQuantum and Classical Logic  \nCORRECTPropositional and First-order Logic  \nQUESTIONWhat do formal logic systems test?  \nOPTIONThe correctness of arguments  \nOPTIONThe speed of computations  \nOPTIONThe beauty of proofs  \nOPTIONThe length of statements  \nCORRECTThe correctness of arguments  \nQUESTIONWhat type of statements are propositions?  \nOPTIONStatements that are always true  \nOPTIONStatements that are always false  \nOPTIONStatements that are either true or false  \nOPTIONStatements that are neither true nor false  \nCORRECTStatements that are either true or false  \nQUESTIONIs '2 is an odd number' a true proposition?  \nOPTIONTrue  \nOPTIONFalse  \nCORRECTFalse  \nQUESTIONWhat do quantifiers in first-order logic include?  \nOPTIONUniversal and Existential  \nOPTIONDynamic and Static  \nOPTIONBasic and Advanced  \nOPTIONPrimary and Secondary  \nCORRECTUniversal and Existential  \nENDQUIZ', refusal=None, role='assistant', audio=None, function_call=None, tool_calls=None))"
# quizStr = "Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content='BEGINQUIZ QUESTIONWhat are formal logic systems used for? OPTIONTo test correctness of arguments OPTIONTo prove mathematical statements OPTIONFor programming languages OPTIONTo write essays CORRECTTo test correctness of arguments QUESTIONWhat connects propositions in propositional logic? OPTIONConnectives OPTIONQuantifiers OPTIONStatements OPTIONFormulas CORRECTConnectives QUESTIONWhich normal forms are discussed? OPTIONConjunctive and disjunctive OPTIONTransitional and circular OPTIONNegative and positive OPTIONSimple and complex CORRECTConjunctive and disjunctive QUESTIONAre propositions either true or false? OPTIONTrue OPTIONFalse OPTIONSometimes OPTIONDepends CORRECTTrue QUESTIONWhat chapter focuses on statements and proofs? OPTIONChapter 1 OPTIONChapter 3 OPTIONChapter 2 OPTIONChapter 4 CORRECTChapter 2 ENDQUIZ', refusal=None, role='assistant', audio=None, function_call=None, tool_calls=None))"

import re


def clean_quiz_text(raw_quiz_text):
    # Attempt to find the content strictly between BEGINQUIZ and ENDQUIZ
    quiz_content_match = re.search(r"BEGINQUIZ\s*(.*?)\s*ENDQUIZ", raw_quiz_text, re.DOTALL | re.IGNORECASE)
    if quiz_content_match:
        # Strip any extra whitespace from extracted content
        return f"BEGINQUIZ\n{quiz_content_match.group(1).strip()}\nENDQUIZ"
    return ""

# def clean_quiz_text(raw_quiz_text):
#     quizWords = raw_quiz_text.split()
#     print(quizWords)
#     start = quizWords.index("message=ChatCompletionMessage(content='BEGINQUIZ")
#     end = quizWords.index("\\nENDQUIZ',")
#     cleanQuizWords = []
#     for i in range(len(quizWords)):
#         if i > start and i < end:
#             word = quizWords[i]
#             cleanQuizWords.append[word]
#     cleanQuiz = ' '.join(cleanQuizWords)
#     print(cleanQuiz)
#     return cleanQuiz

def parse_quiz_text(quiz_text):
    # Print the cleaned quiz_text to verify correct extraction
    print("Cleaned quiz text:", quiz_text)
    
    # Extract content between BEGINQUIZ and ENDQUIZ
    content_match = re.search(r"BEGINQUIZ\s*(.*?)\s*ENDQUIZ", quiz_text, re.DOTALL | re.IGNORECASE)
    if not content_match:
        return []

    content = content_match.group(1)

    # Adjusted regex to capture each QUESTION and corresponding OPTIONS and CORRECT
    questions_raw = re.findall(r"QUESTION\s*(.*?)\s*(OPTION.*?)(?=CORRECT)", content, re.DOTALL)
    correct_answers = re.findall(r"CORRECT\s*(.*?)\s*(?=QUESTION|$)", content, re.DOTALL)
    
    questions = []
    
    for idx, (question_text, options_block) in enumerate(questions_raw):
        # Clean up question text
        question_text = question_text.strip()

        # Extract options fully, handling any whitespace or newlines
        options = re.findall(r"OPTION\s*(.*?)\s*(?=OPTION|CORRECT|$)", options_block, re.DOTALL)
        options = [option.strip() for option in options]

        # Find the correct answer index from the captured correct_answers
        correct_answer_text = correct_answers[idx].strip()
        correct_answer_index = options.index(correct_answer_text) if correct_answer_text in options else None

        # Append the question in dictionary format
        questions.append({
            "question": question_text,
            "options": options,
            "correct_answer_index": correct_answer_index
        })

    return questions

# Assuming quizStr is the response in raw format from the API
cleaned_quiz_str = clean_quiz_text(quizStr)

# Convert the cleaned quiz text to dictionary format
questions = parse_quiz_text(cleaned_quiz_str)
print(questions)

