import tkinter as tk
from tkinter import *
from tkinter import ttk
from ollama import chat
from ollama import ChatResponse
import requests as req
import os

# Define colors.
neon_green = "#18f50a"
DEFAULT_MODEL = "deepseek-r1:1.5b"
MAIN_FONT = ("new_courier", 12, "bold")

def load_models():
    try:
        response = req.get("http://localhost:11434/api/tags")
        models = [m["name"] for m in response.json()["models"]]
        model_dropdown["values"] = models
        if DEFAULT_MODEL in models:
            model_var.set(DEFAULT_MODEL)
        else:
            model_dropdown.current(0)
    except:
        model_dropdown["values"] = ["Ollama not running"]
    

# Submit prompt to local LLM and receive response.
def submit():
    global chat_history
    global stats
    stats.delete("0.0", END)
    prompt = chat_history + prompt_entry.get()
    model = model_var.get()
    response = chat(model=model, messages=[
        {
            'role': 'user',
            'content': prompt
        },
    ])
    txt.insert(END, "User: \n" + prompt_entry.get() + "\n")
    txt.insert(END, "\nchatbot: \n" + response.message.content + "\n\n")
    prompt_tokens = "Prompt Tokens: " + (response.prompt_eval_count).__str__()
    response_tokens = "Response Tokens: " + (response.eval_count).__str__()

    response_stats = prompt_tokens + "\n" + response_tokens
    chat_history = prompt + (response.message.content)
    stats.insert(END, response_stats)

# Clear prompt input field on button press.
def reset_input():
    prompt_entry.delete(first="0", last=END)
    
def stop_models():
    stop_list = req.get("http://localhost:11434/api/ps")
    stop_list = [m["name"] for m in stop_list.json()["models"]]
    for model in stop_list:
        os.system("ollama stop " + model)
    

root = Tk()
root.title("Test Bot")
root.geometry("505x700")

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
    height=700
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

# Model selection
model_var = tk.StringVar()
model_dropdown = ttk.Combobox(
    mainframe, 
    textvariable=model_var, 
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
    height=130
    )


load_models()
root.mainloop()