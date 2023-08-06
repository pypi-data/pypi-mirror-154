
import os

try:

    from mygui import lgrid
except:
    os.system('pip install mygui')
    from mygui import lgrid

from tkinter import Tk

root = Tk()
root.minsize(300, 100)
# Add Icon to windows Titlebar if running Windows.
if os.name == 'nt':
    homepath = os.path.expanduser('~')
    tempFile = '%s\Caveman Software\%s' % (homepath, 'Icon\icon.ico')

    if (os.path.exists(tempFile) == True):
        root.wm_iconbitmap(default=tempFile)

    else:
        os.system('pip install create_icon')
        import create_icon
        print('File Created')
        root.wm_iconbitmap(default=tempFile)
lgrid(root, 'Label placed in grid 5,5', 5, 5)
lgrid(root, 'Label placed in grid 6,6', 6, 6)

root.mainloop()
