import pygame
import random

# Inicialização
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hit the Box")

# Cores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Fonte
font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 72)

# Paddle
paddle_width, paddle_height = 100, 20
paddle = pygame.Rect(WIDTH // 2 - paddle_width // 2, HEIGHT - 40, paddle_width, paddle_height)

# Bola
ball_radius = 10
ball = pygame.Rect(WIDTH // 2 - ball_radius, HEIGHT // 2 - ball_radius, ball_radius * 2, ball_radius * 2)
ball_speed_x, ball_speed_y = 6, -6  # Velocidade aumentada

# Caixas
box_width, box_height = 80, 30
boxes = []

# Variáveis do jogo
score = 0
phase = 1
game_state = "menu"

def create_boxes():
    global boxes
    boxes = []
    for _ in range(4 * phase):
        while True:
            x = random.randint(0, WIDTH - box_width)
            y = random.randint(50, HEIGHT // 2)
            new_box = pygame.Rect(x, y, box_width, box_height)
            if not any(new_box.colliderect(box) for box in boxes):
                boxes.append(new_box)
                break

def draw_menu():
    screen.fill(RED)
    title = title_font.render("Hit the Box", True, WHITE)
    play_button = font.render("PLAY", True, BLACK)
    button_rect = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 50, 150, 60)
    
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))
    pygame.draw.rect(screen, WHITE, button_rect)
    screen.blit(play_button, (WIDTH // 2 - play_button.get_width() // 2, HEIGHT // 2 + 65))
    
    return button_rect

def draw_game():
    screen.fill(RED)
    pygame.draw.rect(screen, WHITE, paddle)
    pygame.draw.ellipse(screen, BLACK, ball)
    for box in boxes:
        pygame.draw.rect(screen, GREEN, box)
    
    score_text = font.render(f"Pontos: {score}", True, WHITE)
    phase_text = font.render(f"Fase: {phase}", True, WHITE)
    
    screen.blit(score_text, (10, 10))
    screen.blit(phase_text, (WIDTH - 100, 10))

def draw_game_over():
    screen.fill(BLACK)
    game_over_text = title_font.render("Game Over", True, WHITE)
    score_text = font.render(f"Pontuação: {score}", True, WHITE)
    play_again_button = font.render("Jogar Novamente", True, BLACK)
    button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 60)
    
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    pygame.draw.rect(screen, WHITE, button_rect)
    screen.blit(play_again_button, (WIDTH // 2 - play_again_button.get_width() // 2, HEIGHT // 2 + 65))
    
    return button_rect

running = True
clock = pygame.time.Clock()

create_boxes()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "menu" and play_button_rect.collidepoint(event.pos):
                game_state = "playing"
            elif game_state == "game_over" and play_again_button_rect.collidepoint(event.pos):
                game_state = "playing"
                score = 0
                phase = 1
                create_boxes()
                ball.center = (WIDTH // 2, HEIGHT // 2)
    
    if game_state == "menu":
        play_button_rect = draw_menu()
    elif game_state == "playing":
        paddle.centerx = pygame.mouse.get_pos()[0]
        paddle.clamp_ip(screen.get_rect())
        
        ball.x += ball_speed_x
        ball.y += ball_speed_y
        
        if ball.left <= 0 or ball.right >= WIDTH:
            ball_speed_x = -ball_speed_x
        if ball.top <= 0:
            ball_speed_y = -ball_speed_y
        
        if ball.colliderect(paddle):
            ball_speed_y = -ball_speed_y
        
        for box in boxes[:]:
            if ball.colliderect(box):
                boxes.remove(box)
                ball_speed_y = -ball_speed_y
                score += 1
        
        if len(boxes) == 0:
            phase += 1
            create_boxes()
        
        if ball.bottom >= HEIGHT:
            game_state = "game_over"
        
        draw_game()
    elif game_state == "game_over":
        play_again_button_rect = draw_game_over()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
