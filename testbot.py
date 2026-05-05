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
    response = chat(model='gemma3:12b', messages=[
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
root.geometry("800x600")

mainframe = ttk.Frame(root)
mainframe.grid(columnspan=2, rowspan=5)

chatframe = ttk.Frame(mainframe)
chatframe.pack
chatframe.grid(column=0, row=1)

txt = Text(chatframe, bg="lightgray", fg="black", wrap=tk.WORD, width=60)
txt.grid(column=0, row=0)

# scrollbar = Scrollbar(txt)
# scrollbar.place(relheight=1, relx=0.974)

prompt = StringVar()
prompt_entry = ttk.Entry(mainframe, width=80, textvariable=prompt)
prompt_entry.grid(column=0, row=2)

chat_history = ""

submit_button = ttk.Button(mainframe, text="Submit", command=lambda: [submit(), reset_input()]).grid(column=0, row=3)
quit_button = ttk.Button(mainframe, text="Quit", command=root.destroy).grid(column=0, row=4)

stats = StringVar()
stats.set("Ready...")
stats_display = Label(mainframe, textvariable=stats)
stats_display.grid(column=1, row=0)

root.mainloop()