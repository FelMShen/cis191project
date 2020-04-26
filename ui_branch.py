#uses the graphics library pygame
import pygame


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

#checks if the mouse button is clicked, initializes as true
#todo: modify code to not require this
clicked = False
intro = True

title = titleFont.render("Vim Game", True, (0, 200, 0))
subtitle = subtitleFont.render("Click anywhere to begin", True, (26,134,230))
titlePos = title.get_rect()
sTitlePos = subtitle.get_rect()

intro_background = pygame.Surface(screen.get_size())
intro_background = intro_background.convert()
intro_background.fill((250, 250, 250))
titlePos.centerx = intro_background.get_rect().centerx
titlePos.centery = intro_background.get_rect().centery - 20
sTitlePos.centerx = intro_background.get_rect().centerx
sTitlePos.centery = titlePos.centery + 30

intro_background.blit(title, titlePos)
intro_background.blit(subtitle, sTitlePos)

#selected letter

#game engine
while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN and intro:
            intro = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True

        # more events can be added for functions
        #todo:
        # add vim command functionality

    if intro:
        screen.blit(intro_background, (0,0))

    #checks to see if we clicked on something
    if clicked:
        screen.fill(WHITE)
        pos = pygame.mouse.get_pos()
        x = pos[0]
        y = pos[1]

        g = Grid()
        g.show(screen)
        g.select(2,3, screen)

        #helper to see where I click, remove later
        text = font.render("click!", True, GREEN)
        screen.blit(text, [x, y])

        #rather than detect a keypress up, we just allow a single action per event
        clicked = False

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    # Limit frames per second
    clock.tick(60)

# Be IDLE friendly
pygame.quit()
