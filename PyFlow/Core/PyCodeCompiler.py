## Copyright 2015-2019 Ilgar Lunin, Pedro Cabrera

## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at

##     http://www.apache.org/licenses/LICENSE-2.0

## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.


from PyFlow.PyFlow.Core.Interfaces import ICodeCompiler

class Py3FunctionCompiler(ICodeCompiler):
    """Compiles string to python function
    """
    def __init__(self, fooName=None, *args, **kwargs):
        super(Py3FunctionCompiler, self).__init__(*args, **kwargs)
        assert(isinstance(fooName, str))
        self._fooName = fooName

    def compile(self, code):
        """Wraps code to function def

        :param code: Code to wrap
        :type code: :class:`str`
        :returns: Function object
        :rtype: :class:`function`
        """
        foo = "def {}(self):".format(self._fooName)
        lines = [i for i in code.split('\n') if len(i) > 0]
        for line in lines:
            foo += '\n\t{}'.format(line)
        if len(lines) == 0:
            foo += "\n\tpass"
        codeObject = compile(foo, "PyFlowCodeCompiler", "exec")
        mem = {}
        exec(codeObject, mem)
        return mem[self._fooName]


class Py3CodeCompiler(ICodeCompiler):
    """Generic python code compiler"""
    def __init__(self):
        super(Py3CodeCompiler, self).__init__()

    def compile(self, code, moduleName="PyFlowCodeCompiler", scope={}):
        """Evaluates supplied string

        Used by python node

        :param code: Whatever python code
        :type code: str
        :param moduleName: Used for runtime error messages
        :type moduleName: str
        :param scope: Storage where symbols will be placed
        :type scope: dict
        """
        codeObject = compile(code, moduleName, "exec")
        exec(codeObject, scope)
        return scope
