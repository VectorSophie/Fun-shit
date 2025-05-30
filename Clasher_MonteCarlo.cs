using System;

class Skill
{
    public int Base { get; }
    public int Coin { get; }
    public int Count { get; }

    public Skill(int baseValue, int coin, int count)
    {
        Base = baseValue;
        Coin = coin;
        Count = count;
    }

    public int Roll(Random rng)
    {
        int total = Base;
        for (int i = 0; i < Count; i++)
        {
            total += rng.Next(2) * Coin; // 0 or 1
        }
        return total;
    }
}

class Program
{
    static bool SimulateClash(Skill skill1, Skill skill2, Random rng)
    {
        int c1 = skill1.Count;
        int c2 = skill2.Count;

        while (c1 > 0 && c2 > 0)
        {
            int s1Roll = skill1.Base;
            for (int i = 0; i < c1; i++)
            {
                s1Roll += rng.Next(2) * skill1.Coin;
            }

            int s2Roll = skill2.Base;
            for (int i = 0; i < c2; i++)
            {
                s2Roll += rng.Next(2) * skill2.Coin;
            }

            if (s1Roll > s2Roll)
            {
                c2--;
            }
            else if (s2Roll > s1Roll)
            {
                c1--;
            }
        }

        return c1 > 0;
    }

    static double MonteCarlo(Skill skill1, Skill skill2, int trials = 100000)
    {
        Random rng = new Random();
        int wins = 0;

        for (int i = 0; i < trials; i++)
        {
            if (SimulateClash(skill1, skill2, rng))
            {
                wins++;
            }
        }

        return (double)wins / trials;
    }

    static Skill ReadSkill()
    {
        string[] parts = Console.ReadLine().Split();
        int baseValue = int.Parse(parts[0]);
        int coin = int.Parse(parts[1]);
        int count = int.Parse(parts[2]);
        return new Skill(baseValue, coin, count);
    }

    static void Main()
    {
        Skill skill1 = ReadSkill();
        Skill skill2 = ReadSkill();

        double probability = MonteCarlo(skill1, skill2);
        Console.WriteLine(probability);
    }
}
