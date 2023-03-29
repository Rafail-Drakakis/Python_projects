import pygame

#pong_game.py
def init_pong_game():
    pygame.init()
    screen_size = (400, 300)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Pong")
    return screen

def handle_events(paddle_1_position, paddle_2_position):
    paddle_speed = 40
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, paddle_1_position, paddle_2_position
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                paddle_1_position = max(0, paddle_1_position - paddle_speed)
            elif event.key == pygame.K_s:
                paddle_1_position = min(300, paddle_1_position + paddle_speed)
            elif event.key == pygame.K_UP:
                paddle_2_position = max(0, paddle_2_position - paddle_speed)
            elif event.key == pygame.K_DOWN:
                paddle_2_position = min(300, paddle_2_position + paddle_speed)
    return True, paddle_1_position, paddle_2_position

def update_ball_position(ball_position, ball_speed):
    ball_position[0] += ball_speed[0]
    ball_position[1] += ball_speed[1]
    return ball_position

def check_ball_collision(ball_position, ball_speed, paddle_1_position, paddle_2_position):
    if ball_position[1] < 0 or ball_position[1] > 300:
        ball_speed[1] = -ball_speed[1]
    if ball_position[0] < 0:
        ball_speed[0] = -ball_speed[0]
        ball_position[0] = 200
        ball_position[1] = 150
    elif ball_position[0] > 400:
        ball_speed[0] = -ball_speed[0]
        ball_position[0] = 200
        ball_position[1] = 150

    if ball_position[0] < 25 and ball_position[1] > paddle_1_position - 50 and ball_position[1] < paddle_1_position + 50:
        ball_speed[0] = -ball_speed[0]
        ball_position[0] = 25
    elif ball_position[0] > 375 and ball_position[1] > paddle_2_position - 50 and ball_position[1] < paddle_2_position + 50:
        ball_speed[0] = -ball_speed[0]
        ball_position[0] = 375

    return ball_position, ball_speed

def draw_objects(screen, ball_position, paddle_1_position, paddle_2_position):
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(0, paddle_1_position - 50, 25, 100))
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(375, paddle_2_position - 50, 25, 100))
    pygame.draw.circle(screen, (255, 255, 255), ball_position, 10)
    pygame.display.flip()

def pong_game():
    pygame.init()
    screen_size = (400, 300)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Pong")

    ball_speed = [2, 2]
    ball_position = [200, 150]
    paddle_1_position = 150
    paddle_2_position = 150

    running = True
    while running:
        running, paddle_1_position, paddle_2_position = handle_events(paddle_1_position, paddle_2_position)
        ball_position = update_ball_position(ball_position, ball_speed)
        ball_position, ball_speed = check_ball_collision(ball_position, ball_speed, paddle_1_position, paddle_2_position)
        draw_objects(screen, ball_position, paddle_1_position, paddle_2_position)
        pygame.time.delay(10)

    pygame.quit()
