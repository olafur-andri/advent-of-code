I've figured out that there are only 6 nodes that end with an `A`, so we can probably store a lot of data for each of them without running out of memory.

Also, according to `cycle.py`, I have the following info:

```
DRA: Needed 20780 steps to completely cycle at 'KFL' with direction loop offset = 3
AAA: Needed 18675 steps to completely cycle at 'HKC' with direction loop offset = 2
CMA: Needed 13943 steps to completely cycle at 'RLL' with direction loop offset = 4
MNA: Needed 17623 steps to completely cycle at 'DLL' with direction loop offset = 2
NJA: Needed 19204 steps to completely cycle at 'FLD' with direction loop offset = 5
RVA: Needed 12363 steps to completely cycle at 'JMN' with direction loop offset = 2
```

I could store, for each starting node $p$, their infinite path of nodes in finite memory (as long as I know where to loop back to) as a list of strings `["n1", "n3", "n5", "n3", "n5", ...]`. This would allow me to be able to skip forward an arbitrary amount of nodes in constant-time.

From this string, I can also precompute the distance to the next *target node*, and I'll pick the highest distance out of all of them.

Can I maybe just do some math instead?