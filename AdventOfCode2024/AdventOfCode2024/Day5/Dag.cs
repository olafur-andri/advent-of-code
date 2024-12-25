namespace AdventOfCode2024.Day5;

public class Dag
{
    private readonly Dictionary<PageNumber, List<PageNumber>> _outgoingEdges = new();
    
    public Dag(IReadOnlyList<OrderingRule> orderingRules)
    {
        foreach (OrderingRule orderingRule in orderingRules)
        {
            if (!_outgoingEdges.ContainsKey(orderingRule.Left))
            {
                _outgoingEdges[orderingRule.Left] = [];
            }
            
            _outgoingEdges[orderingRule.Left].Add(orderingRule.Right);
        }
    }
    
    public IReadOnlyList<PageNumber> GetOutgoingEdges(PageNumber pageNumber)
    {
        return _outgoingEdges.GetValueOrDefault(pageNumber, []);
    }
}