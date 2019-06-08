

class Version(object):
    """docstring for Version"""
    def __init__(self, major, minor, patch):
        super(Version, self).__init__()
        assert(isinstance(major, int))
        assert(isinstance(minor, int))
        assert(isinstance(patch, int))
        self._major = major
        self._minor = minor
        self._patch = patch

    @staticmethod
    def fromString(string):
        major, minor, patch = string.split('.')
        return Version(int(major), int(minor), int(patch))

    def __str__(self):
        return "{0}.{1}.{2}".format(self.minor, self.major, self.patch)

    @property
    def major(self):
        return self._major

    @property
    def minor(self):
        return self._minor

    @property
    def patch(self):
        return self._patch

    def __eq__(self, other):
        return all([self.major == other.major,
                    self.minor == other.minor,
                    self.patch == other.patch])

    def __gt__(self, other):
        lhs = int("".join([str(self.major), str(self.minor), str(self.patch)]))
        rhs = int("".join([str(other.major), str(other.minor), str(other.patch)]))
        return lhs > rhs


def currentVersion():
    return Version(1, 1, 0)
