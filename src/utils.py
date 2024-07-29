import cv2
import pickle
import numpy as np

class Park_classifier():    
    def __init__(self, car_park_positions_path:pickle, rect_width:int=None, rect_height:int=None):
        """
        Initialize the classifier with parking positions and rectangle dimensions.
        """
        self.car_park_positions = self._read_positions(car_park_positions_path)
        self.rect_width = 107 if rect_width is None else rect_width
        self.rect_height = 48 if rect_height is None else rect_height
    
    def _read_positions(self, car_park_positions_path:pickle)->list:
        """It reads the pickle file and return list of the tuples which stores the top left point coordinates of rectangle of car park. 
        Example Demostration :  [(x_1, y_1), ..., [x_n, y_n]]
        """
        car_park_positions = None
        try:
            car_park_positions = pickle.load(open(car_park_positions_path, 'rb'))
        except Exception as e:
            print(f"Error: {e}\n Raised while reading the car park positions file.")
        return car_park_positions

    def classify(self, image:np.ndarray, processed_image:np.ndarray, threshold:int=900)->np.ndarray:
        """
        Classify parking spaces in the image as empty or occupied.
        """
        empty_car_park = 0
        for x, y in self.car_park_positions:
            col_start, col_stop = x, x + self.rect_width
            row_start, row_stop = y, y + self.rect_height

            crop = processed_image[row_start:row_stop, col_start:col_stop]
            count = cv2.countNonZero(crop)
            
            if count < threshold:
                empty_car_park += 1
                color, thick = (0, 255, 0), 5
            else:
                color, thick = (0, 0, 255), 2
            
            cv2.rectangle(image, (x, y), (x + self.rect_width, y + self.rect_height), color, thick)

        cv2.rectangle(image, (45, 30), (250, 75), (180, 0, 180), -1)
        ratio_text = f'Free: {empty_car_park}/{len(self.car_park_positions)}'
        cv2.putText(image, ratio_text, (50, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
        
        return image, empty_car_park
        
    def implement_process(self, image:np.ndarray)->np.ndarray:
        """ Process the image using OpenCV digital image processing methods."""
        kernel_size = np.ones((3, 3), np.uint8)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3, 3), 1)
        Thresholded = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
        blur = cv2.medianBlur(Thresholded, 5)
        dilate = cv2.dilate(blur, kernel_size, iterations=1)
        
        return dilate

class Coordinate_denoter():
    """ Class for managing and denoting parking space coordinates."""
    def __init__(self, rect_width:int=107, rect_height:int=48, car_park_positions_path:pickle="data/source/CarParkPos"):
        self.rect_width = rect_width
        self.rect_height = rect_height
        self.car_park_positions_path = car_park_positions_path
        self.car_park_positions = list()

    def read_positions(self)->list:
        """ Read parking positions from the pickle file."""
        try:
            self.car_park_positions = pickle.load(open(self.car_park_positions_path, 'rb'))
        except Exception as e:
            print(f"Error: {e}\n Raised while reading the car park positions file.")

        return self.car_park_positions

    def mouseClick(self, events:int, x:int, y:int, flags:int, params:int):
        """ Handle mouse click events to add or remove parking space coordinates."""
        if events == cv2.EVENT_LBUTTONDOWN:
            self.car_park_positions.append((x, y))
        
        if events == cv2.EVENT_MBUTTONDOWN:
            for index, pos in enumerate(self.car_park_positions):
                x1, y1 = pos
                if x1 <= x <= x1 + self.rect_width and y1 <= y <= y1 + self.rect_height:
                    self.car_park_positions.pop(index)

        with open(self.car_park_positions_path, 'wb') as f:
            pickle.dump(self.car_park_positions, f)
