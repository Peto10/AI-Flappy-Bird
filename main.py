import os
import threading
from typing import Deque

import neat
import neat.config
import neat.parallel
import pygame as pg

from game import Game, PILLAR_SPAWN_RATE
from player import Player
from pillar import Pillar, GAP_LENGTH

FPS = 48

def get_closest_pillar(player: Player, pillars: Deque[Pillar]) -> Pillar:
    closest_pillar = None
    for pillar in pillars:
        if pillar.top_pill.right > player.hitbox.left + player.hitbox.width * 0.25:
            if closest_pillar is None:
                closest_pillar = pillar
                continue
            if pillar.top_pill.right < closest_pillar.top_pill.right:
                closest_pillar = pillar
    return closest_pillar

def reset_game() -> None:
    game.pillars_q.clear()
    game.pillars_q.append(Pillar(game.screen))
    pg.time.set_timer(game.PILL_SPAWN_EVENT, PILLAR_SPAWN_RATE)

def calculate_distances(player: Player) -> int:
    pill = get_closest_pillar(player, game.pillars_q)
    return pill.top_pill.bottom + GAP_LENGTH / 2

def eval_genome(genome: neat.DefaultGenome, config: neat.config.Config) -> float:
    player = Player(game.screen)
    game.players.append(player)
    fitness = 0
    clock = pg.time.Clock()

    net = neat.nn.FeedForwardNetwork.create(genome, config)
    while not player.player_dead:
        fitness += .2
        mid = calculate_distances(player)
        output = net.activate((mid - player.hitbox.centery,))
        if output[0] < 0.5:
            player.jump()
        clock.tick(FPS)

    game.players.remove(player)

    if (len(game.players) == 0):
        reset_game()
    return fitness

def run_game_loop() -> None:
    clock = pg.time.Clock()
    while (game.game_step() and not game.game_stop):
        clock.tick(FPS)

def run(config_file: str) -> None:
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)
    p = neat.Population(config)
    game_thread = threading.Thread(target=run_game_loop)
    game_thread.start()

    pe = neat.ThreadedEvaluator(config.pop_size, eval_genome)
    p.run(pe.evaluate, 20)

    game.game_stop = True
    game_thread.join()

local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, 'config-feedforward')

pg.init()
game = Game()
run(config_path)
pg.quit()
