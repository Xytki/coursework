from typing import Optional

from unit import BaseUnit


class BaseSingleton(type):
    """base class"""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    """battlefield"""
    STAMINA_PER_ROUND: int = 1
    player = BaseUnit
    enemy = BaseUnit
    game_is_running: float = False

    def start_game(self, player: BaseUnit, enemy: BaseUnit) -> None:
        self.player = player
        self.enemy = enemy
        self.game_is_running = True

    def _check_players_hp(self) -> Optional[str]:
        """end of the battle"""
        if self.player.hp <= 0 and self.enemy.hp <= 0:
            self.battle_result = f'Ничья между {self.player.name} и {self.enemy.name}!'
        elif self.player.hp >= 0 >= self.enemy.hp:
            self.battle_result = f'{self.player.name} победил {self.enemy.name}'
        elif self.player.hp <= 0 <= self.enemy.hp:
            self.battle_result = f'{self.player.name} проиграл {self.enemy.name}'
        elif (self.player.hp and self.enemy.hp) >= 0:
            return None
        return self._end_game()

    def _stamina_regeneration(self) -> None:
        """recovery stamina"""
        if self.player.stamina + self.STAMINA_PER_ROUND > self.player.unit_class.max_stamina:
            self.player.stamina = self.player.unit_class.max_stamina
        elif self.player.stamina < self.player.unit_class.max_stamina:
            self.player.stamina += self.STAMINA_PER_ROUND
        if self.enemy.stamina + self.STAMINA_PER_ROUND > self.enemy.unit_class.max_stamina:
            self.enemy.stamina = self.enemy.unit_class.max_stamina
        elif self.enemy.stamina < self.enemy.unit_class.max_stamina:
            self.enemy.stamina += self.STAMINA_PER_ROUND

    def next_turn(self) -> str:
        result: Optional[str] = self._check_players_hp()
        if result:
            return result
        if self.game_is_running:
            self._stamina_regeneration()
            self.player.stamina = round(self.player.stamina, 1)
            self.enemy.stamina = round(self.enemy.stamina, 1)
            self.player.hp = round(self.player.hp, 1)
            self.enemy.hp = round(self.enemy.hp, 1)
            return self.enemy.hit(self.player)

    def _end_game(self) -> str:
        self._instances = {}
        result = self.battle_result
        self.game_is_running = False
        return result

    def player_hit(self) -> str:
        result = self.player.hit(self.enemy)
        turn_result = self.next_turn()
        return f"{result}\n{turn_result}"

    def player_use_skill(self) -> str:
        result = self.player.use_skill(self.enemy)
        turn_result = self.next_turn()
        return f"{result}\n{turn_result}"