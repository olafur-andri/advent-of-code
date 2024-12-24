using System.Text.RegularExpressions;

namespace AdventOfCode2024.Day1;

public partial record Input(IReadOnlyList<LocationId> LeftList, IReadOnlyList<LocationId> RightList)
{
    [GeneratedRegex(@"\s+")]
    private static partial Regex OneOrMoreWhitespacesRegex();
    
    public static Input GetFromInputFile()
    {
        var leftList = new List<LocationId>();
        var rightList = new List<LocationId>();

        foreach (string line in File.ReadAllLines(@"Day1\input.txt"))
        {
            string[] splitLine = OneOrMoreWhitespacesRegex().Split(line);
            var (leftNumber, rightNumber) = (Convert.ToInt32(splitLine[0]), Convert.ToInt32(splitLine[1]));
            
            leftList.Add(new LocationId(leftNumber));
            rightList.Add(new LocationId(rightNumber));
        }
        
        return new Input(leftList, rightList);
    }
}