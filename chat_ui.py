# -*- coding: UTF-8 -*-
import datetime
import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
from tkinter import *
from chatbot_graph import ChatBotGraph
import get_tts

class Chat_UI(object):
    def __init__(self):
        self.top = tk.Tk()
        self.top.geometry('650x500')
        self.handler = ChatBotGraph()

        self.chat_box_title = ttk.LabelFrame(self.top, text='Medical QA')
        self.chat_box_title.grid(column=0, row=0, padx=10, pady=10)
        self.chat_box = scrolledtext.ScrolledText(self.chat_box_title, width=60, height=30, wrap=tk.WORD)
        self.chat_box.grid(column=0, columnspan=3)

        self.content_entry = scrolledtext.ScrolledText(self.top, width=50, height=2, wrap=tk.WORD)
        self.content_entry.bind("<Up>", self.send_message)
        self.send_button = tk.Button(self.top, bitmap="info", command=lambda :self.send_message(1), height=16, width=45)
        self.play_button = tk.Button(self.top, bitmap="gray50", command=self.play_mp3, height=16, width=45)
        self.img_user = PhotoImage(file='./image/user_resize.png')
        self.img_AI = PhotoImage(file='./image/AI_resize.png')

        self.back_ground = PhotoImage(file='./image/back_resize.png')
        self.back_label = tk.Label(self.top, image=self.back_ground, justify=tk.LEFT)
        self.back_label.place(x=465, y=20)

        self.content_entry.place(x=11, y=440)
        self.send_button.place(x=400, y=440)
        self.play_button.place(x=400, y=470)

    def send_message(self, event):
        self.question = self.content_entry.get('0.0', 'end-1c') + '\n'
        self.answer = self.handler.chat_main(self.question)
        self.content_entry.delete('0.0', 'end-1c')
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.chat_box.insert(tk.INSERT, '                '+nowTime+'\n')

        max_line_lenth = 18
        legal_total_length = 54
        q_length = len(self.question) - 1
        space_length = legal_total_length -2*q_length
        if q_length > max_line_lenth:
            for i in range(q_length+1):
                line_num = int(i / 18)
                char_num = i % 18
                if char_num == 0:
                    self.chat_box.insert(tk.INSERT, '                  ')
                self.chat_box.insert(tk.INSERT, self.question[i])
                if char_num == 17:
                    if line_num == 0:
                        self.chat_box.insert(tk.INSERT, ' ')
                        self.chat_box.image_create('end-1c', image=self.img_user)
                        self.chat_box.insert(tk.INSERT, '\n')
                    else:
                        if self.question[i] != '\n':
                            self.chat_box.insert(tk.INSERT, '\n')
        else:
            for i in range(q_length):
                if i == 0:
                    for j in range(space_length):
                        self.chat_box.insert(tk.INSERT, ' ')
                self.chat_box.insert(tk.INSERT, self.question[i])
            self.chat_box.insert(tk.INSERT, ' ')
            self.chat_box.image_create('end-1c', image=self.img_user)
            self.chat_box.insert(tk.INSERT, '\n')

        answer_list = self.answer.split('\n')
        self.chat_box.image_create('end-1c', image=self.img_AI)
        j = 0
        for a in answer_list:
            a_length = len(a)
            for i in range(a_length):
                char_num = i % 18
                line_num = i / 18
                if char_num == 0:
                    if line_num == 0 and j == 0:
                        self.chat_box.insert(tk.INSERT, ' ')
                    else:
                        self.chat_box.insert(tk.INSERT, '     ')
                self.chat_box.insert(tk.INSERT, a[i])
                if char_num == 17:
                    self.chat_box.insert(tk.INSERT, '\n')
                if char_num != 17 and i == a_length-1:
                    self.chat_box.insert(tk.INSERT, '\n')
            j = j + 1
        self.chat_box.insert(tk.INSERT, '\n')
        self.chat_box.see('end-1c')

    def play_mp3(self):
        file_name = get_tts.get_mp3file(self.answer)
        text_length = len(self.answer)
        get_tts.mp3_play(text_length, file_name)

def init():
    chat = Chat_UI()
    tk.mainloop()

if __name__ == '__main__':
    init()