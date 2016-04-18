from colors import Colors


class PlayListMember(object):
    def __init__(self, movie, runMode):
        self.movie = movie
        self.runMode = runMode


class Score(object):
    LOCK_ITEMS, UNLOCK_ITEMS, SKIP_LOCK = range(3)

    FROM_CURRENT, FROM_START, NEW_ANIMATION_ONLY, ONLY_IF_VISIBLE = range(4)

    def __init__(self):
        self.index = {}
        self.playList = []

    def hasQueuedMovies(self):
        return len(self.playList) > 0

    def prepare(self, movie, runMode, lockMode):
        if lockMode == Score.LOCK_ITEMS:
            for item in movie:
                if runMode != Score.ONLY_IF_VISIBLE or item.demoItem().isVisible():
                    item.lockItem(True)
                    item.prepare()
        elif lockMode == Score.UNLOCK_ITEMS:
            for item in movie:
                if runMode != Score.ONLY_IF_VISIBLE or item.demoItem().isVisible():
                    item.lockItem(False)
                    item.prepare()
        else:
            for item in movie:
                if runMode != Score.ONLY_IF_VISIBLE or item.demoItem().isVisible():
                    item.prepare()

    def play(self, movie, runMode):
        if runMode == Score.NEW_ANIMATION_ONLY:
            for item in movie:
                if item.notOwnerOfItem():
                    item.play(True)
        elif runMode == Score.ONLY_IF_VISIBLE:
            for item in movie:
                if item.demoItem().isVisible():
                    item.play(runMode == Score.FROM_START)
        else:
            for item in movie:
                item.play(runMode == Score.FROM_START)

    def playMovie(self, indexName, runMode=FROM_START, lockMode=SKIP_LOCK):
        try:
            movie = self.index[indexName]
        except KeyError:
            return

        self.prepare(movie, runMode, lockMode)
        self.play(movie, runMode)

    def queueMovie(self, indexName, runMode=FROM_START, lockMode=SKIP_LOCK):
        try:
            movie = self.index[indexName]
        except KeyError:
            Colors.debug("Queuing movie:", indexName, "(does not exist)")
            return

        self.prepare(movie, runMode, lockMode)
        self.playList.append(PlayListMember(movie, runMode))
        Colors.debug("Queuing movie:", indexName)

    def playQue(self):
        for member in self.playList:
            self.play(member.movie, member.runMode)

        self.playList = []
        Colors.debug("********* Playing que *********")

    def insertMovie(self, indexName):
        movie = []
        self.index[indexName] = movie

        return movie
