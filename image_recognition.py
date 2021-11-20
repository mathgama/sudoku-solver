import cv2
import numpy as np
import pytesseract

class ImageReader:
  def __init__(self, img_path):
    self.imgWidth = 450
    self.imgHeight = 450
    self.original_image = cv2.imread(img_path)

  def fetch_board_state(self):
    resized_image = self.resize_image(self.original_image)
    image_threshold = self.prepare_image(resized_image)
    contours = self.find_contours(image_threshold)
    biggest_contour = self.find_biggest_contour(contours)
    board = self.crop_board(resized_image, biggest_contour)
    cells = self.crop_cells(board)
    board_state = self.recognize_board_state(cells)
    return board_state

  def reorder_corner_points(self, corners):
    corners = corners.reshape((4, 2))
    sum = np.sum(corners, axis=1)
    diff = np.diff(corners, axis=1)

    ordered_corners = np.zeros((4, 1, 2), dtype=np.int32)
    ordered_corners[0] = corners[np.argmin(sum)] # top-left
    ordered_corners[3] = corners[np.argmax(sum)] # bottom-right
    ordered_corners[1] = corners[np.argmin(diff)] # top-right
    ordered_corners[2] = corners[np.argmax(diff)] # bottom-left
    return ordered_corners

  def resize_image(self, image):
    return cv2.resize(image, (self.imgWidth, self.imgHeight))

  def prepare_image(self, image):
    preparedImg = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert image to grayscale
    preparedImg = cv2.GaussianBlur(preparedImg, (5, 5), 1)
    return cv2.adaptiveThreshold(preparedImg, 255, 1, 1, 11, 2)

  def find_contours(self, image):
    contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

  def find_biggest_contour(self, contours):
    biggest = np.array([])
    max_area = 0

    for i in contours:
      area = cv2.contourArea(i)

      if area > 50:
        perimeter = cv2.arcLength(i, True)
        approx = cv2.approxPolyDP(i, 0.02 * perimeter, True)

        if area > max_area and len(approx) == 4:
          biggest = approx
          max_area = area
      
    return biggest

  def crop_board(self, image, contour):
    if contour.size != 0:
      contour = self.reorder_corner_points(contour)
      
      pts1 = np.float32(contour)
      pts2 = np.float32([[0, 0], 
                            [self.imgWidth, 0], 
                            [0, self.imgHeight],
                            [self.imgWidth, self.imgHeight]])
      
      matrix = cv2.getPerspectiveTransform(pts1, pts2)
      imgWarpColored = cv2.warpPerspective(image, matrix, (self.imgWidth, self.imgHeight))
      imgWarpGray = cv2.cvtColor(imgWarpColored,cv2.COLOR_BGR2GRAY)
      return imgWarpGray

  def crop_cells(self, image):
    rows = np.vsplit(image, 9)
    cells = []

    for row in rows:
        cells += np.hsplit(row, 9)

    return cells

  def recognize_board_state(self, cells):
    board_state = []

    for cell in cells:
      cell = np.asarray(cell)
      img = cell[4:cell.shape[0] - 4, 4:cell.shape[1] -4]
  
      rsz = cv2.resize(img, (0, 0), fx=2, fy=2)
      thr = cv2.threshold(rsz, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
      blr = cv2.GaussianBlur(thr, (3, 3), 0)
      value = pytesseract.image_to_string(blr, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')

      try:
        value = int(value[:1])
      except:
        value = 0

      board_state.append(value)
    
    board_state = np.array(board_state).reshape(9, 9)
    return board_state

""" reader = ImageReader('img/1.jpg')
board_state = reader.fetch_board_state()
print(board_state) """