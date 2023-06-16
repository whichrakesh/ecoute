INITIAL_RESPONSE = "Welcome to Sage.AI 👋"
def create_prompt(transcript, is_example):
        if(is_example):
                prompt = f"""You are a Sales Person showing a demo of TurboHire to the speaker. A poor transcription of conversation is given below. 
        
{transcript}.

Please provide an example based on the conversation and the last phrase. Only Provide the example, nothing else. Confidently give a straightforward response to the speaker, even if you don't understand them. Give your response in square brackets. DO NOT ask to repeat, and DO NOT ask for clarification."""
                print(prompt + "\n\n\n")
                return prompt
        else:
                prompt = f"""You are a Sales Person showing a demo of TurboHire to the speaker. A poor transcription of conversation is given below. 
        
{transcript}.

Please respond, in detail, to the conversation. Confidently give a straightforward response to the speaker, even if you don't understand them. Give your response in square brackets. DO NOT ask to repeat, and DO NOT ask for clarification. Just answer the speaker directly."""
                print(prompt + "\n\n\n")
                return prompt
        