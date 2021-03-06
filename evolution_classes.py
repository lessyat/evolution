import os

import pygame
import random
from config import *


main_dir = os.path.split(os.path.abspath(__file__))[0]


class Creature(pygame.sprite.Sprite):
    def __init__(self, day):
        super().__init__()
        self.replication_rate = 0
        self.death_rate = 0
        self.birthday = day


    def replicate(self, day):
        if random.random() < self.replication_rate:
            return Creature(day=day)
        return None


class World:
    def __init__(self):
        self.birth_rate_nusha = NUSHA_B
        self.birth_rate_kopatich = KOPATICH_B
        self.creatures = []
        self.days = 0
        self.creatures_group = pygame.sprite.Group()
        self.init_birth()

    def init_birth(self):
        for _ in range(NUSHA_I):
            new_creature = Nusha(day=self.days)
            self.creatures.append(new_creature)
            self.creatures_group.add(new_creature)
        for _ in range(KOPATICH_I):
            new_creature = Kopatich(day=self.days)
            self.creatures.append(new_creature)
            self.creatures_group.add(new_creature)

    def spontaneous_birth(self):
        if random.random() < self.birth_rate_nusha:
            new_creature = Nusha(day=self.days)
            self.creatures.append(new_creature)
            self.creatures_group.add(new_creature)
        if random.random() < self.birth_rate_kopatich:
            new_creature = Kopatich(day=self.days)
            self.creatures.append(new_creature)
            self.creatures_group.add(new_creature)

    def death(self):
        for creature in self.creatures:
            if random.random() < creature.death_rate + len(self.creatures)*COMPETITION_COEF:
                self.creatures.remove(creature)
                creature.kill()

    def replication(self):
        for creature in self.creatures:
            new_creature = creature.replicate(day=self.days)
            if new_creature is not None:
                self.creatures.append(new_creature)
                self.creatures_group.add(new_creature)

    def evolve(self):
        self.days += 1
        self.spontaneous_birth()
        self.death()
        self.replication()


class Nusha(Creature):
    def __init__(self, day):
        super().__init__(day)
        self.death_rate = NUSHA_D
        self.replication_rate = NUSHA_R
        self.mutation_rate = NUSHA_M_KOPATICH
        self.image = load_image('nusha.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREENRECT.width-self.rect.width)
        self.rect.y = random.randint(0, SCREENRECT.height-self.rect.height)

    def replicate(self, day):
        if random.random() < self.replication_rate:
            if random.random() < self.mutation_rate:
                return Kopatich(day=day)
            return Nusha(day=day)
        return None


class Kopatich(Creature):
    def __init__(self, day):
        super().__init__(day)
        self.death_rate = KOPATICH_D
        self.replication_rate = KOPATICH_R
        self.mutation_rate = KOPATICH_M_SOVA
        self.image = load_image('kopatich.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREENRECT.width-self.rect.width)
        self.rect.y = random.randint(0, SCREENRECT.height-self.rect.height)

    def replicate(self, day):
        if random.random() < self.replication_rate:
            if random.random() < self.mutation_rate:
                return Sova(day=day)
            return Kopatich(day=day)
        return None


class Sova(Creature):
    def __init__(self, day):
        super().__init__(day)
        self.death_rate = SOVA_D
        self.replication_rate = SOVA_R
        self.image = load_image('sova.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREENRECT.width-self.rect.width)
        self.rect.y = random.randint(0, SCREENRECT.height-self.rect.height)

    def replicate(self, day):
        if random.random() < self.replication_rate:
            return Sova(day=day)
        return None


def load_image(file):
    file = os.path.join(main_dir, 'data', file)
    image = pygame.image.load(file)
    image = image.convert_alpha()
    return image





