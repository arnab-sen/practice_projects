from PIL import Image
import os

def create_directories(*directories):
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
    
def get_image(file_name):
    return Image.open("Input\\" + file_name)

def save_image(image, save_name):
    image.save("Output\\" + save_name)

def get_RGBA(image):
    return list(image.getdata())

def check_pixel(rgba, wanted_colour):
    if rgba[:3] == wanted_colour:
        return True
    else:
        return False

def change_pixels(image, new_pixel_data):
    image.putdata(new_pixel_data)
    
def main():
    create_directories("Input", "Output")
    file_name = input("Enter your file name (e.g. file1.png): ")
    image = get_image(file_name).convert("RGBA")
    pixel_data = get_RGBA(image)
    new_pixel_data = pixel_data
    white = (255, 255, 255)
    for i in range(len(pixel_data)):
        if check_pixel(pixel_data[i], white):
            # Make pixel transparent by making the alpha
            # channel 0
            new_pixel_data[i] = (0, 0, 0, 0)
    change_pixels(image, new_pixel_data)
    save_image(image, file_name)

if __name__ == "__main__":
    main()
