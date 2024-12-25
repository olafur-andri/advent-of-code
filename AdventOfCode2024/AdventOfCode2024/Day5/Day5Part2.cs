namespace AdventOfCode2024.Day5;

public static class Day5Part2
{
    public static void Run(string filepath)
    {
        Input input = Input.GetFromFile(filepath);

        var result = 0;

        foreach (PageNumberSequence sequence in input.PageNumberSequences)
        {
            if (SequenceIsCorrect(sequence, input.OrderingRules, out (PageNumber Left, PageNumber Right)? swap))
            {
                continue;
            }

            PageNumberSequence newSequence = SwapNumbersInSequence(sequence, swap!.Value.Left, swap.Value.Right);

            while (!SequenceIsCorrect(newSequence, input.OrderingRules, out swap))
            {
                newSequence = SwapNumbersInSequence(newSequence, swap!.Value.Left, swap.Value.Right);
            }

            result += GetMiddlePageNumber(newSequence);
        }
        
        Console.WriteLine(result);
    }
    
    private static PageNumber GetMiddlePageNumber(PageNumberSequence pageNumberSequence)
    {
        return pageNumberSequence.PageNumbers[pageNumberSequence.PageNumbers.Count / 2];
    }

    /// <summary>
    /// Returns <c>true</c> if the given <paramref name="sequence"/> is correct according to the given
    /// <paramref name="allOrderingRules"/>. Returns <c>false</c> otherwise and sets <paramref name="swap"/> to the
    /// numbers that must be swapped for the given <paramref name="sequence"/> to be "more correct".
    /// </summary>
    private static bool SequenceIsCorrect(
        PageNumberSequence sequence,
        IReadOnlyList<OrderingRule> allOrderingRules,
        out (PageNumber Left, PageNumber Right)? swap)
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
                    swap = (pageNumber, queueItem.PageNumber);
                    
                    return false;
                }
            }
        }

        swap = null;
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
    
    /// <returns>
    /// A new sequence where the given <paramref name="left"/> and <paramref name="right"/> page numbers have been
    /// swapped
    /// </returns>
    private static PageNumberSequence SwapNumbersInSequence(
        PageNumberSequence sequence,
        PageNumber left,
        PageNumber right)
    {
        List<PageNumber> newPageNumbers = sequence.PageNumbers.ToList();
        int leftIndex = newPageNumbers.IndexOf(left);
        int rightIndex = newPageNumbers.IndexOf(right);

        newPageNumbers[leftIndex] = right;
        newPageNumbers[rightIndex] = left;

        return new PageNumberSequence(newPageNumbers);
    }
    
    private record QueueItem(PageNumber PageNumber, List<PageNumber> Path);
}