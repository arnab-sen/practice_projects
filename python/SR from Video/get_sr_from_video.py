# Only working with python 3.5.2
import cv2
import os
import copy
from PIL import Image

white = (255, 255, 255)
black = (0, 0, 0)

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
        if sum(pixel_data[i]) > average + (average // 2):
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

    save_digits = True
    if save_digits:
        for i, image in enumerate(digits):
            image.save("digit " + str(i) + ".png")

    return digits

def get_thirds(images):
    thirds = []
    temp = []
    
    for image in images:
        width, height = image.size[0], image.size[1]
        third = height // 3
        temp += [image.crop((0, 0, width, third))]
        temp += [image.crop((0, third, width, third * 2))]
        temp += [image.crop((0, third * 2, width, height))]
        thirds += [temp]
        temp = []

    return thirds

def count_digits(thirds):
    # Count the white pixels in each third
    temp = []
    pixel_counts = []
    
    for digits in thirds:
        for third in digits:
            count = 0
            pixel_data = list(third.getdata())
            for pixel in pixel_data:
                if pixel == white: count += 1
            temp += [count]
        pixel_counts += [temp]
        temp = []

    return pixel_counts

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
    
    thirds = get_thirds(digits)
    pixel_counts = count_digits(thirds)

    #print(pixel_counts)
    #thirds[0][0].save("digits\\0_third_1.png")
        
    return pixel_counts

def reset_counts(pixel_differences):
    for i in range(10):
        pixel_differences[str(i)] = 0

def recognise_digits(digits, pixel_counts):
    # If in doubt, the priority for recognition goes to the
    # total pixel count
    
    thirds = get_thirds(digits)
    pixel_counts = count_digits(thirds)
    base_pixel_counts = get_base_data()
    pixel_differences = {}
    differences = 0
    min_difference = 1000
    closest_match = 0
    matches = []
    all_matches = []
    total_differences = 0
    total_counts = []
    base_total_counts = []
    min_difference_total = 1000
    total_matches = []
    sr = ""
    
    reset_counts(pixel_differences)
        
    for i, digit in enumerate(pixel_counts):
        for j in range(3):
            for k in range(10):
                difference = abs(digit[j] - base_pixel_counts[k][j])
                #print(digit[j], base_pixel_counts[k][j], difference)
                if difference < min_difference:
                    closest_match = k
                    #print(closest_match)
                    min_difference = difference
                    
            matches += [closest_match]
            min_difference = 1000
        all_matches += [matches]
        matches = []

    for third_counts in base_pixel_counts:
        base_total_counts += [sum(third_counts)]

    for third_counts in pixel_counts:
        total_counts += [sum(third_counts)]

    for i, total in enumerate(total_counts):
        for j in range(10):
            total_difference = abs(total - base_total_counts[j])
            if total_difference < min_difference:
                closest_total_match = j
                min_difference = total_difference
        total_matches += [closest_total_match]
        closest_match_total = []
        min_difference = 1000
    #print(total_matches)

    for i, match in enumerate(all_matches):
        likely_digit = total_matches[i]
        # Priority goes to repeats, then to the uppermost third's match
        # Check for repeats:
        if match[1] == match[2]: likely_digit = match[1]
        sr += str(likely_digit)

    print(sr)
    #print(all_matches)     
        
def main():   
    file_name = "tests\\nums "
    for i in range(1, 8):
        file_name = "tests\\nums " + str(i)
        sr_block = get_sr_block(get_frame("nums " + str(i)))
        #sr_block.save("sr_block_cropped.png")
        #sr_block.save(file_name + ".png")
        simplify_image(sr_block)
        sr_block.save(file_name + ".png")
        #get_data()
        #print(type(frame))
        sr_block = Image.open(file_name + ".png")
        digits = get_digits(sr_block)
        pixel_counts = get_base_data()
        print(file_name[6:] + ": ", end = "")
        recognise_digits(digits, pixel_counts)
    
    pass

if __name__ == "__main__":
    main()

"""
ISSUES:
- Confused between 6, 8, 9, 0
- Digit divisions are not clean (they have remainders of surrounding
  digits), so cleaning these divisions may help with image recognition
"""
