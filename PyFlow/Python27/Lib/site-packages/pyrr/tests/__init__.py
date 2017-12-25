import unittest

if not hasattr(unittest, 'skip'):
    def skip(fn):
        def empty(*args, **kwargs):
            pass
        return empty
    unittest.skip = skip