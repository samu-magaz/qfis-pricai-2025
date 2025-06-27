class TrapezoidalMF:
    "Implements a trapezoidal membership function"

    def __init__(self, start, left_low, left_high, right_high, right_low, end):
        """Constructor for TrapezoidalMF

        Args:
            start (float): Start of the domain of the function.
            left_low (float): Lower threshold on the left of the trapezoid.
            left_high (float): Upper threshold on the left of the trapezoid.
            right_high (float): Upper threshold on the right of the trapezoid.
            right_low (float): Lower threshold on the right of the trapezoid.
            end (float): End of the domain of the function.
        """
        self._start = start
        self._left_low = left_low
        self._left_high = left_high
        self._right_high = right_high
        self._right_low = right_low
        self._end = end

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, start):
        self._start = start

    @property
    def left_low(self):
        return self._left_low

    @left_low.setter
    def left_low(self, left_low):
        self._left_low = left_low

    @property
    def left_high(self):
        return self._left_high

    @left_high.setter
    def left_high(self, left_high):
        self._left_high = left_high

    @property
    def right_high(self):
        return self._right_high

    @right_high.setter
    def right_high(self, right_high):
        self._right_high = right_high

    @property
    def right_low(self):
        return self._right_low

    @right_low.setter
    def right_low(self, right_low):
        self._right_low = right_low

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, end):
        self._end = end

    def evaluate(self, value):
        evaluation = -1
        if value < self.start:
            value = self.start
        elif value > self.end:
            value = self.end
        if self.start <= value <= self.left_low or self.right_low <= value <= self.end: # Low level
            evaluation = 0
        elif self.left_high < value <= self.right_high:                                 # Top level
            evaluation = 1
        elif self.left_low < value <= self.left_high:                                   # Upwards slope
            evaluation = (value - self.left_low)/(self.left_high - self.left_low)
        elif self.right_high < value < self.right_low:                                  # Downwards slope
            evaluation = (self.right_low - value)/(self.right_low - self.right_high)
        return evaluation

class TriangularMF(TrapezoidalMF):
    """Implements a triangular membership function using a trapezoidal MF."""
    def __init__(self, start, left, top, right, end):
        super().__init__(start, left, top, top, right, end)

class LinearZMF(TrapezoidalMF):
    """Implements a linear Z-shaped membership function using a trapezoidal MF."""
    def __init__(self, start, left, right, end):
        super().__init__(start-1, start-1, start-1, left, right, end)

class LinearSMF(TrapezoidalMF):
    """Implements a linear S-shaped membership function using a trapezoidal MF."""
    def __init__(self, start, left, right, end):
        super().__init__(start, left, right, end+1, end+1, end+1)

class ConstMF:
    def __init__(self, const):
        self._const = const

    @property
    def const(self):
        return self._const

    @const.setter
    def const(self, const):
        self._const = const

    def evaluate(self, value):
        return self.const * value