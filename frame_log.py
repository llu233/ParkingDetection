import cv2
import numpy as np
import time  # Import time module for measuring time
import logging

# Set up logging
logging.basicConfig(filename='metrics.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def demonstration(video_path, carp_park_positions_path, rect_width=107, rect_height=48):
    """Demonstration of the parking detection application."""

    # Check if video and positions file exist
    if not os.path.exists(video_path):
        print(f"Error: Video file '{video_path}' not found.")
        return
    if not os.path.exists(carp_park_positions_path):
        print(f"Error: Parking positions file '{carp_park_positions_path}' not found.")
        return

    # Creating the classifier instance which uses basic image processes to classify
    classifier = Park_classifier(carp_park_positions_path, rect_width, rect_height)

    # Implementation of the classifier
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Unable to open video file '{video_path}'.")
        return

    frame_count = 0
    total_time = 0.0

    while True:
        # Reading the video frame by frame
        ret, frame = cap.read()
        if not ret:
            print("Reached the end of the video.")
            break
        
        # Measure start time for processing
        start_time = time.time()
        
        # Processing the frames to prepare for classification
        processed_frame = classifier.implement_process(frame)
        
        # Measure processing time
        processing_time = time.time() - start_time
        total_time += processing_time
        frame_count += 1

        # Log metrics for each frame
        logging.info(f"Frame {frame_count}: Processing Time = {processing_time:.4f} seconds")

        # Drawing car parks according to their status 
        denoted_image = classifier.classify(frame, processed_frame)
        
        # Displaying the results
        cv2.imshow("Car Park Image Classified as Empty or Occupied", denoted_image)
        
        # Exit condition
        k = cv2.waitKey(1)
        if k & 0xFF == ord('q'):
            break
        if k & 0xFF == ord('s'):
            cv2.imwrite("output.jpg", denoted_image)

    # Calculate and log average processing time
    average_time = total_time / frame_count if frame_count > 0 else 0.0
    logging.info(f"Average Processing Time per Frame: {average_time:.4f} seconds")

    # Log total processing time
    logging.info(f"Total Processing Time: {total_time:.4f} seconds")

    # Release resources
    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    import sys
    import os
    from src.utils import Park_classifier

    if len(sys.argv) < 3:
        print("Usage: python script.py <video_path> <carp_park_positions_path>")
    else:
        video_path = sys.argv[1]
        carp_park_positions_path = sys.argv[2]
        demonstration(video_path, carp_park_positions_path)
