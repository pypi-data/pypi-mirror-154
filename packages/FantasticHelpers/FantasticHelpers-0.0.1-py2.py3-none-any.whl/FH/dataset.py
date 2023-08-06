import torch_geometric.transforms as T
from torch_geometric.datasets import Planetoid, CitationFull


def get_dataset(name, path='~/datasets'):
    assert name in ['Cora', 'CiteSeer', 'PubMed', 'dblp']

    return (CitationFull if name == 'dblp' else Planetoid)(
        path,
        name,
        transform=T.NormalizeFeatures())
