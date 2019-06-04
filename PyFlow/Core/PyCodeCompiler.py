from PyFlow.Core.Interfaces import ICodeCompiler


class Py3FunctionCompiler(ICodeCompiler):
    '''
        Compiles string to function object
    '''

    def __init__(self, fooName=None, *args, **kwargs):
        super(Py3FunctionCompiler, self).__init__(*args, **kwargs)
        assert(isinstance(fooName, str))
        self._fooName = fooName

    def compile(self, code):
        """wraps code to function def

        Arguments:
            code [str] -- code to wrap
        Returns:
            function object
        """
        foo = "def {}(self):".format(self._fooName)
        lines = [i for i in code.split('\n') if len(i) > 0]
        for line in lines:
            foo += '\n\t{}'.format(line)
        if len(lines) == 0:
            foo += "\n\tpass"
        codeObject = compile(foo, "fake", "exec")
        mem = {}
        exec(codeObject, mem)
        return mem[self._fooName]


class Py3CodeCompiler(ICodeCompiler):
    """docstring for Py3CodeCompiler."""
    def __init__(self):
        super(Py3CodeCompiler, self).__init__()

    def compile(self, code):
        codeObject = compile(code, "fake", "exec")
        mem = {}
        exec(codeObject, mem)
        return mem
