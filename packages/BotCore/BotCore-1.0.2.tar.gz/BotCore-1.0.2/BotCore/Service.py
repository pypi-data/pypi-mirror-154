
from typing import TypeVar, Generic, Type

T = TypeVar("T")


class Service(Generic[T]):

	def __init__(self, info_type: Type[T], fields: list[str]):
		self.info_type = info_type
		self.fields = fields

	def to_objects(self, rows: list[tuple]) -> list[T]:
		return [self.to_object(row) for row in rows]

	def to_object(self, row: tuple) -> T:
		return self.info_type(dict(zip(self.fields, row)))
