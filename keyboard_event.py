from queue import Queue
import time
import ctypes
from unbind_all import unbind
import keyboard
#SendInput = ctypes.windll.user32.SendInput

# C struct redefinitions

PUL = ctypes.POINTER(ctypes.c_ulong)

key = {"up":0x48, "down":0x50, "left":0x4D, "right":0x4B,"z":0x2C,"Enter":0x1C,"Shift":0x2A}
key_num=[0x4B,0x48,0x4d,0x50]
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


# Actuals Functions
def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def SafePressKey(key_name,waiter=0.1):
    try:
        if type(key_name) is int:
            hexCode=key_name
        else:
            hexCode=key[key_name]
        PressKey(hexCode)
        time.sleep(waiter)
        ReleaseKey(hexCode)
    except Exception as e:
        unbind(ReleaseKey)
        raise e()
    
def get_keyevent():
    r=[0,0,0,0]
    get_key_list = [code for code in keyboard._pressed_events]
    if 72 in get_key_list:
        r[0] = 1
    if 80 in get_key_list:
        r[1] = 1
    if 75 in get_key_list:
        r[2] = 1
    if 77 in get_key_list:
        r[3] = 1
    return r
class key_event:
    def __init__(self):
        self.key_q=Queue()
        self.last_key=Queue()
        pass
    def add(self,key):
        self.key_q.put_nowait(key)
    def execute(self,waiter=1/360,timer=None):
        t_func=time.time
        if not time is None:
            t_func=timer
        s_t=time.time()
        while not self.last_key.empty():
            k=self.last_key.get()
            ReleaseKey(k)
        while not self.key_q.empty():
            k=self.key_q.get_nowait()
            self.last_key.put_nowait(k)
            PressKey(k)
        time.sleep(waiter)

        return 0
    def reset(self):
        while not self.key_q.empty():
            self.key_q.get_nowait()
        return 

#(0,0) (64,67) (776,894)
#東方輝針城　～ Double Dealing Character. ver 1.00a
#
#
#