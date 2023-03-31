"""
Module that contains the Temporal Backend.
"""

from clingo.symbol import Function, Number
from clingo import parse_term
from clingo.script import enable_python

# Self defined
from clinguin.server import ClinguinModel
from clinguin.server.application.backends.clingo_backend import ClingoBackend
from clinguin.server.application.backends.standard_utils.brave_cautious_helper import *

enable_python()


class TemporalBackend(ClingoBackend):
    """
    TODO -> Add documentation!
    """

    def __init__(self, args):
        self._step = 1
        self._last_grounded_step = 0
        self._full_plan = None
        super().__init__(args)

    def _init_ctl(self):
        self._step = 1
        self._last_grounded_step = 0
        self._full_plan = None
        super()._init_ctl()

    def _ground(self):
        if not self._last_grounded_step:
            self._ctl.ground([("base", [])])
        while self._step > self._last_grounded_step:
            self._last_grounded_step += 1
            self._ctl.ground([("step", [Number(self._step)])])
        if self._step > 1:
            self._ctl.assign_external(
                Function("query", [Number(self._step - 1)]), False
            )
        self._ctl.assign_external(Function("query", [Number(self._step)]), True)

    def _find_incrementally(self):
        if self._step > 1:
            self._ctl.assign_external(
                Function("check", [Number(self._step - 1)]), False
            )
        self._ctl.assign_external(Function("check", [Number(self._step)]), True)
        plan = self._find_plan()

        while plan is None or self._step > 100:
            self._step += 1
            self._ground()
            if self._step > 1:
                self._ctl.assign_external(
                    Function("check", [Number(self._step - 1)]), False
                )
            self._ctl.assign_external(Function("check", [Number(self._step)]), True)
            plan = self._find_plan()

        if self._full_plan is None:
            raise RuntimeError("No plan found before 100 steps")

        return self._full_plan

    def _find_plan(self):
        self._ctl.configuration.solve.enum_mode = "auto"
        hdn = self._ctl.solve(
            assumptions=[(a, True) for a in self._assumptions], yield_=True
        )
        itr = iter(hdn)
        try:
            model = next(itr)
            self._full_plan = model.symbols(atoms=True)
            hdn.cancel()
        except StopIteration:
            hdn.cancel()
            self._full_plan = None

        return self._full_plan

    def find_plan(self):
        if not self._full_plan:
            self._find_incrementally()

        symbols = "\n".join([str(s) + "." for s in self._full_plan])
        wctl = ClinguinModel.wid_control(self._ui_files, symbols)
        self._model = ClinguinModel.from_ctl(wctl)
        return self.get()

    def assume_and_step(self, predicate):
        predicate_symbol = parse_term(predicate)
        self._assumptions.add(predicate_symbol)
        self._step += 1
        self._ground()
        self._end_browsing()
        self._update_model()
        return self.get()

    def remove_assumption(self, predicate):
        raise NotImplementedError()

    def next_solution(self):
        raise NotImplementedError()
