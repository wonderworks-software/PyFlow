from PyFlow.Core.Interfaces import ICodeCompiler

# TODO: docs checkpoint
class Py3FunctionCompiler(ICodeCompiler):
    '''
        Compiles string to function object
    '''

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
        codeObject = compile(foo, "fake", "exec")
        mem = {}
        exec(codeObject, mem)
        return mem[self._fooName]


class Py3CodeCompiler(ICodeCompiler):
    """Generic python code compiler"""
    def __init__(self):
        super(Py3CodeCompiler, self).__init__()

    def compile(self, code, moduleName="fake", scope={}):
        codeObject = compile(code, moduleName, "exec")
        exec(codeObject, scope)
        return scope
