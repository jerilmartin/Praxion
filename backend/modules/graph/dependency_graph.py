"""
Infrastructure Dependency Graph Module   (OBJ-3, FR-03)

Builds and queries a NetworkX graph of infrastructure resources.
"""
from __future__ import annotations
from typing import Any
import networkx as nx


class InfrastructureGraph:
    """NetworkX-backed dependency graph for cloud resources."""

    def __init__(self):
        self.G: nx.DiGraph = nx.DiGraph()

    def build_from_db(self, resources: list[dict], relationships: list[dict]) -> None:
        """
        Populate the graph from database records.

        Args:
            resources: List of InfrastructureResource dicts (id, name, type, …)
            relationships: List of ResourceRelationship dicts (source_id, target_id, relation_type)
        """
        for r in resources:
            self.G.add_node(r["id"], **r)
        for rel in relationships:
            self.G.add_edge(rel["source_id"], rel["target_id"], relation=rel["relation_type"])

    def get_attack_paths(self, source_id: str, target_id: str) -> list[list[str]]:
        """Return all simple paths from source to target (potential attack paths)."""
        try:
            return list(nx.all_simple_paths(self.G, source_id, target_id))
        except nx.NetworkXNoPath:
            return []

    def get_risk_subgraph(self, resource_ids: list[str]) -> dict[str, Any]:
        """Return subgraph containing only high-risk resources and their neighbours."""
        subgraph = self.G.subgraph(resource_ids)
        return nx.node_link_data(subgraph)

    def to_json(self) -> dict[str, Any]:
        """Serialise the full graph to node-link JSON for API / frontend."""
        return nx.node_link_data(self.G)

    def centrality_scores(self) -> dict[str, float]:
        """Compute betweenness centrality to surface high-impact nodes."""
        return nx.betweenness_centrality(self.G)
