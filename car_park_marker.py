import cv2
import pickle

class CoordinateDenoter:
    def __init__(self):
        self.car_park_positions = []
        self.rect_width = 107
        self.rect_height = 48

    def mouseClick(self, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            # Add the clicked position
            position = [x, y]
            self.car_park_positions.append(position)
            print(f"Position added: {position}")

    def save_positions(self, file_path):
        with open(file_path, 'wb') as f:
            pickle.dump(self.car_park_positions, f)
            print(f"Positions saved to {file_path}")

    def delete_last_position(self):
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
    
    image = cv2.imread(image_path)

    cv2.namedWindow("Image")
    cv2.setMouseCallback("Image", coordinate_denoter.mouseClick)

    while True:
        temp_image = image.copy()

        # Draw rectangles
        for pos in coordinate_denoter.car_park_positions:
            start = (pos[0], pos[1])
            end = (pos[0] + coordinate_denoter.rect_width, pos[1] + coordinate_denoter.rect_height)
            cv2.rectangle(temp_image, start, end, (0, 255, 0), 2)

        cv2.imshow("Image", temp_image)

        # Press 'q' to quit, 's' to save, and 'd' to delete the last position
        key = cv2.waitKey(1)
        if key == ord("q"):
            break
        elif key == ord("s"):
            coordinate_denoter.save_positions(output_path)
        elif key == ord("d"):
            coordinate_denoter.delete_last_position()
    
    cv2.destroyAllWindows()

if __name__ == "__main__":
    import sys
    import os
    image_path = sys.argv[1] if len(sys.argv) > 1 else "data/source/example_image.png"
    output_path = sys.argv[2] if len(sys.argv) > 2 else "data/source/CarParkPos.pickle"
    main(image_path, output_path)
