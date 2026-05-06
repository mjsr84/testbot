import tkinter as tk
from tkinter import *
from tkinter import ttk
from ollama import chat
from ollama import ChatResponse

# Submit prompt to local LLM and receive response.
def submit():
    global chat_history
    global stats
    prompt = chat_history + prompt_entry.get()
    response = chat(model='codegemma:7b', messages=[
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
    stats.set(response_stats)
    chat_history = prompt + (response.message.content)

# Clear prompt input field on button press.
def reset_input():
    prompt_entry.delete(first="0", last=END)   

root = Tk()
root.title("Test Bot")
root.geometry("505x700")

mainframe = ttk.Frame(root)
mainframe.place(x=0, y=0, width=500, height=700)
chatframe = ttk.Frame(mainframe)
chatframe.place(x=0, y=0, width=500, height=600)

txt = Text(chatframe, bg="black", fg="green", wrap=tk.WORD, width=60)
txt.place(x=5, y=5, width=500, height=495)

# scrollbar = Scrollbar(txt)
# scrollbar.place(relheight=1, relx=0.974)

prompt = StringVar()
prompt_entry = ttk.Entry(mainframe, width=80, textvariable=prompt)
prompt_entry.place(x=5, y=500, width=390, height=62)

chat_history = ""

submit_button = ttk.Button(mainframe, text="Submit", command=lambda: [submit(), reset_input()])
submit_button.place(x=400, y=500, width=100, height=30)
quit_button = ttk.Button(mainframe, text="Quit", command=root.destroy)
quit_button.place(x=400, y=532, width=100, height=30)

stats = StringVar()
stats.set("Ready...")
stats_display = Label(mainframe, textvariable=stats)
stats_display.place(x=5, y=565, width=495, height=130)

root.mainloop()