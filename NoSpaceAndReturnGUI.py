import tkinter as tk  # 引入Tkinter库中的函数，并重命名为tk
import re
import pangu


def clearSpace(text):
    match_regex = re.compile(
        u'[\u4e00-\u9fa5。，#@$%&*？！：；《》、（）]{1} +(?<![a-zA-Z])|\d+ +| +\d+|[a-z A-Z0-9{},.:;\-/"\'()?!\[\]]+')
    should_replace_list = match_regex.findall(text)
    order_replace_list = sorted(should_replace_list, key=lambda i: len(i), reverse=True)
    for i in order_replace_list:
        if i == u' ':
            continue
        new_i = i.strip()    # 去除重复空格
        new_i = ' '.join(new_i.split())
        text = text.replace(i, new_i)
    return text


def clearReplace(text):
    j = []
    p = re.compile(r'\n\s*\n')
    text_segment = p.split(text)
    for i in text_segment:
        j.append(i.replace('\n', ' '))

    fine_text = '\n\n'.join(j)    # 多次换行保留为直接换两行
    new_text = pangu.spacing_text(fine_text)
    return new_text


def format_text(long_str):
    long_str = clearSpace(long_str)
    long_str = clearReplace(long_str)
    window.clipboard_clear()
    window.clipboard_append(long_str)


def rebuildMac(mac_byte_list, mac_type):
    mac_string = ''
    mac_address = []
    result = ''
    mac_count = len(mac_byte_list)
    invalid_flag = 0

    if isinstance(mac_byte_list, str):
        invalid_flag = 1

    for i in range(0, mac_count):
        mac_string = mac_string + str(mac_byte_list[i])

    if mac_type == 1 and invalid_flag == 0:
        for i in range(0, 12, 2):
            mac_address.append(str(mac_string[i:i + 2]))
            result = ':'.join(mac_address)
    elif mac_type == 2 and invalid_flag == 0:
        for i in range(0, 9, 4):
            mac_address.append(str(mac_string[i:i + 4]))
            result = '.'.join(mac_address)
    elif mac_type == 3 and invalid_flag == 0:
        for i in range(0, 9, 4):
            mac_address.append(str(mac_string[i:i + 4]))
            result = '-'.join(mac_address)
    else:
        result = "Invalid MAC address"

    window.clipboard_clear()
    window.clipboard_append(result)


def checkMac(raw_mac):
    raw_mac = raw_mac.strip()
    if raw_mac.find(':') != -1:
        mac_byte = raw_mac.split(':')
    elif raw_mac.find('.') != -1:
        mac_byte = raw_mac.split('.')
    elif raw_mac.find('-') != -1:
        mac_byte = raw_mac.split('-')
    else:
        mac_byte = 'Invalid MAC address'
        return mac_byte
    return mac_byte


def buttonClick():
    clipboard_str = window.clipboard_get()
    text_box.delete('1.0', tk.END)  # 清除text组件内容
    format_text(clipboard_str)
    result_str = window.clipboard_get()
    text_box.insert(tk.INSERT, result_str)


def checkBoxClick():
    if is_on_top.get() == 1:
        window.wm_attributes('-topmost', 1)  # 锁定窗口置顶
    else:
        window.wm_attributes('-topmost', 0)  # 释放窗口置顶


def buttonClickColon():
    clipboard_str = window.clipboard_get()
    text_box.delete('1.0', tk.END)  # 清除text组件内容
    spliced_mac = checkMac(clipboard_str)
    rebuildMac(spliced_mac, 1)
    result_str = window.clipboard_get()
    text_box.insert(tk.INSERT, result_str)


def buttonClickDot():
    clipboard_str = window.clipboard_get()
    text_box.delete('1.0', tk.END)  # 清除text组件内容
    spliced_mac = checkMac(clipboard_str)
    rebuildMac(spliced_mac, 2)
    result_str = window.clipboard_get()
    text_box.insert(tk.INSERT, result_str)


def buttonClickDash():
    clipboard_str = window.clipboard_get()
    text_box.delete('1.0', tk.END)  # 清除text组件内容
    spliced_mac = checkMac(clipboard_str)
    rebuildMac(spliced_mac, 3)
    result_str = window.clipboard_get()
    text_box.insert(tk.INSERT, result_str)


window = tk.Tk()  # 创建Tkinter窗口
window.title('文本去空格/换行')
window.geometry('480x200-50-0')
window.minsize(width=480, height=200)

button_no_space = tk.Button(window, text=" 去空格/换行 ", command=buttonClick)
button_no_space.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
button_no_space.rowconfigure(0, weight=1)

button_mac_colon = tk.Button(window, text="MAC地址\n: 格式", command=buttonClickColon)
button_mac_colon.grid(row=0, column=1, padx=10, pady=10)
button_mac_colon.rowconfigure(0, weight=1)

button_mac_dot = tk.Button(window, text="MAC地址\n. 格式", command=buttonClickDot)
button_mac_dot.grid(row=0, column=2, padx=10, pady=10)
button_mac_dot.rowconfigure(0, weight=1)

button_mac_dash = tk.Button(window, text="MAC地址\n- 格式", command=buttonClickDash)
button_mac_dash.grid(row=0, column=3, padx=10, pady=10)
button_mac_dash.rowconfigure(0, weight=1)

# 文本框和滚动条
s1 = tk.Scrollbar(window, )
s1.grid(row=1, column=5, sticky=tk.N + tk.S + tk.E)
global text_box
text_box = tk.Text(window, yscrollcommand=s1.set, wrap=tk.WORD)
text_box.grid(row=1, column=0, columnspan=5, sticky=tk.E + tk.W + tk.N + tk.S)

# 置顶窗口复选框
is_on_top = tk.IntVar()
check_box = tk.Checkbutton(window, text="置顶窗口", variable=is_on_top, command=checkBoxClick)
check_box.deselect()
check_box.grid(row=0, column=4, sticky=tk.E)

window.rowconfigure(1, weight=1)
window.columnconfigure(0, weight=1)
window.mainloop()
