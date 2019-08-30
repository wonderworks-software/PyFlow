import unittest


if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = loader.discover("PyFlow/Tests")
    unittest.TextTestRunner().run(suite)
