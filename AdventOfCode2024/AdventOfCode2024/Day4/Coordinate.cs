namespace AdventOfCode2024.Day4;

public readonly record struct Coordinate(int Row, int Column)
{
    public Coordinate Move(Direction direction)
    {
        return direction switch
        {
            Direction.North => this with { Row = Row - 1 },
            Direction.Northwest => new Coordinate(Row - 1, Column - 1),
            Direction.West => this with { Column = Column - 1 },
            Direction.Southwest => new Coordinate(Row + 1, Column - 1),
            Direction.South => this with { Row = Row + 1 },
            Direction.Southeast => new Coordinate(Row + 1, Column + 1),
            Direction.East => this with { Column = Column + 1 },
            Direction.Northeast => new Coordinate(Row - 1, Column + 1),
            _ => throw new ArgumentOutOfRangeException(nameof(direction), direction, null)
        };
    }
    
    public static IEnumerable<Coordinate> Range(int nrOfRows, int nrOfColumns)
    {
        for (var row = 0; row < nrOfRows; row += 1)
        {
            for (var column = 0; column < nrOfColumns; column += 1)
            {
                yield return new Coordinate(row, column);
            }
        }
    }
}