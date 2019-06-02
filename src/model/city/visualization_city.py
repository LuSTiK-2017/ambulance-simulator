from abc import ABC, abstractmethod
from src.model.singleton import Singleton
import pygame


WINDOW_TITLE = "Ambulance Car On The City"
WIDTH = 800
HEIGHT = 608
FPS = 60

all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()


def load_level(name):
    fullname = 'img/' + name
    with open(fullname, 'r') as map_file:
        level_map = []
        for line in map_file:
            line = line.strip()
            level_map.append(line)

    return level_map


def draw_level(level_map):
    new_player, x, y = None, None, None
    for y in range(len(level_map)):
        for x in range(len(level_map[y])):
            if level_map[y][x] == "1":
                Tile('asphalt.png', x, y)
            elif level_map[y][x] == "0":
                Tile('grown.png', x, y)
            elif level_map[y][x] == "h":
                Tile('hospital.png', x, y)
            elif level_map[y][x] == "c":
                Tile('station.png', x, y)
            elif level_map[y][x] == "q":
                Tile('house.png', x, y)
            elif level_map[y][x] == "2":
                Tile('asphalt.png', x, y)
                new_player = Car(x, y)

    return new_player, x, y


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = load_image(tile_type)
        self.rect = self.image.get_rect().move(16 * pos_x, 16 * pos_y)

        self.add(tiles_group, all_sprites)


class Car(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()

        self.image = load_image('Ambulance.png')
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(16 * pos_x, 16 * pos_y)

        self.add(player_group, all_sprites)

    def move_up(self):
        self.image = load_image('Ambulance.png')
        self.rect = self.rect.move(0, -16)

    def move_down(self):
        self.image = load_image('Ambulance_down.png')
        self.rect = self.rect.move(0, +16)

    def move_left(self):
        self.image = load_image('Ambulance_left.png')
        self.rect = self.rect.move(-16, 0)

    def move_right(self):
        self.image = load_image('Ambulance_right.png')
        self.rect = self.rect.move(+16, 0)


class Drawer(ABC):
    def draw(self):
        pass


class Handler(ABC):
    def handle_events(self):
        pass


class Updater(ABC):
    def update(self):
        pass


class Game(Drawer, Handler, Updater):
    done = False
    color_bg = pygame.Color('darkgrey')

    @abstractmethod
    def main_loop(self):
        pass


class VisualCity(Game, Singleton):
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()

        self.player, self.level_x, self.level_y = draw_level(load_level("city_matrix.txt"))

    def main_loop(self):
        while not self.done:
            self.handle_events()
            self.update()
            self.draw()

    def draw(self):
        tiles_group.draw(self.screen)
        player_group.draw(self.screen)

        pygame.display.flip()
        self.clock.tick(FPS)

    def update(self):
        pass

    def handle_events(self):
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                self.done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.done = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                self.player.move_up()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                self.player.move_down()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                self.player.move_left()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                self.player.move_right()


def load_image(name):
    fullname = 'img' + '/' + name
    try:
        if name[-2:] == 'jpg':
            image = pygame.image.load(fullname).convert()
        else:
            image = pygame.image.load(fullname).convert_alpha()
    except:
        print('Cannot load image', name)
        raise SystemExit()

    return image


if __name__ == "__main__":
    visual_city = VisualCity()
    visual_city.main_loop()
