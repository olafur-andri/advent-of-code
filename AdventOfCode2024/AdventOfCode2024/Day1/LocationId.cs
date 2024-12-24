namespace AdventOfCode2024.Day1;

public record struct LocationId(int Value)
{
    public static implicit operator int(LocationId locationId) => locationId.Value;
}