import pygame


class EditableGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def manage_click(self, event):
        for s in self.sprites():
            s.selected = False
            if s.rect.collidepoint(event.pos):
                s.selected = True

    def manage_key(self, event):
        for s in self.sprites():
            if s.selected:
                if event.key == pygame.K_BACKSPACE:
                    s.text = s.text[:-1]
                elif event.unicode.isalnum():
                    s.text += event.unicode
