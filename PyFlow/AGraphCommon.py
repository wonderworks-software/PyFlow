'''
common defines, functions and structures
'''
import math


FLAG_SYMBOL = "~"


def clamp(n, vmin, vmax):
    return max(min(n, vmax), vmin)


def roundup(x, to):
    return int(math.ceil(x / to)) * to


def portAffects(affects_port, affected_port):
    '''
    this function for establish dependencies bitween ports,
    for simulating dirty propogation
    '''
    affects_port.affects.append(affected_port)
    affected_port.affected_by.append(affects_port)


def calc_multithreaded(ls, debug=False):
    if debug:
        print('START', [n.name for n in ls])

    def compute_executor():
        for n in ls:
            n.compute()
    threads = []
    for n in ls:
        t = Thread(target=compute_executor, name='{0}_thread'.format(n.name))
        threads.append(t)
        t.start()
        if debug:
            print(n.name, 'started in', t.name)

    if debug:
        print('_WAITING FOR ALL LAYER NODES TO FINISH')
    [t.join() for t in threads]

    if debug:
        print('DONE', [n.name for n in ls], '\n')


def cycle_check(src, dst):

    # allow cycles on execs
    if src.data_type == DataTypes.Exec or dst.data_type == DataTypes.Exec:
        return False

    if src.type == PinTypes.Input:
        src, dst = dst, src
    start = src
    if src in dst.affects:
        return True
    for i in dst.affects:
        if cycle_check(start, i):
            return True
    return False


def find_ports_behind(start_from):
    out = []

    def foo(start_from):
        if not start_from.affected_by == []:
            for p in start_from.affected_by:
                out.append(p)
                foo(p)
    foo(start_from)
    return out


def push(start_from):
    if not start_from.affects == []:
        start_from.set_dirty()
        for i in start_from.affects:
            i.set_dirty()
            push(i)


class DataTypes:
    Float = 0
    Int = 1
    String = 2
    Bool = 3
    Array = 4
    Any = 5
    Reroute = 6
    Exec = 7
    Reference = 8


class ObjectTypes(object):
    Port = 0
    Node = 1
    Graph = 2
    Grouper = 3
    Connection = 4
    NodeName = 5
    SelectionRect = 6
    Scene = 7
    NodeBox = 8


class PinTypes:
    Input = 0
    Output = 1


class NodeTypes:
    Callable = 0
    Pure = 1
    Latent = 2
