namespace AdventOfCode2024.Day3;

public record Input(string Instructions)
{
    public static Input GetFromFile()
    {
        return new Input(File.ReadAllText(@"Day3\input.txt"));
    }
}