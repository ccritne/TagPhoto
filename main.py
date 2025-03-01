import tkinter as tk
from PIL import Image, ImageTk, UnidentifiedImageError
import glob
from tkinter import filedialog
import shutil
import os

class GetFolder:
    def open_directory(self):
        dir_path  = filedialog.askdirectory()

        self.root.destroy()

        root_viewer_tk = tk.Tk()

        PhotoViewer(root_viewer_tk, dir_path, "outputs")
    
    def __init__(self, root):
        self.root = root

        self.label = tk.Label(root)
        self.label.pack()

        self.open_button = tk.Button(root, text="Load folder", command=self.open_directory)
        self.open_button.pack()

class PhotoViewer:
    def __init__(self, root, dir_path, output):
        self.root = root
        self.root.title("Photo Viewer")

        self.name_project = os.path.basename(dir_path)
        self.output_path = output

        self.images = self.get_valid_images(dir_path)
        self.current_index = 0

        if not self.images:
            print("No images found!")
            self.root.destroy()
            return
        
        self.label = tk.Label(root)
        self.label.pack()

        self.text_entry = tk.Entry(root, width=50)
        self.text_entry.pack(pady=10)

        # Bind Enter key to show next image
        self.root.bind("<Return>", self.show_next_image)  # Press Enter to go to the next image

        # Show the first image
        self.show_image()

    def show_image(self):
        # Display the current image
        file_path = self.images[self.current_index]["path"]
        name = os.path.basename(file_path)
        image = Image.open(file_path)
        image = image.resize((500, 500))  # Resize for display
        self.photo = ImageTk.PhotoImage(image)

        self.label.config(image=self.photo)
        self.root.title(f"Photo Viewer - {name}")

    def show_next_image(self, event=None):
        self.images[self.current_index]["tags"] = self.text_entry.get().split(" ")
        self.text_entry.delete(0, tk.END)
        # Show the next image when Enter is pressed"""
        self.current_index += 1
        if self.current_index >= len(self.images):

            output_dir = os.path.join(self.output_path, self.name_project)

            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            for image in self.images:
                
                for tag in image["tags"]:
                    suboutput_dir = os.path.join(output_dir, tag)

                    if not os.path.exists(suboutput_dir):
                        os.makedirs(suboutput_dir)
                    
                    shutil.copy(image["path"], suboutput_dir)

            self.root.quit()  # Quit after last image
            return
        
        self.show_image()

    def get_valid_images(self, path):
        # Get all valid image files from the folder
        all_files = glob.glob(f"{path}/*")  # Get all files in the folder
        valid_images = []

        for file in all_files:
            if not os.path.isfile(file):  # Ignore folders
                continue
            try:
                Image.open(file).verify()  # Check if it's a valid image
                valid_images.append({
                    "path": file,
                    "tags": []
                })
            except (UnidentifiedImageError, IOError):
                print(f"Skipping invalid image: {file}")

        return valid_images  # Sort the list alphabetically

if __name__ == "__main__":


    root = tk.Tk()

    file = GetFolder(root)
    
    root.mainloop()