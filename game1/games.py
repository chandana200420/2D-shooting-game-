import pygame

pygame.init()

# Set up display
win = pygame.display.set_mode((500, 480))
pygame.display.set_caption("TRIAL")

# Load images
walkRight = [pygame.image.load(f'R{i}.png') for i in range(1, 10)]
walkLeft = [pygame.image.load(f'L{i}.png') for i in range(1, 10)]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')

clock = pygame.time.Clock()
bulletsound = pygame.mixer.Sound('gun-shots6-times-fast-230509.mp3')
hitsound = pygame.mixer.Sound('bullet-hit-metal-84818.mp3')
music = pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)

score = 0
hit_count = 0  # Player collision counter

# Player class
class Player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isjump = False
        self.jumpcount = 10
        self.left = False
        self.right = False
        self.walkcount = 0
        self.walkRight = walkRight
        self.walkLeft = walkLeft
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

    def draw(self, win):
        if self.walkcount + 1 >= 27:
            self.walkcount = 0

        if not self.standing:
            if self.left:
                win.blit(self.walkLeft[self.walkcount // 3], (self.x, self.y))
                self.walkcount += 1
            elif self.right:
                win.blit(self.walkRight[self.walkcount // 3], (self.x, self.y))
                self.walkcount += 1
        else:
            if self.right:
                win.blit(self.walkRight[0], (self.x, self.y))
            else:
                win.blit(self.walkLeft[0], (self.x, self.y))

        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

    def hit(self):
        global hit_count
        hit_count += 1
        self.isjump = False
        self.jumpcount = 10
        self.x = 60
        self.y = 410
        self.walkcount = 0
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('-5', 1, (255, 0, 0))
        win.blit(text, (250 - text.get_width() / 2, 200))
        pygame.display.update()
        i = 0
        while i < 300:
            pygame.time.delay(5)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

# Projectile class
class Projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

# Enemy class
class Enemy(object):
    walkRight = [pygame.image.load(f'R{i}E.png') for i in range(1, 12)]
    walkLeft = [pygame.image.load(f'L{i}E.png') for i in range(1, 12)]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.path = [x, end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10
        self.visible = True

    def draw(self, win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

            # Health bar
            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))

            self.hitbox = (self.x + 17, self.y + 2, 31, 57)

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel *= -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel *= -1
                self.walkCount = 0

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
        print('Enemy hit!')

# Redraw window
def redrawGameWindow():
    win.blit(bg, (0, 0))
    text = font.render('Score: ' + str(score), 1, (0, 0, 0))
    win.blit(text, (350, 10))
    man.draw(win)
    globin.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()

# Game variables
man = Player(300, 410, 64, 64)
globin = Enemy(100, 410, 64, 64, 300)
bullets = []
shootLoop = 0
font = pygame.font.SysFont('Comic Sans MS', 30, True)

# Main game loop
run = True
while run:
    clock.tick(27)

    if globin.visible:
        if man.hitbox[1] < globin.hitbox[1] + globin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > globin.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > globin.hitbox[0] and man.hitbox[0] < globin.hitbox[0] + globin.hitbox[2]:
                man.hit()
                score -= 5
                bullets.clear()

    if hit_count >= 2:
        win.blit(bg, (0, 0))
        text = font.render("You Lost! Enemy Won!", 1, (255, 0, 0))
        win.blit(text, (100, 200))
        pygame.display.update()
        pygame.time.delay(3000)
        run = False

    if not globin.visible:
        win.blit(bg, (0, 0))
        text = font.render("wow You Won!!!", 1, (0, 34, 0))
        win.blit(text, (200, 200))
        pygame.display.update()
        pygame.time.delay(3000)
        run = False

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if globin.visible:
            if bullet.y - bullet.radius < globin.hitbox[1] + globin.hitbox[3] and bullet.y + bullet.radius > globin.hitbox[1]:
                if bullet.x + bullet.radius > globin.hitbox[0] and bullet.x - bullet.radius < globin.hitbox[0] + globin.hitbox[2]:
                    hitsound.play()
                    globin.hit()
                    score += 1
                    bullets.remove(bullet)

        if 0 < bullet.x < 500:
            bullet.x += bullet.vel
        else:
            bullets.remove(bullet)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootLoop == 0:
        bulletsound.play()
        facing = -1 if man.left else 1
        if len(bullets) < 5:
            bullets.append(Projectile(round(man.x + man.width // 2), round(man.y + man.height // 2), 6, (255, 0, 0), facing))
        shootLoop = 1

    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < 500 - man.width - man.vel:
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    else:
        man.standing = True
        man.walkcount = 0

    if not man.isjump:
        if keys[pygame.K_UP]:
            man.isjump = True
            if keys[pygame.K_LEFT]:
                man.left = True
                man.right = False
            elif keys[pygame.K_RIGHT]:
                man.left = False
                man.right = True
            man.walkcount = 0
    else:
        if man.jumpcount >= -10:
            neg = 1
            if man.jumpcount < 0:
                neg = -1
            man.y -= (man.jumpcount ** 2) * 0.5 * neg
            man.jumpcount -= 1
        else:
            man.isjump = False
            man.jumpcount = 10

    redrawGameWindow()

pygame.quit()

