# Copyright 2021 AIPlan4EU project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
'''This module defines the different remover classes.'''

from unified_planning.model import AbstractProblem
from unified_planning.plans import Plan
from unified_planning.solvers import Credits
from typing import Optional


class Transformer:
    '''Represents a generic Transformer with all the needed methods shared among them.'''
    def __init__(self, problem: AbstractProblem, name: str):
        self._name = name
        self._problem = problem
        self._env = problem.env
        credits = self.get_credits()
        if credits is not None and self._env.credits_stream is not None:
            credits.write_credits(self._env.credits_stream, full_credits=True)

    def get_credits(self) -> Optional[Credits]:
        '''This method returns the credits of this transformer, that are printed in the __init__ function.'''
        return None

    def get_rewritten_problem(self) -> AbstractProblem:
        '''This function should rewrite the problem according to the Transformer specifics.'''
        raise NotImplementedError

    def rewrite_back_plan(self, plan: Plan) -> Plan:
        '''Takes the plan of the problem (created with
        the method "self.get_rewritten_problem()" and translates the plan back
        to be a plan of the original problem.
        '''
        raise NotImplementedError
