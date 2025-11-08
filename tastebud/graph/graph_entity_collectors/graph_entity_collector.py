from polars import DataFrame
from tqdm import tqdm

from tastebud.graph.graph_entity_collectors.entity_relationship_source_protocol import EntityRelationshipSource


class GraphEntityCollector:
    def __init__(self, relationship_source: EntityRelationshipSource):
        self.relationship_source = relationship_source

    def create_schema(self, unique_entities: set[str]) -> tuple[DataFrame, DataFrame]:
        nodes = [{"name": entity, "type": "entity|known"} for entity in unique_entities]
        edges = []
        seen_nodes = unique_entities.copy()
        seen_edges = set()

        for entity in tqdm(unique_entities, desc="Collecting related entities"):
            related_entities = self.relationship_source.get_related_entities([entity])

            for related_entity in related_entities:
                if related_entity not in seen_nodes:
                    nodes.append({"name": related_entity, "type": "entity|unknown"})
                    seen_nodes.add(related_entity)

                edge_candidate = {"subject": entity, "object": related_entity, "weight": 1.0, "predicate": "related_to"}
                edge_key = frozenset(edge_candidate.items())

                if edge_key not in seen_edges:
                    edges.append(edge_candidate)
                    seen_edges.add(edge_key)

        return DataFrame(nodes), DataFrame(edges)
