#uses the graphics library pygame
import pygame
vec = pygame.math.Vector2



#this contains code to modify specific letters stored in individual cells
class Cell():
    def __init__(self, x, y):
        #these are the coordinates in relation to the grid
        self.x = x
        self.y = y
        self.c = '`'
        self.selected = False

    def update_letter(self, c):
        self.c = c

    def show(self, screen):
        if self.selected:
            pygame.draw.rect(screen, RED, ((self.x * CELL_WIDTH) + 1, (self.y * CELL_HEIGHT) + 1, CELL_WIDTH - 1, CELL_HEIGHT - 1), 0)
            text = font.render(self.c, True, GREEN)
            screen.blit(text, [ self.x * CELL_WIDTH + 10, self.y * CELL_HEIGHT + 6])
        else:
            pygame.draw.rect(screen, BLUE, ((self.x * CELL_WIDTH) + 1, (self.y * CELL_HEIGHT) + 1, CELL_WIDTH - 1, CELL_HEIGHT - 1), 0)
            text = font.render(self.c, True, GREEN)
            screen.blit(text, [ self.x * CELL_WIDTH + 10, self.y * CELL_HEIGHT + 6])


    def select(self, screen):
        self.selected = True

    def unselect(self, screen):
        self.selected = False

#this stores a grid of cells that spells out the entire text document
class Grid():
    def __init__(self):
        self.cells = [[Cell(x,y) for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]
        self.x = 0
        self.y = 0
        self.cells[0][0].selected = True
        self.solution = ""
        self.level = ""

    #draws the grid
    def show(self, screen):
        for row in self.cells:
            for cell in row:
                cell.show(screen)

    #draws the cursor
    def select(self, x, y, screen):
        self.cells[self.x][self.y].unselect(screen)
        self.x = x
        self.y = y
        self.cells[x][y].select(screen)

    #gets the cursor coords
    def get_selected_coords(self):
        return (self.x,self.y)


    #note that the grid coordinates are 90 degrees off
    #takes two strings to be the level and the solution
    def import_level(self, level, solution):
        #resets board
        self.cells = [[Cell(x,y) for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]
        self.level = level
        self.solution = solution
        #loads the string into the grid
        y = 0
        x = 0
        for c in level:
            if (c == '\n'):
                y = 0
                x += 1
                continue
            self.cells[x][y].update_letter(c)
            if (y == 19):
                y = 0
                x += 1
            y +=1

    #checks the solution loaded into the grid
    def check_solution(self):
        check = ""
        for i in range(GRID_HEIGHT):
            hasChars = False
            for j in range(GRID_WIDTH):
                ch = self.cells[i][j].c
                if (ch == '`'):
                    ch = ""
                else:
                    hasChars = True
                check = check + ch
            #adds the line break
            if (hasChars):
                check = check + '\n'
        return check == self.solution

    #x and y are switched
    def x_command(self):
        i = self.x
        j = self.y
        while (j < GRID_WIDTH - 1):
            self.cells[i][j].c = self.cells[i][j+1].c
            j += 1
        self.cells[i][j].c = '`'

    # dd to delete row
    def dd_command(self, screen):
        i = self.x
        j = self.y
        while (i < GRID_HEIGHT - 1):
            for j in range(GRID_WIDTH):
                self.cells[i][j].c = self.cells[i+1][j].c
            i += 1
        #i = grid_height so we set all of these to the placeholder char
        for j in range(GRID_WIDTH):
            self.cells[i][j].c = '`'

    # dw to delete word
    #deletes all of the word from the cursor onward
    def dw_command(self, screen):
        i = self.x
        j = self.y
        index = j
        while (self.cells[i][index].c != ' ' and self.cells[i][index].c != '`'):
            for j_i in range(j, GRID_WIDTH - 1):
                self.cells[i][j_i].c = self.cells[i][j_i+1].c

        if (self.cells[i][j].c == ' '):
            for j_i in range(j, GRID_WIDTH - 1):
                self.cells[i][j_i].c = self.cells[i][j_i+1].c
        #i = grid_height so we set all of these to the placeholder char

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

  def push(self, character):
      self.text += character

  def add_text(self, key):
    text = list(self.text)
    if key == pygame.K_BACKSPACE:
        if len(text) != 0:
            text.pop()
    elif event.key == pygame.K_SEMICOLON and pygame.key.get_mods() & pygame.KMOD_SHIFT:
        text.append(':')
    elif key == pygame.K_RETURN:
        curr_command = ''.join(text)
        if curr_command == ':q':
            text.clear()
            self.text = ''
            self.active = False
            return True
        text.clear()
    elif key in [pygame.K_a, pygame.K_b, pygame.K_c, pygame.K_d, pygame.K_e,pygame.K_f, pygame.K_g, pygame.K_h,pygame.K_i,pygame.K_j,pygame.K_k,pygame.K_l,pygame.K_m,pygame.K_n,pygame.K_o,pygame.K_p,pygame.K_q,pygame.K_r,pygame.K_s,pygame.K_t,pygame.K_u,pygame.K_v,pygame.K_w,pygame.K_x,pygame.K_y,pygame.K_z]:
        text.append(chr(key))

    self.text = ''.join(text)
    return False


# the main game engine is here. Will have to restructure a bit

#initialize the engine
pygame.init()
# Select the font to use, size, bold, italics
font = pygame.font.SysFont('Calibri', 22, False, False)
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
BLUE = [0, 0, 50]
RED = [255, 0, 0]

# Set the height and width of the screen
screen = pygame.display.set_mode((800, 550))

#set the grid as 20x10
GRID_HEIGHT = 10
GRID_WIDTH = 20

# Loop until the user clicks the close button.
done = False

clock = pygame.time.Clock()


#array for textbox click check
textboxes = []
textboxes.append(TextBox(0, 500, 800, 50))

#array for buttons (also level selector)
buttons = []
buttons.append(Button(240, 320, 80, 40, RED, "LEVEL 1", 20))
buttons.append(Button(360, 320, 80, 40, RED, "LEVEL 2", 20))
buttons.append(Button(480, 320, 80, 40, RED, "LEVEL 3", 20))


#checks if the mouse button is clicked, initializes as true
#todo: modify code to not require this
ls_clicked = False
fs_clicked = False
intro = True
intro_clicked = False
reset = False
loading_screen = False
final_screen = False


#inits the grid
g = Grid()
level1 = open('level1.txt',"r").read()
level2 = open('level2.txt',"r").read()
level3 = open('level3.txt',"r").read()
solution1 = open('level1_solution.txt',"r").read()
solution2 = open('level2_solution.txt',"r").read()
solution3 = open('level3_solution.txt',"r").read()
g.import_level(level1, solution1)
curr_level = 1

#command state for multi-letter commands
#as of now, only dd is implemented
state = ""

#game engine
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN and intro:
            intro = False
            intro_clicked = True
        if event.type == pygame.MOUSEBUTTONDOWN and final_screen:
            final_screen = False
            intro = True
        if event.type == pygame.MOUSEBUTTONDOWN and loading_screen:
            loading_screen = False
            if curr_level == 1:
                    g.import_level(level1, solution1)
            elif curr_level == 2:
                    g.import_level(level2, solution2)
            elif curr_level == 3:
                    g.import_level(level3, solution3)

        #intro and menu
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

        if loading_screen:
            title = titleFont.render("Completed Level " + str(curr_level - 1) + "!", True, (0, 200, 0))
            subtitle = subtitleFont.render("Click anywhere to begin next level!", True, (26,134,230))
            titlePos = title.get_rect()
            sTitlePos = subtitle.get_rect()

            loading_background = pygame.Surface(screen.get_size())
            loading_background = loading_background.convert()
            loading_background.fill((250, 250, 250))
            titlePos.centerx = loading_background.get_rect().centerx
            titlePos.centery = loading_background.get_rect().centery - 60
            sTitlePos.centerx = loading_background.get_rect().centerx
            sTitlePos.centery = titlePos.centery + 30

            loading_background.blit(title, titlePos)
            loading_background.blit(subtitle, sTitlePos)

            screen.blit(loading_background, (0,0))

        if final_screen:
            title = titleFont.render("You completed the Vim Game!!", True, (0, 200, 0))
            subtitle = subtitleFont.render("Click anywhere to return home!", True, (26,134,230))
            subtitle2 = subtitleFont.render("Hope you enjoyed!", True, (26,134,230))
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

            screen.blit(intro_background, (0,0))

        # more events can be added for functions
        #todo:
        # add vim command functionality
        if intro_clicked:
            pos = pygame.mouse.get_pos()
            if buttons[0].check_click(pos):
                g.import_level(level1, solution1)
                curr_level = 1
            elif buttons[1].check_click(pos):
                g.import_level(level2, solution2)
                curr_level = 2
            elif buttons[2].check_click(pos):
                g.import_level(level3, solution3)
                curr_level = 3
            else:
                g.import_level(level1, solution1)
                curr_level = 1
            intro_clicked = False
            # need to have level loader here

        if not intro and not loading_screen and not final_screen:
            screen.fill(WHITE)
            g.show(screen)
            if event.type == pygame.KEYDOWN:
            #allows hjkl navigation of selected tile (with bumpers)
            #the coordinate system is off
                if textboxes[0].active:
                    reset = textboxes[0].add_text(event.key)
                    if reset:
                        intro = True
                        intro_clicked = False
                        reset = False
                        curr_level = 1

                elif event.key == pygame.K_SEMICOLON and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    textboxes[0].active = True
                    textboxes[0].push(":")
                elif event.key == pygame.K_k:
                    coords = g.get_selected_coords()
                    y = coords[0] - 1
                    if (y < 0):
                        y = 0
                    g.select(y, coords[1], screen)

                elif event.key == pygame.K_h:
                    coords = g.get_selected_coords()
                    x =  coords[1] - 1
                    if (x < 0):
                        x = 0
                    g.select(coords[0],x, screen)

                elif event.key == pygame.K_l:
                    coords = g.get_selected_coords()
                    x = coords[1] + 1
                    if (x > GRID_WIDTH - 1):
                        x = GRID_WIDTH - 1
                    g.select(coords[0], x, screen)

                elif event.key == pygame.K_j:
                    coords = g.get_selected_coords()
                    y = coords[0] + 1
                    if (y > GRID_HEIGHT - 1):
                        y = GRID_HEIGHT - 1
                    g.select(y, coords[1], screen)


                #x command to delete cursored charcter
                elif event.key == pygame.K_x:
                    g.x_command()

                #for the second d once state has been created as 'd'
                elif state == 'd':
                    #if dd was pressed
                    if event.key == pygame.K_d:
                        g.dd_command(screen)

                    #if dw was pressed
                    if event.key == pygame.K_w:
                        g.dw_command(screen)

                    #something else was pressed or command finishes sucessfully
                    state = ''


                #dd command to delete row , updates
                elif event.key == pygame.K_d:
                    state = 'd'



                #just a random character to check a solution
                elif event.key == pygame.K_z:
                    if (g.check_solution()):
                        if (curr_level == 3):
                            final_screen = True
                        else:
                            loading_screen = True
                            curr_level += 1
                    else:
                        if curr_level == 1:
                            g.import_level(level1, solution1)
                        elif curr_level == 2:
                            g.import_level(level2, solution2)
                        elif curr_level == 3:
                            g.import_level(level3, solution3)


                #show the updated screen
                g.show(screen)

        # more events can be added for functions
        #todo: add vim command functionality


        #draws textboxes
        for textbox in textboxes:
            textbox.draw(screen)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.update()
    # Limit frames per second
    clock.tick(60)

# Be IDLE friendly
pygame.quit()
