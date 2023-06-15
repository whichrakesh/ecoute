import openai
from keys import OPENAI_API_KEY
from prompts import create_prompt, INITIAL_RESPONSE
import time

openai.api_key = OPENAI_API_KEY

question_words = ["what", "why", "when", "where", "who", "tell",
             "name", "is", "how", "do", "does", 
             "which", "are", "can", "could", "would", 
             "should", "has", "have", "whom", "whose", "don't"]

def detect_question(text):
        phrases = text.strip().split("\n\n")
        last_phrase = phrases[-1]
        last_phrase = last_phrase.replace('You:', '').strip().replace('[', '').replace(']', '')
        last_phrase = last_phrase.lower()
        texts = last_phrase.split()
        
        if any(x in texts[0] for x in question_words):
            print(f"Detected Question: {last_phrase}");
            return True
        else:
            return False

def generate_response_from_transcript(transcript):
    try:
        response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0301",
                messages=[{"role": "system", "content": create_prompt(transcript)}],
                temperature = 0.0
        )
    except Exception as e:
        print(e)
        return ''
    full_response = response.choices[0].message.content
    try:
        return full_response.split('[')[1].split(']')[0]
    except:
        return ''
    
class GPTResponder:
    def __init__(self):
        self.response = INITIAL_RESPONSE
        self.response_interval = 1

    def respond_to_transcriber(self, transcriber):
        while True:
            if transcriber.transcript_changed_event.is_set():
                start_time = time.time()

                transcriber.transcript_changed_event.clear() 
                transcript_string = transcriber.get_transcript()

                if(detect_question(transcript_string)):
                    response = generate_response_from_transcript(
                        transcript_string)

                    end_time = time.time()  # Measure end time
                    # Calculate the time it took to execute the function
                    execution_time = end_time - start_time

                    if response != '':
                        self.response = response
                        print(f"Response from ChatGPT: {response}")

                    remaining_time = self.response_interval - execution_time
                    if remaining_time > 0:
                        time.sleep(remaining_time)
                else:
                    time.sleep(0.3)
            else:
                time.sleep(0.3)