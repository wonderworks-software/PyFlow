def portAffects(affects_port, affected_port):
    '''
    this function for establish dependencies bitween ports,
    for simulating maya's dirty propogation
    '''
    affects_port.affects.append(affected_port)
    affected_port.affected_by.append(affects_port)


def push(start_from):

    if not start_from.affects == []:
        # print start_from.parent.name, start_from.name, '|DIRTY|>',
        start_from.dirty = True
        for i in start_from.affects:
            i.dirty = True
            push(i)


class AGObjectTypes(object):

    tPort = 'port_object'
    tEdge = 'edge_object'
    tNode = 'node_object'
    tGraph = 'graph_object'

    def __init__(self):
        super(AGObjectTypes, self).__init__()


class AGPortTypes(object):

    kInput = 'input_port'
    kOutput = 'output_port'

    def __init__(self, arg):
        super(AGPortTypes, self).__init__()


class AGEdge(object):

    def __init__(self, source, destination):
        super(AGEdge, self).__init__()
        self.source = source
        self.destination = destination
        self.object_type = AGObjectTypes.tEdge

    def __str__(self):
        return self.source.parent.name + '.' + self.source.name + \
        ' >>> ' + self.destination.parent.name + '.' + self.destination.name


class AGPort(object):

    def __init__(self, name, parent):
        super(AGPort, self).__init__()
        self.name = name
        self.type = None
        self.object_type = AGObjectTypes.tPort
        self.dirty = True
        self._data = None
        self.parent = parent
        self.affects = []
        self.affected_by = []
        self.edge_list = []

    def get_data(self):

        if self.type == AGPortTypes.kOutput:
            if self.dirty:
                # print self.parent.name, '.', self.name, 'dirty. requesting compute'
                self.parent.compute()
                self.dirty = False
                return self._data
            else:
                return self._data
        if self.type == AGPortTypes.kInput:
            if self.dirty:
                out = [i for i in self.affected_by if i.type == AGPortTypes.kOutput]
                if not out == []:
                    # print out[0].parent.name, '.', out[0].name, 'dirty. requesting compute'
                    out[0].parent.compute()
                    self.dirty = False
                    out[0].dirty = False
                    return out[0]._data
                else:
                    return self._data
            else:
                return self._data

    def set_data(self, data, dirty_propagate=True):

        self._data = data
        if dirty_propagate:
            push(self)


class AGNode(object):
    def __init__(self, name):
        super(AGNode, self).__init__()
        self.graph = None
        self.name = name
        self.object_type = AGObjectTypes.tNode
        self.selected = False
        self.inputs = []
        self.outputs = []

    def add_port(self, port_name, port_type):
        p = AGPort(port_name, self)
        if port_type == AGPortTypes.kInput:
            self.inputs.append(p)
            p.type = AGPortTypes.kInput
            return p
        else:
            self.outputs.append(p)
            p.type = AGPortTypes.kOutput
            return p

    def get_port_by_name(self, name):
        for p in self.inputs + self.outputs:
            if p.name == name:
                return p

    def compute(self):
        '''
        node calculations here
        '''
        # getting data from inputs

        # do stuff

        # write data to outputs
        return


class AGraph(object):

    def __init__(self, name):

        super(AGraph, self).__init__()
        self.object_type = AGObjectTypes.tGraph
        self.name = name
        self.nodes = []
        self.edges = []

    def get_evaluation_order(self, node, dirty_only=True):

        order = {0: [node]}
        def foo(n):
            next_layer_nodes = self.get_next_layer_nodes(n, AGPortTypes.kInput, dirty_only)
            layer_idx = max(order.iterkeys()) + 1
            for n in next_layer_nodes:
                if layer_idx not in order:
                    order[layer_idx] = []
                order[layer_idx].append(n)
            if not next_layer_nodes == []:
                for i in next_layer_nodes:
                    foo(i)
        foo(node)
        return order

    @staticmethod
    def get_next_layer_nodes(node, direction=AGPortTypes.kInput, dirty_only=False):
        nodes = []
        if direction == AGPortTypes.kInput:
            if not node.inputs == []:
                for i in node.inputs:
                    if not i.affected_by == []:
                        for a in i.affected_by:
                            if not dirty_only:
                                nodes.append(a.parent)
                            else:
                                if a.dirty:
                                    nodes.append(a.parent)
            return nodes
        if direction == AGPortTypes.kOutput:
            if not node.outputs == []:
                for i in node.outputs:
                    if not i.affects == []:
                        for p in i.affects:
                            if not dirty_only:
                                nodes.append(p.parent)
                            else:
                                if not [dout for dout in p.affects if dout.dirty] == []:
                                    nodes.append(p.parent)
            return nodes

    def nodes(self):

        return self.nodes

    def add_node(self, node):

        self.nodes.append(node)
        node.graph = self

    def remove_node_by_name(self, name):

        [self.nodes.remove(n) for n in self.nodes if name == n.name]

    def count(self):

        return self.nodes.__len__()

    def add_edge(self, src, dst):

        if src in dst.affected_by:
            print 'already connected. skipped'
            return
        if src.type == dst.type:
            print 'same types can not be connected'
            return
        if src.parent == dst.parent:
            print 'can not connect to self'
            return

        portAffects(src, dst)
        e = AGEdge(src, dst)
        self.edges.append(e)
        src.edge_list.append(e)
        dst.edge_list.append(e)
        dst.dirty = True
        src.dirty = True
        dst.set_data(src._data, False)
        return e

    @staticmethod
    def remove_edge(edge):

        edge.destination.affected_by.remove(edge.source)
        edge.source.affects.remove(edge.destination)
        edge.destination.edge_list.remove(edge)
        edge.source.edge_list.remove(edge)

    def plot(self):
        print self.name+'\n----------\n'
        for n in self.nodes:
            print n.name
            for inp in n.inputs:
                print '|---', inp.name, 'data - {0}'.format(inp._data), \
                    'affects on', [i.name for i in inp.affects], \
                    'affected_by ', [p.name for p in inp.affected_by], \
                    'DIRTY ', inp.dirty
                for e in inp.edge_list:
                    print '\t|---', e.__str__()
            for out in n.outputs:
                print '|---' + out.name, 'data - {0}'.format(out._data),
                if out.affects:
                    print 'affects on', [i.name for i in out.affects],
                print 'affected_by ', [p.name for p in out.affected_by],
                print 'DIRTY', out.dirty
                for e in out.edge_list:
                    print '\t|---', e.__str__()
