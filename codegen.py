# codegen.py
from PIL import Image

def data_to_binary(data):
    return ''.join(format(byte, '08b') for byte in data)

def binary_to_image(binary_data, output_path="code.png"):
    binary_data = binary_data.ljust(1024, '0')
    img_size = 32
    pixel_size = 10
    img = Image.new("RGB", (img_size * pixel_size, img_size * pixel_size))

    for i, bit in enumerate(binary_data):
        x = (i % img_size) * pixel_size
        y = (i // img_size) * pixel_size
        color = (255, 0, 0) if bit == '1' else (0, 0, 0)
        for px in range(pixel_size):
            for py in range(pixel_size):
                img.putpixel((x + px, y + py), color)

    img.save(output_path)
    return output_path

def generate_code(data, output_path="code.png"):
    binary = data_to_binary(data)
    print("Binary data before encoding to image:", binary)  # Debug print
    return binary_to_image(binary, output_path)
