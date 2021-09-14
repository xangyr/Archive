class Golfer:
    def __init__(self,Name = '',Score=0):
        self.Name = Name
        self.Score = Score
    def __str__(self):
        return self.Name + ':' + str(self.Score)
    def __gt__(self,other):
        if self.Score > other.Score:
            return False
        else:
            return True
class Queue:
    def __init__(self):
        self.items = []

    def insert(self,Golfer):
        self.items.append(Golfer)

    def __str__(self):
        return ' '.join([i.Name + ':' + str(i.Score) for i in self.items]) 

    def remove(self):
        maxi = 0
        for i in range(1,len(self.items)):
            if self.items[i] > self.items[maxi]:
                maxi = i
        item = self.items[maxi]
        del self.items[maxi]
        return item
    def is_empty(self):
        return self.items == []
if __name__ == '__main__':
    golfer = Queue()
    for x in range(3):
        Name = input('Input a name:' )
        Score = int(input('Input a Score:' ))
        Golfers = Golfer(Name,Score)
        golfer.insert(Golfers)
    print(golfer)
    while not golfer.is_empty():
        print(golfer.remove())