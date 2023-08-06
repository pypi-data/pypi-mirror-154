# mygui 0.0.9
## lgrid
+ A new Command that allows you to place a label in a grid. 
+ Simple and elegant implimentation as follows:
#
- lgrid({window_or_frame},{Text for label}, {Column Number},{Row Number})
- lgrid(root,"hello",1,5) Places a word 'hello' in row 1 column 5
#

## egrid
+ A new Command that allows you to place an entry box in a grid. 
+ Simple and elegant implimentation as follows:

Example script:

#

    import os
    from tkinter import Tk
    from mygui import egrid, lgrid

    root = Tk()
    root.minsize(300, 100)
    lgrid(root, 'Label placed in grid 0,0', 0, 0)
    lgrid(root, 'Label placed in grid 0,1', 0, 1)
    egrid(root, 1, 0)
    root.mainloop()

#

