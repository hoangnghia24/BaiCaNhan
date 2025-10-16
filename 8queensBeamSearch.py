import pygame
import heapq

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

def an_toan(state, col, row):
    """Kiểm tra xem vị trí mới có an toàn không."""
    if state == []:
        return True
    for r, c in enumerate(state):
        if c == col or abs(c - col) == abs(r - row):
            return False
    return True

def hn(state, row):
    """tính số ô quân hậu không thể đặt."""
    count = 0
    cols = [False] * 8
    diagchinh = [False] * (2 * 8 - 1)
    diagphu = [False] * (2 * 8 - 1)
    for r, c in enumerate(state):
        cols[c] = True
        diagchinh[r + c] = True
        diagphu[r - c + 7] = True
    for r in range(row, 8):
        for c in range(8):
            if cols[c] or diagchinh[r + c] or diagphu[r - c + 7]:
                count += 1
    return count + row * 8

def beamSearch():
    branch = 5
    q = []
    heapq.heappush(q,(0,[]))
    solutions = []
    while True:
        stateList = []
        for cost,state in q:
            row = len(state)
            if row == 8:
                solutions.append(state)
            for col in range(8):
                if an_toan(state,col,row):
                    currentState = state + [col]
                    cost = hn(currentState,row+1)
                    stateList.append((cost,currentState))
        if not stateList:
            break
        beam = heapq.nsmallest(branch,stateList)
        q = beam
        heapq.heapify(q)
    return solutions
solutions = beamSearch()
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
    positions = list(beamSearch())
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