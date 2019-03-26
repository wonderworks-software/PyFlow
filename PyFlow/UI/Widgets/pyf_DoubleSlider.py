from Qt import QtWidgets


class pyf_DoubleSlider(QtWidgets.QSlider):

    def __init__(self, *args, **kwargs):
        super(pyf_DoubleSlider, self).__init__(*args, **kwargs)
        self.decimals = 5
        self._max_int = 10 ** self.decimals

        super(pyf_DoubleSlider, self).setMinimum(0)
        super(pyf_DoubleSlider, self).setMaximum(self._max_int)

        self._min_value = 0.0
        self._max_value = 1.0

    @property
    def _value_range(self):
        return self._max_value - self._min_value

    def value(self):
        return float(super(pyf_DoubleSlider, self).value()) / self._max_int * self._value_range + self._min_value

    def setValue(self, value):
        super(pyf_DoubleSlider, self).setValue(
            int((value - self._min_value) / self._value_range * self._max_int))

    def setMinimum(self, value):
        if value > self._max_value:
            raise ValueError("Minimum limit cannot be higher than maximum")

        self._min_value = value
        self.setValue(self.value())

    def setMaximum(self, value):
        if value < self._min_value:
            raise ValueError("Minimum limit cannot be higher than maximum")

        self._max_value = value
        self.setValue(self.value())

    def minimum(self):
        return self._min_value

    def maximum(self):
        return self._max_value
