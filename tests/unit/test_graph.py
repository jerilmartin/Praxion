"""
Unit tests – Dependency Graph Module
"""
import pytest
from backend.modules.graph.dependency_graph import InfrastructureGraph


def _sample_data():
    resources = [
        {"id": "r1", "name": "web-server", "resource_type": "compute"},
        {"id": "r2", "name": "data-bucket", "resource_type": "storage"},
        {"id": "r3", "name": "admin-role",  "resource_type": "iam"},
    ]
    relationships = [
        {"source_id": "r1", "target_id": "r2", "relation_type": "accesses"},
        {"source_id": "r3", "target_id": "r1", "relation_type": "assumes"},
    ]
    return resources, relationships


def test_graph_builds_correctly():
    g = InfrastructureGraph()
    resources, relationships = _sample_data()
    g.build_from_db(resources, relationships)
    assert g.G.number_of_nodes() == 3
    assert g.G.number_of_edges() == 2


def test_attack_path_found():
    g = InfrastructureGraph()
    resources, relationships = _sample_data()
    g.build_from_db(resources, relationships)
    paths = g.get_attack_paths("r3", "r2")
    assert len(paths) > 0


def test_to_json_serialisable():
    g = InfrastructureGraph()
    resources, relationships = _sample_data()
    g.build_from_db(resources, relationships)
    data = g.to_json()
    assert "nodes" in data
    assert "links" in data
