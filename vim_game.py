#uses the graphics library pygame
import pygame


#this contains code to modify specific letters stored in individual cells
class Cell():
    def __init__(self, x, y):
        #these are the coordinates in relation to the grid
        self.x = x
        self.y = y
        self.c = 'F'
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
        self.cells = [[Cell(x,y) for x in range(20)] for y in range(10)]
        self.x = 0
        self.y = 0
        self.cells[0][0].selected = True


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
#todo: implement levels class
#class Level():



# the main game engine is here. Will have to restructure a bit

#initialize the engine
pygame.init()
# Select the font to use, size, bold, italics
font = pygame.font.SysFont('Calibri', 18, False, False)


CELL_WIDTH = 30
CELL_HEIGHT = 30

# Define the colors we will use in RGB format
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]
RED = [255, 0, 0]

# Set the height and width of the screen
size = [800, 500]
screen = pygame.display.set_mode(size)

# Loop until the user clicks the close button.
done = False

clock = pygame.time.Clock()

#checks if the mouse button is clicked, initializes as true
#todo: modify code to not require this
clicked = True

#set screen to black
screen.fill(WHITE)

#selected letter

#inits the grid
g = Grid()

#game engine
while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True


        elif event.type == pygame.KEYDOWN:
            #allows hjkl navigation of selected tile
            #only if the key is preseed
            #todo: add bumpers for movement
            if event.key == pygame.K_k:
                coords = g.get_selected_coords()
                g.select(coords[0] - 1, coords[1], screen)
            elif event.key == pygame.K_h:
                coords = g.get_selected_coords()
                g.select(coords[0], coords[1] - 1, screen)
            elif event.key == pygame.K_l:
                coords = g.get_selected_coords()
                g.select(coords[0], coords[1] + 1, screen)
            elif event.key == pygame.K_j:
                coords = g.get_selected_coords()
                g.select(coords[0] + 1, coords[1], screen)
            g.show(screen)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True

        # more events can be added for functions
        #todo: add vim command functionality


    #checks to see if we clicked on something
    if clicked:
        pos = pygame.mouse.get_pos()
        x = pos[0]
        y = pos[1]


        g.show(screen)
        #g.select(2,3, screen)

        #helper to see where I click, remove later
        text = font.render("click!", True, GREEN)
        screen.blit(text, [x, y])

        #todo: menu navigation

        #rather than detect a keypress up, we just allow a single action per event
        clicked = False

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    # Limit frames per second
    clock.tick(60)

# Be IDLE friendly
pygame.quit()
