import pygame
import random
import asyncio
import platform

# Game constants
GRID_WIDTH, GRID_HEIGHT = 10, 20
BLOCK_SIZE = 30
FPS = 60

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]]   # Z
]

COLORS = [
    (0, 255, 255),  # Cyan (I)
    (255, 255, 0),  # Yellow (O)
    (128, 0, 128),  # Purple (T)
    (255, 165, 0),  # Orange (L)
    (0, 0, 255),    # Blue (J)
    (0, 255, 0),    # Green (S)
    (255, 0, 0)     # Red (Z)
]

class Tetris:
    def __init__(self):
        self.grid = [[(0, 0, 0) for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.score = 0
        self.game_over = False

    def new_piece(self):
        shape = random.choice(SHAPES)
        color = COLORS[SHAPES.index(shape)]
        return {"shape": shape, "color": color, "x": GRID_WIDTH // 2 - len(shape[0]) // 2, "y": 0}

    def move(self, dx, dy):
        if not self.collision(self.current_piece, dx, dy):
            self.current_piece["x"] += dx
            self.current_piece["y"] += dy
            return True
        return False

    def rotate(self):
        shape = self.current_piece["shape"]
        new_shape = [[shape[y][x] for y in range(len(shape))] for x in range(len(shape[0]) - 1, -1, -1)]
        if not self.collision({"shape": new_shape, "x": self.current_piece["x"], "y": self.current_piece["y"]}):
            self.current_piece["shape"] = new_shape
            return True
        return False

    def collision(self, piece, dx=0, dy=0):
        for y, row in enumerate(piece["shape"]):
            for x, cell in enumerate(row):
                if cell:
                    new_x, new_y = piece["x"] + x + dx, piece["y"] + y + dy
                    if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT or (new_y >= 0 and self.grid[new_y][new_x] != (0, 0, 0)):
                        return True
        return False

    def merge(self):
        for y, row in enumerate(self.current_piece["shape"]):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[self.current_piece["y"] + y][self.current_piece["x"] + x] = self.current_piece["color"]

    def clear_lines(self):
        lines_cleared = 0
        for y in range(GRID_HEIGHT - 1, -1, -1):
            if all(self.grid[y]):
                self.grid.pop(y)
                self.grid.insert(0, [(0, 0, 0) for _ in range(GRID_WIDTH)])
                lines_cleared += 1
        self.score += lines_cleared * 100

    def update(self):
        if not self.move(0, 1):
            self.merge()
            self.clear_lines()
            self.current_piece = self.new_piece()
            if self.collision(self.current_piece):
                self.game_over = True

    def draw(self, screen):
        for y, row in enumerate(self.grid):
            for x, color in enumerate(row):
                if color != (0, 0, 0):
                    pygame.draw.rect(screen, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(screen, (255, 255, 255), (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)
        for y, row in enumerate(self.current_piece["shape"]):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, self.current_piece["color"], 
                                     ((self.current_piece["x"] + x) * BLOCK_SIZE, (self.current_piece["y"] + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(screen, (255, 255, 255), 
                                     ((self.current_piece["x"] + x) * BLOCK_SIZE, (self.current_piece["y"] + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

async def main():
    pygame.init()
    screen = pygame.display.set_mode((GRID_WIDTH * BLOCK_SIZE, GRID_HEIGHT * BLOCK_SIZE))
    clock = pygame.time.Clock()
    game = Tetris()

    while not game.game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move(-1, 0)
                if event.key == pygame.K_RIGHT:
                    game.move(1, 0)
                if event.key == pygame.K_DOWN:
                    game.move(0, 1)
                if event.key == pygame.K_UP:
                    game.rotate()

        game.update()
        screen.fill((0, 0, 0))
        game.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(1.0 / FPS)

    pygame.quit()

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())
