import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMap = {}
        self._bestPath = []


    def getPath(self, source):
        self._bestPath = []
        parziale = [source]
        self._ricorsione(parziale, float("-inf"))
        return self._bestPath


    def _ricorsione(self, parziale, peso_prec):
        if len(parziale) > len(self._bestPath):
            self._bestPath = copy.deepcopy(parziale)

        for n in nx.neighbors(self._graph, parziale[-1]):
            peso_corr = self._graph[parziale[-1]][n]["weight"]
            if peso_corr >= peso_prec and n not in parziale:
                parziale.append(n)
                self._ricorsione(parziale, peso_corr)
                parziale.pop()



    def buildGraph(self, year, color):
        self._graph.clear()
        self._idMap = {}
        nodes = DAO.getAllNodes(color)
        self._graph.add_nodes_from(nodes)
        for node in nodes:
            self._idMap[node.Product_number] = node
        edges = DAO.getAllEdges(color, year, self._idMap)
        for edge in edges:
            self._graph.add_edge(edge[0], edge[1], weight = edge[2])


    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)


    def getTop3Archi(self):
        orderedEdges = sorted(self._graph.edges(data=True), key = lambda x: x[2]["weight"], reverse = True)
        return orderedEdges[:3]


    def getNodiRipetuti(self, top3):
        # CONTARE LE OCCORRENZE DEI NODI A PARTORE DA UN INSIEME DI ARCHI
        # conteggio = {}
        # for u, v, _ in top3:
        #     conteggio[u.Product_number] = conteggio.get(u.Product_number, 0) + 1
        #     conteggio[v.Product_number] = conteggio.get(v.Product_number, 0) + 1
        # return conteggio

        # Raccogli tutti i prodotti dei 3 archi in una lista (con ripetizioni)
        products = []
        for u, v, _ in top3:
            products.append(u.Product_number)
            products.append(v.Product_number)

        # Stampa quelli che appaiono più di una volta (con il metodo count)
        repeated = [p for p in products if products.count(p) > 1]
        # Ritorno un set cosi non restituisco i duplicati
        return set(repeated)


    def getAllYears(self):
        return DAO.getAllYears()


    def getAllColors(self):
        return DAO.getAllColors()


    def getAllProducts(self):
        return self._graph.nodes

