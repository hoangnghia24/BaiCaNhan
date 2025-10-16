import pygame
from queue import LifoQueue
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
def an_toan(state, col,row):
    for r, c in enumerate(state):
        if c == col or abs(c - col) == abs(r - row):
            return False
    return True

# function depth-limited-search(problem, limit):
#   return recursive_dls(problem.init(), limit)
# recursive_dls(node, problem, limit):
#   cutoff_occurred = false
#   if problem.goal_test(node.state):
#     return node
#   else if depth[node] == limit:
#     return cutoff
#   else:
#     for each successor in expand(node, problem) do
#       result = recursive_dls(successor, problem, limit):
#       if result == cutoff:
#         cutoff_occurred = true
#       else if result != failure:
#         return result
#     if cutoff_occurred:
#       return cutoff
#     else:
#       return failure
def recursive_DLS(state, depth):
    if len(state) == 8:
        return [state]
    elif depth == 0:
        return None
    else:
        solutions = []
        for col in range(8):
            if an_toan(state, col, len(state)):
                result = recursive_DLS(state + [col], depth - 1)
                if result is not None:
                    solutions += result
        return solutions if solutions else None
def dls():
    limit = 8
    return recursive_DLS([], limit)
solutions = dls()
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
    positions = list(dls())
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
                if i > sumsolutions:
                    i  =0
            chessboard()
            queen(i)
    txtbtn = pygame.font.SysFont('Times New Roman', 24).render("Change",True,white)
    recbtn = txtbtn.get_rect(center = (100,screenHeight+20))
    windown.blit(txtbtn,recbtn)
    pygame.display.flip()
pygame.quit()