from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, ColorProperty, StringProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint
from kivy.core.window import Window

# Classe da Bola
class PongBall(Widget):
    # Velocidade horizontal e vertical da bola
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    # Junta as duas velocidades num vetor
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    # Cor da bola (RGBA) — começa branca
    color = ColorProperty([1, 1, 1, 1])

    # Função que move a bola com base na velocidade
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

    # Quando a bola colide com a raquete
    def bounce_paddle(self, paddle):
        self.velocity_x *= -1.1  # inverte e acelera no eixo X
        self.velocity_y += paddle.velocity_y / 2  # afeta Y com base na raquete
        self.color = [1, 0, 0, 1]  # muda a cor pra vermelho
        # Volta à cor original depois de 0.5s
        Clock.schedule_once(lambda dt: self.reset_color(), 0.5)

    # Reseta a cor para branco
    def reset_color(self, *args):
        self.color = [1, 1, 1, 1]

# Classe da Raquete
class PongPaddle(Widget):
    # Pontuação do jogador
    score = NumericProperty(0)
    # Velocidade vertical da raquete
    velocity_y = NumericProperty(0)

    # Verifica colisão com a bola
    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            ball.bounce_paddle(self)

# Classe principal do jogo
class PongGame(Widget):
    # Texto que mostra o vencedor
    winner_text = StringProperty("")
    # Referências à bola e raquetes (ligadas pelo .kv)
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(PongGame, self).__init__(**kwargs)
        # Conecta as teclas do teclado
        Window.bind(on_key_down=self._on_key_down)
        Window.bind(on_key_up=self._on_key_up)
        # Guarda as teclas pressionadas
        self.keys_pressed = set()

    # Quando tecla pressionada
    def _on_key_down(self, window, key, scancode, codepoint, modifiers):
        self.keys_pressed.add(key)

    # Quando tecla solta
    def _on_key_up(self, window, key, *args):
        self.keys_pressed.discard(key)

    # Inicia a bola no centro com velocidade aleatória
    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = Vector(vel[0], vel[1]).rotate(randint(0, 360))

    # Atualiza o jogo (movimento da bola, raquetes, colisões, pontuação)
    def update(self, dt):
        # Se já tem vencedor, para o jogo
        if self.winner_text:
            return

        # Move a bola
        self.ball.move()

        # Zera velocidades verticais das raquetes para atualizar depois
        self.player1.velocity_y = 0
        self.player2.velocity_y = 0

        # Controles do Jogador 1 (W = 119, S = 115)
        if 119 in self.keys_pressed:
            self.player1.center_y += 10
            self.player1.velocity_y = 10
        if 115 in self.keys_pressed:
            self.player1.center_y -= 10
            self.player1.velocity_y = -10

        # Controles do Jogador 2 (setas cima = 273, baixo = 274)
        if 273 in self.keys_pressed:
            self.player2.center_y += 10
            self.player2.velocity_y = 10
        if 274 in self.keys_pressed:
            self.player2.center_y -= 10
            self.player2.velocity_y = -10

        # Rebote da bola nas bordas superior e inferior
        if self.ball.y < 0 or self.ball.top > self.height:
            self.ball.velocity_y *= -1

        # Rebote da bola nas raquetes
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # Atualiza pontuação e reinicia bola se passar da borda
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(4, 0))
        elif self.ball.right > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))

        # Verifica vitória (5 pontos)
        if self.player1.score >= 5 or self.player2.score >= 5:
            winner = "Jogador 1" if self.player1.score >= 5 else "Jogador 2"
            self.winner_text = f"{winner} ganhou!!"
            self.ball.velocity = (0, 0)

# Classe principal da aplicação Kivy
class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        # Atualiza o jogo 60 vezes por segundo para fluidez
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game

# Executa o app
if __name__ == '__main__':
    PongApp().run()
