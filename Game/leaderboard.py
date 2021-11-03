import json
import logging

log = logging.getLogger(__name__)


class Leaderboard:
    def __init__(self, leaderboard: dict, path=None, sort: bool = True):
        if sort:
            for mode in leaderboard:
                leaderboard[mode]["entries"].sort(
                    key=(lambda x: x["score"]),
                    reverse=True,
                )
        self.lb = leaderboard
        self.path = path

    def __iter__(self):
        for var in self.lb:
            yield var

    def __getitem__(self, key):
        return self.lb[key]

    @classmethod
    def from_file(cls, path):
        with open(path, "r") as f:
            data = json.load(f)
        log.debug(f"Successfully loaded leaderboard from {path}")
        return cls(data, path=path)

    def to_file(self, path=None):
        path = path or self.path
        if not path:
            raise ValueError(f"excepted 'path' kwarg or 'self.path' to be not None")
        with open(path, "w") as f:
            json.dump(self.lb, f)
        log.debug(f"Successfully saved leaderboard into {path}")

    def add_entry(
        self,
        score: int,
        kills: int,
        mode: str,
        username: str = "player",
        limit: int = 5,
    ):
        if not mode in self.lb:
            self.lb[mode] = {}
            self.lb[mode]["slug"] = mode
            self.lb[mode]["entries"] = []
        board = self.lb[mode]["entries"]
        pos = 0
        if board:
            if score < board[-1]["score"]:
                log.debug("Score is less than worst recorded result, ignoring")
                return

            for num, item in enumerate(board):
                if item["score"] < score:
                    pos = num
                    break

        data = {}
        data["name"] = username
        data["score"] = score
        data["kills"] = kills

        board.insert(pos, data)
        board = board[:limit]
