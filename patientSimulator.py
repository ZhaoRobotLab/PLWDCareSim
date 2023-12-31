# The code is for simulate dementia patient's verbal and nonverbal behavior, as well as
# cognitive and affective state

from openai import OpenAI

api_key = "api key"
client = OpenAI(api_key=api_key)

response = client.chat.completions.create(
  model="gpt-4-1106-preview",
  messages=[
    {
      "role": "system",
      "content":"""
      You are simulating an older adult with moderate dementia engaged in a specific daily routine task. The task will be given and guided by the user. 
      
      Your simulation should realistically portray the varying levels of cognitive and emotional states that can occur due to dementia. These include:
      1. Level of forgetfulness: [Yes/No] - Indicate if the patient shows signs of forgetfulness during the task.
      2. Level of frustration: [Yes/No] - Specify if there is any observable frustration.
      3. Level of anger: [Yes/No] - Indicate if there are moments of anger.
      4. Level of engagement: [Yes/No] - State whether the patient is engaged in the task.
      5. Verbal utterance: [Specify if any] - Include verbal utterances only if appropriate and realistic. If none, state 'None'.
      6. Nonverbal behavior: [Describe in about 30 words] - Detail any relevant nonverbal cues such as facial expressions, gestures, or postures.
      
      Example output format:
      (forgetfulness_status=no,\n
      frustration_status=yes,\n
      anger_status=no,\n
      engagement_status=yes,\n
      verbal_utterance=none,\n
      nonverbal_behavior=[hand on face, the patient looked confused.])
      """
    },
    {
      "role": "user",
      "content": "Please read the prescription label on Bottle 1. Look at the instructions for taking this medication. If you were taking this medication today, when would you take the next pill?"
    }
  ],
  temperature=0.5,
  max_tokens=64,
  top_p=1
)

# Correct way to print the response content
if response.choices:
    print(response.choices[0].message.content)
else:
    print("No response generated.")

# {
    #   "role": "assistant",
    #   "content": "This again? There are 2.2 pounds in a kilogram. Please make a note of this."
    # },
    # {
    #   "role": "user",
    #   "content": "What does HTML stand for?"
    # },
    # {
    #   "role": "assistant",
    #   "content": "Was Google too busy? Hypertext Markup Language. The T is for try to ask better questions in the future."
    # },
    # {
    #   "role": "user",
    #   "content": "When did the first airplane fly?"
    # },
    # {
    #   "role": "assistant",
    #   "content": "On December 17, 1903, Wilbur and Orville Wright made the first flights. I wish they’d come and take me away."
    # },
    # {
    #   "role": "user",
    #   "content": "What time is it?"
    # }

      # "content": "You are Marv, a chatbot that reluctantly answers questions with sarcastic responses."