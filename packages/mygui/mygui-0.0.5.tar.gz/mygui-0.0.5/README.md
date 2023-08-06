# mygui 0.0.5
## lgrid
+ A new Command that allows you to place a label in a grid. 
+ Simple and elegant implimentation as follows:
#
- lgrid({window_or_frame},{Text for label}, {Column Number},{Row Number})
- lgrid(root,"hello",1,5) Places a word 'hello' in row 1 column 5
#
Example script:

#

    import os
    from mygui import lgrid
    from tkinter import Tk
    root=Tk()
    root.minsize(300,100)
    lgrid(root,'Label placed in grid 5,5', 5,5)
    lgrid(root,'Label placed in grid 6,6', 6,6)

    root.mainloop()

#

