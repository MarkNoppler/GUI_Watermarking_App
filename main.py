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
from typing import Optional


class WatermarkApp:
    """
    A GUI application for adding text-based watermarks to images using Tkinter and PIL.

    Features:
    - Upload an image.
    - Apply a user-defined text watermark.
    - Save the watermarked image.
    """

    def __init__(self, root: tk.Tk) -> None:
        """Initialize the watermarking application UI."""
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

        self.image: Optional[Image.Image] = None
        self.tk_image: Optional[ImageTk.PhotoImage] = None

    def upload_image(self) -> None:
        """
        Opens a file dialog for the user to select an image file, loads the image,
        and displays it on the canvas.
        """
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if file_path:
            self.image = Image.open(file_path)
            self.image.thumbnail((400, 400))
            self.tk_image = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(250, 200, image=self.tk_image)

    def add_watermark(self) -> None:
        """
        Applies a text watermark to the uploaded image. If no image is uploaded,
        or no text is provided, an error message is shown.
        """
        if self.image is None:
            messagebox.showerror("Error", "Please upload an image first")
            return

        watermark_text = self.text_entry.get().strip()
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

    def save_image(self) -> None:
        """
        Opens a file dialog to save the watermarked image in PNG or JPG format.
        If no image is available, an error message is displayed.
        """
        if self.image is None:
            messagebox.showerror("Error", "No image to save")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All Files", "*.*")]
        )
        if file_path:
            self.image.save(file_path)
            messagebox.showinfo("Success", "Image saved successfully")


if __name__ == "__main__":
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop()



