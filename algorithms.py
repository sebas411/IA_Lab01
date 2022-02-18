def heuristic1(problem, node):
  d = float('inf')
  for finish in problem.finishlist:
    dy = abs(finish[1] - node[1])
    dx = abs(finish[0] - node[0])
    if dx + dy < d: d = dx + dy
  return float(d)


def heuristic2(problem, node):
  d = float('inf')
  for finish in problem.finishlist:
    dy = abs(finish[1] - node[1])
    dx = abs(finish[0] - node[0])
    if dx + dy < d: d = dx + dy
  return d * 1.01


def breath_first(problem):
  frontier = [[problem.startpos]]
  explored = []

  while True:
    if len(frontier):
      path = frontier.pop(0)
      #print(len(path))
      s = path[-1]
      explored.append(s)
      if problem.goalTest(s):
        return path
      for a in problem.actions(s):
        result = problem.result(s, a)
        if result not in explored:
          new_path = path[:]
          new_path.append(result)
          frontier.append(new_path)
    else:
      return False


def depth_first(problem, node = None, visited=[]):
  if node is None: node = problem.startpos
  if not node in visited:
    posible_paths = []
    visited.append(node)
    if problem.goalTest(node):
      return [node]
    for a in problem.actions(node):
      result = problem.result(node, a)
      path = depth_first(problem, result, visited[:])
      if path: posible_paths.append(path)
    if not posible_paths: return []
    smallest = posible_paths[0]
    for p in posible_paths:
      if len(p) < len(smallest):
        smallest = p
    smallest.insert(0, node)
    return smallest
  else:
    return []


def astar(problem, heu):
  openList = [(problem.startpos,0,[])]
  closedList = []
  while openList:
    current = openList[0]
    for node in openList:
      if node[1] < current[1]:
        current = node
    openList.remove(current)
    s = current[0]
    closedList.append(s)
    if problem.goalTest(s):
      return current[2]
    for a in problem.actions(s):
      result = problem.result(s, a)
      if result in closedList: continue
      g = current[2][:]
      g.append(result)
      h = heu(problem, s)
      f = len(g) + h
      cont = False
      for op in openList:
        if op[0] == result and len(g) > len(op[2]):
          cont = True
          break
      if cont: continue
      openList.append((result, f, g))
  else:
    return []
