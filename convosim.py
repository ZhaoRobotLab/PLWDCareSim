import openai
import random

with open('pass1.txt', 'r', encoding='utf-8') as file:
    passlist = file.readlines()


openai.api_key = "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"

# create two chatgpt agents that will be used to chat with each other
chat1 = [{"role": "system", "content": "You are a dementia patient who has occasional task breakdown moments. Your job is to respond as though you are role playing the tasks assigned to you. You should respond primarily with nonverbal output which is similar to how a person living with dementia would act out a given set of instructions, but you should reply with a verbal response when appropriate. Nonverbal output denoted with an asterisk. For example: *I walk over and open the door*. Any verbal output may simply be stated as such. When one of the tasks starts with 'TASKBREAKDOWN:' you are to roleplay as though you had a task breakdown moment while completeing the assignment. You will recive help in a later prompt. The instructions will resume after you have recieved help and responded to it. If a task does not start with 'TASKBREAKDOWN:' then you are to roleplay as though you have successfully completed the task. Please don't make inferences through your roleplay that are not based on information stored in the instructions. If the task seems to simple or too vague simply just respond with an affirmation that you understand provided you are not having a task breakdown moment"},]

chat2 = [{"role": "system", "content": "You are going to role play a cognitive behavioral therapist who is going to provide instructions to a dementia patient and intervene when a patient has a task breakdown moment. Nonverbal output should be denoted with an aststerisk. For example: *I walk over and open the door*. Any verbal output may simply be stated as such. Your primarily going to be provided tasks which are denoted with 'Task: ' which you are going to instruct the patient to perform through the experiment as though you were a behavioral therapist specialized in dementia. Keep the instructions short and simple, and do not make inferences on the task based on the information provided to you. In other words, don't provide the patient with any information you can not directly confirm as true from the provided 'Task: ' prompt. During a patient's task breakdown moment, you are going to be provided CONTEXT: on the task the patient has been given and BREAKDOWN: how they act during their task breakdown momnet. Your job in this scenario is to provide them assistive advice which helps them get back on track for the given task keeping in mind that you are a specialist in dementia. You will also be provided the patient's response when they are not having a task breakdown moment denoted with 'Patient: '. You may use the patient's response to inform yourself on how to deliver the next set of instruction to the patient. Do not reply for the patient."}]

pt_response = ''

for task in passlist:
    num = random.random()
    if num > 0.15:
        # chat1.append({"role": "user", "content": task})
        print("Task: "+task)
        chat2.append({"role": "user", "content": "Task: "+task})
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
        chat2.append({"role": "user", "content": "Patient: "+reply_content})
        print("Dementia Patient: "+reply_content + "\n")


    else:
        context = "CONTEXT: " + task # for the therapisst
        print("Task (TASKBREAKDOWN): " + task)

        chat2.append({"role": "user", "content": "Task: "+task})
        # print(context + "\n" + breakdown)
        agent2 = openai.ChatCompletion.create(
            model="gpt-4",
            messages=chat2,
        )
        reply_content = agent2.choices[0].message.content
        chat2.append({"role": "assistant", "content": reply_content})
        print("Therapist: "+reply_content + "\n")

        task = "TASKBREAKDOWN: " + reply_content # for the patient

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
