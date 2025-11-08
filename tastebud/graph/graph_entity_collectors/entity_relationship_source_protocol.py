from typing import Protocol


class EntityRelationshipSource(Protocol):
    def get_related_entities(self, entities: list[str]) -> list[str]:
        pass
