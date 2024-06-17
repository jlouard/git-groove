#!/usr/bin/env python3

import tkinter as tk
from tkinter import *
from DabMoveDetection import DabMoveDetection

if __name__ == "__main__":
    root = tk.Tk()
    app = DabMoveDetection(root, 0)
    root.mainloop()
    root.configure(background='black') 
    root.mainloop()