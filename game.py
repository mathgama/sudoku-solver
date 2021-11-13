import pygame
from pygame.draw import line

width = 500
background_color = (255, 255, 255)

def main():
  pygame.init()
  pygame.display.set_caption('Sudoku Game')

  window = pygame.display.set_mode((width, width))
  window.fill(background_color)

  for i in range(0,10):
    if(i%3 == 0):
      line_thickness = 4
    else:
      line_thickness = 2

    pygame.draw.line(window, (0,0,0), (25+50*i, 25), (25+50*i, 475), line_thickness)
    pygame.draw.line(window, (0,0,0), (25, 25+50*i), (475, 25+50*i), line_thickness)

  pygame.display.update()

  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        return

main()