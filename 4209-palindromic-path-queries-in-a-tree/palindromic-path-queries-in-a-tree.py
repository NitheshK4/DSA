from typing import List

class Solution:
    def palindromePath(self, n: int, edges: List[List[int]],
                       s: str, queries: List[str]) -> List[bool]:

        graph = [[] for _ in range(n)]
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)

        LOG = n.bit_length()
        parent = [[0] * n for _ in range(LOG)]
        depth = [0] * n
        tin = [0] * n
        tout = [0] * n
        prefix = [0] * n
        timer = 0

        # DFS: Euler tour, parents and prefix masks
        stack = [(0, -1, 0)]
        while stack:
            u, p, state = stack.pop()

            if state == 0:
                tin[u] = timer
                timer += 1

                if p != -1:
                    parent[0][u] = p
                    depth[u] = depth[p] + 1
                    prefix[u] = prefix[p] ^ (1 << (ord(s[u]) - 97))
                else:
                    prefix[u] = 1 << (ord(s[u]) - 97)

                for k in range(1, LOG):
                    parent[k][u] = parent[k - 1][parent[k - 1][u]]

                stack.append((u, p, 1))
                for v in graph[u]:
                    if v != p:
                        stack.append((v, u, 0))
            else:
                tout[u] = timer

        # Binary lifting LCA
        def lca(u, v):
            if depth[u] < depth[v]:
                u, v = v, u

            diff = depth[u] - depth[v]
            for k in range(LOG):
                if diff & (1 << k):
                    u = parent[k][u]

            if u == v:
                return u

            for k in range(LOG - 1, -1, -1):
                if parent[k][u] != parent[k][v]:
                    u = parent[k][u]
                    v = parent[k][v]

            return parent[0][u]

        # Fenwick tree for XOR range updates
        bit = [0] * (n + 2)

        def update(i, val):
            while i <= n:
                bit[i] ^= val
                i += i & -i

        def point_query(i):
            result = 0
            while i > 0:
                result ^= bit[i]
                i -= i & -i
            return result

        chars = list(s)
        ans = []

        for q in queries:
            parts = q.split()

            if parts[0] == "update":
                u = int(parts[1])
                c = parts[2]

                delta = (1 << (ord(chars[u]) - 97)) ^ (
                    1 << (ord(c) - 97)
                )

                if delta:
                    update(tin[u] + 1, delta)
                    update(tout[u] + 1, delta)
                    chars[u] = c

            else:
                u, v = int(parts[1]), int(parts[2])
                w = lca(u, v)

                pu = prefix[u] ^ point_query(tin[u] + 1)
                pv = prefix[v] ^ point_query(tin[v] + 1)

                mask = pu ^ pv ^ (1 << (ord(chars[w]) - 97))

                ans.append((mask & (mask - 1)) == 0)

        return ans