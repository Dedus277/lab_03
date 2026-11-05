from dataclasses import  dataclass
from datetime import date
from .exceptions import InvalidEntityError

allowed_categories = frozenset({"bus", "train", "trolleybus", "metro"})
min_year = 1800
@dataclass(frozen=True)
class Route:
    """Транспортный маршрут. Неверный объект создать нельзя."""

    id: str
    name: str
    category: str
    year: int
    length_km: float
    stop_count: int

    def __post_init__(self):
        for field_name in ("id","name", "category"):
            value = getattr(self, field_name)
            if not isinstance(value,str) or not value.strip():
                raise InvalidEntityError(
                f"Поле {field_name} должно быть непустой строкой."
                )
        if self.category not in allowed_categories:
           raise InvalidEntityError(
            f"Категория {self.category} не поддерживается."
            )
        if not is_int(self.year) or not min_year <= self.year <= date.today().year:
            raise InvalidEntityError(
                f"Год {self.year} должен быть между {min_year} и {date.today().year}."
            )
        if not is_int(self.stop_count) or self.stop_count < 2:
            raise InvalidEntityError(
                f"Количество остановок {self.stop_count} должно быть целым числом больше 1."
            )
        if not is_number(self.length_km) or self.length_km <= 0:
            raise InvalidEntityError(
            f"Длина маршрута {self.length_km} должна быть положительным числом."
            )
def is_int(value) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)

def is_number(value) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)
    
   