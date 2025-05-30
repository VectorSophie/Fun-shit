using System;
using System.Collections.Generic;

class Skill
{
    public int Base { get; }
    public int Coin { get; }
    public int Count { get; }

    public Skill(int basePower, int coin, int count)
    {
        Base = basePower;
        Coin = coin;
        Count = count;
    }

    public Dictionary<int, double> PowerDistribution()
    {
        var dist = new Dictionary<int, double>();
        for (int heads = 0; heads <= Count; heads++)
        {
            int power = Base + heads * Coin;
            double prob = BinomialCoefficient(Count, heads) / Math.Pow(2, Count);
            if (!dist.ContainsKey(power))
                dist[power] = 0;
            dist[power] += prob;
        }
        return dist;
    }

    private static double BinomialCoefficient(int n, int k)
    {
        if (k < 0 || k > n) return 0;
        if (k == 0 || k == n) return 1;

        double res = 1;
        for (int i = 1; i <= k; i++)
        {
            res *= (n - (k - i));
            res /= i;
        }
        return res;
    }
}

class ClashTreeSolver
{
    private Dictionary<(int, int), double> memo = new Dictionary<(int, int), double>();
    private Skill skill1;
    private Skill skill2;

    public ClashTreeSolver(Skill s1, Skill s2)
    {
        skill1 = s1;
        skill2 = s2;
    }

    public double Solve()
    {
        return Recurse(skill1.Count, skill2.Count);
    }

    private double Recurse(int c1, int c2)
    {
        if (c1 <= 0) return 0.0;
        if (c2 <= 0) return 1.0;

        var key = (c1, c2);
        if (memo.ContainsKey(key)) return memo[key];

        var s1 = new Skill(skill1.Base, skill1.Coin, c1);
        var s2 = new Skill(skill2.Base, skill2.Coin, c2);

        var dist1 = s1.PowerDistribution();
        var dist2 = s2.PowerDistribution();

        double total = 0.0;

        foreach (var p1 in dist1)
        {
            foreach (var p2 in dist2)
            {
                double clash = p1.Value * p2.Value;

                if (p1.Key > p2.Key)
                    total += clash * Recurse(c1, c2 - 1);
                else if (p2.Key > p1.Key)
                    total += clash * Recurse(c1 - 1, c2);
                else
                    total += clash * Recurse(c1 - 1, c2 - 1);
            }
        }

        memo[key] = total;
        return total;
    }
}

class Program
{
    static Skill ReadSkill()
    {
        var input = Console.ReadLine().Split();
        int basePower = int.Parse(input[0]);
        int coin = int.Parse(input[1]);
        int count = int.Parse(input[2]);
        return new Skill(basePower, coin, count);
    }

    static void Main(string[] args)
    {
        Skill skill1 = ReadSkill();
        Skill skill2 = ReadSkill();

        var solver = new ClashTreeSolver(skill1, skill2);
        double probability = solver.Solve();
        Console.WriteLine(probability);
    }
}
