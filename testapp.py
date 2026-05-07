import tkinter as tk
from tkinter import *
from tkinter import ttk
from ollama import chat
from ollama import ChatResponse
import requests as req
import os
import psutil

# Define colors.
neon_green = "#18f50a"
DEFAULT_MODEL = "deepseek-r1:1.5b"
MAIN_FONT = ("new_courier", 12, "bold")

def load_models():
    try:
        llm_response = req.get("http://localhost:11434/api/tags")
        models = [m["name"] for m in llm_response.json()["models"]]
        model_dropdown["values"] = models
        if DEFAULT_MODEL in models:
            model_select.set(DEFAULT_MODEL)
        else:
            model_dropdown.current(0)
    except:
        model_dropdown["values"] = ["Ollama not running"]


# Submit prompt to local LLM and receive llm_response.
def submit():
    global chat_history
    global stats
    global new_chat_history

    stats.delete("0.0", END)
    
    history = open("chat_history.txt", "r")
    history = history.read()
    prompt = "The following is our chat history, new prompt will follow:\n" + history + "\nNew Prompt: " + prompt_entry.get()
    model = model_select.get()
    llm_response = chat(model=model, messages=[
        {
            'role': 'user',
            'content': prompt
        },
    ])

    txt.insert(END, "User: \n" + prompt_entry.get() + "\n")
    txt.insert(END, "\nchatbot: \n" + llm_response.message.content + "\n\n")
# Conversation history is saved to a text file, which is read in full and sent with each prompt to provide context. This is not the most efficient method for long conversations, but it is the simplest way to maintain conversation history without using a database or more complex data structure. Future iterations could implement a more efficient method of storing and retrieving conversation history.
    try:
        new_chat_history = open("chat_history.txt", "x")
        new_chat_history.write("User: " + prompt_entry.get() + "\nLLM Response: " + llm_response.message.content + "\n")   
    except:
        new_chat_history = open("chat_history.txt", "a")
        new_chat_history.write("User: " + prompt_entry.get() + "\nLLM Response: " + llm_response.message.content + "\n")
    
    prompt_tokens = "Prompt Tokens: " + (llm_response.prompt_eval_count).__str__()
    llm_response_tokens = "llm_response Tokens: " + (llm_response.eval_count).__str__()
    llm_response_stats = prompt_tokens + "\n" + llm_response_tokens
    stats.insert(END, "CPU: " + cpu_model + "\nTotal Memory: " + str(total_mem) + " GB\n\n" + llm_response_stats)

# Clear prompt input field on button press.
def reset_input():
    prompt_entry.delete(first="0", last=END)
    
def stop_models():
    stop_list = req.get("http://localhost:11434/api/ps")
    stop_list = [m["name"] for m in stop_list.json()["models"]]
    for model in stop_list:
        os.system("ollama stop " + model)

# System info functions 
# Still need to add CPU model name function for windows compatibility, currently only works on linux.    
def get_cpu_model():
    try:
        with open("/proc/cpuinfo", "r") as f:
            for line in f:
                if "model name" in line:
                    return line.split(":")[1].strip()
    except:
        return "Unknown CPU"

# System info variables
cpu_model = get_cpu_model()
mem = psutil.virtual_memory()
total_mem = round(mem.total / (1024 ** 3), 2)


root = Tk()
root.title("Test Bot")
root.geometry("505x750")

style = ttk.Style()
style.map(
    "TButton",
    foreground=[("active", neon_green), ("!active", "black")],
    background=[("active", "black"), ("!active", neon_green)],
    font=[("active", MAIN_FONT), ("!active", MAIN_FONT)],
    padding=[("active", 0), ("!active", 0)]
)
style.map(
    "danger.TButton",
    background=[("active", "white"), ("!active", "red")],
    foreground=[("active", "red"), ("!active", "white")]
)

# Main window
mainframe = ttk.Frame(root)
mainframe.place(
    x=0, 
    y=0, 
    width=500, 
    height=750
)

# Chat window
chatframe = ttk.Frame(mainframe)
chatframe.place(
    x=0, 
    y=0, 
    width=500, 
    height=600
)
txt = Text(
    chatframe, 
    bg="black", 
    fg=neon_green, 
    wrap=tk.WORD, 
    width=60
    )
txt.place(
    x=5, 
    y=5, 
    width=500, 
    height=495
    )

# scrollbar = Scrollbar(txt)
# scrollbar.place(relheight=1, relx=0.974)

# Prompt entry
prompt = StringVar()
prompt_entry = ttk.Entry(
    mainframe, 
    width=80, 
    textvariable=prompt, 
    foreground="black",
    font=("new_courier", 12, "bold")
    )
prompt_entry.place(
    x=5, 
    y=500, 
    width=390, 
    height=30
    )

chat_history = ""
new_chat_history = ""

# Model selection
model_select = tk.StringVar()
model_dropdown = ttk.Combobox(
    mainframe, 
    textvariable=model_select, 
    state="readonly", 
    width=30
    )
model_dropdown["values"] = ["loading..."]
model_dropdown.current(0)
model_dropdown.place(
    x=5,
    y=532,
    width=200,
    height=30
    )

# Buttons
submit_button = ttk.Button(
    mainframe, 
    text="Submit",
    style="TButton",
    command=lambda: [submit(), reset_input()])
submit_button.place(
    x=400, 
    y=500, 
    width=100, 
    height=30
    )
quit_button = ttk.Button(
    mainframe, 
    text="Quit",
    style="danger.TButton",
    command=lambda: [root.destroy(), stop_models()]
    )
quit_button.place(
    x=400, 
    y=532, 
    width=100, 
    height=30
    )

# Stats
stats = Text(
    mainframe, 
    bg="black", 
    fg=neon_green, 
    wrap=tk.WORD, 
    width=60,
    font=("courier", 10, "bold")
    )
stats.place(
    x=5, 
    y=565, 
    width=495, 
    height=180
    )
stats.insert(END, "CPU: " + cpu_model + "\nTotal Memory: " + str(total_mem) + " GB\n\n")

load_models()
root.mainloop()