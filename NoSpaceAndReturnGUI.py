import noSpaceReturn
import re
import pangu
import sys
import ipaddress
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt


class NoSpaceReturn(QMainWindow):

    def __init__(self, parent=None):
        super(QMainWindow, self).__init__(parent)
        self.ui = noSpaceReturn.Ui_MainWindow()
        self.ui.setupUi(self)

        self.flag_keep_period_replace = 0

    # 文本处理
    def clearSpace(self, text):
        # 文本分行至列表
        text_line_list = re.split(r'(\n)', text)

        # 删除空元素
        while '' in text_line_list:
            text_line_list.remove('')

        for l_index, text_line in enumerate(text_line_list):
            # 如果是换行符跳过处理
            if text_line == '\n':
                continue
            else:
                # 匹配带空格的中文分割文本至列表
                word_list = re.split(r'([\u4e00-\u9fa5。，#@$%&*？！：；《》、（）]{1} +)', text_line)
                # 删除空元素
                while '' in word_list:
                    word_list.remove('')

                for index, words in enumerate(word_list):
                    # 逐项去除重复空格
                    new_words = words.strip()
                    # 处理英文句子中的重复空格
                    if len(new_words.split()) != 1:
                        new_words = ' '.join(new_words.split())
                    # 更新结果
                    word_list[index] = new_words
                nice_line = ''.join(word_list)
                # 更新结果
                text_line_list[l_index] = nice_line
        # 重新组合所有行
        nice_text = ''.join(text_line_list)
        return nice_text

    def clearReplace(self, text):
        paragraph = []
        multi_replace_regexp = re.compile(r'\n\s*\n')
        text_segment = multi_replace_regexp.split(text)

        period_replace_regexp = re.compile(r'\n')

        for i in text_segment:
            line_i = i.strip()
            if self.flag_keep_period_replace == 1:
                line_tmp = []
                line_segment = period_replace_regexp.split(line_i)
                for j in line_segment:
                    line_j = j.strip()
                    if re.match(r'.*[.:?!。：？！]$', line_j):
                        line_tmp.append(line_j)
                        line_tmp.append('\n')
                    else:
                        line_tmp.append(line_j)
                        line_tmp.append(' ')
                paragraph.append(''.join(line_tmp))
            else:
                paragraph.append(line_i.replace('\n', ' '))

        fine_text = '\n\n'.join(paragraph)  # 多次换行保留为直接换两行
        new_text = pangu.spacing_text(fine_text)
        return new_text

    def formatText(self, long_str):
        long_str = self.clearSpace(long_str)
        long_str = self.clearReplace(long_str)
        clipboard = QApplication.clipboard()
        clipboard.setText(long_str)

    # 是否保留行尾句号分段
    def checkBoxClick(self):

        if self.ui.chkbox_is_keep_period.isChecked():
            self.flag_keep_period_replace = 1
        else:
            self.flag_keep_period_replace = 0

    def buttonClickNoSpace(self):
        clipboard_str = QApplication.clipboard()
        self.formatText(clipboard_str.text())
        # 为避免英文换行时行尾和行头两个单词相连，替换时会增加一个空格（没有人工智能识别行尾单词是否完整，采用比较原始的处理）
        # 这可能导致第一次处理后中文之间仍有空格存在，故处理两次
        clipboard_str = QApplication.clipboard()
        self.formatText(clipboard_str.text())

        clipboard_str = QApplication.clipboard()
        result_str = clipboard_str.text()
        self.ui.plainTextEdit.setPlainText(result_str)

    # MAC 处理
    def rebuildMac(self, mac_byte_list, mac_type):
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

        clipboard = QApplication.clipboard()
        clipboard.setText(result)

    def checkMac(self, raw_mac):
        raw_mac = raw_mac.strip().lower()
        valid_mac = re.match('([0-9a-f]{2}[:\-]){5}([0-9a-f]{2})|([0-9a-f]{4}[.\-]){2}([0-9a-f]{4})', raw_mac)
        print(valid_mac)
        if raw_mac != "" and valid_mac is not None:
            if raw_mac.find(':') != -1:
                mac_byte = raw_mac.split(':')
            elif raw_mac.find('.') != -1:
                mac_byte = raw_mac.split('.')
            elif raw_mac.find('-') != -1:
                mac_byte = raw_mac.split('-')
            else:
                return "Invalid MAC address"
            return mac_byte
        else:
            return "Invalid MAC address"

    def buttonClickColon(self):
        clipboard_str = QApplication.clipboard()
        spliced_mac = self.checkMac(clipboard_str.text())
        if spliced_mac:
            self.rebuildMac(spliced_mac, 1)
            clipboard_str = QApplication.clipboard()
            result_str = clipboard_str.text()
            self.ui.plainTextEdit.setPlainText(result_str)
        else:
            self.ui.plainTextEdit.setPlainText("Invalid MAC address")
            pass

    def buttonClickDot(self):
        clipboard_str = QApplication.clipboard()
        spliced_mac = self.checkMac(clipboard_str.text())
        self.rebuildMac(spliced_mac, 2)
        result_str = clipboard_str.text()
        self.ui.plainTextEdit.setPlainText(result_str)

    def buttonClickDash(self):
        clipboard_str = QApplication.clipboard()
        spliced_mac = self.checkMac(clipboard_str.text())
        self.rebuildMac(spliced_mac, 3)
        result_str = clipboard_str.text()
        self.ui.plainTextEdit.setPlainText(result_str)

    def generateEui64Address(self, mac_string=None):
        if mac_string is not None and len(mac_string) == 12:
            # 将 mac 字符串分为 aa, bbcc, ddeeff 三段
            sg = re.split('(.{2})(.{2})(.{2})(.{2})(.{2})(.{2})', mac_string)
            print(sg)

            # 删除空元素
            while '' in sg:
                sg.remove('')

            # 将 MAC 地址第 7 bit 取反
            sg[0] = hex(int("0x"+sg[0], 16) ^ 0x2)[2:4]
            print(sg)

            # 组合成 EUI-64 链路本地地址
            ll_addr = "fe80::"+sg[0]+sg[1]+":"+sg[2]+"ff:fe"+sg[3]+":"+sg[4]+sg[5]
            result = ipaddress.IPv6Address(ll_addr).compressed

        else:
            result = "Invalid MAC address"

        clipboard = QApplication.clipboard()
        clipboard.setText(result)




    def buttonClickEui64Lla(self):
        clipboard_str = QApplication.clipboard()
        spliced_mac = self.checkMac(clipboard_str.text())
        mac_str = "".join(spliced_mac)
        if mac_str.find('Invalid'):
            self.generateEui64Address(mac_str)
        else:
            self.ui.plainTextEdit.setPlainText(mac_str)
            return

        sg = re.split('(.{2})(.{2})(.{2})(.{2})(.{2})(.{2})', mac_str)
        # 删除空元素
        while '' in sg:
            sg.remove('')
        mac_add = ":".join(sg)

        self.ui.plainTextEdit.setPlainText("原MAC: "+mac_add)
        result_str = clipboard_str.text()
        self.ui.plainTextEdit.appendPlainText("链接本地 IPv6: "+result_str)

    # 置顶复选框
    def checkBoxOnTop(self):
        if self.ui.chkbox_is_on_top.isChecked().__bool__():
            self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        else:
            self.setWindowFlag(Qt.WindowStaysOnTopHint, False)  # 释放窗口置顶

        if not self.isVisible():
            self.setVisible(True)


if __name__ == '__main__':
    # application 对象
    app = QApplication(sys.argv)

    # QMainWindow对象在类NoSpaceReturn生成
    main_window = NoSpaceReturn()

    # 控件关联信号和外部槽函数
    main_window.ui.bt_no_space.clicked.connect(main_window.buttonClickNoSpace)
    main_window.ui.chkbox_is_keep_period.clicked.connect(main_window.checkBoxClick)

    main_window.ui.bt_mac_colon.clicked.connect(main_window.buttonClickColon)
    main_window.ui.bt_mac_dot.clicked.connect(main_window.buttonClickDot)
    main_window.ui.bt_mac_dash.clicked.connect(main_window.buttonClickDash)
    main_window.ui.bt_eui64_lla.clicked.connect(main_window.buttonClickEui64Lla)

    main_window.ui.chkbox_is_on_top.clicked.connect(main_window.checkBoxOnTop)

    # 显示
    main_window.show()
    sys.exit(app.exec_())
