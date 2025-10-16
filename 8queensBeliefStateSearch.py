import pygame
import random
import math
pygame.init()
screenWidth = 700
screenHeight = 700
windown = pygame.display.set_mode((screenWidth+300, screenHeight+100))
pygame.display.set_caption("Eight Queens!!!")
white = (255, 255, 255)
black = (0, 0, 0)
squareBoard = screenWidth // 8
i = 0
def chessboard():
    for row in range(8):
        for col in range(8):
            if (row + col) % 2 == 0:
                color = white
            else:
                color = black
            pygame.draw.rect(windown, color, (col * squareBoard, row * squareBoard, squareBoard, squareBoard))

def isSafe(state, row, col):
    for r, c in enumerate(state):
        if c == col or abs(c - col) == abs(r - row):
            return False
    return True

def beliefStateSearch():
    init = [[]]
    solutions = []
    while init:
        N = []
        for state in init:
            row = len(state)
            for col in range(8):
                if isSafe(state, row, col):
                    N.append(state + [col])
        init = N
        complete = [rs for rs in init if len(rs) == 8]
        solutions.extend(complete)
        init = [start for start in init if len(start) < 8]
    return solutions


solutions = beliefStateSearch()
sumsolutions = len(solutions)

def coordinate(position):
    '''In tọa độ trên màn hình'''
    pygame.draw.rect(windown, black, (screenWidth + 10, 100, 300, screenHeight))
    spacing = pygame.font.SysFont('Times New Roman', 24).get_linesize()
    header = pygame.font.SysFont('Times New Roman', 32).render("Coordinate queens:", True, (255,50,100))
    windown.blit(header, (screenWidth+10, 100))
    for i, j in enumerate(position):
        text_surface = pygame.font.SysFont('Times New Roman', 24).render(f"({i}, {j})", True, (255,50,100))
        windown.blit(text_surface, (screenWidth+10,100 + (i + 1) * spacing))

def queen(i):
    '''In các ô vuông đại diện cho quân hậu'''
    positions = list(beliefStateSearch())
    if len(positions) == 0:
        return
    position = positions[i]
    for (i,j) in enumerate(position):
        pygame.draw.rect(windown, (155,255,155,0.5), (j * squareBoard+10, i * squareBoard+10, squareBoard-20, squareBoard-20))
    coordinate(position)
isRunning = True
while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            txtbtn = pygame.font.SysFont('Times New Roman', 24).render("Change",True,white)
            recbtn = txtbtn.get_rect(center = (100,screenHeight+20))
            if recbtn.collidepoint(event.pos):
                i += 1
                if i >= sumsolutions:
                    i  =0
            chessboard()
            queen(i)
    txtbtn = pygame.font.SysFont('Times New Roman', 24).render("Change",True,white)
    recbtn = txtbtn.get_rect(center = (100,screenHeight+20))
    windown.blit(txtbtn,recbtn)
    pygame.display.flip()
pygame.quit()