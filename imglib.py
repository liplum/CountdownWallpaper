from typing import Literal

from PIL import Image, ImageDraw, ImageFont


def newImg(size,
           mode: Literal["1", "CMYK", "F", "HSV", "I", "L", "LAB", "P", "RGB", "RGBA", "RGBX", "YCbCr"] = "RGB",
           bk="#FFFFFF") -> Image:
    im = Image.new(mode, size, bk)
    ImageDraw.Draw(im)
    return im


def drawText(img, pos, text, fontPath, size, anchor="ms", color="#000000"):
    font = ImageFont.truetype(fontPath, size)
    draw = ImageDraw.Draw(img)
    draw.text(pos, text, font=font, anchor=anchor, fill=color)
