from Nodes.branch import branch
from Nodes.charge import charge
from Nodes.delay import delay
from Nodes.deltaTime import deltaTime
from Nodes.doN import doN
from Nodes.doOnce import doOnce
from Nodes.flipFlop import flipFlop
from Nodes.forLoop import forLoop
from Nodes.forLoopWithBreak import forLoopWithBreak
from Nodes.implicitPinCall import implicitPinCall
from Nodes.retriggerableDelay import retriggerableDelay
from Nodes.sequence import sequence
from Nodes.switchOnString import switchOnString
from Nodes.timer import timer
from Nodes.whileLoop import whileLoop


def GetNodeClasses():
    functionBasedNodes = []
    return [
        branch,
        charge,
        delay,
        deltaTime,
        doN,
        doOnce,
        flipFlop,
        forLoop,
        forLoopWithBreak,
        implicitPinCall,
        retriggerableDelay,
        sequence,
        switchOnString,
        timer,
        whileLoop
    ] + functionBasedNodes
