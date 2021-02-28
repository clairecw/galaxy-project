import pygame as pg
import fam_feud as ff


COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
FONT = pg.font.Font(None, 32)
WHITE = (255, 255, 255)
GREEN = (78, 255, 87)
YELLOW = (241, 255, 0)
BLUE = (80, 255, 239)
PURPLE = (203, 0, 255)
RED = (237, 28, 36)

class TextBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = pg.font.Font(None, 20).render(text, True, self.color)
        self.active = False

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        ans = ''
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    # print(self.text)
                    ans = self.text
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)
        return ans

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)



def main():
    pg.init()
    screen = pg.display.set_mode((640, 480))
    clock = pg.time.Clock()
    input_box1 = InputBox(100, 100, 140, 32)
    input_boxes = [input_box1]
    bar_obj = Bar(screen)
    bar = pygame.sprite.GroupSingle(bar_obj)
    
    done = False
    feud = ff.FamFeud()
    idx, qn = feud.draw_next_q()
    lastscoreText = TextBox(200, 50, 140, 32, text="")

    while not done:
        titleText = TextBox(20, 50, 140, 32, text=qn)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            for box in input_boxes:
                ans = box.handle_event(event)
                if ans:
                    score, sols = feud.score_ans(idx, ans)
                    lastscoreText = TextBox(400, 5, 140, 32, text=str(score))
                    idx, qn = feud.draw_next_q()
                    titleText = TextBox(20, 50, 140, 32, text=qn)



        for box in input_boxes:
            box.update()

        screen.fill((30, 30, 30))
        for box in input_boxes:
            box.draw(screen)
        titleText.draw(screen)
        lastscoreText.draw(screen)

        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    main()
    pg.quit()
