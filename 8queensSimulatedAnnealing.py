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

def h(X):
    '''Tính chi phí dựa cặp quân hậu tấn công nhau'''
    cap = 0 # số cặp quân hậu đang ăn nhau
    n = len(X)
    for i in range(n):
        for j in range(i + 1, n):
            if abs(X[i] - X[j]) == abs(i - j) or X[i] == X[j]: # kiểm tra xem cùng hàng hay đường chéo không
                cap += 1
    return cap
def accep(deltaE,T):
    if deltaE <= 0:
        return 1.0
    if T == 0:
        return 0.0
    return math.exp(-deltaE/T)
def SimulatedAnnealing():
    '''Thuật toán Simulated Annealing'''
    solutions = []
    alpha = 0.2
    while True:
        # khởi tạo trạng thái ban đầu của 8 quân hậu
        X = [random.randint(0, 7) for _ in range(8)]
        T = 0.7
        while T > 0.00001:
            E = h(X) # Chi phí của trạng thái ban đầu
            if E == 0:
                solutions.append(X)
                break
            N = list(X) #Khởi tạo N để có thể duyệt tìm trạng thái lân cận
            # Tìm trạng thái lân cận tốt nhất
            row = random.randint(0,7) #tạo hàng ngẫu nhiên
            col = random.randint(0,7) #tạo cột ngẫu nhiên
            while col == N[row]:
                col = random.randint(0,7)
            N[row] = col
            E1 = h(X)
            deltaE = E1 - E
            if accep(deltaE,T) > random.random():
                X = N
                E = E1
            T *= alpha
        if len(solutions) >= 1:  # nếu có lời giải thì dừng
            break
    return solutions

solutions = SimulatedAnnealing()
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
    positions = list(SimulatedAnnealing())
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