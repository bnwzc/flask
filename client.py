import random
import pygame

from components import EditableGroup, TextBox
from api import post_score

API_TOKEN = "58c2096c4e7de7aee98a404d5fbd8eea"


def main():
    pygame.init()
    pygame.key.set_repeat(500, 50)
    window = pygame.display.set_mode((800, 600))

    score = TextBox((400, 150), "", id="score", color=(0, 0, 0), bgcolor=(150, 150, 150), font_size=96, center=True)
    score.rect.topleft = (200, 50)

    play = TextBox(
        (200, 80), "Play", id="play_button", color=(255, 255, 255), bgcolor=(0, 150, 0), font_size=24, center=True
    )
    play.rect.topleft = (300, 250)

    token = TextBox((600, 60), API_TOKEN, id="user_token", color=(255, 255, 255), bgcolor=(0, 0, 255), font_size=18)
    token.rect.topleft = (100, 400)

    submit = TextBox(
        (200, 80),
        "Submit score",
        id="submit_button",
        color=(255, 255, 255),
        bgcolor=(200, 0, 0),
        font_size=24,
        center=True,
    )
    submit.rect.topleft = (300, 480)

    group = EditableGroup()
    group.add(score)
    group.add(token)

    clock = pygame.time.Clock()

    running = True

    while running:
        clock.tick(60)
        window.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                if play.rect.collidepoint(event.pos):
                    score.text = str(random.randint(0, 10000))
                if submit.rect.collidepoint(event.pos):
                    post_score({"user_token": token.text, "score": score.text})
                group.manage_click(event)
            if event.type == pygame.KEYDOWN:
                group.manage_key(event)

        group.draw(window)
        window.blit(play.image, play.rect)
        window.blit(submit.image, submit.rect)
        pygame.display.update()


if __name__ == "__main__":
    main()
