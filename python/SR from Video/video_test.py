# Only working with python 3.5.2
import cv2
from PIL import Image
import os

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
    sr_block = career_profile.crop((1053, 82, 1094, 103))
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
            

def get_average_colour(image):
    pixel_data = list(image.getdata())
    total = 0
    for i in range(len(pixel_data)):
        total += sum(pixel_data[i])
    average_colour_sum = total // len(pixel_data)
    
    return average_colour_sum

def main():   
    file_name = "test"
    sr_block = get_sr_block(get_frame(file_name))    
    sr_block.save("test_sr_block.png")
    simplify_image(sr_block)
    sr_block.save("test_contrast.png")
    #print(type(frame))

if __name__ == "__main__":
    main()
