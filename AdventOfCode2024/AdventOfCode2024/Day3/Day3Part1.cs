using System.Text.RegularExpressions;

namespace AdventOfCode2024.Day3;

public static partial class Day3Part1
{
    [GeneratedRegex(@"mul\(\d+\,\d+\)")]
    private static partial Regex MultiplicationRegex();
    
    public static void Run()
    {
        Input input = Input.GetFromFile();

        IReadOnlyList<MultiplicationInstruction> multiplicationInstructions = ParseMultiplicationInstructions(input);
        
        int result = multiplicationInstructions.Sum(instruction => instruction.Result());
        
        Console.WriteLine(result);
    }

    private static IReadOnlyList<MultiplicationInstruction> ParseMultiplicationInstructions(Input input)
    {
        MatchCollection multiplicationMatches = MultiplicationRegex().Matches(input.Instructions);
        
        List<MultiplicationInstruction> multiplicationInstructions = [];

        foreach (Match multiplicationMatch in multiplicationMatches)
        {
            List<int> numbers = multiplicationMatch
                .Value
                .Replace("mul(", "")
                .Replace(")", "")
                .Split(',')
                .Select(int.Parse)
                .ToList();
            
            multiplicationInstructions.Add(new MultiplicationInstruction(numbers[0], numbers[1]));
        }

        return multiplicationInstructions;
    }
    
    private record MultiplicationInstruction(int Left, int Right)
    {
        public int Result()
        {
            return Left * Right;
        }
    }
}