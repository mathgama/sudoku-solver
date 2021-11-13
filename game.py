import pygame
import requests

background_color = (255, 255, 255)
padding = 25
cell_size = 50
width = (2 * padding) + (cell_size * 9)

initial_board = requests.get('https://sugoku.herokuapp.com/board?difficulty=easy').json()['board']

def draw_empty_grid(window):
  for i in range(0,10):
    if(i%3 == 0):
      line_thickness = 4
    else:
      line_thickness = 2

    # Vertical lines
    pygame.draw.line(window, 
                     (0,0,0), 
                     (padding + cell_size * i, padding),
                     (padding + cell_size * i, width - padding), 
                     line_thickness)

    # Horizontal lines
    pygame.draw.line(window, 
                     (0,0,0), 
                     (padding, padding + cell_size * i), 
                     (width - padding, padding + cell_size * i), 
                     line_thickness)

def main():
  pygame.init()
  pygame.display.set_caption('Sudoku Game')

  window = pygame.display.set_mode((width, width))
  window.fill(background_color)

  draw_empty_grid(window)

  pygame.display.update()

  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        return

main()