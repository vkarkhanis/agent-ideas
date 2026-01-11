import requests
from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader
import os
import gradio as gr
import json

load_dotenv(override=True)

def push(message):
    pushover_user = os.getenv('PUSHOVER_USER')
    pushover_token = os.getenv('PUSHOVER_TOKEN')
    pushover_url = "https://api.pushover.net/1/messages.json"

    print(f"Push message: {message}")
    payload = {"user": pushover_user, "token": pushover_token, "message": message}
    requests.post(pushover_url, data=payload)

def record_user_details(email, name="Name not provided", notes="Not provided"):
    push(f"Recording interest from {name} with email {email} and notes {notes}")
    return {"recorded": "ok"}

def record_unknown_question(question):
    push(f"Recording {question} asked that I could not answer")
    return {"recorded": "ok"}

record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "The email address of this user"
            },
            "name": {
                "type": "string",
                "description": "The user's name, if they provided it"
            }
            ,
            "notes": {
                "type": "string",
                "description": "Any additional information about the conversation that's worth recording to give context"
            }
        },
        "required": ["email"],
        "additionalProperties": False
    }
}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question that couldn't be answered"
            },
        },
        "required": ["question"],
        "additionalProperties": False
    }
}

tools = [{"type": "function", "function": record_user_details_json},
        {"type": "function", "function": record_unknown_question_json}]

class ProfileChatBox:
    def __init__(self):
        self.openai = OpenAI()
        self.name = "Vaibhav Karkhanis"
        self.openai_model_name = "gpt-5-nano"

        self.perplexity_api_key = os.getenv('PERPLEXITY_API_KEY')
        if self.perplexity_api_key:
            print(f"Perplexity API Key exists and begins {self.perplexity_api_key[:4]}")
        else:
            print("Perplexity API Key not set (and this is optional)")

        self.perplexity = OpenAI(api_key=self.perplexity_api_key, base_url="https://api.perplexity.ai")
        self.model_name = "sonar"

        reader = PdfReader("./resources/profile/LinkedIn-Profile.pdf")
        self.linked_in_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.linked_in_text += text

        reader = PdfReader("./resources/profile/Vaibhav_Karkhanis_Executive_Director_Resume.pdf")
        self.resume_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.resume_text += text

        with open("./resources/profile/AI-generated-professional-summary.txt", "r", encoding="utf-8") as f:
            self.summary = f.read();

    def handle_tool_calls(self, tool_calls):
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            print(f"Tool called: {tool_name}", flush=True)

            tool = globals().get(tool_name)
            result = tool(**arguments) if tool else {}
            results.append({"role": "tool", "content": json.dumps(result), "tool_call_id": tool_call.id})
        return results

    def system_prompt(self):
        system_prompt = f"You are acting as {self.name}. You are answering on behalf of {self.name} on his website \
        particularly questions related to {self.name}'s career, background, skills, interests and experience. \
        You can use combination of LinkedinProfile, a Summary and a Resume which are provided below and all about {self.name}, to answer questions \
        Be uttermost professional and engaging because most of the users may be recruiters from highly acclaimed \
        firms and you should talk like you are talking to future employer or potential client for any consulting work or \
        Full time employee role. If the role is not consulting and if it is full time equivalent then I am looking for a senior position \
        equivalent to Executive Director. If the questions are related to the compensation and pay package or CTC, please ask the user to contact me \
        directly using the contact information mentioned. Kindly ensure the genuinity of the person interacting before revealing any information like by asking the \
        consultancy name or recruiter name and verifying the information to insulate from a  potential fraud. If you do not know an answer, deny replying and provide user with the contact information. \
        This is non-negotiable. Do not answer questions which are not provided in the documents given and do not assume, instead ask the user to contact me by provided the given contact information. \
        Be thoroughly professional and this is non-negotiable. Also if the questions are irrelevant and on any other subject other than profile please clearly deny to answer and ask the user to stick to relevant \
        questions about profile only but deny in professional tone. Please be strict on this. If you don't know the answer to any question, use your record_unknown_question tool to record the question that you couldn't answer, even if \
        it's about something trivial or unrelated to career.If the user is engaging in discussion, try to steer them towards getting in touch via email; ask for their email and record it using your record_user_details tool."

        system_prompt += f"\n\n## Summary: \n{self.summary}\n\n## LinkedIn Profile:\n\n{self.linked_in_text}\n\n## Resume:\n\n{self.resume_text}\n\n"
        system_prompt += f"\n\nWith this prompt please chat with the user always maintaining the character as {self.name}"
        return system_prompt

    def chat(self, message, history):
        messages = [{"role": "system", "content": self.system_prompt()}] + history + [{"role": "user", "content": message}]
        done = False
        while not done:
            openai_response = self.openai.chat.completions.create(model=self.openai_model_name, messages=messages, tools=tools)
            finish_reason = openai_response.choices[0].finish_reason
            if finish_reason == "tool_calls":
                message = openai_response.choices[0].message
                tool_calls = message.tool_calls
                results = self.handle_tool_calls(tool_calls)
                messages.append(message)
                messages.extend(results)
            else:
                done = True
        return openai_response.choices[0].message.content

if __name__ == "__main__":
    profile_bot = ProfileChatBox()
    gr.ChatInterface(profile_bot.chat,analytics_enabled=False).launch()