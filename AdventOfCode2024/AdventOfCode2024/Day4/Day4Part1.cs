namespace AdventOfCode2024.Day4;

public static class Day4Part1
{
    private const string SearchString = "XMAS";
    
    public static void Run(string filepath)
    {
        Grid grid = Grid.GetFromFile(filepath);

        var result = 0;

        // ReSharper disable once LoopCanBeConvertedToQuery
        foreach (Coordinate coordinate in Coordinate.Range(grid.NrOfRows, grid.NrOfColumns))
        {
            if (grid.At(coordinate) != SearchString[0])
            {
                continue;
            }
            
            // ReSharper disable once LoopCanBeConvertedToQuery
            foreach (Direction direction in Enum.GetValues<Direction>())
            {
                if (GridContainsString(grid, coordinate, direction, SearchString))
                {
                    result += 1;
                }
            }
        }
        
        Console.WriteLine(result);
    }

    private static bool GridContainsString(
        Grid grid,
        Coordinate startCoordinate,
        Direction direction,
        string searchString)
    {
        Coordinate currentCoordinate = startCoordinate;
        var currentString = "";
        
        while (grid.ContainsCoordinate(currentCoordinate) && currentString.Length < searchString.Length)
        {
            currentString += grid.At(currentCoordinate);
            currentCoordinate = currentCoordinate.Move(direction);
        }

        return currentString == searchString;
    }
}