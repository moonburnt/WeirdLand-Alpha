import logging

log = logging.getLogger(__name__)

# Disabling the annoying pygame's greeter. Nothing personal, but it should be
# done out of box, with just engine's version being sent to logging module, Imho
from os import environ

environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
