## WeirdLand - an arcade shooting game.
## Copyright (c) 2021 moonburnt
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see https://www.gnu.org/licenses/gpl-3.0.txt

from Game.main import make_game
import argparse
import logging

log = logging.getLogger()
log.setLevel(logging.INFO)
formatter = logging.Formatter(
    fmt="[%(asctime)s][%(name)s][%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
log.addHandler(handler)

ap = argparse.ArgumentParser()
ap.add_argument(
    "--debug",
    action="store_true",
    help="Adds debug messages to log output",
)
args = ap.parse_args()

if args.debug:
    log.setLevel(logging.DEBUG)

game = make_game()
log.info("Running the game")
try:
    game.run()
except KeyboardInterrupt:
    game.exit()
    # continue
# except Exception as e:
#    log.critical(e)
#    exit(2)
