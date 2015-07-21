from threading import Thread


def portAffects(affects_port, affected_port):
    '''
    this function for establish dependencies bitween ports,
    for simulating maya's dirty propogation
    '''
    affects_port.affects.append(affected_port)
    affected_port.affected_by.append(affects_port)


def calc_multithreaded(ls, debug=False):
    if debug:
        print 'START', [n.name for n in ls]
    def compute_executor():
        for n in ls:
            n.compute()
    threads = []
    for n in ls:
        t = Thread(target=compute_executor, name='{0}_thread'.format(n.name))
        threads.append(t)
        t.start()
        if debug:
            print n.name, 'started in', t.name

    if debug:
        print '_WAITING FOR ALL LAYER NODES TO FINISH'
    [t.join() for t in threads]

    if debug:
        print 'DONE', [n.name for n in ls], '\n'


def push(start_from, update=False):

    if not start_from.affects == []:
        if update:
            start_from.update()
        start_from.set_dirty()
        for i in start_from.affects:
            i.set_dirty()
            if update:
                i.update()
            if update:
                push(i, True)
            else:
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

    def current_value(self):

        return self._data

    def set_clean(self):

        self.dirty = False

    def set_dirty(self):

        self.dirty = True
        for i in self.affects:
            i.dirty = True

    def get_data(self):

        debug = self.parent.graph.is_debug()
        if self.type == AGPortTypes.kOutput:
            if self.dirty:
                compute_order = self.parent.graph.get_evaluation_order(self.parent)
                for i in reversed(sorted([i for i in compute_order.keys()])):
                    if not self.parent.graph.is_multithreaded():
                        for n in compute_order[i]:
                            if debug:
                                print n.name, 'calling compute'
                            n.compute()
                    else:
                        if debug:
                            print 'multithreaded calc of layer', [n.name for n in compute_order[i]]
                        calc_multithreaded(compute_order[i], debug)
                self.dirty = False
                return self._data
            else:
                return self._data
        if self.type == AGPortTypes.kInput:
            if self.dirty:
                out = [i for i in self.affected_by if i.type == AGPortTypes.kOutput]
                if not out == []:
                    compute_order = out[0].parent.graph.get_evaluation_order(out[0].parent)
                    for i in reversed(sorted([i for i in compute_order.keys()])):
                        if not self.parent.graph.is_multithreaded():
                            for n in compute_order[i]:
                                if debug:
                                    print n.name, 'calling compute'
                                n.compute()
                        else:
                            if debug:
                                print 'multithreaded calc of layer', [n.name for n in compute_order[i]]
                            calc_multithreaded(compute_order[i], debug)
                    self.dirty = False
                    out[0].dirty = False
                    return out[0]._data
            else:
                return self._data
        else:
            return self._data

    def set_data(self, data, dirty_propagate=True):

        self._data = data
        self.set_clean()
        if self.type == AGPortTypes.kOutput:
            for i in self.affects:
                i._data = data
                i.set_clean()
        if dirty_propagate:
            push(self)


class AGNode(object):
    def __init__(self, name, graph):
        super(AGNode, self).__init__()
        self.graph = graph
        self.name = name
        self.object_type = AGObjectTypes.tNode
        self.inputs = []
        self.outputs = []

    def add_input_port(self, port_name):
        p = AGPort(port_name, self)
        self.inputs.append(p)
        p.type = AGPortTypes.kInput
        return p

    def add_output_port(self, port_name):
        p = AGPort(port_name, self)
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
        self._debug = False
        self._multithreaded = False
        self.name = name
        self.nodes = []
        self.edges = []

    def is_debug(self):

        return self._debug

    def set_debug(self, state):
        if not isinstance(state, bool):
            print 'bool expected. skipped'
            return
        self._debug = state

    def is_multithreaded(self):

        return self._multithreaded

    def set_multithreaded(self, state):

        self._multithreaded = state

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
        # make sure no copies of nodes in higher layers (non directional cycles)
        for i in reversed(sorted([i for i in order.iterkeys()])):
            for iD in range(i-1, -1, -1):
                for check_node in order[i]:
                    if check_node in order[iD]:
                        order[iD].remove(check_node)
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

    def add_node(self, node):

        self.nodes.append(node)
        node.graph = self

    def remove_node_by_name(self, name):

        [self.nodes.remove(n) for n in self.nodes if name == n.name]

    def count(self):

        return self.nodes.__len__()

    def add_edge(self, src, dst):

        debug = self.is_debug()
        if src in dst.affected_by:
            if debug:
                print 'already connected. skipped'
            return
        if src.type == dst.type:
            if debug:
                print 'same types can not be connected'
            return
        if src.parent == dst.parent:
            if debug:
                print 'can not connect to self'
            return

        if src.type == AGPortTypes.kInput:
            portAffects(dst, src)
            e = AGEdge(dst, src)
        else:
            portAffects(src, dst)
            e = AGEdge(src, dst)
        self.edges.append(e)
        src.edge_list.append(e)
        dst.edge_list.append(e)
        src.set_dirty()
        dst._data = src._data
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
