from collections import defaultdict
from functools import lru_cache
from itertools import product
import math

class Skill:
    def __init__(self, base, coin, count):
        self.base = base
        self.coin = coin
        self.count = count

    def power_distribution(self):
        dist = defaultdict(float)
        for heads in range(self.count + 1):
            power = self.base + heads * self.coin
            prob = math.comb(self.count, heads) / (2 ** self.count)
            dist[power] += prob
        return dist

def clash_tree(skill1, skill2):
    @lru_cache(maxsize=None)
    def recurse(c1, c2):
        if c1 <= 0: return 0.0  
        if c2 <= 0: return 1.0  

        s1 = Skill(skill1.base, skill1.coin, c1)
        s2 = Skill(skill2.base, skill2.coin, c2)

        dist1 = s1.power_distribution()
        dist2 = s2.power_distribution()

        total = 0.0

        for p1, prob1 in dist1.items():
            for p2, prob2 in dist2.items():
                clash = prob1 * prob2
                if p1 > p2:
                    total += clash * recurse(c1, c2 - 1)
                elif p2 > p1:
                    total += clash * recurse(c1 - 1, c2)
                else:
                    total += clash * recurse(c1-1, c2-1)
        return total

    return recurse(skill1.count, skill2.count)
    
def read():
    base, coin, count = map(int,input().split())
    return Skill(base, coin, count)

if __name__ == "__main__":
    skill1 = read()
    skill2 = read()
    prob = clash_tree(skill1, skill2)
    print(prob)