import sys
import getopt
import pygame
import datetime
from image_reader import ImageReader
from grid import Grid

background_color = (255, 255, 255)

def main():
  pygame.init()
  pygame.display.set_caption("Sudoku Game")

  initial_board = []

  try:
    opts, args = getopt.getopt(sys.argv[1:],"hi:",["image="])
  except getopt.GetoptError:
    print("game.py -i <image_path>")
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print("game.py -i <image_path>")
      sys.exit()
    elif opt in ("-i", "--image"):
      img_path = arg
      image_reader = ImageReader(img_path)
      initial_board = image_reader.fetch_board_state()

  window = pygame.display.set_mode((590, 590))
  grid = Grid(25, window, initial_board)

  window.fill(background_color)
  grid.draw()
  pygame.display.update()

  while True:
    update_view = False

    for event in pygame.event.get():
      if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
        grid.select_cell(pygame.mouse.get_pos())
        update_view = True
      if event.type == pygame.KEYDOWN:
        if event.key == 1073741882:
          start = datetime.datetime.now()
          grid.solve()
          end = datetime.datetime.now()
          print('Time to solve:', end - start)
          update_view = True
        elif (
            event.key == 1073741903 or # right arrow
            event.key == 1073741904 or # left arrow
            event.key == 1073741905 or # down arrow
            event.key == 1073741906    # up arrow
           ):
          grid.move_selection(event.key - 1073741903)
        else:
          if event.key == 8 or event.key == 127:
            value = 0
          else:
            value = event.key - 48

          grid.type(value)

        update_view = True
      if event.type == pygame.QUIT:
        pygame.quit()
        return

      if update_view:
        window.fill(background_color)
        grid.draw()
        pygame.display.update()

main()