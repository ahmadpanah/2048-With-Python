#coding:utf-8

import os, sys, random, msvcrt

class Game:
    def __init__(self, size):
        self.size  = size
        self.score = 0
        self.state = [0] * (self.size * self.size)
        self.add_random()

    def blank(self):
        return self.state.count(0)

    def add(self, num):
        pos = random.randint(0, self.blank()-1)
        for i in range(self.size * self.size):
            if self.state[i] == 0:
                if pos == 0: 
                    self.state[i] = num
                    break
                else:
                    pos -= 1
        return self.blank()

    def add_random(self):
        numbers = [2,2,2,2,2,2,4]
        return self.add(random.choice(numbers))

    def show(self):
        os.system("cls")
        print "[%s]\n%s" % (self.score, "-" * (self.size * 5 + 3))
        for i in range(self.size):
            print "|",
            for j in range(self.size):
                print "%4d" % self.state[i * self.size + j] if self.state[i * self.size + j] else "    ",
            print "|"
            if i == self.size - 1:
                print "-" * (self.size * 5 + 3)
            else:
                print "|%s |" %  ("     " * self.size)

    def move(self, d):
        old_state = self.state[:]
        if   d == "a": pass
        elif d == "w": self.rotate()        
        elif d == "d": self.rotate() or self.rotate()
        elif d == "s": self.rotate() or self.rotate() or self.rotate()
        else: return False
        for i in range(self.size): self.move_line(i)
        if d == "s": self.rotate()
        if d == "d": self.rotate() or self.rotate()
        if d == "w": self.rotate() or self.rotate() or self.rotate()
        if old_state == self.state: return False
        return True

    def move_line(self, line_no):
        moved, merged = [], False
        for i in range(self.size):
            n = self.state[line_no * self.size + i]
            if n: 
                if not merged and moved and moved[-1] == n : 
                    moved[-1] = n * 2
                    merged = True
                    self.score += n * 2
                else: moved.append(n)
        moved.extend([0]*(self.size - len(moved)))
        self.state[line_no * self.size: line_no * self.size + self.size] = moved

    def can_move(self):
        for d in ["w", "a", "s", "d"]:
            old_state = self.state
            try:
                if self.move(d):
                    return True
            finally:
                self.state = old_state
        return False

    

    def rotate(self):
        new_state = []
        for i in range(self.size - 1, -1, -1):
            for j in range(self.size):
                new_state.append(self.state[j * self.size + i])
        self.state = new_state
        
game = Game(5)
while 1:    
    game.show()
    if 2048 in game.state: 
        print "Win !"
        break
    if game.move(msvcrt.getch()):
        if not game.add_random():
            if not game.can_move():
                game.show()
                print "Game Over"
                break