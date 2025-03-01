from windows.PhotoViewer import PhotoViewer

import tkinter as tk
from tkinter import filedialog

class GetFolder:
    def open_directory(self):
        dir_path  = filedialog.askdirectory()

        self.root.destroy()

        root_viewer_tk = tk.Tk()

        PhotoViewer(root_viewer_tk, dir_path, "../outputs")

    def __init__(self, root):
        self.root = root

        self.label = tk.Label(root)
        self.label.pack()

        self.open_button = tk.Button(root, text="Load folder", command=self.open_directory)
        self.open_button.pack()