def dfs(p, graph, targetSet):
    visited = set()
    stack = [(p,0,len(graph[p]))]
    while stack:
        idx = stack[-1][1]
        while idx < stack[-1][2] and graph[stack[-1][0]][idx] in visited:
            idx += 1
        if idx == stack[-1][2]:
            # leaf call: tear down current stack frame
            stack.pop()
            continue
        else: 
            # non-leaf call: there are still nbrs to explore. Take the next neighbour, `current`.
            # also increase idx in the current stack frame.
            # print(current)
            stack[-1] = (stack[-1][0], stack[-1][1] + 1, stack[-1][2])
            current = graph[stack[-1][0]][idx]
            visited.add(current)
            if current in targetSet:
                # found a path ending in an unmatched node (<=> flow augmenting path)
                print("returning True")
                return True, [t[0] for t in stack] + [current] 
            elif current in graph:
                # dfs:  if there are paths present, push new stack frame to stack:
                stack.append((current,0,len(graph[current])))
                continue
            else:
                # apparently no connections from current. That means that we are in a leaf call
                stack.pop()
                continue
                
    return False, []