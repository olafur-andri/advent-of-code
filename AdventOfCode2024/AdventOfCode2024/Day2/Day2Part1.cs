namespace AdventOfCode2024.Day2;

public static class Day2Part1
{
    public static void Run()
    {
        Input input = Input.GetFromFile();

        int result = input.Reports.Where(ReportIsSafe).Count();
        
        Console.WriteLine(result);
    }
    
    private static bool ReportIsSafe(Report report)
    {
        List<int> differences = [];
        
        // get differences between levels
        for (var i = 0; i < report.Levels.Count - 1; i += 1)
        {
            int difference = report.Levels[i + 1] - report.Levels[i];
            differences.Add(difference);
        }

        bool isMonotonic = differences.All(difference => difference >= 0) ||
                           differences.All(difference => difference <= 0);

        if (!isMonotonic)
        {
            return false;
        }

        bool areWithinRange = differences.All(difference => Math.Abs(difference) is >= 1 and <= 3);

        return areWithinRange;
    }
}