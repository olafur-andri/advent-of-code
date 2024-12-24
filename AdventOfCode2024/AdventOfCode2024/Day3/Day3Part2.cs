using System.Text.RegularExpressions;

namespace AdventOfCode2024.Day3;

public partial class Day3Part2
{
    private const string MultiplicationPattern = @"mul\(\d+\,\d+\)";
    private const string DoPattern = @"do\(\)";
    private const string DontPattern = @"don't\(\)";
    private const string AnyInstructionPattern = $"({MultiplicationPattern})|({DoPattern})|({DontPattern})";
    
    [GeneratedRegex(MultiplicationPattern)]
    private static partial Regex MultiplicationRegex();

    [GeneratedRegex(DoPattern)]
    private static partial Regex DoRegex();

    [GeneratedRegex(DontPattern)]
    private static partial Regex DontRegex();

    [GeneratedRegex(AnyInstructionPattern)]
    private static partial Regex AnyInstructionRegex();
    
    public static void Run()
    {
        Input input = Input.GetFromFile();

        IReadOnlyList<IInstruction> allInstructions = ParseAllInstructions(input);

        var multiplicationIsEnabled = true;
        var result = 0;

        foreach (IInstruction instruction in allInstructions)
        {
            switch (instruction)
            {
                case DoInstruction:
                    multiplicationIsEnabled = true;
                    break;
                case DontInstruction:
                    multiplicationIsEnabled = false;
                    break;
                case MultiplicationInstruction multiplicationInstruction when multiplicationIsEnabled:
                    result += multiplicationInstruction.GetResult();
                    break;
            }
        }
        
        Console.WriteLine(result);
    }
    
    private static List<IInstruction> ParseAllInstructions(Input input)
    {
        MatchCollection matches = AnyInstructionRegex().Matches(input.Instructions);
        
        List<IInstruction> allInstructions = [];

        foreach (Match match in matches)
        {
            if (DoRegex().IsMatch(match.Value)) // if it is a "do" instruction
            {
                allInstructions.Add(new DoInstruction());
            }
            else if (DontRegex().IsMatch(match.Value)) // if it is a "don't" instruction
            {
                allInstructions.Add(new DontInstruction());
            }
            else // if it is a multiplication instruction 
            {
                List<int> numbers = match.Value
                    .Replace("mul(", "")
                    .Replace(")", "")
                    .Split(',')
                    .Select(int.Parse)
                    .ToList();
            
                allInstructions.Add(new MultiplicationInstruction(numbers[0], numbers[1]));
            }
        }

        return allInstructions;
    }

    private interface IInstruction;
    
    private record MultiplicationInstruction(int Left, int Right) : IInstruction
    {
        public int GetResult()
        {
            return Left * Right;
        }
    }
    
    private record DoInstruction : IInstruction;

    private record DontInstruction : IInstruction;
}