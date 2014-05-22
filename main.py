import pygame
import nonogram
import examples

def main():
    pygame.init() #must be called first
    dimensions = (800, 500)
    padding = 5
    displaysurf = pygame.display.set_mode(dimensions)
    pygame.draw.rect(displaysurf, (255, 255, 255), pygame.Rect(0, 0, dimensions[0], dimensions[1]))
    #HOW ABOUT UPDATE DISPLAY? SHOULD I DO THAT AFTER EVERY DRAWING OPERATION? NO PROBABLY NOT, ONLY AFTER EVERYTHING HAS BEEN DRAWN AFTER A GIVEN DRAW CALL

    #Construct nonogram (REPLACE THIS):
    #nng = examples.constructnonogram(4)
    #nng = nonogram.readnonogramfromfile("1_alt.txt")
    nng = nonogram.readnonogramfromfile("8.txt")
    nng.solve()
    nngvis = nonogram.NonogramVisualizer(nng, (padding, padding), tuple(dim - 2*padding for dim in dimensions))

    nngvis.draw(displaysurf)
    pygame.display.update()
    input()
    pygame.quit() #until this is called, screen is locked

if __name__ == '__main__':
    main()