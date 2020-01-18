import smartpy as sp

class Dama(sp.Contract):
    def __init__(self, players, board, currentPlayer):
        sp.default_verify_message=sp.unit
        self.add_flag('unit_failwith')
        self.init(
            players = players,
            currentPlayer = currentPlayer,
            winner = -1,
            isOver = False,
            board = sp.matrix(board)
        )
    
    @sp.entry_point
    def playerMove(self, params):
        
        sp.verify(sp.sender == self.data.players[self.data.currentPlayer])
        
        sp.verify(~self.data.isOver)
        
        
        sp.verify((params.start_x >= 0) & (params.start_x < 8), message = "AAAAA") 
        sp.verify((params.start_y >= 0) & (params.start_y < 8)) 
        sp.verify((params.target_x >= 0) & (params.target_x < 8)) 
        sp.verify((params.target_y >= 0) & (params.target_y < 8)) 
        
        
        piece = self.data.board[params.start_x][params.start_y]
        sp.verify(abs(piece) == self.data.currentPlayer)
        
        
        sp.verify(self.data.board[params.target_x][params.target_y] == 0)
        
        
        sp.verify(((self.data.currentPlayer == 1) & (params.start_y <= params.target_y)) | ((self.data.currentPlayer == 2) & (params.start_y >= params.target_y)) | (self.data.board[params.start_x][params.start_y] < 0))
        
        
        deltaX = abs(params.target_x - params.start_x)
        deltaY = abs(params.target_y - params.start_y)
        
        sp.verify((deltaX == 0) | (deltaY == 0))
        
        
        shouldJump = sp.local('shouldJump', False)
        enemyPlayer = sp.local('enemyPlayer', abs(3 - sp.to_int(self.data.currentPlayer)))
        
        
        sp.for x in sp.range(0, 8):
            sp.for y in sp.range(0, 8):
                sp.if abs(self.data.board[x][y]) == self.data.currentPlayer:
                    # left
                    sp.if x > 1:
                        sp.for k in sp.range(0, x):
                            sp.if ~shouldJump.value & (self.data.board[k][y] == 0) & (abs(self.data.board[k+1][y]) == enemyPlayer.value) & (((self.data.board[x][y] > -1) & (k == x-2)) | (self.data.board[x][y] < 0)):
                                shouldJump.value =(True)
                                sp.for kk in sp.range(k+2, x):
                                    sp.if self.data.board[kk][y] != 0:
                                        shouldJump.value =(False)
                    # right
                    sp.if x < 6:
                        sp.for k in sp.range(x+1, 7):
                            sp.if ~shouldJump.value & (self.data.board[k+1][y] == 0) & (abs(self.data.board[k][y]) == enemyPlayer.value) & (((self.data.board[x][y] > -1) & (k == x+1)) | (self.data.board[x][y] < 0)):
                                shouldJump.value =(True)
                                sp.for kk in sp.range(x+1, k):
                                    sp.if self.data.board[kk][y] != 0:
                                        shouldJump.value =(False)
                    # top
                    sp.if (y < 6) & ((self.data.board[x][y] != 2) | (abs(self.data.board[x][y]) < 0)):
                        sp.for k in sp.range(y+1, 7):
                            sp.if ~shouldJump.value & (self.data.board[x][k+1] == 0) & (abs(self.data.board[x][k]) == enemyPlayer.value) & (((self.data.board[x][y] > -1) & (k == y+1)) | (self.data.board[x][y] < 0)):
                                shouldJump.value =(True)
                                sp.for kk in sp.range(y+1, k):
                                    sp.if self.data.board[x][kk] != 0:
                                        shouldJump.value =(False)
                    # bottom
                    sp.if (y > 1) & ((self.data.board[x][y] != 1) | (abs(self.data.board[x][y]) < 0)):
                        sp.for k in sp.range(0, y):
                            sp.if ~shouldJump.value & (self.data.board[x][k] == 0) & (abs(self.data.board[x][k+1]) == enemyPlayer.value) & (((self.data.board[x][y] > -1) & (k == y-2)) | (self.data.board[x][y] < 0)):
                                shouldJump.value =(True)
                                sp.for kk in sp.range(k+2, y):
                                    sp.if self.data.board[x][kk] != 0:
                                        shouldJump.value =(False)
   
        sp.if shouldJump.value:
            
            sp.verify(((deltaY < 3) & (deltaX < 3)) | (piece < 0))
        sp.else:
            
            sp.verify(((deltaY < 2) & (deltaX < 2)) | (piece < 0))
        
        
        self.move(params.start_x, params.start_y, params.target_x, params.target_y)
        
        sp.if shouldJump.value:
            
            sp.if deltaX == 0:
                sp.if params.start_y < params.target_y:
                    sp.verify(abs(self.data.board[params.target_x][params.target_y - 1]) != self.data.currentPlayer)
                    sp.verify(abs(self.data.board[params.target_x][params.target_y - 1]) != 0)
                    self.data.board[params.target_x][params.target_y - 1] = 0
                sp.else:
                    sp.verify(abs(self.data.board[params.target_x][params.target_y + 1]) != self.data.currentPlayer)
                    sp.verify(abs(self.data.board[params.target_x][params.target_y + 1]) != 0)
                    self.data.board[params.target_x][params.target_y + 1] = 0
            sp.else:
                sp.if params.target_x > params.start_x:
                    sp.verify(abs(self.data.board[params.target_x - 1][params.target_y]) != self.data.currentPlayer)
                    sp.verify(abs(self.data.board[params.target_x - 1][params.target_y]) != 0)
                    self.data.board[params.target_x - 1][params.target_y] = 0
                sp.else:
                    sp.verify(abs(self.data.board[params.target_x + 1][params.target_y]) != self.data.currentPlayer)
                    sp.verify(abs(self.data.board[params.target_x + 1][params.target_y]) != 0)
                    self.data.board[params.target_x + 1][params.target_y] = 0
        
        
        sp.if (((params.target_y == 7) & (self.data.currentPlayer == 1)) | ((params.target_y == 0) & (self.data.currentPlayer == 2))) & (self.data.board[params.target_x][params.target_y] > 0):
            self.data.board[params.target_x][params.target_y] = -self.data.board[params.target_x][params.target_y]

        
        
        continueMove = sp.local('continueMove', False)
        # left
        sp.if params.target_x > 1:
            sp.for k in sp.range(0, params.target_x):
                sp.if (~continueMove.value) & (self.data.board[k][params.target_y] == 0) & (abs(self.data.board[k+1][params.target_y]) == enemyPlayer.value) & (((self.data.board[params.target_x][params.target_y] > -1) & (k == params.target_x-2)) | (self.data.board[params.target_x][params.target_y] < 0)):
                    continueMove.value =(True)
                    sp.for kk in sp.range(k+2, params.target_x):
                        sp.if self.data.board[kk][params.target_y] != 0:
                            continueMove.value =(False)
        # right
        sp.if params.target_x < 6:
            sp.for k in sp.range(params.target_x, 7):
                sp.if (~continueMove.value) & (self.data.board[k][params.target_y] == 0) & (abs(self.data.board[k-1][params.target_y]) == enemyPlayer.value) & (((self.data.board[params.target_x][params.target_y] > -1) & (k == params.target_y+2)) | (self.data.board[params.target_x][params.target_y] < 0)):
                    continueMove.value =(True)
                    sp.for kk in sp.range(params.target_x, k):
                        sp.if self.data.board[kk][params.target_y] != 0:
                            continueMove.value =(False)
        # top
        sp.if params.target_y < 6:
            sp.for k in sp.range(params.target_y+1, 7):
                sp.if (~continueMove.value) & (self.data.board[params.target_x][k+1] == 0) & (abs(self.data.board[params.target_x][k]) == enemyPlayer.value) & (((self.data.board[params.target_x][params.target_y] > -1) & (k == params.target_y+1)) | (self.data.board[params.target_x][params.target_y] < 0)):
                    continueMove.value =(True)
                    sp.for kk in sp.range(params.target_y+1, k):
                        sp.if self.data.board[params.target_x][kk] != 0:
                            continueMove.value =(False)
        # bottom
        sp.if params.target_y > 1:
            sp.for k in sp.range(0, params.target_y):
                sp.if (~continueMove.value) & (self.data.board[params.target_x][k] == 0) & (abs(self.data.board[params.target_x][k+1]) == enemyPlayer.value) & (((self.data.board[params.target_x][params.target_y] > -1) & (k == params.target_y-2)) | (self.data.board[params.target_x][params.target_y] < 0)):
                    continueMove.value =(True)
                    sp.for kk in sp.range(k+2, params.target_y):
                        sp.if self.data.board[params.target_x][kk] != 0:
                            continueMove.value =(False)
           
        sp.if ~(continueMove.value & shouldJump.value):                     
                sp.if self.data.currentPlayer == 1:
                    self.data.currentPlayer = 2
                sp.else:
                    self.data.currentPlayer = 1
            
        
        player1Damas = sp.local('player1Damas', 0)
        player1DamasKing = sp.local('player1DamasKing', 0)
        player2Damas = sp.local('player2Damas', 0)
        player2DamasKing = sp.local('player2DamasKing', 0)

        sp.for x in sp.range(0, 8):
            sp.for y in sp.range(0, 8):
                sp.if self.data.board[x][y] == 1:
                    player1Damas.value =(player1Damas.value + 1)
                    
                sp.if self.data.board[x][y] == -1:
                    player1DamasKing.value =(player1DamasKing.value + 1)
                    
                sp.if self.data.board[x][y] == 2:
                    player2Damas.value =(player2Damas.value + 1)
                
                sp.if self.data.board[x][y] == -2:
                    player2DamasKing.value =(player2DamasKing.value + 1)
                    
        
        sp.if (player1Damas.value == 0) & (player1DamasKing.value == 0):
            self.data.isOver = True
            self.data.winner = 2
        
        sp.if (player2Damas.value == 0) & (player2DamasKing.value == 0):
            self.data.isOver = True
            self.data.winner = 1
            
        sp.if (player1Damas.value == 1) & (player1DamasKing.value == 0) & (player2DamasKing.value > 0):
            self.data.isOver = True
            self.data.winner = 2
            
        sp.if (player2Damas.value == 1) & (player2DamasKing.value == 0) & (player1DamasKing.value > 0):
            self.data.isOver = True
            self.data.winner = 1
        
    
    
    def move(self, start_x, start_y, target_x, target_y):
        self.data.board[target_x][target_y] = self.data.board[start_x][start_y]
        self.data.board[start_x][start_y] = 0


@sp.add_test(name = "Test-Black-Dama-Sequencial-Jumps-Left")
def test():
    
    scenario = sp.test_scenario()
    
    playersMap = {}
    playersMap[0] = sp.address("tz1XtadTb6vAKdnn1Ljvp2Pa9SK5UbLssxzd")
    playersMap[1] = sp.address("tz1R1ycY61pBEY7s23Fj8nP3rQLccE2t9kQy")
    
    currentPlayer = 1
    board = [
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,0,2,0],
        [0,1,1,0,2,0,2,0],
        [0,1,1,0,0,0,2,0],
        [0,1,1,0,2,0,2,0],
        [0,1,1,0,1,0,2,0]
    ]
    
    
    c = Dama(playersMap, board, currentPlayer)
    scenario.register(c, show = True)
    
    scenario += c.playerMove(start_x=7, start_y=4, target_x=5, target_y=4).run(sender=playersMap[1], valid = True)
    
    scenario.verify((c.data.currentPlayer == 1) & (c.data.board == sp.matrix([
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,0,2,0],
        [0,1,1,0,2,0,2,0],
        [0,1,1,0,1,0,2,0],
        [0,1,1,0,0,0,2,0],
        [0,1,1,0,0,0,2,0]
    ])))


@sp.add_test(name = "Test-Move-Black-King-Dama-Backwards")
def test():
    
    scenario = sp.test_scenario()
    
    playersMap = {}
    playersMap[0] = sp.address("tz1XtadTb6vAKdnn1Ljvp2Pa9SK5UbLssxzd")
    playersMap[1] = sp.address("tz1R1ycY61pBEY7s23Fj8nP3rQLccE2t9kQy")
    
    currentPlayer = 1
    board = [
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,2,0,2,-1]
    ]
    
    
    c = Dama(playersMap, board, currentPlayer)
    scenario.register(c, show = True)
    
    scenario += c.playerMove(start_x=7, start_y=7, target_x=7, target_y=5).run(sender=playersMap[1], valid = True)
    
    scenario.verify((c.data.currentPlayer == 1) & (c.data.board == sp.matrix([
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,2,-1,0,0]
    ])))
      


@sp.add_test(name = "Test-Move-Black-Dama")
def test():
    
    scenario = sp.test_scenario()
    
    playersMap = {}
    playersMap[0] = sp.address("tz1XtadTb6vAKdnn1Ljvp2Pa9SK5UbLssxzd")
    playersMap[1] = sp.address("tz1R1ycY61pBEY7s23Fj8nP3rQLccE2t9kQy")
    
    currentPlayer = 1
    board = [
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0]
    ]
    
    
    c = Dama(playersMap, board, currentPlayer)
    scenario.register(c, show = True)
    
    scenario += c.playerMove(start_x=0, start_y=2, target_x=0, target_y=3).run(sender=playersMap[currentPlayer], valid = True)
      

@sp.add_test(name = "Test-Black-Dama-Sequencial-Jumps")
def test():
    
    scenario = sp.test_scenario()
    
    playersMap = {}
    playersMap[1] = sp.address("tz1XtadTb6vAKdnn1Ljvp2Pa9SK5UbLssxzd")
    playersMap[2] = sp.address("tz1R1ycY61pBEY7s23Fj8nP3rQLccE2t9kQy")
    
    currentPlayer = 1
    board = [
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,2,0,2,0,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0]
    ]
    
    
    c = Dama(playersMap, board, currentPlayer)
    scenario.register(c, show = True)
    
    scenario += c.playerMove(start_x=2, start_y=2, target_x=2, target_y=4).run(sender=playersMap[1], valid = True)
    
    scenario.verify((c.data.currentPlayer == 1) & (c.data.board == sp.matrix([
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,0,0,1,2,0,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0]
    ])))
    
    scenario += c.playerMove(start_x=2, start_y=4, target_x=2, target_y=6).run(sender=playersMap[1], valid = True)

    scenario.verify((c.data.currentPlayer == 2) & (c.data.board == sp.matrix([
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,0,0,0,0,1,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0]
    ])))
    

@sp.add_test(name = "Test-White-Dama-Sequencial-Jumps")
def test():
    
    scenario = sp.test_scenario()
    
    playersMap = {}
    playersMap[1] = sp.address("tz1XtadTb6vAKdnn1Ljvp2Pa9SK5UbLssxzd")
    playersMap[2] = sp.address("tz1R1ycY61pBEY7s23Fj8nP3rQLccE2t9kQy")
    
    currentPlayer = 2
    board = [
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,0,1,0,1,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0]
    ]
    
    
    c = Dama(playersMap, board, currentPlayer)
    scenario.register(c, show = True)
    
    scenario += c.playerMove(start_x=2, start_y=5, target_x=2, target_y=3).run(sender=playersMap[2], valid = True)
    
    scenario.verify((c.data.currentPlayer == 2) & (c.data.board == sp.matrix([
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,0,1,2,0,0,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0]
    ])))
    
    scenario += c.playerMove(start_x=2, start_y=3, target_x=2, target_y=1).run(sender=playersMap[2], valid = True)
    
    scenario.verify((c.data.currentPlayer == 1) & (c.data.board == sp.matrix([
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,2,0,0,0,0,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0]
    ])))
    

@sp.add_test(name = "Test-Black-King-Sequencial-Jumps")
def test():
    
    scenario = sp.test_scenario()
    
    playersMap = {}
    playersMap[1] = sp.address("tz1XtadTb6vAKdnn1Ljvp2Pa9SK5UbLssxzd")
    playersMap[2] = sp.address("tz1R1ycY61pBEY7s23Fj8nP3rQLccE2t9kQy")
    
    currentPlayer = 1
    board = [
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,-1,-2,0,0,-2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0]
    ]
    
    
    c = Dama(playersMap, board, currentPlayer)
    scenario.register(c, show = True)

    scenario += c.playerMove(start_x=2, start_y=2, target_x=2, target_y=4).run(sender=playersMap[1], valid = True)
    
    scenario.verify((c.data.currentPlayer == 1) & (c.data.board == sp.matrix([
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,0,0,-1,0,-2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0]
    ])))
    
    scenario += c.playerMove(start_x=2, start_y=4, target_x=2, target_y=7).run(sender=playersMap[1], valid = True)
    
    scenario.verify((c.data.currentPlayer == 2) & (c.data.board == sp.matrix([
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,0,0,0,0,0,-1],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0]
    ])))
    

@sp.add_test(name = "Test-White-King-Sequencial-Jumps")
def test():
    
    scenario = sp.test_scenario()
    
    playersMap = {}
    playersMap[1] = sp.address("tz1XtadTb6vAKdnn1Ljvp2Pa9SK5UbLssxzd")
    playersMap[2] = sp.address("tz1R1ycY61pBEY7s23Fj8nP3rQLccE2t9kQy")
    
    currentPlayer = 2
    board = [
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,-1,0,0,-1,-2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0]
    ]
    
    
    c = Dama(playersMap, board, currentPlayer)
    scenario.register(c, show = True)

    scenario += c.playerMove(start_x=2, start_y=5, target_x=2, target_y=3).run(sender=playersMap[2], valid = True)
    
    scenario.verify((c.data.currentPlayer == 2) & (c.data.board == sp.matrix([
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,-1,0,-2,0,0,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0]
    ])))
    
    scenario += c.playerMove(start_x=2, start_y=3, target_x=2, target_y=0).run(sender=playersMap[2], valid = True)
    
    scenario.verify((c.data.currentPlayer == 1) & (c.data.board == sp.matrix([
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [-2,0,0,0,0,0,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0]
    ])))
    

@sp.add_test(name = "Test-Black-Dama-MovingJumping-Backwards")
def test():
    
    scenario = sp.test_scenario()
    
    playersMap = {}
    playersMap[1] = sp.address("tz1XtadTb6vAKdnn1Ljvp2Pa9SK5UbLssxzd")
    playersMap[2] = sp.address("tz1R1ycY61pBEY7s23Fj8nP3rQLccE2t9kQy")
    
    currentPlayer = 1
    board = [
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,2,1,0,1,0,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0]
    ]
    
    
    c = Dama(playersMap, board, currentPlayer)
    scenario.register(c, show = True)

    scenario += c.playerMove(start_x=2, start_y=4, target_x=2, target_y=3).run(sender=playersMap[1], valid = False)
    scenario += c.playerMove(start_x=2, start_y=2, target_x=2, target_y=0).run(sender=playersMap[1], valid = False)
    

@sp.add_test(name = "Test-White-Dama-MovingJumping-Backwards")
def test():
    
    scenario = sp.test_scenario()
    
    playersMap = {}
    playersMap[1] = sp.address("tz1XtadTb6vAKdnn1Ljvp2Pa9SK5UbLssxzd")
    playersMap[2] = sp.address("tz1R1ycY61pBEY7s23Fj8nP3rQLccE2t9kQy")
    
    currentPlayer = 2
    board = [
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,0,2,0,2,1,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0]
    ]
    
    
    c = Dama(playersMap, board, currentPlayer)
    scenario.register(c, show = True)

    scenario += c.playerMove(start_x=2, start_y=3, target_x=2, target_y=4).run(sender=playersMap[currentPlayer], valid = False)
    
    scenario += c.playerMove(start_x=2, start_y=5, target_x=2, target_y=7).run(sender=playersMap[currentPlayer], valid = False)
    

@sp.add_test(name = "Test-Dama-Moving-Left-and-Right")
def test():
    
    scenario = sp.test_scenario()
    
    playersMap = {}
    playersMap[1] = sp.address("tz1XtadTb6vAKdnn1Ljvp2Pa9SK5UbLssxzd")
    playersMap[2] = sp.address("tz1R1ycY61pBEY7s23Fj8nP3rQLccE2t9kQy")
    
    currentPlayer = 2
    board = [
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,0,2,0,2,1,0],
        [0,1,0,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0]
    ]
    
    
    c = Dama(playersMap, board, currentPlayer)
    scenario.register(c, show = True)

    scenario += c.playerMove(start_x=2, start_y=3, target_x=3, target_y=3).run(sender=playersMap[currentPlayer], valid = True)
    
    scenario.verify((c.data.currentPlayer == 1) & (c.data.board == sp.matrix([
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,0,0,0,2,1,0],
        [0,1,0,2,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0]
    ])))
    
    scenario += c.playerMove(start_x=1, start_y=2, target_x=2, target_y=2).run(sender=playersMap[1], valid = True)
    
    scenario.verify((c.data.currentPlayer == currentPlayer) & (c.data.board == sp.matrix([
        [0,1,1,0,0,2,2,0],
        [0,1,0,0,0,2,2,0],
        [0,1,1,0,0,2,1,0],
        [0,1,0,2,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0]
    ])))
    

@sp.add_test(name = "Test-Dama-Jumping-Left-Right")
def test():
    
    scenario = sp.test_scenario()
    
    playersMap = {}
    playersMap[1] = sp.address("tz1XtadTb6vAKdnn1Ljvp2Pa9SK5UbLssxzd")
    playersMap[2] = sp.address("tz1R1ycY61pBEY7s23Fj8nP3rQLccE2t9kQy")
    
    currentPlayer = 1
    board = [
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,0,2,2,0,2,0],
        [0,1,0,1,1,0,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0]
    ]
    
    
    c = Dama(playersMap, board, currentPlayer)
    scenario.register(c, show = True)

    scenario += c.playerMove(start_x=3, start_y=3, target_x=1, target_y=3).run(sender=playersMap[currentPlayer], valid = True)
    
    scenario.verify((c.data.currentPlayer == 2) & (c.data.board == sp.matrix([
        [0,1,1,0,0,2,2,0],
        [0,1,1,1,0,2,2,0],
        [0,1,0,0,2,0,2,0],
        [0,1,0,0,1,0,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0]
    ])))
    
    scenario += c.playerMove(start_x=2, start_y=4, target_x=4, target_y=4).run(sender=playersMap[2], valid = True)
    
    scenario.verify((c.data.currentPlayer == currentPlayer) & (c.data.board == sp.matrix([
        [0,1,1,0,0,2,2,0],
        [0,1,1,1,0,2,2,0],
        [0,1,0,0,0,0,2,0],
        [0,1,0,0,0,0,2,0],
        [0,1,1,0,2,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0]
    ])))
    

@sp.add_test(name = "Test-King-Moving-Left-and-Right")
def test():
    
    scenario = sp.test_scenario()
    
    playersMap = {}
    playersMap[1] = sp.address("tz1XtadTb6vAKdnn1Ljvp2Pa9SK5UbLssxzd")
    playersMap[2] = sp.address("tz1R1ycY61pBEY7s23Fj8nP3rQLccE2t9kQy")
    
    currentPlayer = 2
    board = [
        [0,1,-1,0,0,2,2,0],
        [0,1,0,0,0,2,2,0],
        [0,1,1,0,-2,0,2,0],
        [0,1,0,0,0,2,2,0],
        [0,1,0,0,0,2,2,0],
        [0,1,1,-1,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0]
    ]
    
    
    c = Dama(playersMap, board, currentPlayer)
    scenario.register(c, show = True)

    scenario += c.playerMove(start_x=2, start_y=4, target_x=7, target_y=4).run(sender=playersMap[currentPlayer], valid = True)
    
    scenario.verify((c.data.currentPlayer == 1) & (c.data.board == sp.matrix([
        [0,1,-1,0,0,2,2,0],
        [0,1,0,0,0,2,2,0],
        [0,1,1,0,0,0,2,0],
        [0,1,0,0,0,2,2,0],
        [0,1,0,0,0,2,2,0],
        [0,1,1,-1,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,-2,2,2,0]
    ])))
    
    scenario += c.playerMove(start_x=5, start_y=3, target_x=0, target_y=3).run(sender=playersMap[1], valid = True)
    
    scenario.verify((c.data.currentPlayer == currentPlayer) & (c.data.board == sp.matrix([
        [0,1,-1,-1,0,2,2,0],
        [0,1,0,0,0,2,2,0],
        [0,1,1,0,0,0,2,0],
        [0,1,0,0,0,2,2,0],
        [0,1,0,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,0,2,2,0],
        [0,1,1,0,-2,2,2,0]
    ])))
    

@sp.add_test(name = "Test-Game-Over")
def test():
    
    scenario = sp.test_scenario()
    
    playersMap = {}
    playersMap[1] = sp.address("tz1XtadTb6vAKdnn1Ljvp2Pa9SK5UbLssxzd")
    playersMap[2] = sp.address("tz1R1ycY61pBEY7s23Fj8nP3rQLccE2t9kQy")
    
    currentPlayer = 2
    board = [
        [0,0,0,0,0,0,2,0],
        [0,0,0,0,0,0,2,0],
        [0,0,0,0,0,0,2,0],
        [0,0,0,0,0,0,2,0],
        [0,0,0,0,0,0,2,0],
        [0,-1,0,0,0,0,-2,0],
        [0,0,0,0,0,0,2,0],
        [0,1,0,0,0,0,2,0],
    ]
    
    
    c = Dama(playersMap, board, currentPlayer)
    scenario.register(c, show = True)

    scenario += c.playerMove(start_x=5, start_y=6, target_x=5, target_y=0).run(sender= playersMap[currentPlayer], valid = True)
    
    scenario.verify((c.data.isOver == True) & (c.data.winner == currentPlayer))