from enum import IntEnum


class VisibilityPolicy(IntEnum):
    AlwaysVisible = 1
    AlwaysHidden = 2
    Auto = 3


## This function clears property view's layout.
# @param[in] layout QLayout class
def clearLayout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget() is not None:
            child.widget().deleteLater()
        elif child.layout() is not None:
            clearLayout(child.layout())
