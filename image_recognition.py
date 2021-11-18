import cv2
import numpy

class ImageReader:
  def __init__(self, imgPath):
    self.imgWidth = 450
    self.imgHeight = 450
    self.original_image = cv2.imread(imgPath)

  def fetch_board_state(self):
    resized_image = self.resize_image(self.original_image)
    image_threshold = self.prepare_image(resized_image)
    contours = self.find_contours(image_threshold)
    biggest_contour = self.find_biggest_contour(contours)
    board = self.crop_board(resized_image, biggest_contour)

    return board

  def reorder_corner_points(self, corners):
    corners = corners.reshape((4, 2))
    sum = numpy.sum(corners, axis=1)
    diff = numpy.diff(corners, axis=1)

    ordered_corners = numpy.zeros((4, 1, 2), dtype=numpy.int32)
    ordered_corners[0] = corners[numpy.argmin(sum)] # top-left
    ordered_corners[3] = corners[numpy.argmax(sum)] # bottom-right
    ordered_corners[1] = corners[numpy.argmin(diff)] # top-right
    ordered_corners[2] = corners[numpy.argmax(diff)] # bottom-left
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
    biggest = numpy.array([])
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
      
      pts1 = numpy.float32(contour)
      pts2 = numpy.float32([[0, 0], 
                            [self.imgWidth, 0], 
                            [0, self.imgHeight],
                            [self.imgWidth, self.imgHeight]])
      
      matrix = cv2.getPerspectiveTransform(pts1, pts2)
      imgWarpColored = cv2.warpPerspective(image, matrix, (self.imgWidth, self.imgHeight))
      imgWarpGray = cv2.cvtColor(imgWarpColored,cv2.COLOR_BGR2GRAY)
      return imgWarpGray

reader = ImageReader('img/1.jpg')
board = reader.fetch_board_state()

cv2.imshow("Image Warp", board)
cv2.waitKey(0)