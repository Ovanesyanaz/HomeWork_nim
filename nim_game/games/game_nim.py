import json

from nim_game.common.enumerations import Players
from nim_game.environments.environment_nim import EnvironmentNim
from nim_game.common.models import NimStateChange, GameState
from nim_game.agents.agent import Agent


class GameNim:
    _environment: EnvironmentNim        # состояния кучек
    _agent: Agent                       # бот

    def __init__(self, path_to_config: str) -> None:
        game = load_file(path_to_config)
        self._environment = EnvironmentNim(game["heaps_amount"])
        self._agent = Agent(game["opponent_level"])

    def make_steps(self, player_step: NimStateChange) -> GameState:
        """
        Изменение среды ходом игрока + ход бота

        :param player_step: изменение состояния кучек игроком
        """
        Game_state = GameState()
        self._environment.change_state(player_step)
        Game_state.heaps_state = self.heaps_state
        Game_state.opponent_step = player_step

        if self.is_game_finished():
            Game_state.winner = Players.USER

        agent_step = self._agent.make_step(self.heaps_state)
        self._environment.change_state(agent_step)
        Game_state.heaps_state = self.heaps_state
        Game_state.opponent_step = agent_step

        if self.is_game_finished():
            Game_state.winner = Players.BOT

        return Game_state

    def is_game_finished(self) -> bool:
        """
        Проверить, завершилась ли игра, или нет

        :return: True - игра окончена, False - иначе
        """
        return sum(self.heaps_state) == 0

    @property
    def heaps_state(self) -> list[int]:
        return self._environment.get_state()


def load_file(path: str) -> dict:
    try:
        with open(path) as file:
            res = json.load(file)
    except FileNotFoundError:
        raise ("invalid path")
    return res
