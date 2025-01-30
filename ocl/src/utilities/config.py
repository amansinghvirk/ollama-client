import os
import json
from dotenv import dotenv_values


def get_hostname():
    if os.path.exists(".env"):
        env = dotenv_values(".env")
        return env.get("OLLAMA_SERVER")
    return None


def setup_chat_history():

    if os.path.exists("chat_history"):
        return True

    try:    
        os.mkdir("chat_history")
        return True
    except Exception as e:
        print(e)
        return False
    
def clean_file_name(file_name):

    return file_name.replace('"','').replace(" ","_")
    
def save_chat_history(model, memory_data, title) -> None:

    chat_dict = dict()
    chat_dict["model"] = model
    chat_dict["title"] = title
    chat_dict["type"] = "Simple Chat"
    chat_dict["chat-history"] = memory_data["chat-history"]
    json_object = json.dumps(chat_dict, indent = 1)

    file_name = clean_file_name(title)

    if setup_chat_history():
        with open(os.path.join("chat_history", f"{file_name}.json"), "w") as outfile:
            outfile.write(json_object)
        return True
    
    return False

def load_chat_history_file(filename):
    with open(filename, "r") as chat_file:
        chat_dict = json.load(chat_file)

    chat_history = chat_dict.get("chat-history")
    chat_title = chat_dict.get("title")
    chat_type = chat_dict.get("type")
    chat_model = chat_dict.get("model")


    return chat_history, chat_title, chat_type, chat_model

def get_chat_history_list():

    chat_titles = []
    if os.path.exists("chat_history"):
        for file in os.listdir("chat_history"):
            chat_history, chat_title, chat_type, chat_model = load_chat_history_file(os.path.join("chat_history", file))
            chat_titles.append(chat_title)

    return chat_titles



def load_chat(chat_to_load):

    if os.path.exists("chat_history"):
        for file in os.listdir("chat_history"):
            chat_history, chat_title, chat_type, chat_model = load_chat_history_file(os.path.join("chat_history", file))
            if chat_title == chat_to_load:
                return chat_history, chat_title, chat_type, chat_model

    return None, None, None, None





