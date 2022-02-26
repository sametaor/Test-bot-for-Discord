import random
from PIL import Image

games = []


def getGames():
    return games


def getGamesByUser(user: str):
    for game in games:
        userid = str(game.getId())
        if userid == user:
            return game


def getGamesByMessage(message: str):
    for game in games:
        if game.getMessageId == message:
            return game


class GameGrid:

    def __init__(self, user_id: str):
        self.message_id = ''
        self.imageDir = 'Cogsforbot/Twentyfortyeight/images/tiles/'
        self.matrix = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.grid = Image.open('Cogsforbot/Twentyfortyeight/images/grid.png').convert('RGBA')
        self.temp = 'Cogsforbot/Twentyfortyeight/images/temp/'
        self.defaultBg = 26
        self.user = user_id
        self.running = True
        self.image_id = ''

    def randomNumber(self):
        x = random.randint(0, 3)
        y = random.randint(0, 3)

        if self.matrix[x][y] == 0:
            self.matrix[x][y] = 2
        else:
            self.randomNumber()

    def drawMatrix(self):
        print('--------------')
        print(self.matrix[0])
        print(self.matrix[1])
        print(self.matrix[2])
        print(self.matrix[3])
        freshGrid = Image.open('Cogsforbot/Twentyfortyeight/images/grid.png').convert('RGBA')
        for y in range(0, 4):
            for x in range(0, 4):
                num = self.matrix[y][x]

                if num == 0:
                    continue

                iml = Image.open(self.imageDir + f'{num}.png').convert('RGBA')
                freshGrid.paste(iml, (x * 200, y * 200))
                iml.close()

        self.grid = freshGrid

    def slideUp(self):

        def shiftUp():
            for p in range(0, 3):
                for yin in range(1, 4):
                    for xin in range(0, 4):
                        if self.matrix[yin][xin] != 0 and self.matrix[yin - 1][xin] == 0:
                            self.matrix[yin - 1][xin] = self.matrix[yin][xin]
                            self.matrix[yin][xin] = 0

        shiftUp()
        for y in range(1, 4):
            for x in range(0, 4):
                if self.matrix[y][x] == self.matrix[y - 1][x]:
                    self.matrix[y - 1][x] = self.matrix[y - 1][x] * 2
                    self.matrix[y][x] = 0

        shiftUp()

    def slideDown(self):

        def shiftDown():
            for p in range(0, 3):
                for yin in range(2, -1, -1):
                    for xin in range(3, -1, -1):
                        if self.matrix[yin][xin] != 0 and self.matrix[yin + 1][xin] == 0:
                            self.matrix[yin + 1][xin] = self.matrix[yin][xin]
                            self.matrix[yin][xin] = 0

        shiftDown()
        for y in range(2, -1, -1):
            for x in range(3, -1, -1):
                if self.matrix[y][x] == self.matrix[y + 1][x]:
                    self.matrix[y + 1][x] = self.matrix[y + 1][x] * 2
                    self.matrix[y][x] = 0

        shiftDown()

    def slideLeft(self):

        def shiftLeft():
            for p in range(0, 3):
                for xin in range(1, 4):
                    for yin in range(0, 4):
                        if self.matrix[yin][xin] != 0 and self.matrix[yin][xin - 1] == 0:
                            self.matrix[yin][xin - 1] = self.matrix[yin][xin]
                            self.matrix[yin][xin] = 0

        shiftLeft()
        for x in range(1, 4):
            for y in range(0, 4):
                if self.matrix[y][x] == self.matrix[y][x - 1]:
                    self.matrix[y][x - 1] = self.matrix[y][x - 1] * 2
                    self.matrix[y][x] = 0

        shiftLeft()

    def slideRight(self):

        def shiftRight():
            for p in range(0, 3):
                for xin in range(2, -1, -1):
                    for yin in range(3, -1, -1):
                        if self.matrix[yin][xin] != 0 and self.matrix[yin][xin + 1] == 0:
                            self.matrix[yin][xin + 1] = self.matrix[yin][xin]
                            self.matrix[yin][xin] = 0

        shiftRight()
        for x in range(2, -1, -1):
            for y in range(3, -1, -1):
                if self.matrix[y][x] == self.matrix[y][x + 1]:
                    self.matrix[y][x + 1] = self.matrix[y][x + 1] * 2
                    self.matrix[y][x] = 0

        shiftRight()

    def start(self):
        if getGamesByUser(self.user):
            self.stop()
        self.running = True
        self.randomNumber()
        self.randomNumber()
        self.drawMatrix()
        games.append(self)

    def getGrid(self):
        return self.grid

    def stop(self):
        self.running = False
        self.grid.close()
        games.remove(self)

    def isRunning(self):
        return self.running

    def saveImage(self, user: str):
        self.grid.save(self.temp + f'{user}.png')

    def setMessageId(self, msgid: str):
        self.message_id = msgid

    def setImageId(self, imgid: str):
        self.image_id = imgid

    def getMessageId(self):
        return self.message_id

    def getId(self):
        return self.user


#All credits go to AbhigyaKrishna