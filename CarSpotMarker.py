import cv2 # OpenCV library for image processing
import pickle

class CoordinateDenoter:
    def __init__(self):
        self.car_park_positions = [] # List to store car park positions
        self.rect_width = 107 # Width of the rectangle to be drawn
        self.rect_height = 48 # Height of the rectangle to be drawn

    def mouseClick(self, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            # Add the clicked position to the list
            position = [x, y]
            self.car_park_positions.append(position)
            print(f"Position added: {position}")

    def save_positions(self, file_path):
        # Save the positions to a file using pickle
        with open(file_path, 'wb') as f:
            pickle.dump(self.car_park_positions, f)
            print(f"Positions saved to {file_path}")

    def delete_last_position(self):
        # Remove the last added position from the list
        if self.car_park_positions:
            removed_position = self.car_park_positions.pop()
            print(f"Position removed: {removed_position}")
        else:
            print("No positions to remove.")

def main(image_path="data/source/example_image.png", output_path="data/source/CarParkPos.pickle"):
    # Check if image file exists
    if not os.path.exists(image_path):
        print(f"Error: Image file '{image_path}' not found.")
        return
    
    coordinate_denoter = CoordinateDenoter()
    
    image = cv2.imread(image_path) # Read the image

    cv2.namedWindow("Image") # Create a named window
    cv2.setMouseCallback("Image", coordinate_denoter.mouseClick) # Set the mouse callback function

    while True:
        temp_image = image.copy() # Make a copy of the image for drawing

        # Draw rectangles for each stored position
        for pos in coordinate_denoter.car_park_positions:
            start = (pos[0], pos[1])
            end = (pos[0] + coordinate_denoter.rect_width, pos[1] + coordinate_denoter.rect_height)
            cv2.rectangle(temp_image, start, end, (0, 255, 0), 2) # Draw the rectangle

        cv2.imshow("Image", temp_image) # Display the image with rectangles

        # Press 'q' to quit, 's' to save, and 'd' to delete the last position
        key = cv2.waitKey(1)
        if key == ord("q"):
            break
        elif key == ord("s"):
            coordinate_denoter.save_positions(output_path)
        elif key == ord("d"):
            coordinate_denoter.delete_last_position()
    
    cv2.destroyAllWindows() # Destroy all the windows

if __name__ == "__main__":
    import sys
    import os
    # Get the image and output file paths from command-line arguments
    image_path = sys.argv[1] if len(sys.argv) > 1 else "data/source/example_image.png"
    output_path = sys.argv[2] if len(sys.argv) > 2 else "data/source/CarParkPos.pickle"
    main(image_path, output_path)
