from random import choice, randint

from nim_game.common.enumerations import AgentLevels
from nim_game.common.models import NimStateChange


class Agent:
    """
    В этом классе реализованы стратегии игры для уровней сложности
    """

    _level: AgentLevels         # уровень сложности

    def __init__(self, level: str) -> None:
        if not (isinstance(level, str)) or \
                not (level in [item.value for item in AgentLevels]):
            raise ValueError
        self._level = level

    def make_step(self, state_curr: list[int]) -> NimStateChange:
        """
        Сделать шаг, соотвутствующий уровню сложности

        :param state_curr: список целых чисел - состояние кучек
        :return: стуктуру NimStateChange - описание хода
        """
        return {
            self._level == AgentLevels.EASY: simple_step(state_curr),
            self._level == AgentLevels.NORMAL:  usual_step(state_curr),
            self._level == AgentLevels.HARD:  smart_step(state_curr)
        }[False]


def nim_sum(state_curr: list[int]) -> int:
    ret = state_curr[0]
    for i in range(1, len(state_curr)):
        ret ^= state_curr[i]
    return ret


def simple_step(state_curr: list[int]) -> NimStateChange:
    valid_id = choice([i for i in range(len(state_curr))
                       if state_curr[i] != 0])
    decrease = randint(1, state_curr[valid_id])
    return NimStateChange(valid_id, decrease)


def usual_step(state_curr: list[int]) -> NimStateChange:
    return choice([simple_step(state_curr), smart_step(state_curr)])


def smart_step(state_curr: list[int]) -> NimStateChange:
    for i in range(len(state_curr)):
        buf = nim_sum(state_curr) ^ state_curr[i]
        if (buf) < state_curr[i]:
            return NimStateChange(i, state_curr[i] - (buf))
    return simple_step(state_curr)
