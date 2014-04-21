import pygame
import nonogram

def main():
    pygame.init() #must be called first
    dimensions = (800, 500)
    padding = 5
    displaysurf = pygame.display.set_mode(dimensions)
    pygame.draw.rect(displaysurf, (255, 255, 255), pygame.Rect(0, 0, dimensions[0], dimensions[1]))
    #HOW ABOUT UPDATE DISPLAY? SHOULD I DO THAT AFTER EVERY DRAWING OPERATION? NO PROBABLY NOT, ONLY AFTER EVERYTHING HAS BEEN DRAWN AFTER A GIVEN DRAW CALL

    #Construct nonogram (REPLACE THIS):
    nng = nonogram.Nonogram(5,5)
    nng.addline(0, [2], [1])
    nng.addline(0, [1,1,1], [1,1,1])
    nng.addline(0, [2,2], [1,1])
    nng.addline(0, [3], [1])
    nng.addline(0, [1], [1])

    nng.addline(1, [3], [1])
    nng.addline(1, [1,1], [1,1])
    nng.addline(1, [1,1], [1,1])
    nng.addline(1, [3], [1])
    nng.addline(1, [3], [1])

    nngvis = nonogram.NonogramVisualizer(nng, (padding, padding), tuple(dim - 2*padding for dim in dimensions))

    nngvis.draw(displaysurf)
    pygame.display.update()
    input()
    pygame.quit() #until this is called, screen is locked

if __name__ == '__main__':
    main()