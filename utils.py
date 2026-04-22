import os

def safe_delete(path):
    try:
        if path and os.path.exists(path):
            os.remove(path)
    except:
        pass