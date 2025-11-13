from dataclasses import dataclass
from typing import Self


@dataclass(frozen=True)
class CoffeeOrder:
    base: str
    size: str
    milk: str
    syrups: tuple[str, ...]
    sugar: int
    iced: bool
    price: float
    description: str

    def __str__(self) -> str:
        return self.description if self.description else f"Coffee order: {self.price}"


class CoffeeOrderBuilder:
    """
    Билдер для создания заказов кофе.

    Правила и ограничения:
    - Основа и размер обязательны, остальное можно не указывать
    - Сиропы: максимум 4 разных, повторения не считаются
    - Сахар: от 0 до 5 ложек
    - Цена: базовая цена * на размер + молоко + сиропы (каждый по 40) + лед (0.2 если есть)
    - Билдер можно использовать много раз, build() создает новый заказ который уже нельзя менять
    """
    
    BASE_PRICES = {
        "espresso": 200,
        "americano": 250,
        "latte": 300,
        "cappuccino": 320
    }
    SIZE_MULTIPLIERS = {
        "small": 1.0,
        "medium": 1.2,
        "large": 1.4
    }
    MILK_PRICES = {
        "none": 0.0,
        "whole": 30,
        "skim": 30,
        "oat": 60,
        "soy": 50
    }
    SYRUP_PRICE = 40
    ICED_PRICE = 0.2
    MAX_SYRUPS = 4
    MAX_SUGAR = 5
    MIN_SUGAR = 0

    def __init__(self) -> None:
        self._base: str | None = None
        self._size: str | None = None
        self._milk: str = "none"
        self._syrups: set[str] = set()
        self._sugar: int = 0
        self._iced: bool = False

    def set_base(self, base: str) -> Self:
        if base not in self.BASE_PRICES:
            raise ValueError(f"Invalid base: {base}")
        self._base = base
        return self

    def set_size(self, size: str) -> Self:
        if size not in self.SIZE_MULTIPLIERS:
            raise ValueError(f"Invalid size: {size}")
        self._size = size
        return self

    def set_milk(self, milk: str) -> Self:
        if milk not in self.MILK_PRICES:
            raise ValueError(f"Invalid milk: {milk}")
        self._milk = milk
        return self

    def add_syrup(self, name: str) -> Self:
        if len(self._syrups) >= self.MAX_SYRUPS:
            raise ValueError(f"Maximum {self.MAX_SYRUPS} syrups allowed")
        self._syrups.add(name)
        return self

    def set_sugar(self, teaspoons: int) -> Self:
        if not (self.MIN_SUGAR <= teaspoons <= self.MAX_SUGAR):
            raise ValueError(f"Sugar must be between {self.MIN_SUGAR} and {self.MAX_SUGAR}")
        self._sugar = teaspoons
        return self

    def set_iced(self, iced: bool = True) -> Self:
        self._iced = iced
        return self

    def clear_extras(self) -> Self:
        self._milk = "none"
        self._syrups.clear()
        self._sugar = 0
        self._iced = False
        return self

    def build(self) -> CoffeeOrder:
        if self._base is None:
            raise ValueError()
        if self._size is None:
            raise ValueError("Size must be set")
        
        # Расчет цены
        base_price = self.BASE_PRICES[self._base]
        size_multiplier = self.SIZE_MULTIPLIERS[self._size]
        milk_price = self.MILK_PRICES[self._milk]
        syrup_price = len(self._syrups) * self.SYRUP_PRICE
        iced_price = self.ICED_PRICE if self._iced else 0
        price = (base_price * size_multiplier) + milk_price + syrup_price + iced_price
        
        # Описание заказа
        desc_parts = [self._size, self._base]
        if self._milk != "none":
            desc_parts.append(f"with {self._milk} milk")
        if self._syrups:
            syrup_list = ", ".join(sorted(self._syrups))
            desc_parts.append(f"+{syrup_list}")
        if self._iced:
            desc_parts.append("(iced)")
        if self._sugar > 0:
            desc_parts.append(f"{self._sugar} tsp sugar")
        description = " ".join(desc_parts)
        
        return CoffeeOrder(
            base=self._base,
            size=self._size,
            milk=self._milk,
            syrups=tuple(sorted(self._syrups)),
            sugar=self._sugar,
            iced=self._iced,
            price=price,
            description=description
        )
