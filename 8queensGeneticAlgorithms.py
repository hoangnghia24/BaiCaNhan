import pygame
import random

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

def fitness(X):
    pairQueen = 8 * (8 - 1) // 2
    return pairQueen - h(X)

def initialize(size):
    """Tạo quần thể ban đầu"""
    population = []
    for _ in range(size):
        chromosome = list(range(8))
        random.shuffle(chromosome)
        population.append(chromosome)
    return population

def selection(population, fitnesses):
    """Chọn cặp cá thể bằng Tournament Selection."""
    tournamentSize = 4
    
    def tournament():
        choice = random.sample(range(len(population)), tournamentSize)
        bestI = choice[0]
        bestFit = fitnesses[bestI]
        for index in choice[1:]:
            if fitnesses[index] > bestFit:
                bestFit = fitnesses[index]
                bestI = index
        return population[bestI]

    parent1 = tournament()
    parent2 = tournament()
    return parent1, parent2

def crossover(parent1, parent2):
    """Lai ghép"""
    n = 8
    child = [None] * n
    start, end = sorted(random.sample(range(n), 2))
    child[start:end] = parent1[start:end]
    parent2Gen = [gene for gene in parent2 if gene not in child[start:end]]
    p2I = 0

    for i in range(start):
        child[i] = parent2Gen[p2I]
        p2I += 1

    for i in range(end, n):
        child[i] = parent2Gen[p2I]
        p2I += 1
    return child

def mutate(chromosome, mutationRate):
    """Đột biến"""
    if random.random() < mutationRate:
        idx1, idx2 = random.sample(range(8), 2)
        chromosome[idx1], chromosome[idx2] = chromosome[idx2], chromosome[idx1]
    return chromosome

def GeneticAlgorithm():
    population = initialize(100)
    bestChromosomeOverall = population[0]
    bestFitnessOverall = fitness(population[0])

    for generation in range(1000):
        fitnesses = [fitness(c) for c in population]
        bestFitness = max(fitnesses)
        bestIndex = fitnesses.index(bestFitness)
        bestChromosome = population[bestIndex]
        if bestFitness > bestFitnessOverall:
            bestFitnessOverall = bestFitness
            bestChromosomeOverall = bestChromosome
        if bestFitness == 28:
            return [bestChromosome]

        newPopulation = []

        newPopulation.append(bestChromosome)

        for _ in range(100 - 1):
            parent1, parent2 = selection(population, fitnesses)
            child = crossover(parent1, parent2)
            child = mutate(child, 0.05)
            newPopulation.append(child)
        population = newPopulation
    return [bestChromosomeOverall]

solutions = GeneticAlgorithm()
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
    positions = list(GeneticAlgorithm())
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