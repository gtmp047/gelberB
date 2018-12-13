#!/usr/bin/env python3
import hlt
from hlt import constants
from hlt.positionals import Direction
import random
import logging

""" <<<Game Begin>>> """
game = hlt.Game()
all_cells_collection = [hlt.Position(i, y) for i in range(game.game_map.width) for y in range(game.game_map.height)]
game.ready("simple_rad_v1")
logging.info("Successfully created bot! My Player ID is {}.".format(game.my_id))
""" <<<Game Loop>>> """

while True:
    game.update_frame()
    me = game.me
    game_map = game.game_map
    halite_map = {cell: game_map[cell].halite_amount for cell in all_cells_collection}
    # logging.info("{}.".format(all_cells_collection))
    # logging.info("{}.".format(halite_map))

    command_queue = []
    direction_order = [Direction.North, Direction.South, Direction.East, Direction.West, Direction.Still]
    for ship in me.get_ships():

        position_options = ship.position.get_surrounding_cardinals() + [ship.position]

        position_dict = {}
        halite_dict = {}

        for n, direction in enumerate(direction_order):
            position_dict[direction] = position_options[n]

        for direction in position_dict:
            position = position_dict[direction]
            halite_dict[position] = game_map[position].halite_amount


        logging.info("{}.".format(position_options))
        logging.info("{}.".format(halite_dict))

        if game_map[ship.position].halite_amount < constants.MAX_HALITE / 10 or ship.is_full:
            command_queue.append(
                ship.move(
                    random.choice([Direction.North, Direction.South, Direction.East, Direction.West])))
        else:
            command_queue.append(ship.stay_still())

    if game.turn_number <= 200 and me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_occupied:
        command_queue.append(me.shipyard.spawn())

    game.end_turn(command_queue)
