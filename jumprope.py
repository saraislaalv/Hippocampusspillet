from constants import *
from main import *


class JumpingRopeGame(MiniGame):
    def __init__(self):
        super().__init__()
        self.player = PlayerRope(WIDTH // 2 - 50, HEIGHT - 220, 80, 110, RED)
        self.rope = Rope(WIDTH//2, HEIGHT//2, 10, BLUE)
        self.running = True  # Definer running-variabelen her
        self.jump_over_rope = False
        self.countdown_timer = 3

    def redraw_window(self, player, rope):
        screen.blit(self.background_img, (0, 0))
        screen.blit(player_img, (self.player.x, self.player.y))  # Tegn playeren som seahorse.png
        pg.draw.circle(screen, self.rope.color, (self.rope.x, self.rope.y), self.rope.radius)
        score_text = font.render(f"Poengsum: {self.score}", True, RED)
        screen.blit(score_text, (10, 90))
        self.home_button.draw()

    def run(self):
        run = True
        
        countdown_font = pg.font.SysFont("Verdana", 150)
        
        while self.countdown_timer > 0:
            screen.blit(self.background_img, (0, 0))
            countdown_text = countdown_font.render(f"{self.countdown_timer}", True, BLUE)
            screen.blit(countdown_text, (WIDTH // 2 - countdown_text.get_width() // 2, HEIGHT // 2 - countdown_text.get_height() // 2))
            pg.display.flip()
            pg.time.delay(1000) # Vent i 1 sekund
            self.countdown_timer -= 1
        
        while self.running:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False  
            keys = pg.key.get_pressed()
            if keys[pg.K_LEFT] and self.player.x > self.player.vel:
                self.player.x -= self.player.vel
            if keys[pg.K_RIGHT] and self.player.x < WIDTH - self.player.width - self.player.vel:
                self.player.x += self.player.vel
            # jump hvis mellomromstasten trykkes og playeren ikke allerede jumper
            if not self.player.isJumping:
                if keys[pg.K_SPACE]:
                    self.player.isJumping = True
            else:
                # Utfør jump
                if self.player.speed >= -10:
                    neg = 1
                    if self.player.speed < 0:
                        neg = -1
                    self.player.y -= (self.player.speed ** 2) * 0.5 * neg
                    self.player.speed -= 1
                else:
                    self.player.isJumping = False
                    self.player.speed = 10

            self.rope.update()  # Oppdater tauets posisjon

            # Sjekk om playeren jumper over tauet og legg til poeng
            if self.player.y < self.rope.y and self.rope.x - self.rope.radius < self.player.x < self.rope.x + self.rope.radius * 2 and not self.jump_over_rope:
                self.score += 1
                self.jump_over_rope = True
            elif self.player.y >= self.rope.y:
                self.jump_over_rope = False

            # Sjekk om playeren og tauet kolliderer og avslutt spillet
            self.player_rect = pg.Rect(self.player.x, self.player.y, self.player.width, self.player.height)
            self.rope_rect = pg.Rect(self.rope.x - self.rope.radius, self.rope.y - self.rope.radius, 2 * self.rope.radius, 2 * self.rope.radius)
            if self.player_rect.colliderect(self.rope_rect):
                return self.score
                
            self.redraw_window(self.player, self.rope)  # Tegn spillet

            pg.display.flip()

        return self.score  # Returner self.score når løkken er ferdig

class PlayerRope:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.vel = 5
        self.isJumping = False
        self.speed = 10

class Rope:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius  # Tauets radius
        self.color = color
        self.angle = -math.pi/1  # Startvinkel for tauet (endret til negativ verdi)
        self.angular_speed = 0.08  # Hastighet for svinging av tauet
        self.radius_multiplier = 1.15  # Multiplikator for å endre tauets lengde

    def update(self):
        self.angle += self.angular_speed  # Oppdater vinkelen til tauet
        self.angular_speed += 0.00005  # Øk svinghastigheten litt for hver oppdatering
        # Beregn nye koordinater for tauet basert på vinkelen og multiplikatoren
        self.x = int(WIDTH // 2 + math.cos(self.angle) * (WIDTH // 4) * self.radius_multiplier)
        self.y = int(HEIGHT // 2 + math.sin(self.angle) * (HEIGHT // 4) * self.radius_multiplier)

    def draw(self):
        # Tegn tauet som en sirkel
        pg.draw.circle(self.color, (self.x, self.y), self.radius)
        
