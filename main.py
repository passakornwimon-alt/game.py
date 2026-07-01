import pygame
import random
import sys

pygame.init()

# ----------------------------
# Settings
# ----------------------------
WIDTH = 600
HEIGHT = 600
GRID = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

# Colors
BG = (25, 25, 35)
GRID_COLOR = (40, 40, 50)
SNAKE = (0, 220, 120)
HEAD = (0, 255, 180)
FOOD = (255, 80, 80)
TEXT = (255, 255, 255)

font = pygame.font.SysFont("Arial", 28)
big_font = pygame.font.SysFont("Arial", 60, bold=True)


def random_food(snake):
    while True:
        x = random.randrange(0, WIDTH, GRID)
        y = random.randrange(0, HEIGHT, GRID)
        if (x, y) not in snake:
            return (x, y)


def draw_grid():
    for x in range(0, WIDTH, GRID):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))


def reset_game():
    snake = [(300, 300)]
    direction = (GRID, 0)
    food = random_food(snake)
    score = 0
    return snake, direction, food, score


snake, direction, food, score = reset_game()

running = True
game_over = False

while running:

    clock.tick(10)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if game_over:
                if event.key == pygame.K_r:
                    snake, direction, food, score = reset_game()
                    game_over = False

            else:
                if event.key == pygame.K_UP and direction != (0, GRID):
                    direction = (0, -GRID)

                elif event.key == pygame.K_DOWN and direction != (0, -GRID):
                    direction = (0, GRID)

                elif event.key == pygame.K_LEFT and direction != (GRID, 0):
                    direction = (-GRID, 0)

                elif event.key == pygame.K_RIGHT and direction != (-GRID, 0):
                    direction = (GRID, 0)

    if not game_over:

        head_x = snake[0][0] + direction[0]
        head_y = snake[0][1] + direction[1]

        new_head = (head_x, head_y)

        # Wall collision
        if (
            head_x < 0
            or head_x >= WIDTH
            or head_y < 0
            or head_y >= HEIGHT
        ):
            game_over = True

        # Self collision
        elif new_head in snake:
            game_over = True

        else:
            snake.insert(0, new_head)

            if new_head == food:
                score += 1
                food = random_food(snake)
            else:
                snake.pop()

    # Draw
    screen.fill(BG)
    draw_grid()

    # Food
    pygame.draw.circle(
        screen,
        FOOD,
        (food[0] + GRID // 2, food[1] + GRID // 2),
        GRID // 2 - 2,
    )

    # Snake
    for i, segment in enumerate(snake):
        color = HEAD if i == 0 else SNAKE
        pygame.draw.rect(
            screen,
            color,
            (segment[0] + 1, segment[1] + 1, GRID - 2, GRID - 2),
            border_radius=5,
        )

    score_text = font.render(f"Score : {score}", True, TEXT)
    screen.blit(score_text, (10, 10))

    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        text = big_font.render("GAME OVER", True, (255, 70, 70))
        screen.blit(text, (110, 220))

        restart = font.render(
            "Press R to Restart",
            True,
            TEXT,
        )
        screen.blit(restart, (180, 310))

    pygame.display.flip()

pygame.quit()
sys.exit()