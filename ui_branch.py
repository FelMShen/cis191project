#uses the graphics library pygame
import pygame
vec = pygame.math.Vector2


#this contains code to modify specific letters stored in individual cells
class Cell():
    def __init__(self, x, y):
        #these are the coordinates in relation to the grid
        self.x = x
        self.y = y
        self.c = 'F'

    def update_letter(self, c):
        self.c = c

    def show(self, screen):
        pygame.draw.rect(screen, BLUE, ((self.x * CELL_WIDTH) + 1, (self.y * CELL_HEIGHT) + 1, CELL_WIDTH - 1, CELL_HEIGHT - 1), 0)
        text = font.render(self.c, True, GREEN)
        screen.blit(text, [ self.x * CELL_WIDTH + 10, self.y * CELL_HEIGHT + 6])

    def select(self, screen):
        pygame.draw.rect(screen, RED, ((self.x * CELL_WIDTH) + 1, (self.y * CELL_HEIGHT) + 1, CELL_WIDTH - 1, CELL_HEIGHT - 1), 0)
        text = font.render(self.c, True, GREEN)
        screen.blit(text, [ self.x * CELL_WIDTH + 10, self.y * CELL_HEIGHT + 6])

#this stores a grid of cells that spells out the entire text document
class Grid():
    def __init__(self):
        self.cells = [[Cell(x,y) for x in range(20)] for y in range(10)]

    def show(self, screen):
        for row in self.cells:
            for cell in row:
                cell.show(screen)

    def select(self, x, y, screen):
        self.cells[x][y].select(screen)

#class for buttons
class Button():
  def __init__(self, x, y, width, height, bg_color, text, font_size=25, text_color=(0,0,0)):
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.pos = vec(x, y)
    self.size = vec(width, height)
    self.surface = pygame.Surface((width, height))
    self.color = bg_color
    self.text = text
    self.font_size = font_size
    self.font = pygame.font.SysFont('sfprodisplayregularotf', self.font_size)
    self.text_color = text_color

  def draw(self, window):
      self.surface.fill(self.color)
      text = self.font.render(self.text, True, self.text_color)
      text_height = text.get_height()
      text_width = text.get_width()
      self.surface.blit(text, (((self.width - text_width)//2), (self.height - text_height)//2))
      window.blit(self.surface, self.pos)

  def check_click(self, pos):
      return pos[0] > self.x and pos[0] < self.x + self.width and pos[1] > self.y and pos[1] < self.y + self.height

#class for text input box
class TextBox():
  def __init__(self, x, y, width, height, bg_color=(124, 124, 124), active_color=(255,255,255), font_size=25):
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.bg_color = bg_color
    self.pos = vec(x, y)
    self.size = vec(width, height)
    self.surface = pygame.Surface((width, height))
    self.active_color = active_color
    self.active = False
    self.text = ""
    self.font_size = font_size
    self.font = pygame.font.SysFont('sfprodisplayregularotf', self.font_size)

  def draw(self, window):
    if not self.active:
      self.surface.fill(self.bg_color)
      text = self.font.render(self.text, False, (255, 255, 255))
      text_height = text.get_height()
      text_width = text.get_width()
      self.surface.blit(text, (0, (self.height - text_height)//2))
    else:
      self.surface.fill(self.active_color)
      text = self.font.render(self.text, False, (0, 0, 0))
      text_height = text.get_height()
      text_width = text.get_width()
      self.surface.blit(text, (0, (self.height - text_height)//2))

    window.blit(self.surface, self.pos)

  def check_click(self, pos):
    if pos[0] > self.x and pos[0] < self.x + self.width:
      if pos[1] > self.y and pos[1] < self.y + self.height:
        self.active = True
      else:
        self.active = False
    else:
      self.active = False
    return self.active
  
  def add_text(self, key):
    text = list(self.text)
    text.append(chr(key))
    self.text = ''.join(text)

# the main game engine is here. Will have to restructure a bit

#initialize the engine
pygame.init()
# Select the font to use, size, bold, italics
font = pygame.font.SysFont('Calibri', 18, False, False)
titleFont = pygame.font.SysFont('sfprodisplayregularotf', 40)
subtitleFont = pygame.font.SysFont('sfprodiplayregularotf', 20)

#set name of window
pygame.display.set_caption('Vim Game')

# Render the text. "True" means anti-aliased text.
# Black is the color. This creates an image of the
# letters, but does not put it on the screen
CELL_WIDTH = 40
CELL_HEIGHT = 50

# Define the colors we will use in RGB format
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]
RED = [255, 0, 0]

# Set the height and width of the screen
screen = pygame.display.set_mode((800, 400))

# Loop until the user clicks the close button.
done = False

clock = pygame.time.Clock()




#array for textbox click check
textboxes = []
textboxes.append(TextBox(0, 350, 800, 50))

#array for buttons (also level selector)
buttons = []
buttons.append(Button(240, 220, 80, 40, RED, "LEVEL 1", 20))
buttons.append(Button(360, 220, 80, 40, RED, "LEVEL 2", 20))
buttons.append(Button(480, 220, 80, 40, RED, "LEVEL 3", 20))

#checks if the mouse button is clicked, initializes as true
#todo: modify code to not require this
clicked = False
intro = True
intro_clicked = False

#selected letter

#game engine
while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN and intro:
            intro = False
            intro_clicked = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = not textboxes[0].check_click(pygame.mouse.get_pos())
        if event.type == pygame.KEYDOWN:
            if textboxes[0].active:
                textboxes[0].add_text(event.key)

    if intro:
        title = titleFont.render("Vim Game", True, (0, 200, 0))
        subtitle = subtitleFont.render("Click anywhere to begin", True, (26,134,230))
        subtitle2 = subtitleFont.render("Or, click on one of the level buttons", True, (26,134,230))
        titlePos = title.get_rect()
        sTitlePos = subtitle.get_rect()
        s2TitlePos = subtitle2.get_rect()

        intro_background = pygame.Surface(screen.get_size())
        intro_background = intro_background.convert()
        intro_background.fill((250, 250, 250))
        titlePos.centerx = intro_background.get_rect().centerx
        titlePos.centery = intro_background.get_rect().centery - 60
        sTitlePos.centerx = intro_background.get_rect().centerx
        sTitlePos.centery = titlePos.centery + 30
        s2TitlePos.centerx = titlePos.centerx
        s2TitlePos.centery = sTitlePos.centery + 15

        intro_background.blit(title, titlePos)
        intro_background.blit(subtitle, sTitlePos)
        intro_background.blit(subtitle2, s2TitlePos)

        for button in buttons:
          button.draw(intro_background)

        screen.blit(intro_background, (0,0))


    # more events can be added for functions
    #todo:
    # add vim command functionality
    if intro_clicked:
        pos = pygame.mouse.get_pos()
        x = pos[0]
        y = pos[1]
        intro_clicked = False
        # need to have level loader here

    #checks to see if we clicked on something
    
    if not intro:
        screen.fill(WHITE)
        pos = pygame.mouse.get_pos()
        x = pos[0]
        y = pos[1]

        g = Grid()
        g.show(screen)
        g.select(2,3, screen)

        if clicked:
            #helper to see where I click, remove later
            text = font.render("click!", True, GREEN)
            screen.blit(text, [x, y])
            #rather than detect a keypress up, we just allow a single action per event
            clicked = False
        
        for textbox in textboxes:
            textbox.draw(screen)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.update()
    # Limit frames per second
    clock.tick(60)

# Be IDLE friendly
pygame.quit()
