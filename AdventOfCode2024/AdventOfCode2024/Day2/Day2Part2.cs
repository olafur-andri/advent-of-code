namespace AdventOfCode2024.Day2;

public static class Day2Part2
{
    public static void Run()
    {
        Input input = Input.GetFromFile();

        int result = input.Reports.Where(ReportToleratesAtMostOneBadLevel).Count();
        
        Console.WriteLine(result);
    }

    private static bool ReportToleratesAtMostOneBadLevel(Report report)
    {
        for (var i = 0; i < report.Levels.Count; i += 1)
        {
            if (ReportIsSafe(LevelRemovedFromReport(report, i)))
            {
                return true;
            }
        }

        return false;
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
    
    private static Report LevelRemovedFromReport(Report report, int index)
    {
        List<Level> newLevels = report.Levels.Where((_, i) => i != index).ToList();
        return new Report(newLevels);
    }

    public static void Test()
    {
        var testReport = new Report([ 1, 3, 2, 4, 5 ]);
        
        Console.WriteLine(ReportToleratesAtMostOneBadLevel(testReport));
    }
}