from polars import DataFrame
from tqdm import tqdm

from tastebud.graph.graph_dataclass import GraphSchema
from tastebud.graph.graph_entity_collectors.entity_relationship_source_protocol import EntityRelationshipSource


class GraphEntityCollector:
    def __init__(self, relationship_source: EntityRelationshipSource):
        self.relationship_source = relationship_source

    def create_schema(self, unique_entities: set[str]) -> GraphSchema:
        nodes = [{"name": entity, "type": "entity|known"} for entity in unique_entities]
        edges = []

        for entity in tqdm(unique_entities, desc="Collecting related entities"):
            related_entities = self.relationship_source.get_related_entities(entity)

            for related_entity in related_entities:
                if related_entity not in unique_entities:
                    nodes.append({"name": related_entity, "type": "entity|unknown"})

                edges.append({"subject": entity, "object": related_entity, "weight": 1.0, "predicate": "related_to"})

        return GraphSchema(nodes=DataFrame(nodes), edges=DataFrame(edges))
