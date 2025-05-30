import tkinter as tk
from src.gui.main_window import PDFMakerApp

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFMakerApp(root)
    root.mainloop()