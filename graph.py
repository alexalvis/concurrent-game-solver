import warnings


class DeterministicMultiDiGraph(object):
    OUT = 'out edges'
    IN = 'in edges'

    def __init__(self):
        self._graph = dict()
        self._numnodes = 0
        self._numedges = 0

    def __contains__(self, st):
        return st in self._graph

    def __repr__(self):
        return 'Graph with ' + str(self.number_of_nodes) + ' nodes and ' + str(self.number_of_edges) + 'edges.'

    @property
    def number_of_nodes(self):
        return self._numnodes

    @property
    def number_of_edges(self):
        return self._numedges

    @property
    def nodes(self):
        return set(self._graph.keys())

    def add_node(self, node):
        """
        Adds new node to graph

        :param node: Hashable python object
        :return: None
        """
        if node not in self._graph:
            self._graph[node] = {DeterministicMultiDiGraph.OUT: dict(), DeterministicMultiDiGraph.IN: set()}
            self._numnodes += 1

    def rm_node(self, node):
        """

        Remove existing node       ---Ma

        :param node:
        :return:
        """
        if node in self._graph:
            for nbr in self._graph[node][DeterministicMultiDiGraph.OUT].keys():
                self._graph[nbr][DeterministicMultiDiGraph.IN].discard(node)

            self._graph.pop(node)
            self._numnodes -= 1

    def add_edge(self, src, dst, edge_label=None, **kwargs):
        assert src in self._graph and dst in self._graph, 'node not in graph'
        # Check if edge exists
        edge_exists = False
        if dst in self._graph[src][DeterministicMultiDiGraph.OUT]:
            if edge_label in self._graph[src][DeterministicMultiDiGraph.OUT][dst]:
                edge_exists = True

            ### node exist

        if dst in self._graph[src][DeterministicMultiDiGraph.OUT]:
            self._graph[src][DeterministicMultiDiGraph.OUT][dst].update({edge_label: kwargs})
        else:
            self._graph[src][DeterministicMultiDiGraph.OUT][dst] = {edge_label: kwargs}

        self._graph[dst][DeterministicMultiDiGraph.IN].add(src)

        if not edge_exists:
            self._numedges += 1

    def rm_edge(self, src, dst, edge_label):
        assert src in self._graph and dst in self._graph, 'node not in graph'

        if dst in self._graph[src][DeterministicMultiDiGraph.OUT]:
            if edge_label in self._graph[src][DeterministicMultiDiGraph.OUT][dst]:
                self._graph[src][DeterministicMultiDiGraph.OUT][dst].pop(edge_label)
                if len(self._graph[src][DeterministicMultiDiGraph.OUT][dst]) == 0:
                    self._graph[src][DeterministicMultiDiGraph.OUT].pop(dst)
                    self._graph[dst][DeterministicMultiDiGraph.IN].remove(src)

                self._numedges -= 1

    def out_neighbors(self, node):
        """
        Returns the set of neighboring nodes of given node.

        :param node: Node in graph
        :return: Set of neighbors
        """
        try:
            return set(self._graph[node][DeterministicMultiDiGraph.OUT].keys())
        except KeyError as ex:
            warnings.warn("DeterministicMultiDiGraph.out_neighbors:: Key Error: {0}".format(ex), RuntimeWarning)
            return set()

    def in_neighbors(self, node):
        try:
            return self._graph[node][DeterministicMultiDiGraph.IN]
        except KeyError as ex:
            warnings.warn("DeterministicMultiDiGraph.in_neighbors:: Key Error: {0}".format(ex), RuntimeWarning)
            return dict()
        except Exception as ex:
            raise ex

    def out_edges(self, node):
        """
        Returns the outgoing edges with all attributes from given "src" node.

        :param node: Node in graph
        :return: Dictionary of edges as <dest: <edge_label: <attr: value> > >
        """
        try:
            return self._graph[node][DeterministicMultiDiGraph.OUT]
        except KeyError as ex:
            warnings.warn("DeterministicMultiDiGraph.out_edges:: Key Error: {0}".format(ex), RuntimeWarning)     ###the key is not in the Dict.
            return dict()

    def in_edges(self, node):
        try:
            return self._graph[node][DeterministicMultiDiGraph.IN]
        except KeyError as ex:
            warnings.warn("DeterministicMultiDiGraph.out_edges:: Key Error: {0}".format(ex), RuntimeWarning)
            return dict()

    def has_edge(self, src, dst):
        try:
            return dst in self._graph[src][DeterministicMultiDiGraph.OUT]
        except Exception as ex:
            warnings.warn("DeterministicMultiDiGraph.has_edge:: Key Error: {0}".format(ex), RuntimeWarning)
            return False


MultiDiGraph = DeterministicMultiDiGraph
