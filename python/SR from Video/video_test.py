# Only working with python 3.5.2
import cv2
import os
import copy
from PIL import Image

def get_frame(file_name):
    # Opens the latest video recording and returns
    # one of the last frames, which should be from
    # the user's career profile screen
    # That frame is then saved as a PNG image
    
    cap = cv2.VideoCapture(file_name + ".mp4")
    if not cap.isOpened():
        print("Could not open", file_name + ".mp4")

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    #print(frame_count)
    # set the first frame to the desired frame (the last frame)
    cap.set(1, frame_count - 10) 
    ret, frame = cap.read()
    #cv2.imshow("Window", frame)
    cv2.imwrite(file_name + ".png", frame)

    return file_name + ".png"

def get_sr_block(file_name):
    # Return a cropped image of the user's current SR
    # Cropped image position ((topleft), (bottomright)):
    # ((1053, 80), (1093, 102))
    if file_name[-4:] != ".png": file_name += ".png"
    career_profile = Image.open(file_name)
    career_profile = career_profile.resize((1280, 720), Image.ANTIALIAS)
    sr_block = career_profile.crop((1052, 81, 1097, 103))
    return sr_block

def simplify_image(image):
    # Converts the SR block to a black and white image, where
    # the purple background is black and the text is white,
    # by finding the average colour sum of the image (R + G + B),
    # and for each pixel, if its sum < average, it becomes a white pixel,
    # and if its sum > average, it becomes a black pixel
    white = (255, 255, 255)
    black = (0, 0, 0)
    average = get_average_colour(image)
    pixel_data = list(image.getdata())
    for i in range(len(pixel_data)):
        if sum(pixel_data[i]) > average:
            pixel_data[i] = white
        else:
            pixel_data[i] = black
            
    image.putdata(pixel_data)
    
    return image

def get_average_colour(image):
    pixel_data = list(image.getdata())
    total = 0
    for i in range(len(pixel_data)):
        total += sum(pixel_data[i])
    average_colour_sum = total // len(pixel_data)
    
    return average_colour_sum

def get_data():
    # Gets a set of SR blocks with at least one instance of
    # all numbers from 0 - 9
    file_name = "nums "
    for i in range(1, 8):
        sr_block = get_sr_block(get_frame(file_name + str(i)))
        simplify_image(sr_block)
        sr_block.save(file_name + str(i) + ".png")

def split_list(cols, linear_list):
    # Converts a linear list to a 2D list
    temp_list = []
    split_list = []
    for i in range(len(linear_list)):
        temp_list += [linear_list[i]]
        if (i + 1) % cols == 0:
            split_list += [temp_list]
            temp_list = []

    return split_list

def get_digits(sr_block):
    # Split the SR block into four digits
    pixel_data = list(sr_block.getdata())
    width, height = sr_block.size[0], sr_block.size[1]
    pixel_data = split_list(sr_block.size[0], pixel_data)
    #digits = [copy.deepcopy(pixel_data)]
    digits = [""] * 4
    
    #for i in range(3):
    #    digits += [copy.deepcopy(pixel_data)]

    # Find digit edges:
    white = (255, 255, 255)
    black = (0, 0, 0)
    previous_pixel = black
    
    # First edge:
    #for i, pixel in enumerate(pixel_data[2]):
    #    if pixel == white and previous_pixel == black:
    #        first_edge = i
    #        break
    # Don't think I need the first edge
        
    # Right edges:
    edges = [0]
    for i, pixel in enumerate(pixel_data[2]):
        if pixel == black and previous_pixel == white:
            edges += [i]
        previous_pixel = pixel

    for i in range(len(edges) - 1):
        digits[i] = sr_block.crop((edges[i], 0, edges[i + 1], height))

    for i, image in enumerate(digits):
        image.save("digit " + str(i) + ".png")

def get_base_data():
    # Retrieves the base information for recognising digits:
    # how many white pixels are in each third of each number;
    # each number should have a unique combination of thirds,
    # and when using this for number recognition, the unknown
    # digit will be split up into thirds, and then the number
    # of white pixels in each of its thirds will be compared to
    # those in the known digits, and the unknown digit will be
    # recognised as the digit that its thirds are closest to
    digits = []
    thirds = []
    temp = []
    pixel_counts = []
    white = (255, 255, 255)
    black = (0, 0, 0)    
    
    for i in range(10):
        digits += [Image.open("digits\\" + str(i) + ".png")]

    width, height = digits[0].size[0], digits[0].size[1]
    third = height // 3
    
    for i in range(10):
        temp += [digits[i].crop((0, 0, width, third))]
        temp += [digits[i].crop((0, third, width, third * 2))]
        temp += [digits[i].crop((0, third * 2, width, height))]
        thirds += [temp]
        temp = []

    # Count the white pixels
    for digits in thirds:
        for third in digits:
            count = 0
            pixel_data = list(third.getdata())
            for pixel in pixel_data:
                if pixel == white: count += 1
            temp += [count]
        pixel_counts += [temp]
        temp = []

    #print(pixel_counts)
    #thirds[0][0].save("digits\\0_third_1.png")
        
    return pixel_counts
        
def main():   
    #file_name = "test"
    #sr_block = get_sr_block(get_frame(file_name))
    #sr_block.save("sr_block_cropped.png")
    #sr_block.save("test_sr_block.png")
    #simplify_image(sr_block)
    #sr_block.save("test_contrast.png")
    #get_data()
    #print(type(frame))
    #sr_block = Image.open("nums 6.png")
    #digits = get_digits(sr_block)
    get_base_data()
    
    pass

if __name__ == "__main__":
    main()
