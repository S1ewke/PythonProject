import pygame
import random
import math

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Aim Trainer — шаг 3: рекорды + попадания")

x = 400
y = 300
radius = 40
score = 0

font = pygame.font.SysFont("None", 36)


try:
    with open("Records.txt", "r") as f:
        best_score = int(f.read().strip() or 0)
except (FileNotFoundError, ValueError):
    best_score = 0


running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # клик мышкой
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mx, my = event.pos

                dist = math.dist((mx, my), (x, y))

                if dist < radius:
                    score += 1
                    x = random.randint(radius, 800 - radius)
                    y = random.randint(radius, 600 - radius)


    screen.fill((30, 30, 30))


    pygame.draw.circle(screen, (255, 60, 60), (x, y), radius)

    #текст очков
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    record_text = font.render(f"Record: {best_score}", True, (200, 200, 200))
    screen.blit(record_text, (10, 40))

    pygame.display.flip()

if score > best_score:
    with open("Records.txt", "w") as f:
        f.write(str(score))

pygame.quit()