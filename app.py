import cv2
import numpy as np
import pickle
import sys
import os
from src.utils import Park_classifier

def initialize_classifier(carp_park_positions_path, rect_width, rect_height):
    """Initialize the parking classifier."""
    if not os.path.exists(carp_park_positions_path):
        raise FileNotFoundError(f"Parking positions file '{carp_park_positions_path}' not found.")
    
    classifier = Park_classifier(carp_park_positions_path, rect_width, rect_height)
    return classifier

def process_video_frame(classifier, frame):
    """Process a single frame of the video."""
    processed_frame = classifier.implement_process(frame)
    denoted_image = classifier.classify(frame, processed_frame)
    return denoted_image

def display_and_save_image(denoted_image, save_path):
    """Display the image and save if 's' is pressed."""
    cv2.imshow("Car Park Status", denoted_image)
    k = cv2.waitKey(1)
    if k & 0xFF == ord('q'):
        return False
    if k & 0xFF == ord('s'):
        cv2.imwrite(save_path, denoted_image)
        print(f"Image saved to {save_path}")
    return True

def demonstration(video_path, carp_park_positions_path, rect_width=107, rect_height=48, save_path="output.jpg"):
    """Demonstration of the car park classifier application."""
    try:
        classifier = initialize_classifier(carp_park_positions_path, rect_width, rect_height)
    except FileNotFoundError as e:
        print(e)
        return

    if not os.path.exists(video_path):
        print(f"Error: Video file '{video_path}' not found.")
        return

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Unable to open video file '{video_path}'.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Reached the end of the video.")
            break
        
        denoted_image = process_video_frame(classifier, frame)
        
        if not display_and_save_image(denoted_image, save_path):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py <video_path> <carp_park_positions_path> [rect_width] [rect_height] [save_path]")
    else:
        video_path = sys.argv[1]
        carp_park_positions_path = sys.argv[2]
        rect_width = int(sys.argv[3]) if len(sys.argv) > 3 else 107
        rect_height = int(sys.argv[4]) if len(sys.argv) > 4 else 48
        save_path = sys.argv[5] if len(sys.argv) > 5 else "output.jpg"
        demonstration(video_path, carp_park_positions_path, rect_width, rect_height, save_path)

