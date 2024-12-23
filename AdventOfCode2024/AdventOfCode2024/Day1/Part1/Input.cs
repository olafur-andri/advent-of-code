using System.Text.RegularExpressions;

namespace AdventOfCode2024.Day1.Part1;

public partial record Input(IReadOnlyList<int> LeftList, IReadOnlyList<int> RightList)
{
    [GeneratedRegex(@"\s+")]
    private static partial Regex OneOrMoreWhitespacesRegex();
    
    public static Input GetFromInputFile()
    {
        var leftList = new List<int>();
        var rightList = new List<int>();

        foreach (string line in File.ReadAllLines(@"Day1\Part1\input.txt"))
        {
            string[] splitLine = OneOrMoreWhitespacesRegex().Split(line);
            var (leftNumber, rightNumber) = (Convert.ToInt32(splitLine[0]), Convert.ToInt32(splitLine[1]));
            
            leftList.Add(leftNumber);
            rightList.Add(rightNumber);
        }
        
        return new Input(leftList, rightList);
    }
}