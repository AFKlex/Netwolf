from pyvis.network import Network


class WebReconGraphVisualizer():
    def __init__(self, graph) -> None:
        self.net = Network() 
        self.normalize_to_string_graph(graph)
        self.net.toggle_physics(True)
        self.net.show("WebReconGraph.html", notebook=False) # Notebook false is relevant because with pip verion of pyvis the Network() has the notebook=True set as default

    def normalize_to_string_graph(self, recon_graph):
        for node in recon_graph.graph.nodes:
            self.net.add_node(str(node), label=str(node), color="green")
        for edge in recon_graph.graph.edges:
            self.net.add_edge(str(edge[0]), str(edge[1]))

