import pygame
import random
import math

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Aim Trainer")

x = 400
y = 300
radius = 40

score = 0
shots = 0
hits = 0
accuracy = 0

font = pygame.font.SysFont("None", 36)

try:
    with open("Records.txt", "r") as f:
        best_score = int(f.read().strip() or 0)
except:
    best_score = 0

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                shots += 1
                mx, my = event.pos

                dist = math.dist((mx, my), (x, y))

                if dist < radius:
                    hits += 1
                    score += 1

                    if score > best_score:
                        best_score = score

                    x = random.randint(radius, 800 - radius)
                    y = random.randint(radius, 600 - radius)

    screen.fill((30, 30, 30))

    pygame.draw.circle(screen, (255, 60, 60), (x, y), radius)

    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    record_text = font.render(f"Record: {best_score}", True, (200, 200, 200))
    screen.blit(record_text, (10, 40))

    if shots > 0:
        accuracy = hits / shots * 100
    else:
        accuracy = 0

    acc_text = font.render(f"Acc: {accuracy:.1f}%", True, (180, 180, 255))
    screen.blit(acc_text, (10, 150))

    pygame.display.flip()

if score > best_score:
    best_score = score

with open("Records.txt", "w") as f:
    f.write(str(best_score))

pygame.quit()
