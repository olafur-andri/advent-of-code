namespace AdventOfCode2024.Day4;

public class Grid
{
    public int NrOfRows { get; }
    public int NrOfColumns { get; }
    
    private readonly char[,] _grid;

    private Grid(char[,] grid)
    {
        _grid = grid;
        NrOfRows = _grid.GetLength(0);
        NrOfColumns = _grid.GetLength(1);
    }

    public char At(Coordinate coordinate)
    {
        return _grid[coordinate.Row, coordinate.Column];
    }
    
    public bool ContainsCoordinate(Coordinate coordinate)
    {
        return coordinate.Row >= 0 && coordinate.Row < NrOfRows &&
               coordinate.Column >= 0 && coordinate.Column < NrOfColumns;
    }

    public static Grid GetFromFile(string filepath)
    {
        string[] lines = File.ReadAllLines(filepath);
        
        var grid = new char[lines.Length, lines[0].Length];

        for (var row = 0; row < lines.Length; row += 1)
        {
            for (var column = 0; column < lines[row].Length; column += 1)
            {
                grid[row, column] = lines[row][column];
            }
        }

        return new Grid(grid);
    }
}
