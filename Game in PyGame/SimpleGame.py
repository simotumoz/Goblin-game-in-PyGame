import pygame

pygame.init()

display_width = 1280
display_height = 720
win = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption("Goblin Game")

walk_right = [pygame.image.load('R%s.png' % frame) for frame in range(1, 10)]
walk_left = [pygame.image.load('L%s.png' % frame) for frame in range(1, 10)]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')

clock = pygame.time.Clock()
score = 0
number_of_rounds = 1


class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 3
        self.is_jump = False
        self.jump_count = 10
        self.left = False
        self.right = False
        self.walk_count = 0
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        self.health = 10
        self.visible = True

    def draw_character(self, win):

        if self.visible:
            if self.walk_count + 1 >= 27:
                self.walk_count = 0
            if not self.standing:
                if self.left:
                    win.blit(walk_left[self.walk_count // 3], (self.x, self.y))
                    self.walk_count += 1
                elif self.right:
                    win.blit(walk_right[self.walk_count // 3], (self.x, self.y))
                    self.walk_count += 1
            else:
                if self.right:
                    win.blit(walk_right[0], (self.x, self.y))
                else:
                    win.blit(walk_left[0], (self.x, self.y))

            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0, 0, 255), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))

            self.hitbox = (self.x + 17, self.y + 11, 29, 52)

        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def lose_message(self):
        font1 = pygame.font.SysFont('arial', 80)
        text = font1.render('YOU LOSE', 1, (255, 0, 0))
        win.blit(text, (600 - (text.get_width() / 2), 330))
        pygame.display.update()

    def hit(self):
        self.is_jump = False
        self.jump_count = 10
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
        print('player has been hit')

        # are resetting the player position
        self.x = 60
        self.y = 650
        self.walk_count = 0

        pygame.display.update()


class enemy(object):
    walk_right = [pygame.image.load('R%sE.png' % frame) for frame in range(1, 12)]
    walk_left = [pygame.image.load('L%sE.png' % frame) for frame in range(1, 12)]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.path = [x, end]  # starting and finishing pos of the enemy
        self.walk_count = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10
        self.visible = True

    def draw(self, win):
        self.move()
        if self.visible:
            if self.walk_count + 1 >= 33:
                self.walk_count = 0

            if self.vel > 0:
                win.blit(self.walk_right[self.walk_count // 3], (self.x, self.y))
                self.walk_count += 1
            else:
                win.blit(self.walk_left[self.walk_count // 3], (self.x, self.y))
                self.walk_count += 1

            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)

            # pygame.draw.rect(win, (255,0,0), self.hitbox,2)

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walk_count = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walk_count = 0

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
        print('enemy hit')


class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing  # 1 or -1
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


def redraw_game_window():
    win.blit(bg, (0, 0))
    text = font.render('Score: ' + str(score), 1, (0, 0, 0))
    round_text = font.render('Round #: ' + str(number_of_rounds), 1, (0, 0, 0))
    win.blit(text, (1100, 10))
    win.blit(round_text, (1100, 50))
    plyr.draw_character(win)
    gbln.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    for goblin in goblins:
        goblin.draw(win)
    pygame.display.update()


plyr = player(60, 650, 64, 64)  # player's x,y coordinates + sprites dimensions
# gbln = enemy(100, 655, 64, 64, 600)
goblins = [enemy(200, 655, 64, 64, 1280), enemy(250, 655, 64, 64, 1280), enemy(300, 655, 64, 64, 1280)]
shoot_loop = 0
bullets = []
run = True
font = pygame.font.SysFont('arial', 30, True)

# M A I N   L O O P
while run:
    frame_rate = 27
    clock.tick(frame_rate * 2)

    for gbln in goblins:
        if gbln.visible:
            if plyr.hitbox[1] < gbln.hitbox[1] + gbln.hitbox[3] and plyr.hitbox[1] + plyr.hitbox[3] > gbln.hitbox[1]:
                if plyr.hitbox[0] + plyr.hitbox[2] > gbln.hitbox[0] and plyr.hitbox[0] < gbln.hitbox[0] + gbln.hitbox[
                    2]:
                    plyr.hit()
                    score -= 1

            if gbln.health <= 0:
                goblins.remove(gbln)

            if len(goblins) == 0:
                number_of_rounds += 1
                goblins = [enemy(200, 655, 64, 64, 1280), enemy(250, 655, 64, 64, 1280), enemy(300, 655, 64, 64, 1280)]

        for bullet in bullets:

            if bullet.y - bullet.radius < gbln.hitbox[1] + gbln.hitbox[3] and bullet.y + bullet.radius > gbln.hitbox[1]:
                if bullet.x + bullet.radius > gbln.hitbox[0] and bullet.x - bullet.radius < gbln.hitbox[0] + \
                        gbln.hitbox[2]:
                    gbln.hit()
                    print(gbln.health)
                    score += 1
                    bullets.remove(bullet)

            if 1280 > bullet.x > 0:
                bullet.x += bullet.vel
            else:
                bullets.remove(bullet)

    if plyr.health <= 0:
        plyr.lose_message()
        pygame.time.delay(3000)
        run = False

    if shoot_loop > 0:
        shoot_loop += 1
    if shoot_loop > 3:
        shoot_loop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shoot_loop == 0:
        if plyr.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 5:
            bullets.append(
                projectile(round(plyr.x + plyr.width // 2), round(plyr.y + plyr.height // 2), 6, (173, 216, 230),
                           facing))
        shoot_loop = 1

    if keys[pygame.K_ESCAPE]:
        run = False

    if keys[pygame.K_LEFT] and plyr.x > plyr.vel:
        plyr.x -= plyr.vel
        plyr.left = True
        plyr.right = False
        plyr.standing = False
    elif keys[pygame.K_RIGHT] and plyr.x < display_width - plyr.width - plyr.vel:
        plyr.x += plyr.vel
        plyr.right = True
        plyr.left = False
        plyr.standing = False
    else:
        plyr.standing = True
        plyr.walk_count = 0

    if not plyr.is_jump:
        if keys[pygame.K_UP]:
            plyr.is_jump = True
            plyr.right = False
            plyr.left = False
            plyr.walk_count = 0

    else:
        if plyr.jump_count >= -10:
            neg = 1
            if plyr.jump_count < 0:
                neg = -1

            plyr.y -= (plyr.jump_count ** 2) * 0.5 * neg
            plyr.jump_count -= 1
        else:
            plyr.is_jump = False
            plyr.jump_count = 10

    redraw_game_window()

pygame.quit()
