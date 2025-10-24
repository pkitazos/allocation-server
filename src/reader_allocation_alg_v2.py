from collections import defaultdict, deque
import json

from src.rpa_types import RpaMatchingInput, RpaMatchingOutput

# ---------------- Min-Cost Max-Flow (successive shortest augmenting path) ---------------- #


class MinCostMaxFlow:
    def __init__(self, n):
        self.n = n
        self.adj = [[] for _ in range(n)]

    def add_edge(self, u, v, cap, cost):
        # forward edge
        self.adj[u].append([v, cap, cost, len(self.adj[v])])
        # reverse edge
        self.adj[v].append([u, 0, -cost, len(self.adj[u]) - 1])

    def min_cost_max_flow(self, s, t, maxf=float("inf")):
        n = self.n
        INF = 10**18
        flow = 0
        cost = 0
        # potentials for reduced costs (ensure non-negativity)
        pot = [0] * n

        # Bellman-Ford (optional) to initialize potentials if negative costs existed.
        # We only use non-negative costs, so zeros are fine.

        while flow < maxf:
            dist = [INF] * n
            parent = [(-1, -1)] * n  # (node, edge_index_from_parent)
            inq = [False] * n

            dist[s] = 0

            # Dijkstra with potentials (binary heap would be faster; simple deque works fine at this scale)
            # We'll implement a lightweight Dijkstra using a list as a priority queue.
            # For small graphs in practice this is OK.
            import heapq

            pq = [(0, s)]
            while pq:
                d, u = heapq.heappop(pq)
                if d != dist[u]:
                    continue
                for ei, e in enumerate(self.adj[u]):
                    v, cap, ecost, rev = e
                    if cap <= 0:
                        continue
                    nd = d + ecost + pot[u] - pot[v]
                    if nd < dist[v]:
                        dist[v] = nd
                        parent[v] = (u, ei)
                        heapq.heappush(pq, (nd, v))

            if dist[t] == INF:
                break  # no augmenting path

            # update potentials
            for i in range(n):
                if dist[i] < INF:
                    pot[i] += dist[i]

            # find bottleneck
            addf = maxf - flow
            v = t
            while v != s:
                u, ei = parent[v]
                addf = min(addf, self.adj[u][ei][1])
                v = u

            # apply augmentation
            v = t
            path_cost = 0
            while v != s:
                u, ei = parent[v]
                fwd = self.adj[u][ei]
                rev = self.adj[v][fwd[3]]
                fwd[1] -= addf
                rev[1] += addf
                path_cost += fwd[2]
                v = u

            flow += addf
            cost += addf * path_cost

        return flow, cost


# ---------------- Allocation using MCMF ---------------- #


def allocate_readers_with_capacity_hard(data: RpaMatchingInput) -> RpaMatchingOutput:
    """
    Hard-capacity allocator using min-cost max-flow.

    INPUT
    -----
    {
      "allProjects": ["p1", ...],
      "allReaders": [
        {
          "id": "r1",
          "capacity": 3,
          "preferable": [...],
          "unacceptable": [...],
          "conflict": [...]
        },
        ...
      ]
    }

    RULES
    -----
    - Each project can get at most 1 reader.
    - Reader capacities are HARD limits.
    - Conflicts are hard bans (no edge).
    - Costs: preferable=0, neutral=penalty_neutral (default 1), unacceptable=penalty_unacceptable (default 5).
      Lower total cost is preferred → more preferable matches are chosen, unacceptable used only if needed.

    OUTPUT
    ------
    {
      "assignments": [ {"readerId": "...", "projectId": "..."}, ... ],
      "unassignedProjects": [...],
      "load": {"r1": 3, ...}
    }
    """

    # Deterministic ordering (helps tie-breaking)
    projects = sorted(data.allProjects)
    readers = sorted(
        [
            {
                "id": r.id,
                "preferable": set(r.preferable),
                "unacceptable": set(r.unacceptable),
                "conflict": set(r.conflict),
                "capacity": r.capacity,
            }
            for r in data.allReaders
        ],
        key=lambda r: r["id"],
    )

    penalty_preferable = 0
    penalty_neutral = 1
    penalty_unacceptable = len(projects) + 1

    # --- algorithm starts
    # Graph nodes:
    #  source(0)
    #  projects: 1..P
    #  readers : P+1 .. P+R
    #  sink    : P+R+1
    P = len(projects)
    R = len(readers)
    N = P + R + 2
    S = 0
    T = P + R + 1

    mcmf = MinCostMaxFlow(N)

    # source -> project (cap 1)
    for i in range(P):
        mcmf.add_edge(S, 1 + i, 1, 0)

    # project -> reader edges depending on preference/conflict
    for pIdx, p in enumerate(projects):
        for rIdx, r in enumerate(readers):
            if p in r["conflict"]:
                continue  # hard ban

            cost = penalty_neutral  # neutral

            if p in r["preferable"]:
                cost = penalty_preferable
            elif p in r["unacceptable"]:
                cost = penalty_unacceptable

            mcmf.add_edge(1 + pIdx, 1 + P + rIdx, 1, cost)

    # reader -> sink
    for rIdx, r in enumerate(readers):
        mcmf.add_edge(1 + P + rIdx, T, r["capacity"], 0)

    # Push as much flow as possible (<= number of projects)
    flow, cost = mcmf.min_cost_max_flow(S, T, P)

    # Recover assignments from residual graph:
    # An assignment exists if edge (project -> reader) has residual cap == 0 (i.e., 1 unit used)
    assignments = []
    load = defaultdict(int)

    for pIdx, p in enumerate(projects):
        # Look at outgoing edges to readers
        for v, cap, _, _ in mcmf.adj[pIdx + 1]:
            # v in reader range?
            if not (1 + P <= v and v <= P + R):
                continue

            # Original capacity was 1; if now 0, it was used
            used = cap == 0
            if used:
                readerIdx = v - (1 + P)
                rid = readers[readerIdx]["id"]
                assignments.append({"readerId": rid, "projectId": p})
                load[rid] += 1
                break  # at most one per project

    # Unassigned projects = those without an outgoing used edge
    assigned_projects = {a["projectId"] for a in assignments}
    unassigned = sorted([p for p in projects if p not in assigned_projects])

    return {
        "assignments": assignments,
        "unassignedProjects": unassigned,
        "load": dict(load),
    }
