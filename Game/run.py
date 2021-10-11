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
# except Exception as e:
#    log.critical(e)
#    exit(2)
