import random
import pygame

pygame.init()

def show_score(font, score):
    return font.render('Score: {}'.format(score), 1, (255,255,0))

def generate_cat():
    return (random.randint(50,590), random.randint(50,430))


def main():
    is_running = True
    window = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Batata')
    screen = pygame.display.get_surface()

    x, y = 50, 50
    score = 0

    croc_img = pygame.image.load('croc.png')
    cat_img = pygame.image.load('cat.png')
    meow = pygame.mixer.Sound('meow.wav')

    mono = pygame.font.SysFont('monospace', 15)

    croc_map = (
        (20,  0, 45, 55),
        (100, 0, 45, 55),
        (180, 0, 45, 55),
        (20, 155, 45, 55),
        (100,155, 45, 55),
        (180,155, 45, 55),
        (0, 110, 80, 30),
        (85,110, 80, 30),
        (165,110, 80, 30),
        (0, 60, 80, 30),
        (85,60, 80, 30),
        (165,60, 80, 30),
    )

    choice = croc_map[0]

    cats = map(lambda _: generate_cat(), range(10))

    while is_running:
        ev = pygame.event.poll()
        if ev.type == pygame.KEYDOWN:
            key = ev.dict['key']
            if key == 27:
                is_running = False 

            if key == 274:
                choice = random.choice(croc_map[:3])
                y += 5

            if key == 273:
                choice = random.choice(croc_map[3:6])
                y -= 5

            if key == 275:
                choice = random.choice(croc_map[6:9])
                x += 5

            if key == 276:
                choice = random.choice(croc_map[9:12])
                x -= 5

        if x > 600: x = 20
        if y > 440: y = 20
        if x < 20: x = 600
        if y < 20: y = 440

        screen.fill((200,200,200))

        for cat in cats:
            a = pygame.Rect(cat, cat_img.get_size())
            b = pygame.Rect((x,y), choice[2:])

            if b.colliderect(a):
                score += 1
                cats.remove(cat)
            else:
                screen.blit(cat_img, cat)

        if len(cats) < 10:
            cats.append(generate_cat())

        screen.blit(croc_img, (x,y), choice)
        screen.blit(show_score(mono, score), (10,10))
        pygame.display.flip()

if __name__ == '__main__':
    main()
