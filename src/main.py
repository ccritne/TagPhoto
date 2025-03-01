import tkinter as tk
from windows.GetFolder import GetFolder

if __name__ == "__main__":

    root = tk.Tk()

    file = GetFolder(root)
    
    root.mainloop()