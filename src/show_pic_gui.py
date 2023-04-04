import tkinter as tk
import urllib.request

import PIL
import requests
from PIL import ImageTk, Image
import io


def open_image():
    url = url_entry.get()
    image_bytes = requests.get(url).content
    try:
        data_stream = io.BytesIO(image_bytes)
        pil_image = Image.open(data_stream)
        pil_image = pil_image.resize((400, 400), Image.ANTIALIAS)
        tk_image = ImageTk.PhotoImage(pil_image)
        image_label.config(image=tk_image)
        image_label.image = tk_image
    except PIL.UnidentifiedImageError:
        print('无法识别的图片文件')
    # data_stream = io.BytesIO(image_bytes)
    # print(data_stream)
    # pil_image = Image.open(data_stream)

window = tk.Tk()
window.title("显示图片")

url_label = tk.Label(window, text="图片链接:")
url_label.pack()

url_entry = tk.Entry(window, width=50)
url_entry.pack()

open_button = tk.Button(window, text="打开图片", command=open_image)
open_button.pack()

image_label = tk.Label(window)
image_label.pack()



window.mainloop()
