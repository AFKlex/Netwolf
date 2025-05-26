import networkx as nx 
from src.WebReconGraphVisualizer import * 

class WebReconGraph: 

    def __init__(self) -> None:
        self.graph = nx.Graph()


    def add_node(self, name):
        self.graph.add_node(name)

    def add_edge(self, node_a, node_b):
        self.graph.add_edge(node_a,node_b)

    def draw_graph(self): 
        WebReconGraphVisualizer(self) 
        


