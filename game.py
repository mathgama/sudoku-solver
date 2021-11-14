import pygame
import requests

background_color = (255, 255, 255)
original_element_color = (90, 100, 249)
user_input_color = (0, 0, 0)

class Grid:
  def __init__(self, padding, window):
    self.window = window
    self.width = window.get_size()[0]
    self.padding = padding
    self.cell_size = (self.width - (2 * self.padding)) / 9
    self.initial_board = requests.get('https://sugoku.herokuapp.com/board?difficulty=easy').json()['board']
    self.board_state = [[self.initial_board[i][j] for j in range(9)] for i in range(9)]
    self.selected_cell = None
    #self.cubes = [[Cube(self.board[i][j], i, j) for j in range(9)] for i in range(9)]

  def draw_empty_grid(self):
    for i in range(10):
      if i % 3 == 0:
        line_thickness = 4
      else:
        line_thickness = 2

      # Vertical lines
      pygame.draw.line(self.window, 
                      (0,0,0), 
                      (self.padding + self.cell_size * i, self.padding),
                      (self.padding + self.cell_size * i, self.width - self.padding), 
                      line_thickness)

      # Horizontal lines
      pygame.draw.line(self.window, 
                      (0,0,0), 
                      (self.padding, self.padding + self.cell_size * i), 
                      (self.width - self.padding, self.padding + self.cell_size * i), 
                      line_thickness)

  def render_number(self, value, row, col, user_input):
    font_size = int(self.cell_size * 40 // 60)
    font = pygame.font.Font(pygame.font.get_default_font(), font_size)

    color = user_input_color if user_input == True else original_element_color

    value_render = font.render(str(value), True, color)

    cell_padding_left = self.cell_size * 21 / 60
    cell_padding_top = self.cell_size * 13 / 60

    self.window.blit(value_render,
                     (self.padding + cell_padding_left + (self.cell_size * col),
                     self.padding + cell_padding_top + (self.cell_size * row)))

  def draw_board_state(self):
    for i in range(9):
      for j in range(9):
        value = self.board_state[i][j]

        user_input = True if self.initial_board[i][j] == 0 else False

        if value != 0:
          self.render_number(value, i, j, user_input)

  def highlight_selected_cell(self):
    if self.selected_cell == None:
      return

    left = self.padding + (self.selected_cell[1] * self.cell_size) + 1
    top = self.padding + (self.selected_cell[0] * self.cell_size) + 1

    pygame.draw.rect(self.window,
                     (255, 0, 0),
                     (left, top, self.cell_size, self.cell_size),
                     3)

  def draw(self):
    self.draw_empty_grid()
    self.draw_board_state()
    self.highlight_selected_cell()

  def select_cell(self, mouse_position):
    row = int((mouse_position[1] - self.padding) // self.cell_size)
    col = int((mouse_position[0] - self.padding) // self.cell_size)

    if (row, col) == self.selected_cell:
      self.selected_cell = None
    elif self.initial_board[row][col] == 0:
      self.selected_cell = (row, col)


""" class Cube:
  def __init__(self, value, row, col):
    self.value = value
    self.row = row
    self.col = col """


def main():
  pygame.init()
  pygame.display.set_caption('Sudoku Game')

  window = pygame.display.set_mode((590, 590))
  grid = Grid(25, window)

  window.fill(background_color)
  grid.draw()
  pygame.display.update()

  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        return
      if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
        grid.select_cell(pygame.mouse.get_pos())

      window.fill(background_color)
      grid.draw()
      pygame.display.update()

main()