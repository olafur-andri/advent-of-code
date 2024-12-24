namespace AdventOfCode2024.Day1;

public static class Day1Part2
{
    public static void Run()
    {
        var input = Input.GetFromInputFile();
        
        // count occurrences of each number in the right list
        Dictionary<LocationId, int> getNrOfOccurrences = input.RightList
            .GroupBy(id => id)
            .ToDictionary(grouping => grouping.Key, x => x.Count());

        int result = input.LeftList
            .Select(id => id * getNrOfOccurrences.GetValueOrDefault(id, 0))
            .Sum();
        
        Console.WriteLine(result);
    }
}