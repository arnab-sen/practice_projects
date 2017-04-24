from PIL import Image
import os

def create_directories(*directories):
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
    
def get_image(file_name):
    if file_name[-4:] != ".png": file_name += ".png"
    return Image.open("Input\\" + file_name)

def save_image(image, file_name):
    if file_name[-4:] != ".png": file_name += ".png"
    image.save("Output\\" + file_name)

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
    remove_colours = input("Enter the colour you wish to remove (e.g. 0 0 0): ")
    values = remove_colours.split()
    values = [int(i) for i in values]
    remove_colour = (values[0], values[1], values[2])
    file_name = input("Enter your file name: ")
    while file_name != "exit":
        image = get_image(file_name).convert("RGBA")
        pixel_data = get_RGBA(image)
        new_pixel_data = pixel_data
        for i in range(len(pixel_data)):
            if check_pixel(pixel_data[i], remove_colour):
                # Make pixel transparent by making the alpha
                # channel 0
                new_pixel_data[i] = (0, 0, 0, 0)
        change_pixels(image, new_pixel_data)
        save_image(image, file_name)
        file_name = input("Enter your file name: ")

if __name__ == "__main__":
    main()
