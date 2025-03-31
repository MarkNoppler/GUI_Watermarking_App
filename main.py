"""
What it is:
Watermarking application to add text to an image using Tkinter and Pillow.

How to use:
Run the programme. Application has a button to upload an image, an input for watermarking text and a save function for
the updated image.

Documentation:
https://docs.python.org/3/library/tkinter.html
https://pypi.org/project/pillow/

Made by:
Jacob Fairhurst
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk


class WatermarkApp:
    """
    Creates a watermarking application using TKinter, adding text to images.
    Can upload an image on the programme and apply the text layer.
    Has a save feature on the programme to keep the watermarked image.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Image Watermarking")

        self.canvas = tk.Canvas(root, width=500, height=400)
        self.canvas.pack()

        self.upload_btn = tk.Button(root, text="Upload Image", command=self.upload_image)
        self.upload_btn.pack()

        self.text_entry = tk.Entry(root, width=30)
        self.text_entry.pack()
        self.text_entry.insert(0, "Enter Watermark Text")

        self.add_watermark_btn = tk.Button(root, text="Add Watermark", command=self.add_watermark)
        self.add_watermark_btn.pack()

        self.save_btn = tk.Button(root, text="Save Image", command=self.save_image)
        self.save_btn.pack()

        self.image= None
        self.tk_image = None

    def upload_image(self):
        """
        Function that allows the user to upload an image to the application for watermarking.
        """
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if file_path:
            self.image = Image.open(file_path)
            self.image.thumbnail((400, 400))
            self.tk_image = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(250, 200, image=self.tk_image)

    def add_watermark(self):
        """
        Function to apply the watermarking to the uploaded image.
        Supports image transparency with RGBA, adds text and merges image with text layer.
        Converts back to RGB before saving.
        """
        if self.image is None:
            messagebox.showerror("Error", "Please upload an image first")
            return

        watermark_text = self.text_entry.get()
        if not watermark_text:
            messagebox.showerror("Error", "Please enter watermark text")
            return

        watermark_image = self.image.convert("RGBA")
        txt_layer = Image.new("RGBA", watermark_image.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt_layer)

        try:
            font = ImageFont.truetype("arial.ttf", 30)
        except IOError:
            font = ImageFont.load_default()


        bbox = draw.textbbox((0, 0), watermark_text, font=font)
        text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]


        width, height = watermark_image.size
        position = (width - text_width - 20, height - text_height - 20)


        draw.text(position, watermark_text, fill=(255, 255, 255, 255), font=font)


        watermarked_image = Image.alpha_composite(watermark_image, txt_layer)

        self.image = watermarked_image.convert("RGB")
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(250, 200, image=self.tk_image)

    def save_image(self):
        """Function to save the newly watermarked image."""
        if self.image is None:
            messagebox.showerror("Error", "No image to save")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"),
                                                                                    ("JPEG files", "*.jpg"),
                                                                                    ("All Files", "*.*")])
        if file_path:
            self.image.save(file_path)
            messagebox.showinfo("Success", "Image saved successfully")

#runs programme
if __name__ == "__main__":
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop()


