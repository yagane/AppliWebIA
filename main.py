import threading
import sys
from cefpython3 import cefpython as cef
import app

def run_flask():
    app.app.run(port=5000)

# Lancer Flask dans un thread séparé
threading.Thread(target=run_flask, daemon=True).start()

# Configuration du navigateur embarqué
cef.Initialize()
cef.CreateBrowserSync(url="http://localhost:5000",
                      window_title="Mon App Flask Embarquée")
cef.MessageLoop()
cef.Shutdown()