from PyFlow.Core.AbstractGraph import *
import PyFlow.Nodes as Nodes

G = Graph("TestGraph")

addition = Nodes.delay.delay("test")
