import tkinter as tk  # 引入Tkinter库中的函数，并重命名为tk
import re


def clearSpace(text):
    match_regex = re.compile(u'[\u4e00-\u9fa5。，:#@$%&*？！：；《》、（）]{1} +(?<![a-zA-Z])|\d+ +| +\d+|[a-z A-Z0-9,.()?!\[\]]+')
    should_replace_list = match_regex.findall(text)
    order_replace_list = sorted(should_replace_list, key=lambda i: len(i), reverse=True)
    for i in order_replace_list:
        if i == u' ':
            continue
        new_i = i.strip()
        text = text.replace(i, new_i)
    return text


def clearReplace(text):
    text = text.replace('\r\n', ' ')
    fine_text = " ".join(text.split())
    return fine_text


def format_text():
    long_str = window.clipboard_get()
    long_str = clearReplace(long_str)
    long_str = clearSpace(long_str)
    window.clipboard_clear()
    window.clipboard_append(long_str)


def buttonClick():
    result_str = window.clipboard_get()
    text_box.delete('1.0', tk.END)  # 清除text组件内容
    format_text()
    result_str = window.clipboard_get()
    text_box.insert(tk.INSERT, result_str)


def checkBoxClick():
    if is_on_top.get() == 1:
        window.wm_attributes('-topmost', 1)  # 锁定窗口置顶
    else:
        window.wm_attributes('-topmost', 0)  # 释放窗口置顶


window = tk.Tk()  # 创建Tkinter窗口
window.title('文本去空格/换行')
window.geometry('320x200')
window.minsize(width=320, height=200)

button = tk.Button(window, text="  去!  ", command=buttonClick)
button.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
button.rowconfigure(0, weight=1)


# 文本框和滚动条
s1 = tk.Scrollbar(window)
s1.grid(row=1, column=1, sticky=tk.N + tk.S)
global text_box
text_box = tk.Text(window, yscrollcommand=s1.set, wrap=tk.WORD)
text_box.grid(row=1, column=0, padx=10, pady=10, sticky=tk.E+tk.W+tk.N+tk.S)


# 置顶窗口复选框
is_on_top = tk.IntVar()
check_box = tk.Checkbutton(window, text="置顶窗口", variable=is_on_top, command=checkBoxClick)
check_box.deselect()
check_box.grid(row=0, column=0, sticky=tk.E)

window.rowconfigure(1, weight=1)
window.columnconfigure(0, weight=1)
window.mainloop()
