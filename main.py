import sys
import random
import pygame

pygame.init()

W = 640
H = 400
OFFSET = 50
MAX_CATS = 10
START_POSITION = (OFFSET, OFFSET)


def show_score(font, score):
    return font.render('Score: {}'.format(score), 1, (255, 0, 0))


def generate_point():
    return (random.randint(OFFSET, W-OFFSET),
            random.randint(OFFSET, H-OFFSET))


def main(args):
    is_running = True
    pygame.display.set_mode((W, H))
    pygame.display.set_caption('Croc Eat Cats')

    if len(args) > 1 and args[1] == 'full':
        pygame.display.toggle_fullscreen()

    screen = pygame.display.get_surface()
    clock = pygame.time.Clock()

    x, y = START_POSITION
    score = 0

    bg_img = pygame.image.load('bg.jpg')
    croc_img = pygame.image.load('croc.png')
    cat_img = pygame.image.load('cat.png')
    tiger_img = pygame.image.load('tiger.png')
    meow = pygame.mixer.Sound('cat.wav')
    roar = pygame.mixer.Sound('tiger.wav')

    mono = pygame.font.SysFont('monospace', 15)

    croc_map = (
        (20,  0, 45, 55),
        (100, 0, 45, 55),
        (180, 0, 45, 55),
        (20,  155, 45, 55),
        (100, 155, 45, 55),
        (180, 155, 45, 55),
        (0, 110, 80, 30),
        (85, 110, 80, 30),
        (165, 110, 80, 30),
        (0, 60, 80, 30),
        (85, 60, 80, 30),
        (165, 60, 80, 30),
    )

    choice = croc_map[0]

    cats = map(lambda _: generate_point(), range(10))
    tigers = []

    while is_running:
        ev = pygame.event.poll()
        if ev.type == pygame.KEYDOWN:
            key = ev.dict['key']
            if key == 27:
                is_running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_DOWN]:
            choice = random.choice(croc_map[:3])
            y += 5

        if keys[pygame.K_UP]:
            choice = random.choice(croc_map[3:6])
            y -= 5

        if keys[pygame.K_RIGHT]:
            choice = random.choice(croc_map[6:9])
            x += 5

        if keys[pygame.K_LEFT]:
            choice = random.choice(croc_map[9:12])
            x -= 5

        if x > 600:
            x = 20
        if y > 360:
            y = 20
        if x < 20:
            x = 600
        if y < 20:
            y = 360

        screen.blit(bg_img, (0, 0))

        for cat in cats:
            a = pygame.Rect(cat, cat_img.get_size())
            b = pygame.Rect((x, y), choice[2:])

            if b.colliderect(a):
                score += 1
                cats.remove(cat)
                if score % 5 == 0:
                    tigers.append(generate_point())
            else:
                screen.blit(cat_img, cat)

        for tiger in tigers:
            a = pygame.Rect(tiger, tiger_img.get_size())
            b = pygame.Rect((x, y), choice[2:])

            if b.colliderect(a):
                score -= 5
                roar.play()
                tigers.remove(tiger)
            else:
                screen.blit(tiger_img, tiger)

        if len(cats) < MAX_CATS:
            meow.play()
            cats.append(generate_point())

        screen.blit(croc_img, (x, y), choice)
        screen.blit(show_score(mono, score), (10, 10))
        pygame.display.flip()
        clock.tick(30)

if __name__ == '__main__':
    main(sys.argv)
