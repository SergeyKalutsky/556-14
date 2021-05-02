import pygame, pygame.locals
import sys, random
FPS = 30
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
REVEAL_SPEED = 100 
BOX_SIZE = 40 
GAP_SIZE = 10 
BOARD_WIDTH = 10  
BOARD_HEIGHT = 7  

NMINES = 1 + int(BOARD_WIDTH * BOARD_HEIGHT * 0.16)

XMARGIN = int((WINDOW_WIDTH - (BOARD_WIDTH * (BOX_SIZE + GAP_SIZE))) / 2)
YMARGIN = int((WINDOW_HEIGHT - (BOARD_HEIGHT * (BOX_SIZE + GAP_SIZE))) / 2)

GRAY = (100, 100, 100)
NAVYBLUE = (60, 60, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)

BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = GRAY
HIGHLIGHTCOLOR = BLUE

DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond' # мина
LINES = 'lines'
OVAL = 'oval'

ALL_COLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALL_SHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)


def main():
    global FPS_CLOCK, DISPLAY_SURF
    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    DISPLAY_SURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    mousex = 0 
    mousey = 0
    pygame.display.set_caption('Сапёр')

    mainBoard = getRandomizedBoard()
    revealedBoxes = generateData(False)
    Flags = generateData(False)
    isGameOver = False

    DISPLAY_SURF.fill(BGCOLOR)

    # основной цикл игры
    while True:
        mouseClickedLeft = False
        mouseClickedRight = False

        DISPLAY_SURF.fill(BGCOLOR) 
        drawBoard(mainBoard, revealedBoxes, Flags)


        for event in pygame.event.get():  
            if event.type == pygame.locals.QUIT or (event.type == pygame.locals.KEYUP and event.key == pygame.locals.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.locals.MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == pygame.locals.MOUSEBUTTONDOWN and event.button == 1:  # Левая кнопка
                mousex, mousey = event.pos
                mouseClickedLeft = True
            elif event.type == pygame.locals.MOUSEBUTTONDOWN and event.button == 3:  # Правая кнопка
                mousex, mousey = event.pos
                mouseClickedRight = True

        if isGameOver and mouseClickedRight:
            mainBoard = getRandomizedBoard()
            revealedBoxes = generateData(False)
            Flags = generateData(False)
            isGameOver = False
            mouseClickedRight = False

        if isGameOver:
            myfont = pygame.font.SysFont("monospace", 25)
            if isVictory:
                label = myfont.render('Победа', 1, (0, 255, 0))
                DISPLAY_SURF.blit(label, (200, 415))
            else:
                label = myfont.render('Поражение', 1, (255, 0, 0))
                DISPLAY_SURF.blit(label, (260, 415))
            label = myfont.render('Нажмите ПКМ для рестарта', 1, YELLOW)
            DISPLAY_SURF.blit(label, (155, 445))

        boxx, boxy = getBoxAtPixel(mousex, mousey)
        if boxx != None and boxy != None:
            # Мышь находится над прямоугольником.
            if not revealedBoxes[boxx][boxy] and not isGameOver:
                drawHighlightBox(boxx, boxy)

            if not revealedBoxes[boxx][boxy] and mouseClickedLeft and not isGameOver:

                Flags[boxx][boxy] = False

                if mainBoard[boxx][boxy][0] == DIAMOND: # Событие нажатие на "мину"
                    revealBoxesAnimation(mainBoard, [(boxx, boxy)])
                    revealedBoxes = generateData(True)
                    # Ожидание щелчка правой кнопкой мыши и начало новой игры
                    isGameOver = True
                elif mainBoard[boxx][boxy][0] == SQUARE:
                    # событие нажатия на пустой квадрат
                    openSquares(boxx, boxy, mainBoard, revealedBoxes, Flags)
                else:
                    revealBoxesAnimation(mainBoard, [(boxx, boxy)])
                    revealedBoxes[boxx][boxy] = True  # установка квадрата как "раскрытого"

                drawBoard(mainBoard, revealedBoxes, Flags)

            if not revealedBoxes[boxx][boxy] and mouseClickedRight and not isGameOver:
                Flags[boxx][boxy] = not Flags[boxx][boxy]
                drawBoard(mainBoard, revealedBoxes, Flags)

            isVictory = True
            for x in range(BOARD_WIDTH):
                for y in range(BOARD_HEIGHT):
                    if (mainBoard[x][y][0] == DIAMOND and not Flags[x][y]) or (
                            mainBoard[x][y][0] != DIAMOND and not revealedBoxes[x][y]):
                        isVictory = False

            if isVictory:
                isGameOver = True

        # Перерисовываем экран и ожидание тика
        pygame.display.update()
        FPS_CLOCK.tick(FPS)


def generateData(val):
    revealedBoxes = []
    for i in range(BOARD_WIDTH):
        revealedBoxes.append([val] * BOARD_HEIGHT)
    return revealedBoxes


def getRandomizedBoard():

    icons = []

    mines = 0
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            if mines < NMINES:
                icons.append((DIAMOND, GREEN))
                mines += 1
            else:
                icons.append((SQUARE, WHITE))

    random.shuffle(icons)  # рандом списка значков

    # Создание доски с рандомными значками.
    board = []
    for x in range(BOARD_WIDTH):
        column = []
        for y in range(BOARD_HEIGHT):
            column.append(icons[0])
            del icons[0] 
        board.append(column)

    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            mines = 0
            if x > 0:
                if y > 0:
                    if board[x - 1][y - 1][0] == DIAMOND: mines += 1
                if board[x - 1][y][0] == DIAMOND: mines += 1
                if y < BOARD_HEIGHT - 1:
                    if board[x - 1][y + 1][0] == DIAMOND: mines += 1
            if x < BOARD_WIDTH - 1:
                if y > 0:
                    if board[x + 1][y - 1][0] == DIAMOND: mines += 1
                if board[x + 1][y][0] == DIAMOND: mines += 1
                if y < BOARD_HEIGHT - 1:
                    if board[x + 1][y + 1][0] == DIAMOND: mines += 1
            if y > 0:
                if board[x][y - 1][0] == DIAMOND: mines += 1
            if y < BOARD_HEIGHT - 1:
                if board[x][y + 1][0] == DIAMOND: mines += 1
            # установка количества мин
            if board[x][y][0] != DIAMOND:
                if mines in range(1,9):
                    
                    board[x][y] = (str(mines), WHITE)

    return board


def splitIntoGroupsOf(groupSize, theList):
    result = []
    for i in range(0, len(theList), groupSize):
        result.append(theList[i:i + groupSize])
    return result


def leftTopCoordsOfBox(boxx, boxy):
    left = boxx * (BOX_SIZE + GAP_SIZE) + XMARGIN
    top = boxy * (BOX_SIZE + GAP_SIZE) + YMARGIN
    return (left, top)


def getBoxAtPixel(x, y):
    for boxx in range(BOARD_WIDTH):
        for boxy in range(BOARD_HEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOX_SIZE, BOX_SIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)



def drawIcon(shape, color, boxx, boxy):

    quarter = int(BOX_SIZE * 0.25)
    half = int(BOX_SIZE * 0.5)
    left, top = leftTopCoordsOfBox(boxx, boxy)

    # Рисовка фигур
    if shape == DONUT:
        pygame.draw.circle(DISPLAY_SURF, color, (left + half, top + half), half - 5)
        pygame.draw.circle(DISPLAY_SURF, BGCOLOR, (left + half, top + half), quarter - 5)
    elif shape == SQUARE:
        pygame.draw.rect(DISPLAY_SURF, color, (left, top, BOX_SIZE, BOX_SIZE))
    elif shape == DIAMOND:
        pygame.draw.polygon(DISPLAY_SURF, color, (
        (left + half, top), (left + BOX_SIZE - 1, top + half), (left + half, top + BOX_SIZE - 1), (left, top + half)))
    elif shape == LINES:
        for i in range(0, BOX_SIZE, 4):
            pygame.draw.line(DISPLAY_SURF, color, (left, top + i), (left + i, top))
            pygame.draw.line(DISPLAY_SURF, color, (left + i, top + BOX_SIZE - 1), (left + BOX_SIZE - 1, top + i))
    elif shape == OVAL:
        pygame.draw.ellipse(DISPLAY_SURF, color, (left, top + quarter, BOX_SIZE, half))
    else:
        # рисовка квадрата с цифрой
        pygame.draw.rect(DISPLAY_SURF, color, (left, top, BOX_SIZE, BOX_SIZE))
        fontsize = int(BOX_SIZE)
        myfont = pygame.font.SysFont("monospace", fontsize)
        label = myfont.render(shape, 1, RED)
        DISPLAY_SURF.blit(label, (left + quarter, top))


def getShapeAndColor(board, boxx, boxy):
    return board[boxx][boxy][0], board[boxx][boxy][1]


def drawBoxCovers(board, boxes, coverage):
    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(DISPLAY_SURF, BGCOLOR, (left, top, BOX_SIZE, BOX_SIZE))
        shape, color = getShapeAndColor(board, box[0], box[1])
        drawIcon(shape, color, box[0], box[1])
        if coverage > 0:
            pygame.draw.rect(DISPLAY_SURF, BOXCOLOR, (left, top, coverage, BOX_SIZE))
    pygame.display.update()
    FPS_CLOCK.tick(FPS)


def revealBoxesAnimation(board, boxesToReveal):
    for coverage in range(BOX_SIZE, (-REVEAL_SPEED) - 1, -REVEAL_SPEED):
        drawBoxCovers(board, boxesToReveal, coverage)


def openSquares(x, y, board, revealed, flags):
    if revealed[x][y]: return
    if flags[x][y]: return
    revealBoxesAnimation(board, [(x, y)])
    revealed[x][y] = True
    if board[x][y][0] != SQUARE: return
    if x > 0:
        if y > 0: openSquares(x - 1, y - 1, board, revealed, flags)
        openSquares(x - 1, y, board, revealed, flags)
        if y < BOARD_HEIGHT - 1: openSquares(x - 1, y + 1, board, revealed, flags)
    if x < BOARD_WIDTH - 1:
        if y > 0: openSquares(x + 1, y - 1, board, revealed, flags)
        openSquares(x + 1, y, board, revealed, flags)
        if y < BOARD_HEIGHT - 1: openSquares(x + 1, y + 1, board, revealed, flags)
    if y > 0: openSquares(x, y - 1, board, revealed, flags)
    if y < BOARD_HEIGHT - 1: openSquares(x, y + 1, board, revealed, flags)


def drawBoard(board, revealed, flags):

    for boxx in range(BOARD_WIDTH):
        for boxy in range(BOARD_HEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if not revealed[boxx][boxy]:
                pygame.draw.rect(DISPLAY_SURF, BOXCOLOR, (left, top, BOX_SIZE, BOX_SIZE))
                if flags[boxx][boxy]:
                    for i in range(0, BOX_SIZE, 4):
                        pygame.draw.line(DISPLAY_SURF, CYAN, (left, top + i), (left + i, top))
                        pygame.draw.line(DISPLAY_SURF, CYAN, (left + i, top + BOX_SIZE - 1),
                                         (left + BOX_SIZE - 1, top + i))
            else:
                shape, color = getShapeAndColor(board, boxx, boxy)
                drawIcon(shape, color, boxx, boxy)


def drawHighlightBox(boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAY_SURF, HIGHLIGHTCOLOR, (left - 5, top - 5, BOX_SIZE + 10, BOX_SIZE + 10), 4)


if __name__ == '__main__':
    main()
