import threading
import sys
from cefpython3 import cefpython as cef
import ctypes
import app
import os

def run_flask():
    app.app.run(port=5000)

threading.Thread(target=run_flask, daemon=True).start()

window_info = cef.WindowInfo()

icon_path = os.path.abspath("./static/image/logo.ico")

icon_handle = ctypes.windll.user32.LoadImageW(
    0,
    icon_path,
    1,
    0, 0,
    0x00000010
)

cef.Initialize()
browser = cef.CreateBrowserSync(
    url="http://localhost:5000",
    window_title="Yagane",
)

hwnd = browser.GetWindowHandle()

ctypes.windll.user32.SendMessageW(
    hwnd,
    0x0080,
    0,
    icon_handle,
)

cef.MessageLoop()
cef.Shutdown()