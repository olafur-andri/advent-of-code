namespace AdventOfCode2024.Day4;

public static class Day4Part2
{
    public static void Run(string filepath)
    {
        Grid grid = Grid.GetFromFile(filepath);

        var result = 0;

        // ReSharper disable once LoopCanBeConvertedToQuery
        foreach (Coordinate coordinate in Coordinate.Range(grid.NrOfRows, grid.NrOfColumns))
        {
            if (grid.At(coordinate) != 'A')
            {
                continue;
            }
            
            Coordinate topLeftCoordinate = coordinate.Move(Direction.Northwest);
            bool topLeftIsGood =
                GridContainsString(grid, topLeftCoordinate, Direction.Southeast, "MAS") ||
                GridContainsString(grid, topLeftCoordinate, Direction.Southeast, "SAM");

            if (!topLeftIsGood)
            {
                continue;
            }
                
            Coordinate topRightCoordinate = coordinate.Move(Direction.Northeast);
            bool topRightIsGood =
                GridContainsString(grid, topRightCoordinate, Direction.Southwest, "MAS") ||
                GridContainsString(grid, topRightCoordinate, Direction.Southwest, "SAM");

            if (!topRightIsGood)
            {
                continue;
            }

            result += 1;
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