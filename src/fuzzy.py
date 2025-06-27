from typing import Dict, List

from ._mfs import *

class LinguisticTag:
    """Represents a linguistic tag."""

    def __init__(self, name, mf, variable):
        """Constructor for LinguisticTag

        Args:
            name (str): Name of the tag. Required.
            mf (Callable[float, float]): Membership function of the tag. Required.
        """
        self._name = name
        self._mf = mf
        self._variable = variable

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def mf(self):
        return self._mf

    @mf.setter
    def mf(self, mf):
        self._mf = mf

    @property
    def variable(self):
        return self._variable

    @variable.setter
    def variable(self, variable):
        self._variable = variable

    def __str__(self):
        return f'{self.variable.name} IS {self.name}'

    def __iter__(self):
        yield self


class FuzzyInput:
    """Represents a fuzzy input."""

    def __init__(self, name, mnm, mxm):
        """Constructor for FuzzyInput

        Args:
            name (str): Name of the fuzzy input.
            mnm (float): Lower limit of the range of the value.
            mxm (float): Upper limit of the range of the value.
        """
        self._name = name
        self._mnm = mnm
        self._mxm = mxm
        self._tags = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def mnm(self):
        return self._mnm

    @mnm.setter
    def mnm(self, mnm):
        self._mnm = mnm

    @property
    def mxm(self):
        return self._mxm

    @mxm.setter
    def mxm(self, mxm):
        self._mxm = mxm

    @property
    def tags(self) -> List[LinguisticTag]:
        return self._tags

    def add_tag(self, name: str, mf_type: str, mf_values: List[float]) -> LinguisticTag:
        if any(list(map(lambda x: x < self.mnm or x > self.mxm, mf_values))):
            raise ValueError('Membership values cannot be outside of the input\'s range: ', mf_values)
        match mf_type:
            case 'trapmf':
                mf = TrapezoidalMF(self.mnm, mf_values[0], mf_values[1], mf_values[2], mf_values[3], self.mxm)
            case 'trimf':
                mf = TriangularMF(self.mnm, mf_values[0], mf_values[1], mf_values[2], self.mxm)
            case 'linzmf':
                mf = LinearZMF(self.mnm, mf_values[0], mf_values[1], self.mxm)
            case 'linsmf':
                mf = LinearSMF(self.mnm, mf_values[0], mf_values[1], self.mxm)
            case _:
                raise ValueError('Membership function type is not valid: ', mf_type)
        tag = LinguisticTag(name, mf, self)
        self.tags.append(tag)
        return tag

    def remove_tag(self, tag: LinguisticTag):
        self.tags.remove(tag)

    def evaluate(self, value: float) -> Dict[str, float]:
        evaluations = {}
        for tag in self.tags:
            evaluations[tag.name] = tag.mf.evaluate(value)
        return evaluations

    def __str__(self) -> str:
        return f'{self.name}'


class FuzzyOutput:

    def __init__(self, name, mnm, mxm):
        """Constructor for FuzzyOutput

        Args:
            name (str): Name of the fuzzy output.
            mnm (float): Lower limit of the range of the value.
            mxm (float): Upper limit of the range of the value.
        """
        self._name = name
        self._mnm = mnm
        self._mxm = mxm
        self._tags = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def mnm(self):
        return self._mnm

    @mnm.setter
    def mnm(self, mnm):
        self._mnm = mnm

    @property
    def mxm(self):
        return self._mxm

    @mxm.setter
    def mxm(self, mxm):
        self._mxm = mxm

    @property
    def tags(self) -> List[LinguisticTag]:
        return self._tags

    def add_tag(self, name, value):
        if value < self.mnm or value > self.mxm:
            raise ValueError('Value cannot be outside of the output\'s range: ', value)
        tag = LinguisticTag(name, ConstMF(value), self)
        self.tags.append(tag)
        return tag

    def remove_tag(self, tag):
        self.tags.remove(tag)

    def __str__(self):
        return f'{self.name}'