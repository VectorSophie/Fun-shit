import random

class Skill:
    def __init__(self, base, coin, count):
        self.base = base
        self.coin = coin
        self.count = count

    def roll(self):
        return self.base + sum(random.randint(0, 1) for _ in range(self.count)) * self.coin

def simulate_clash(skill1, skill2):
    c1 = skill1.count
    c2 = skill2.count
    while c1 > 0 and c2 > 0:
        s1_roll = skill1.base + sum(random.randint(0, 1) for _ in range(c1)) * skill1.coin
        s2_roll = skill2.base + sum(random.randint(0, 1) for _ in range(c2)) * skill2.coin

        if s1_roll > s2_roll:
            c2 -= 1
        elif s2_roll > s1_roll:
            c1 -= 1
    return c1 > 0  

def monte_carlo(skill1, skill2, trials=100_000):
    wins = 0
    for _ in range(trials):
        if simulate_clash(skill1, skill2):
            wins += 1
    return wins / trials

def read():
    base, coin, count = map(int,input().split())
    return Skill(base, coin, count)

if __name__ == "__main__":
    skill1 = read()
    skill2 = read()
    prob = monte_carlo(skill1, skill2)
    print(prob)

