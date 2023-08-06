# LGRID & EGRID
import os
from tkinter import Entry, Label


def lgrid(self, text, gridcol, gridrow, **args):
    """  Label Maker
    Example :
        lgrid(root,'text to enter',0,0,**args)

    Where root is the instance of tkinter ,
    'Text to enter' is just that,
    0,0 is the column and row to place them"""
    lbl = Label(self, text=text)
    lbl.grid(column=gridcol, row=gridrow, **args)


def egrid(self, col, row, *args, **kwarg):
    """ Entry Maker
    Example:
    egrid(root,1,0)
    """
    e1 = Entry(self)
    e1.grid(column=col, row=row)
