import win32api
import win32gui
import win32con
import win32clipboard
import win32process

import ctypes
import time
import math

from const import VK_CODE, BALANCE_CONTROL_ID_GROUP

sleep_time = 0.2
retry_time = 5

def get_clipboard_data():
    win32clipboard.OpenClipboard()
    try:
        data = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT) # win32clipboard.CF_UNICODETEXT
    finally:
        win32clipboard.EmptyClipboard()
        win32clipboard.CloseClipboard()
    return data

def hot_key(keys):
    for key in keys:
        win32api.keybd_event(VK_CODE[key], 0, 0, 0)
    for key in reversed(keys):
        win32api.keybd_event(VK_CODE[key], 0, win32con.KEYEVENTF_KEYUP, 0)

def set_text(hwnd, string):
    win32gui.SetForegroundWindow(hwnd)
    win32api.SendMessage(hwnd, win32con.EM_SETSEL, 0, -1)
    win32api.keybd_event(VK_CODE['backspace'], 0, 0, 0)
    win32api.keybd_event(VK_CODE['backspace'], 0, win32con.KEYEVENTF_KEYUP, 0)
    for char in string:
        win32api.keybd_event(VK_CODE[char], 0, 0, 0)
        win32api.keybd_event(VK_CODE[char], 0, win32con.KEYEVENTF_KEYUP, 0)

def get_text(hwnd):
    length = ctypes.windll.user32.SendMessageW(hwnd, win32con.WM_GETTEXTLENGTH)
    buf = ctypes.create_unicode_buffer(length + 1)
    ctypes.windll.user32.SendMessageW(hwnd, win32con.WM_GETTEXT, length, ctypes.byref(buf))
    return buf.value

def parse_table(text):
    lines = text.split('\t\r\n')
    keys = lines[0].split('\t')
    result = []
    for i in range(1, len(lines)):
        info = {}
        items = lines[i].split('\t')
        for j in range(len(keys)):
            info[keys[j]] = items[j]
        result.append(info)
    return result


class ThsAuto:

    def __init__(self, window_title=u'网上股票交易系统5.0'):
        hwnd = win32gui.FindWindow(None, window_title)
        win32gui.SetForegroundWindow(hwnd)
        self.hwnd_main = hwnd

    def get_tree_hwnd(self):
        hwnd = self.hwnd_main
        hwnd = win32gui.FindWindowEx(hwnd, None, u'AfxMDIFrame42s', None)
        hwnd = win32gui.FindWindowEx(hwnd, None, u'AfxWnd42s', None)
        hwnd = win32gui.FindWindowEx(hwnd, None, u'Afx:400000:0', None)
        hwnd = win32gui.FindWindowEx(hwnd, None, u'AfxWnd42s', None)
        hwnd = win32gui.FindWindowEx(hwnd, None, u'SysTreeView32', None)
        return hwnd

    def get_right_hwnd(self):
        hwnd = self.hwnd_main
        hwnd = win32gui.FindWindowEx(hwnd, None, u'AfxMDIFrame42s', None)
        hwnd = win32gui.GetDlgItem(hwnd, 0xE901)
        return hwnd

    def get_balance(self):
        #win32gui.SetForegroundWindow(self.hwnd_main)
        hot_key(['F4'])
        time.sleep(sleep_time)
        self.refresh()
        hwnd = self.get_right_hwnd()
        result = {}
        for key, cid in BALANCE_CONTROL_ID_GROUP.items():
            ctrl = win32gui.GetDlgItem(hwnd, cid)
            result[key] = get_text(ctrl)
        return result
        
    def get_position(self):
        #win32gui.SetForegroundWindow(self.hwnd_main)
        hot_key(['F2'])
        time.sleep(sleep_time)
        hot_key(['F6'])
        time.sleep(sleep_time)
        self.refresh()
        hwnd = self.get_right_hwnd()
        ctrl = win32gui.GetDlgItem(hwnd, 0x417)
        win32gui.SetForegroundWindow(ctrl)
        time.sleep(sleep_time)
        hot_key(['ctrl', 'c'])
        data = None
        retry = 0
        while not data and retry < retry_time:
            retry += 1
            time.sleep(sleep_time)
            data = get_clipboard_data()
        if data:
            return parse_table(data)
        return {}

    def get_active_orders(self):
        #win32gui.SetForegroundWindow(self.hwnd_main)
        hot_key(['F1'])
        time.sleep(sleep_time)
        hot_key(['F8'])
        time.sleep(sleep_time)
        self.refresh()
        hwnd = self.get_right_hwnd()
        ctrl = win32gui.GetDlgItem(hwnd, 0x417)
        win32gui.SetForegroundWindow(ctrl)
        time.sleep(sleep_time)
        hot_key(['ctrl', 'c'])
        data = None
        retry = 0
        while not data and retry < retry_time:
            retry += 1
            time.sleep(sleep_time)
            data = get_clipboard_data()
        if data:
            return parse_table(data)
        return {}
        
    def get_filled_orders(self):
        #win32gui.SetForegroundWindow(self.hwnd_main)
        hot_key(['F2'])
        time.sleep(sleep_time)
        hot_key(['F7'])
        time.sleep(sleep_time)
        self.refresh()
        hwnd = self.get_right_hwnd()
        ctrl = win32gui.GetDlgItem(hwnd, 0x417)
        win32gui.SetForegroundWindow(ctrl)
        time.sleep(sleep_time)
        hot_key(['ctrl', 'c'])
        data = None
        retry = 0
        while not data and retry < retry_time:
            retry += 1
            time.sleep(sleep_time)
            data = get_clipboard_data()
        if data:
            return parse_table(data)
        return {}

    def sell(self, stock_no, amount, price):
        #win32gui.SetForegroundWindow(self.hwnd_main)
        price = '%.3f' % float(price)
        hot_key(['F2'])
        time.sleep(sleep_time)
        hwnd = self.get_right_hwnd()
        ctrl = win32gui.GetDlgItem(hwnd, 0x408)
        set_text(ctrl, stock_no)
        time.sleep(sleep_time)
        ctrl = win32gui.GetDlgItem(hwnd, 0x409)
        set_text(ctrl, price)
        time.sleep(sleep_time)
        ctrl = win32gui.GetDlgItem(hwnd, 0x40A)
        set_text(ctrl, str(amount))
        time.sleep(sleep_time)
        hot_key(['enter'])
        time.sleep(sleep_time)
        result = None
        retry = 0
        while not result and retry < retry_time:
            retry += 1
            time.sleep(sleep_time)
            # robi 注释掉以下代码
            # hot_key(['y'])
            # time.sleep(sleep_time)
            result = self.get_result()
        hot_key(['enter'])
        return result

    def buy(self, stock_no, amount, price):
        #win32gui.SetForegroundWindow(self.hwnd_main)
        price = '%.3f' % float(price)
        hot_key(['F1'])
        time.sleep(sleep_time)
        hwnd = self.get_right_hwnd()
        ctrl = win32gui.GetDlgItem(hwnd, 0x408)
        set_text(ctrl, stock_no)
        time.sleep(sleep_time)
        ctrl = win32gui.GetDlgItem(hwnd, 0x409)
        set_text(ctrl, price)
        time.sleep(sleep_time)
        ctrl = win32gui.GetDlgItem(hwnd, 0x40A)
        set_text(ctrl, str(amount))
        time.sleep(sleep_time)
        hot_key(['enter'])
        time.sleep(sleep_time)
        result = None
        retry = 0
        while not result and retry < retry_time:
            retry += 1
            time.sleep(sleep_time)
            # robi 注释掉以下代码
            # hot_key(['y'])
            # time.sleep(sleep_time)
            result = self.get_result()
        hot_key(['enter'])
        return result

    def cancel(self, entrust_no):
        #win32gui.SetForegroundWindow(self.hwnd_main)
        hot_key(['F3'])
        time.sleep(sleep_time)
        hwnd = self.get_right_hwnd()
        ctrl = win32gui.GetDlgItem(hwnd, 0x417)
        win32gui.SetForegroundWindow(ctrl)
        time.sleep(sleep_time)
        hot_key(['ctrl', 'c'])
        data = None
        retry = 0
        while not data and retry < retry_time:
            retry += 1
            time.sleep(sleep_time)
            data = get_clipboard_data()
        if data:
            entrusts = parse_table(data)
            find = None
            for i, entrust in enumerate(entrusts):
                if str(entrust['合同编号']) == str(entrust_no):
                    find = i
                    break
            if find is None:
                return {'success': False, 'msg': u'没找到指定订单'}
            left, top, right, bottom = win32gui.GetWindowRect(ctrl)
            x = 50 + left
            y = 30 + 16 * find + top
            win32api.SetCursorPos((x, y))

            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            time.sleep(sleep_time)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            time.sleep(sleep_time)
            result = None
            retry = 0
            while not result and retry < retry_time:
                retry += 1
                time.sleep(sleep_time)
                # robi 注释掉以下代码
                #hot_key(['y'])
                #time.sleep(sleep_time)
                result = self.get_result()
            hot_key(['enter'])
            return result

    def cancel_all(self, direct=None): # direct:None|all, '1'|buy, '2'|sell
        #win32gui.SetForegroundWindow(self.hwnd_main)
        hot_key(['F3'])
        time.sleep(sleep_time)
        hwnd = self.get_right_hwnd()
        if direct == '1':
            ctrl = win32gui.GetDlgItem(hwnd, 0x7532)
        elif direct == '2':
            ctrl = win32gui.GetDlgItem(hwnd, 0x7533)
        else:
            ctrl = win32gui.GetDlgItem(hwnd, 0x7531)
        win32gui.SetForegroundWindow(ctrl)
        time.sleep(sleep_time)
        left, top, right, bottom = win32gui.GetWindowRect(ctrl)
        x = 30 + left
        y = 10 + top
        win32api.SetCursorPos((x, y))

        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        time.sleep(sleep_time)
        result = None
        retry = 0
        while not result and retry < retry_time:
            retry += 1
            time.sleep(sleep_time)
            # robi 注释掉以下代码
            # hot_key(['y'])
            # time.sleep(sleep_time)
            result = self.get_result()
        hot_key(['enter'])
        return result


    def get_result(self):
        tid, pid = win32process.GetWindowThreadProcessId(self.hwnd_main)
        def enum_children(hwnd, results):
            try:
                if (win32gui.IsWindowVisible(hwnd) and
                        win32gui.IsWindowEnabled(hwnd)):
                    win32gui.EnumChildWindows(hwnd, handler, results)
            except Exception:
                return

        def handler(hwnd, results):
            if (win32api.GetWindowLong(hwnd, win32con.GWL_ID) == 0x3EC and 
                    win32gui.GetClassName(hwnd) == 'Static'):
                results.append(hwnd)
                return False
            enum_children(hwnd, results)
            return len(results) == 0
        popups = []
        windows = []            
        win32gui.EnumThreadWindows(tid, lambda hwnd, l: l.append(hwnd), windows)
        for hwnd in windows:
            if not handler(hwnd, popups):
                break
        if popups:
            ctrl = popups[0]
            text = get_text(ctrl)
            if u'已成功提交' in text:
                return {
                    'success': True,
                    'msg': text,
                    'entrust_no': text.split(u'合同编号：')[1].split('。')[0]
                }
            else:
                return {
                    'success': False,
                    'msg': text
                }

    def refresh(self):
        left, top, right, bottom = win32gui.GetWindowRect(self.hwnd_main)
        x = 170 + left
        y = 40 + top
        win32api.SetCursorPos((x, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        time.sleep(sleep_time)
