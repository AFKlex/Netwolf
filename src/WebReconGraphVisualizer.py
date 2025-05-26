from pyvis.network import Network
from pathlib import Path
import base64
import json


class WebReconGraphVisualizer:
    """
    Build a themed PyVis visualisation for a (networkx-like) recon_graph
    and write a single, portable HTML file.

    Parameters
    ----------
    graph : networkx.Graph-like
        Must expose `.nodes` and `.edges`.
    icon_path : str or Path, optional
        PNG to use as favicon / on-page logo.
    html_name : str, optional
        Output filename.  Defaults to "WebReconGraph.html".
    accent : str, optional
        Hex colour used for node borders, edges & headings.

    Example
    -------
    WebReconGraphVisualizer(my_graph, "../assets/images/netwolf_transparent.png")
    """

    def __init__(
        self,
        graph,
        icon_path: str | Path = "./assets/images/netwolf_transparent.png",
        html_name: str = "WebReconGraph.html",
        accent: str = "#ff7a00",
    ):
        self.icon_path = Path(icon_path)
        self.html_name = html_name
        self.accent = accent

        # ---------- 1. build the PyVis network ----------------------------
        self.net = Network(height="950px",
                           width="100%",
                           bgcolor="#1a1a1a",     # page background
                           font_color="#ffffff")   # default text colour
        self._normalize_to_string_graph(graph)

        # give Vis.js a hint of our accent colour
        # Replace set_options call with valid JSON-formatted string
        self.net.set_options(json.dumps({
            "nodes": {
                "color": {
                    "border": self.accent,
                    "background": "#2b2b2b",
                    "highlight": {
                        "border": self.accent,
                        "background": "#444444"
                    }
                },
                "font": {"color": "#ffffff"}
            },
            "edges": {
                "color": self.accent
            }
        })) 

        #self.net.toggle_physics(True)

        # ---------- 2. post-process the generated HTML --------------------
        html = self._inject_theme(self.net.generate_html())
        Path(self.html_name).write_text(html, encoding="utf-8")
        print(f"✓  Wrote themed graph to {self.html_name}")

    # ------------------------------------------------------------------
    # helper methods
    # ------------------------------------------------------------------
    def _normalize_to_string_graph(self, recon_graph):
        for node in recon_graph.graph.nodes:
            self.net.add_node(str(node), label=str(node))
        for u, v in recon_graph.graph.edges:
            self.net.add_edge(str(u), str(v))

    def _inject_theme(self, html: str) -> str:
        """Embed favicon, header strip and custom CSS into PyVis HTML."""
        icon_b64 = base64.b64encode(self.icon_path.read_bytes()).decode()

        head_inject = f"""
<link rel="icon" type="image/png" href="data:image/png;base64,{icon_b64}">
<style>
  body        {{ margin:0; background:#1a1a1a; font-family:Segoe UI,Arial,sans-serif; }}
  .header     {{ display:flex; align-items:center; gap:.75rem;
                 padding:.75rem 1rem; background:#111; box-shadow:0 2px 4px rgba(0,0,0,.4); }}
  .header img {{ height:44px; }}
  .header h1  {{ margin:0; font-size:1.40rem; color:{self.accent}; }}
</style>
"""
        body_inject = f"""
<div class="header">
  <img src="data:image/png;base64,{icon_b64}" alt="NetWolf logo">
  <h1>WebRecon Network Graph</h1>
</div>
"""

        # splice our additions straight after <head> and <body>
        html = html.replace("<head>", f"<head>\n{head_inject}", 1)
        html = html.replace("<body>", f"<body>\n{body_inject}", 1)
        return html

