import pygame
import requests

background_color = (255, 255, 255)
original_element_color = (90, 100, 249)

padding = 25
cell_size = 50
width = (2 * padding) + (cell_size * 9)

initial_board_state = requests.get('https://sugoku.herokuapp.com/board?difficulty=easy').json()['board']

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

def draw_initial_board_state(window):
  font = pygame.font.Font(pygame.font.get_default_font(), 40)

  for i in range(0,9):
    for j in range(0,9):
      value = initial_board_state[i][j]

      if(value != 0):
        value_render = font.render(str(value), True, original_element_color)
        window.blit(value_render, 
                    (padding + 15 + (cell_size * j), #40 
                    padding + 10 + (cell_size * i))) #35

def main():
  pygame.init()
  pygame.display.set_caption('Sudoku Game')

  window = pygame.display.set_mode((width, width))
  window.fill(background_color)

  draw_empty_grid(window)
  draw_initial_board_state(window)

  pygame.display.update()

  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        return

main()