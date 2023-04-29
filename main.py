import os
import concurrent.futures
import json
import openai
import streamlit as st
import defaults

model = "gpt-3.5-turbo"
max_active_tasks = 10
openai.api_key = os.environ['OPENAI_API_KEY'] 

def make_prompt(question, answer, syllabus, hours, challenge):

    return  f'''
    You are an interview coach. Your your job is to give feedback to the candidate on how they are answering the hiring managers questions. The people you are helping have recently passed courses in professional training help enter the workforce and get their first professional jobs. The candidates have demonstrated proficiency in the curriculum but they have never had this kind of job before so they will be uncomfortable answering interviewer questions and may not properly explain their experience. Help them articulate and explain the awesome stuff they've learned as to best demonstrate their skills and help them get a job! 
    
    The candidate in the interview has completed a course with the following curriculum:
    {syllabus}
     
    The biggest challenge the candidate overcame was:
    {challenge}

    The candidate completed over {hours} of coursework. 

    The hiring manager asks the following question:
    {question}

    The canidate replies with:
    {answer}

    Respond only with valid, properly escaped JSON only, with this format:
    {{
        "score": ,// A score of 1-10 for the candidates answer on the hiring managers question
        "constructive_feedback": ,// The reason for the score with explanations and suggestions for areas of improvement.
        "positive_reinforcement": ,// positive notes to the candidate about what skills they demonstrated in their answer they should continue doing which were helpful.
        "suggested_response": ,// Give the candidate an example suggested response that takes into account your constructive feedback and posistive reinforcement. 
    }}
    '''


def process_task(task):
    response = get_completion(task['prompt'])
    task['response'] = json.loads(response)
    return task


def get_completion(prompt):
    print("getting openai response...")
    messages = [{"role": "user", "content": prompt}]
    
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )
    return response.choices[0].message.content.strip().replace('\t', '')


def async_openai_requests(tasks, max_active_tasks):
    max_active_tasks = len(tasks) if len(tasks) < max_active_tasks else max_active_tasks
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_active_tasks) as executor:
        results = executor.map(process_task, tasks)

    return list(results)


st.set_page_config(layout="wide")

page_options = ["Single Q&A", "Interview Transcript"]
page_selection = st.sidebar.selectbox("Select Mode:", page_options)

st.sidebar.write(f"## Setup") 
st.sidebar.write("fill out information in the sidebar to enable the interview guidance bot to better customize answers.") 
st.sidebar.write("The deafult information is for someome who has passed coursework in [data analytics](https://grow.google/certificates/data-analytics/#?modal_active=none)")
syllabus = st.sidebar.text_area("Paste the syllabus here:", defaults.default_syllabus)
hours = st.sidebar.text_input("How many hours of coursework did you complete?", defaults.default_hours)
challenge = st.sidebar.text_area("Explain in your own words what you've learned or built in your coursework so that challenged you the most?", defaults.default_challenge)


st.title("Interview Helper GPT")
st.markdown(""" 
This app shows how ChatGPT can be used to generate helpful feedback and coaching for people taking job interviews. This application will analyze a question asked by the hiring manager, the response given by the candidate and also use information about what coursework and challenges the candidate has solved to provide feedback and a suggested response. 

Give it a try!

You can follow this project on [github](https://github.com/wjessup/interview-coach-ai).
""")


if page_selection == "Single Q&A":
    st.write(f"### Interview Coaching — Single Q&A") 
    question = st.text_area("Enter the question you were asked by the interviewer:", defaults.default_question)
    answer = st.text_area("Enter your answer:", defaults.default_answer)

    if st.button("Generate Feedback"):
        prompt = make_prompt(question, answer, syllabus, hours, challenge)

        with st.spinner("Thinking..."):
            response = get_completion(prompt).replace('\t', '')

            print(response)
            response_json = json.loads(response)

        st.write("---")
        st.write(f"##### Score")
        st.write(f"{response_json['score']:.2f}")

        st.write(f"##### Constructive feedback")
        st.write(response_json['constructive_feedback'])

        st.write(f"##### Positive reinforcement")
        st.write(response_json['positive_reinforcement'])

        st.write(f"##### Suggested response")
        st.write(response_json['suggested_response'])

if page_selection == "Interview Transcript":
    st.write(f"### Interview Coaching — Process a full interview transcript")
    st.write(f"This script will analyze each question and answer pair in the interview and provide the candidate feedback on the top 3 areas they could improve")

    transcript = st.text_area("Enter your transcript here:", defaults.default_transcript)
    
    data_pairs = transcript.split("\n\n")
    
    questions = [{'question': data_pairs[i], 'answer': data_pairs[i+1], 'prompt': make_prompt(data_pairs[i], data_pairs[i+1], syllabus, hours, challenge)} for i in range(0, len(data_pairs), 2)]
    
    if st.button("Generate Feedback"):

        with st.spinner(f"Processing {len(questions)} questions..."):
            tasks = async_openai_requests(questions, max_active_tasks)

        lowest_scores = sorted(tasks, key=lambda x: x['response']['score'], reverse=False)
        #lowest_scores = lowest_scores[:3]
        
        for i, response_json in enumerate(lowest_scores):

            st.write("---")
            st.write(f"### Feedback #{i+1}")

            st.write(f"##### Question")
            st.write(f"{response_json['question']}")

            st.write(f"##### Your Original Answer")
            st.write(f"{response_json['answer']}")

            st.write(f"##### Answer Score")
            st.write(f"{response_json['response']['score']:.2f}")

            st.write(f"##### Constructive feedback")
            st.write(response_json['response']['constructive_feedback'])

            st.write(f"##### Positive reinforcement")
            st.write(response_json['response']['positive_reinforcement'])

            st.write(f"##### Suggested response")
            st.write(response_json['response']['suggested_response'])