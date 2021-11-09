import time

import pygame
import os
import win32api
import win32file

devices = []

drives = win32api.GetLogicalDriveStrings().split('\x00')[:-1]

for device in drives:
    devices.append(device)

print(devices)


def scanDevices():
    verif = False
    newDevices = []
    drives = win32api.GetLogicalDriveStrings().split('\x00')[:-1]

    for device in drives:
        newDevices.append(device)

    if devices == newDevices:
        verif = True
    return verif


pygame.init()
pygame.font.init()

clock = pygame.time.Clock()
number = 0
width, height = (1920, 1080)

screen = pygame.display.set_mode((width, height))
icon = pygame.image.load('icon.jpg')
pygame.display.set_icon(icon)
pygame.display.set_caption("VéloEnergie")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (30, 30, 30)
FONT = pygame.font.SysFont("Comic Sans MS", 50)

button = pygame.Rect(0, 100, 200, 200)
textsurface = FONT.render("Vous pouvez brancher votre vélo...", False, (0, 0, 0))


def blitRotate(surf, image, pos, originPos, angle):
    image_rect = image.get_rect(topleft=(pos[0] - originPos[0], pos[1] - originPos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center

    rotated_offset = offset_center_to_pivot.rotate(-angle)

    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)

    surf.blit(rotated_image, rotated_image_rect)


def addtext(text, color, position):
    font = pygame.font.SysFont('arial', 30)
    text_final = font.render(text, True, color)
    screen.blit(text_final, position)
    pygame.display.flip()


def addimage(path, position):
    image = pygame.image.load(path)
    screen.blit(image, position)
    pygame.display.flip()


def DrawBar(pos, size, borderC, barC, progress):
    pygame.draw.rect(screen, borderC, (*pos, *size), 1)
    innerPos = (pos[0] + 3, pos[1] + 3)
    innerSize = ((size[0] - 6) * progress, size[1] - 6)
    pygame.draw.rect(screen, barC, (*innerPos, *innerSize))
    pygame.display.flip()


loading = pygame.transform.scale(pygame.image.load('loading.gif'), (100, 100))
w, h = loading.get_size()
angle = 0

while True:
    pygame.time.Clock().tick(120)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    color = (59, 226, 203)

    if not scanDevices():
        color = (124, 169, 113)
        pourcentage = 0

        for x in range(100):

            if scanDevices():
                exit()
            screen.fill(color)
            addimage('charging.png', (w / 2+675, h / 2+200))
            addtext(str(x) + '% Charging...', (0, 0, 0), (w / 2 + 600, h / 2 + 100))
            DrawBar((w / 2 + 600, h / 2 + 150), (700, 100), (57, 57, 57), (43, 156, 160), x / 100)
            pygame.display.flip()
            time.sleep(0.1)
        pygame.quit()
        exit()

    else:
        screen.blit(textsurface, (width / 2 - 400, height / 2 + 50))
        pos = (screen.get_width() / 2, screen.get_height() / 2)
        blitRotate(screen, loading, pos, (w / 2, h / 2), angle)
        angle += 1

        pygame.display.flip()

    screen.fill(color)

pygame.quit()
