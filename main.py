import g4f
import tkinter as tk
from tkinter import scrolledtext
import sys
import os
import threading


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)


def send_message():
    user_input = user_entry.get()
    if user_input.strip():
        chat_area.config(state=tk.NORMAL)
        chat_area.insert(tk.END, 'You: ' + user_input + '\n')
        user_entry.delete(0, tk.END)
        chat_area.yview(tk.END)
        chat_area.insert(tk.END, "AI: I'm preparing an answer...\n")
        chat_area.yview(tk.END)
        threading.Thread(target=fetch_response, args=(user_input,)).start()


def fetch_response(user_input):
    try:
        response = g4f.ChatCompletion.create(
            model='gpt-4',
            messages=[{'role': 'user', 'content': user_input}]
        )
        ai_response = response['choices'][0]['message']['content'] if not isinstance(response, str) else response
        chat_area.config(state=tk.NORMAL)
        chat_area.delete('end-2l', tk.END)
        chat_area.insert(tk.END, '\nAI: ' + ai_response + '\n')
        chat_area.config(state=tk.DISABLED)
        chat_area.yview(tk.END)
    except Exception:
        chat_area.config(state=tk.NORMAL)
        chat_area.delete('end-1l', tk.END)
        chat_area.insert(tk.END, "AI: An error has occurred. Please try again later.\n")
        chat_area.config(state=tk.DISABLED)
        chat_area.yview(tk.END)


def on_enter(event):
    send_message()


def on_click(event):
    if user_entry.get() == "So what?":
        user_entry.delete(0, tk.END)
        user_entry.config(fg='black')


root = tk.Tk()
root.title("Smart GPT bro")
root.geometry('500x450')
root.iconbitmap(resource_path('sex.ico'))

label = tk.Label(root, text="What question do you want to ask?", font=('Arial', 14), bg='#f4f4f4', fg='#333333')
label.grid(row=0, column=0, padx=10, pady=10)

chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=15, state=tk.DISABLED, font=('Arial', 10),
                                      bg='#e5e5e5', fg='#333333', bd=5, padx=5, pady=5)
chat_area.grid(row=1, column=0, padx=10, pady=10)

user_entry = tk.Entry(root, width=40, font=('Arial', 12), bd=2, relief='solid')
user_entry.grid(row=2, column=0, padx=10, pady=5)
user_entry.insert(0, "So what?")
user_entry.config(fg='gray')
user_entry.bind("<Return>", on_enter)
user_entry.bind('<FocusIn>', on_click)

send_button = tk.Button(root, text='Send', width=10, font=('Arial', 12), bg='#4CAF50', fg='white', relief='solid', bd=3,
                        command=send_message)
send_button.grid(row=3, column=0, padx=10, pady=10)

root.mainloop()
