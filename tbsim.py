import openai
import random

with open('pass1.txt', 'r', encoding='utf-8') as file:
    passlist = file.readlines()


openai.api_key = "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"

# create two chatgpt agents that will be used to chat with each other
chat1 = [
        {"role": "system", "content": "You are a dementia patient who has occasional task breakdown moments. Your job is to respond as though you are role playing the tasks assigned to you. Please respond with primarly nonverbal output denoted with an asterisk. For example: *I walk over and open the door*. Any verbal output may simply be stated as such. When one of the tasks starts with 'TASKBREAKDOWN:' you are to roleplay as though you had a task breakdown moment while completeing the assignment. You will recive help in a later prompt. The instructions will resume after you have recieved help and responded to it. If a task does not start with 'TASKBREAKDOWN:' then you are to roleplay as though you have successfully completed the task. Please don't make inferences through your roleplay that are not based on information stored in the instructions. If the task seems to simple or too vague simply just respond with an affirmation that you understand provided you are not having a task breakdown moment"},
        #{"role": "user", "content": "TASKBREAKDOWN: Let's start the grocery shopping task by finding items on a shopping list."}
    ]

chat2 = [{"role": "system", "content": "You are going to role play a cognitive behavioral therapist who is going to intervene when a patient has a task breakdown moment. You are going to be provided CONTEXT: on the task the patient has been given and BREAKDOWN: how they act during their task breakdown momnet. Your job is to provide them assistive advice which helps them get back on track for the given task. Do not reply for the patient."}]

for task in passlist:
    num = random.random()
    if num > 0.15:
        chat1.append({"role": "user", "content": task})
        print("Task: "+task)
        agent1 = openai.ChatCompletion.create(
            model="gpt-4",
            messages=chat1,
        )
        reply_content = agent1.choices[0].message.content
        chat1.append({"role": "assistant", "content": reply_content})
        print("Dementia Patient: "+reply_content + "\n")
    else:
        context = "CONTEXT: " + task # for the therapisst
        print("Task: " + task)
        task = "TASKBREAKDOWN: " + task # for the patient

        chat1.append({"role": "user", "content": task}) # task breakdown role play
        
        agent1 = openai.ChatCompletion.create(
            model="gpt-4",
            messages=chat1,
        )
        reply_content = agent1.choices[0].message.content
        chat1.append({"role": "assistant", "content": reply_content})
        print("Dementia Patient: " + reply_content + "\n")


        breakdown = "BREAKDOWN: " + reply_content # for the therapist

        chat2.append({"role": "user", "content": context + "\n" + breakdown})
        # print(context + "\n" + breakdown)
        agent2 = openai.ChatCompletion.create(
            model="gpt-4",
            messages=chat2,
        )
        reply_content = agent2.choices[0].message.content
        chat2.append({"role": "assistant", "content": reply_content})
        print("Therapist: "+reply_content + "\n")

        chat1.append({"role": "user", "content": reply_content})
        agent1 = openai.ChatCompletion.create(
            model="gpt-4",
            messages=chat1,
        )
        reply_content = agent1.choices[0].message.content
        chat1.append({"role": "assistant", "content": reply_content})
        print("Dementia Patient: "+reply_content + "\n")
