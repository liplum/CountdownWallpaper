import os


def deleteF(path):
    try:
        os.remove(path)
    except:
        pass
