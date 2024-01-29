from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox

original_image = None
watermarked_image = None
tk_image = None
flipped_image_tk = None
flipped_image = None


def open_file_dialog():
    global original_image
    file_path = filedialog.askopenfilename(filetypes = [("jpeg", ".jpg .jpeg"),
                                                        ("png", ".png"),
                                                        ("bitmap", "bmp"),
                                                        ("gif", ".gif")])
    if file_path:
        original_image = Image.open(file_path)
        display_image(original_image)


def display_image(image):
    global original_image, tk_image
    resized_image = image.resize((400, 300), Image.LANCZOS)
    tk_image = ImageTk.PhotoImage(resized_image)
    # Update the label with the new image
    image_label.config(image=tk_image)
    image_label.image = tk_image
    original_image = resized_image


def add_watermark():
    global original_image, tk_image, watermarked_image, flipped_image
    if flipped_image:
        watermarked_image = flipped_image.copy()
    elif original_image:
        watermarked_image = original_image.copy()
    logo_path = "logo/logo1.png"
    logo_image = Image.open(logo_path)
    # Resize the logo
    logo_width, logo_height = logo_image.size
    logo_target_height = watermarked_image.height // 5
    logo_target_width = int((logo_target_height / logo_height) * logo_width)
    logo_image = logo_image.resize((logo_target_width, logo_target_height), Image.LANCZOS)
    # Paste the logo onto the watermarked image
    paste_position = (watermarked_image.width - logo_image.width - 3, watermarked_image.height - logo_image.height - 3)
    watermarked_image.paste(logo_image, paste_position, logo_image)
    watermarked_tk_image = ImageTk.PhotoImage(watermarked_image)
    # Display the watermarked image in a separate label
    image_label.config(image=watermarked_tk_image)
    image_label.image = watermarked_tk_image


def save_file():
    global watermarked_image
    file = filedialog.asksaveasfilename(defaultextension = ".jpg",
                                                 filetypes = [("JPEG files", "*.jpg"), ("All files", "*.*")],
                                                 title = "Save As",
                                                 initialfile = "watermarked_image.jpg")
    if file:
        finished_img = watermarked_image.convert("RGB")
        finished_img.save(file)
        messagebox.showinfo("Success", "Image successfully saved on your device.")


def flip():
    global original_image, flipped_image
    if flipped_image:
        image = flipped_image.copy()
    else:
        image = original_image.copy()
    flipped_image = image.transpose(Image.Transpose.ROTATE_270).resize((300, 400), Image.LANCZOS)
    flipped_image_tk = ImageTk.PhotoImage(flipped_image)
    image_label.config(image=flipped_image_tk)
    image_label.image = flipped_image_tk


root = tk.Tk()
root.title("Image Watermarking")

logo = Image.open("logo/logo1.png")
logo = logo.resize((200, 200))
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image = logo)
logo_label.image = logo
logo_label.grid(column = 1, row = 1, rowspan=4)

# Create a label to display the original image
image_label = tk.Label(root)
image_label.grid(column = 1, row = 1, rowspan = 4, padx=10, pady=(10,10))

upload_button = tk.Button(root, text = "Upload image", command = open_file_dialog, width = 9)
upload_button.grid(column = 2, row = 1, padx=(0,10))

watermark_button = tk.Button(root, text="Add Watermark", command=add_watermark, width = 9)
watermark_button.grid(column = 2, row= 2, padx=(0,10))

save_button = tk.Button(root, text="Save image", command = save_file, width = 9)
save_button.grid(column=2, row=3, padx=(0,10))

flip_button = tk.Button(root, text="Flip image ⤵", command = flip, width = 9)
flip_button.grid(column = 2, row=4, padx=(0,10))

root.mainloop()
