namespace AdventOfCode2024.Day2;

public record Input(IReadOnlyList<Report> Reports)
{
    public static Input GetFromFile()
    {
        List<Report> reports = [];
        
        // ReSharper disable once LoopCanBeConvertedToQuery
        foreach (string line in File.ReadAllLines(@"Day2\input.txt"))
        {
            List<Level> levels = line
                .Split(' ')
                .Select(level => new Level(Convert.ToInt32(level)))
                .ToList();
            
            reports.Add(new Report(levels));
        }

        return new Input(reports);
    }
}

public record Report(IReadOnlyList<Level> Levels);

public record struct Level(int Value)
{
    public static implicit operator int(Level level) => level.Value;
}