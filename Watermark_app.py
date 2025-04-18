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
from tkinter import filedialog, messagebox, colorchooser
from PIL import Image, ImageDraw, ImageFont, ImageTk
from typing import Optional


class WatermarkApp:
    """
    A GUI application for adding text-based watermarks to images using Tkinter and PIL.

    Features:
    - Upload an image.
    - Apply a user-defined text watermark.
    - Customize text color and opacity.
    - Save the watermarked image.
    """


    def __init__(self, root: tk.Tk) -> None:
        """Initialize the watermarking application UI."""
        self.root = root
        self.root.title("Image Watermarking")

        self.canvas = tk.Canvas(root, width=500, height=400)
        self.canvas.pack(pady=10)

        self.upload_btn = tk.Button(root, text="Upload Image", command=self.upload_image)
        self.upload_btn.pack(pady=10)

        self.text_entry = tk.Entry(root, width=30)
        self.text_entry.pack(pady=5)
        self.text_entry.insert(0, "Enter Watermark Text")

        self.color_btn = tk.Button(root, text="Choose Color", command=self.choose_color)
        self.color_btn.pack(pady=5)

        self.opacity_scale = tk.Scale(root, from_=0, to=255, orient="horizontal", label="Opacity")
        self.opacity_scale.set(255)
        self.opacity_scale.pack(pady=5)

        self.add_watermark_btn = tk.Button(root, text="Add Watermark", command=self.add_watermark)
        self.add_watermark_btn.pack(pady=5)

        self.save_btn = tk.Button(root, text="Save Image", command=self.save_image)
        self.save_btn.pack(pady=5)

        self.original_image: Optional[Image.Image] = None
        self.image: Optional[Image.Image] = None
        self.tk_image: Optional[ImageTk.PhotoImage] = None
        self.text_color = (255, 255, 255)


    def upload_image(self) -> None:
        """
        Opens a file dialog for the user to select an image file, loads the image,
        and displays it on the canvas.
        """
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if file_path:
            self.original_image = Image.open(file_path)
            self.original_image.thumbnail((400, 400))
            self.image = self.original_image.copy()
            self.display_image()


    def display_image(self) -> None:
        """
        Updates the Tkinter canvas to display the current image.
        Converts the PIL image to a Tkinter-compatible format and places it on the canvas.
        """
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(250, 200, image=self.tk_image)


    def choose_color(self) -> None:
        """Opens a color chooser dialog to select the text color."""
        color_code = colorchooser.askcolor(title="Choose Text Color")[0]
        if color_code:
            self.text_color = tuple(int(c) for c in color_code)


    def add_watermark(self) -> None:
        """
        Applies a text watermark to the uploaded image. Allows customization of text color and opacity.
        If no image is uploaded, or no text is provided, an error message is shown.
        """
        if self.original_image is None:
            messagebox.showerror("Error", "Please upload an image first")
            return

        watermark_text = self.text_entry.get().strip()
        if not watermark_text:
            messagebox.showerror("Error", "Please enter watermark text")
            return

        self.image = self.original_image.copy().convert("RGBA")
        txt_layer = Image.new("RGBA", self.image.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt_layer)

        try:
            font = ImageFont.truetype("arial.ttf", 30)
        except IOError:
            font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), watermark_text, font=font)
        text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]

        width, height = self.image.size
        position = (width - text_width - 20, height - text_height - 20)

        opacity = self.opacity_scale.get()
        draw.text(position, watermark_text, fill=(self.text_color[0], self.text_color[1], self.text_color[2], opacity),
                  font=font)

        self.image = Image.alpha_composite(self.image, txt_layer).convert("RGB")
        self.display_image()


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

#run programme
if __name__ == "__main__":
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop()



