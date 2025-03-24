# decode.py
from PIL import Image

def image_to_binary(image_path):
    img = Image.open(image_path).convert("RGB")
    width, height = img.size
    img_size = 32
    pixel_size = width // img_size
    binary = ""

    for i in range(img_size * img_size):
        x = (i % img_size) * pixel_size + pixel_size // 2
        y = (i // img_size) * pixel_size + pixel_size // 2
        r, g, b = img.getpixel((x, y))
        bit = '1' if r > 128 else '0'
        binary += bit

    print("Binary data after decoding from image:", binary)  # Debug print
    return binary

def binary_to_data(binary):
    binary = binary[:len(binary) - (len(binary) % 8)]
    print("Trimmed binary data:", binary)  # Debug print
    data = bytearray()
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        data.append(int(byte, 2))
    print("Decoded bytes:", data)  # Debug print
    return bytes(data)
