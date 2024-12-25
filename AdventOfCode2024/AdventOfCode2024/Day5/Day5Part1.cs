namespace AdventOfCode2024.Day5;

public static class Day5Part1
{
    public static void Run(string filepath)
    {
        Input input = Input.GetFromFile(filepath);

        int result = input.PageNumberSequences
            .Where(sequence => SequenceIsCorrect(sequence, input.OrderingRules))
            .Select(GetMiddlePageNumber)
            .Sum(number => number.Value);
        
        Console.WriteLine(result);
    }
    
    private static PageNumber GetMiddlePageNumber(PageNumberSequence pageNumberSequence)
    {
        return pageNumberSequence.PageNumbers[pageNumberSequence.PageNumbers.Count / 2];
    }

    private static bool SequenceIsCorrect(PageNumberSequence sequence, IReadOnlyList<OrderingRule> allOrderingRules)
    {
        HashSet<PageNumber> visited = [];

        HashSet<PageNumber> relevantPageNumbers = sequence.PageNumbers.ToHashSet();
        List<OrderingRule> relevantOrderingRules = allOrderingRules
            .Where(rule => relevantPageNumbers.Contains(rule.Left) && relevantPageNumbers.Contains(rule.Right))
            .ToList();
        Dag dag = new(relevantOrderingRules);
        
        foreach (PageNumber pageNumber in sequence.PageNumbers)
        {
            visited.Add(pageNumber);

            foreach (QueueItem queueItem in GetReachablePageNumbersFrom(pageNumber, dag))
            {
                if (visited.Contains(queueItem.PageNumber))
                {
                    // Console.WriteLine($"Sequence '{sequence}' is incorrect because '{pageNumber}' comes after '{queueItem.PageNumber}'\n\tpath: {string.Join(",", [..queueItem.Path, queueItem.PageNumber])}");
                    
                    return false;
                }
            }
        }

        return true;
    }
    
    private static IEnumerable<QueueItem> GetReachablePageNumbersFrom(PageNumber sourcePageNumber, Dag dag)
    {
        IReadOnlyList<PageNumber> initialNeighbors = dag.GetOutgoingEdges(sourcePageNumber);
        
        HashSet<PageNumber> visited = [sourcePageNumber, ..initialNeighbors];
        Queue<QueueItem> queue = new();

        foreach (PageNumber initialNeighbor in initialNeighbors)
        {
            QueueItem newQueueItem = new(initialNeighbor, [sourcePageNumber]);
            queue.Enqueue(newQueueItem);
            yield return newQueueItem;
        }
    
        while (queue.TryDequeue(out QueueItem? queueItem))
        {
            foreach (PageNumber neighbor in dag.GetOutgoingEdges(queueItem.PageNumber))
            {
                // ReSharper disable once CanSimplifySetAddingWithSingleCall
                if (visited.Contains(neighbor))
                {
                    continue;
                }

                QueueItem newQueueItem = new(neighbor, [..queueItem.Path, queueItem.PageNumber]);
                
                visited.Add(neighbor);
                queue.Enqueue(newQueueItem);

                yield return newQueueItem;
            }
        }
    }
    
    private record QueueItem(PageNumber PageNumber, List<PageNumber> Path);
}