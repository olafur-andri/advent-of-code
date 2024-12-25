namespace AdventOfCode2024.Day5;

public record Input(IReadOnlyList<OrderingRule> OrderingRules, IReadOnlyList<PageNumberSequence> PageNumberSequences)
{
    public static Input GetFromFile(string filepath)
    {
        List<OrderingRule> orderingRules = [];
        List<PageNumberSequence> pageNumberSequences = [];
        
        string[] lines = File.ReadAllLines(filepath);

        foreach (string line in lines)
        {
            if (line.Contains('|')) // ordering rule line
            {
                List<PageNumber> pageNumbers = line
                    .Trim()
                    .Split('|')
                    .Select(int.Parse)
                    .Select(n => new PageNumber(n))
                    .ToList();
                
                orderingRules.Add(new OrderingRule(pageNumbers[0], pageNumbers[1]));
            }
            else if (line.Contains(',')) // page number sequence line
            {
                List<PageNumber> numbers = line
                    .Trim()
                    .Split(',')
                    .Select(int.Parse)
                    .Select(n => new PageNumber(n))
                    .ToList();
                
                pageNumberSequences.Add(new PageNumberSequence(numbers));
            }
        }

        return new Input(orderingRules, pageNumberSequences);
    }
}

public readonly record struct PageNumber(int Value)
{
    public static implicit operator int(PageNumber pageNumber) => pageNumber.Value;
    
    public static implicit operator PageNumber(int value) => new(value);
    
    public override string ToString()
    {
        return Value.ToString();
    }
}

public readonly record struct OrderingRule(PageNumber Left, PageNumber Right);

public record PageNumberSequence(IReadOnlyList<PageNumber> PageNumbers)
{
    public override string ToString()
    {
        return string.Join(",", PageNumbers);
    }
}
