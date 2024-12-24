namespace AdventOfCode2024.Day1;

public static class Day1Part1
{
    public static void Run()
    {
        var input = Input.GetFromInputFile();
        
        List<LocationId> sortedLeftList = input.LeftList.OrderBy(x => x).ToList();
        List<LocationId> sortedRightList = input.RightList.OrderBy(x => x).ToList();
        
        int result = sortedLeftList
            .Zip(sortedRightList, (left, right) => Math.Abs(left - right)).Sum();
        
        Console.WriteLine(result);
    }
}