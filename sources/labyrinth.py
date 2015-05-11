from Queue import PriorityQueue
from random import *
import pygame
from pygame import *
import sys

from pygame.draw import circle, line
from pygame.gfxdraw import pixel


__author__ = 'primankaden'

LAB_WIDTH = 40
LAB_HEIGHT = 30
LINE_WIDTH = 10
BORDER_WIDTH = 20
COLOR_RANGE = 100


class Edge:
    def __init__(self):
        self.weight = 0
        (self.startX, self.startY) = (0, 0)
        (self.endX, self.endY) = (0, 0)

def getLabyrinth():
    labyrinth = []
    seed(None)
    for i in range(LAB_WIDTH):
        for j in range(LAB_HEIGHT):
            if not (j == LAB_HEIGHT - 1):
                edgeV = Edge()
                (edgeV.startX, edgeV.startY) = (i, j)
                (edgeV.endX, edgeV.endY) = (i, j + 1)
                edgeV.weight = randint(0, COLOR_RANGE)
                labyrinth.append(edgeV)
            if not (i == LAB_WIDTH - 1):
                edgeH = Edge()
                (edgeH.startX, edgeH.startY) = (i, j)
                (edgeH.endX, edgeH.endY) = (i + 1, j)
                edgeH.weight = randint(0, COLOR_RANGE)
                labyrinth.append(edgeH)
    return labyrinth


def getLineColor(i):
    r = (255 * i) / COLOR_RANGE
    g = (255 * (COLOR_RANGE - i)) / COLOR_RANGE
    b = 0
    rgb = (r, g, b)
    color = '#%02x%02x%02x' % rgb
    return Color(color)


def drawLine(edge, isWhite):
    color = getLineColor(edge.weight)
    width = 2
    if isWhite:
        color = Color('#ffffff')
        width = 8
    line(bg, color, (edge.startX * LINE_WIDTH + BORDER_WIDTH, edge.startY * LINE_WIDTH + BORDER_WIDTH),
         (edge.endX * LINE_WIDTH + BORDER_WIDTH, edge.endY * LINE_WIDTH + BORDER_WIDTH), width)

    screen.blit(bg, (0, 0))
    pygame.display.update()


DISPLAY = (LAB_WIDTH * LINE_WIDTH + 2 * BORDER_WIDTH, LAB_HEIGHT * LINE_WIDTH + 2 * BORDER_WIDTH)
pygame.init()
screen = display.set_mode(DISPLAY)
pygame.display.set_caption('Labyrinth')
bg = Surface(DISPLAY)
bg.fill(Color('#000000'))
labyrinth = getLabyrinth()
for l in labyrinth:
    for e in pygame.event.get():
        if e.type == QUIT:
            raise SystemExit, "QUIT"
    drawLine(l, False)


def kruskal(G):
    pq = PriorityQueue()
    for e in G:
        pq.put((e.weight, e))

    treeGroups = []
    treeGroups.append([])

    while not pq.empty():
        curEdge = pq.get()[1]
        startGroup = None
        endGroup = None
        for group in treeGroups:
            hasStart = False
            hasEnd = False
            if group != None:
                for edge in group:
                    hasStart |= (edge.startX == curEdge.startX and edge.startY == curEdge.startY)
                    hasStart |= (edge.endX == curEdge.startX and edge.endY == curEdge.startY)
                    hasEnd |= (edge.startX == curEdge.endX and edge.startY == curEdge.endY)
                    hasEnd |= (edge.endX == curEdge.endX and edge.endY == curEdge.endY)
                    if (hasStart and hasEnd):
                        break
            if hasStart:
                startGroup = group
            if hasEnd:
                endGroup = group
        if startGroup != None and startGroup == endGroup:
            continue
        drawLine(curEdge, True)
        if startGroup == None and endGroup != None:
            endGroup.append(curEdge)
            continue
        if startGroup != None and endGroup == None:
            startGroup.append(curEdge)
            continue
        if startGroup != endGroup:
            startGroup.extend(endGroup)
            treeGroups.remove(endGroup)
            continue
        if startGroup == None and endGroup == None:
            newGroup = [curEdge]
            treeGroups.append(newGroup)
            continue
    return treeGroups[0]


kruskal(labyrinth)

# pygame.image.save(screen, "screen.png")

LEFT_COLOR = "#ff9090"
RIGHT_COLOR = "#90ff90"
UP_COLOR = "#9090ff"
DOWN_COLOR = "#ffff90"
START_COLOR = "#f0f0f0"


def solveLabyrinth():
    seed(None)
    startX = 0
    startY = 0
    while True:
        (r, g, b, a) = bg.get_at((startX, startY))
        if r == g == b == 255:
            break
        else:
            startX += 1
            startY += 1
    (endX,endY) =  bg.get_size()
    endX -= 1
    endY -= 1
    while True:
        (r, g, b, a) = bg.get_at((endX, endY))
        if r == g == b == 255:
            break
        else:
            endX -= 1
            endY -= 1
    queue = PriorityQueue()
    queue.put((randint(0, 100), (startX, startY)))
    pixel(bg, startX, startY, Color(START_COLOR))
    while not queue.empty():
        (a, (x, y)) = queue.get()
        if (endX==x and endY==y):
            break
        # left
        (r, g, b, a) = bg.get_at((x - 1, y))
        if r == g == b == 255:
            queue.put((randint(0, 100), (x - 1, y)))
            pixel(bg, x - 1, y, Color(LEFT_COLOR))
        # right
        (r, g, b, a) = bg.get_at((x + 1, y))
        if r == g == b == 255:
            queue.put((randint(0, 100), (x + 1, y)))
            pixel(bg, x + 1, y, Color(RIGHT_COLOR))
        # up
        (r, g, b, a) = bg.get_at((x, y - 1))
        if r == g == b == 255:
            queue.put((randint(0, 100), (x, y - 1)))
            pixel(bg, x, y - 1, Color(UP_COLOR))
        # down
        (r, g, b, a) = bg.get_at((x, y + 1))
        if r == g == b == 255:
            queue.put((randint(0, 100), (x, y + 1)))
            pixel(bg, x, y + 1, Color(DOWN_COLOR))
        screen.blit(bg, (0, 0))
        pygame.display.update()

    while endX!=startX and endY!=startY:
        color = bg.get_at((endX, endY))
        pixel(bg,endX, endY, Color('#ff0000'))
        if Color(RIGHT_COLOR)==color:
            endX-=1
        if Color(LEFT_COLOR)==color:
            endX+=1
        if Color(UP_COLOR)==color:
            endY+=1
        if Color(DOWN_COLOR)==color:
            endY-=1
        screen.blit(bg, (0, 0))
        pygame.display.update()

solveLabyrinth()


raw_input("Waiting")