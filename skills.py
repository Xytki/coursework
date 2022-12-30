from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from unit import BaseUnit


class Skill(ABC):
    """
     base skills class
    """
    user = None
    target = None

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def stamina(self):
        pass

    @property
    @abstractmethod
    def damage(self):
        pass

    @abstractmethod
    def skill_effect(self) -> str:
        pass

    def _is_stamina_enough(self) -> bool:
        return self.user.stamina > self.stamina

    def use(self, user: BaseUnit, target: BaseUnit) -> str:
        """
        Checking if the player has enough stamina to use the skill.
        """
        self.user = user
        self.target = target
        if self._is_stamina_enough:
            return self.skill_effect()
        return f"{self.user.name} попытался использовать {self.name} но у него не хватило выносливости."


class FuryPunch(Skill):
    name: str = "Свирепый пинок"
    stamina: int = 6
    damage: int = 12

    def skill_effect(self) -> str:
        self.user.stamina -= self.stamina
        self.target.get_damage(self.damage)
        return f"{self.user.name} использует {self.name} и наносит {self.damage} урона сопернику"


class HardShot(Skill):
    name: str = "Мощный укол"
    stamina: int = 5
    damage: int = 15

    def skill_effect(self) -> str:
        self.user.stamina -= self.stamina
        self.target.get_damage(self.damage)
        return f"{self.user.name} использует {self.name} и наносит {self.damage} урона сопернику"
