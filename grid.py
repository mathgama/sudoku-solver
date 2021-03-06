import pygame
import requests

original_element_color = (90, 100, 249)
user_input_color = (0, 0, 0)
error_input_color = (255, 0, 0)

class Grid:
  def __init__(self, padding, window, initial_board=[]):
    self.window = window
    self.width = window.get_size()[0]
    self.padding = padding
    self.cell_size = (self.width - (2 * self.padding)) / 9
    self.selected_cell = None

    if len(initial_board) > 0:
      self.initial_board = initial_board
    else:
      self.initial_board = requests.get('https://sugoku.herokuapp.com/board?difficulty=easy').json()['board']

    self.board_state = [[self.initial_board[i][j] for j in range(9)] for i in range(9)]

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

  def find_next_empty_cell(self):
    for i in range(9):
      for j in range(9):
        if self.board_state[i][j] == 0:
          return i, j

    return None, None

  def solve(self):
    row, col = self.find_next_empty_cell()

    if (row, col) == (None, None):
      return True

    for number in range(1, 10):
      if self.is_input_valid(number, row, col):        
        self.board_state[row][col] = number

        """ self.window.fill(background_color)
        self.draw()
        pygame.display.update() """

        if self.solve():
          return True

    self.board_state[row][col] = 0
    return False

  def is_input_valid(self, value, row, col):
    # check for the same row
    for j in range(9):
      if j != col and self.board_state[row][j] == value:
        return False

    # check for the same column
    for i in range(9):
      if i != row and self.board_state[i][col] == value:
        return False

    # check for the same block
    block_x_start = (row // 3) * 3
    block_y_start = (col // 3) * 3

    for i in range(block_x_start, block_x_start + 3):
      for j in range(block_y_start, block_y_start + 3):
        if (i, j) != (row, col) and self.board_state[i][j] == value:
          return False

    return True

  def render_number(self, value, row, col, user_input):
    font_size = int(self.cell_size * 40 // 60)
    font = pygame.font.Font(pygame.font.get_default_font(), font_size)

    if not user_input:
      color = original_element_color
    elif self.is_input_valid(value, row, col):
      color = user_input_color
    else:
      color = error_input_color

    #color = user_input_color if user_input == True else original_element_color

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
    self.highlight_selected_cell()
    self.draw_board_state()

  def select_cell(self, mouse_position):
    row = int((mouse_position[1] - self.padding) // self.cell_size)
    col = int((mouse_position[0] - self.padding) // self.cell_size)

    if (row, col) == self.selected_cell:
      self.selected_cell = None
      return
    
    self.selected_cell = (row, col)

  def type(self, value):
    # invalid values
    if value < 0 or value > 9:
      return

    # selected cell was on the initial state (fetched from the API)
    if self.initial_board[self.selected_cell[0]][self.selected_cell[1]] != 0:
      return

    self.board_state[self.selected_cell[0]][self.selected_cell[1]] = value

  def move_selection(self, direction):
    if self.selected_cell == None:
      self.selected_cell = (0, 0)
      return

    if direction == 0: # right
      self.selected_cell = (self.selected_cell[0], self.selected_cell[1] + 1)
    elif direction == 1: # left
      self.selected_cell = (self.selected_cell[0], self.selected_cell[1] - 1)
    elif direction == 2: # down
      self.selected_cell = (self.selected_cell[0] + 1, self.selected_cell[1])
    elif direction == 3: # up
      self.selected_cell = (self.selected_cell[0] - 1, self.selected_cell[1])

    if self.selected_cell[0] < 0:
      self.selected_cell = (0, self.selected_cell[1])
    elif self.selected_cell[0] > 8:
      self.selected_cell = (8, self.selected_cell[1])

    if self.selected_cell[1] < 0:
      self.selected_cell = (self.selected_cell[0], 0)
    elif self.selected_cell[1] > 8:
      self.selected_cell = (self.selected_cell[0], 8)