"""Attack Graph — Vol II Ch18, Vol X 'Attack Tree Generation'.

User -> Endpoint -> API -> Database -> Object
Planner prioritizes unexplored nodes and relationships.
"""
from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class Node:
    id: str
    kind: str  # user|endpoint|api|database|object
    explored: bool = False
    metadata: dict = field(default_factory=dict)


class AttackGraph:
    def __init__(self):
        self.nodes: dict[str, Node] = {}
        self.edges: list[tuple[str, str]] = []

    def add_node(self, node_id: str, kind: str, **metadata) -> Node:
        if node_id not in self.nodes:
            self.nodes[node_id] = Node(id=node_id, kind=kind, metadata=metadata)
        return self.nodes[node_id]

    def add_edge(self, src: str, dst: str):
        if (src, dst) not in self.edges:
            self.edges.append((src, dst))

    def mark_explored(self, node_id: str):
        if node_id in self.nodes:
            self.nodes[node_id].explored = True

    def unexplored(self) -> list[Node]:
        return [n for n in self.nodes.values() if not n.explored]

    def to_dict(self) -> dict:
        return {
            "nodes": [{"id": n.id, "kind": n.kind, "explored": n.explored, "metadata": n.metadata}
                      for n in self.nodes.values()],
            "edges": self.edges,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "AttackGraph":
        g = cls()
        for n in data.get("nodes", []):
            node = Node(id=n["id"], kind=n["kind"], explored=n["explored"], metadata=n.get("metadata", {}))
            g.nodes[node.id] = node
        g.edges = [tuple(e) for e in data.get("edges", [])]
        return g
