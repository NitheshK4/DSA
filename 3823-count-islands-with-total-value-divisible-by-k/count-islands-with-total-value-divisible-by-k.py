
class Solution:
    def countIslands(self, grid: List[List[int]], k: int) -> int:
        m, n = len(grid), len(grid[0])
        ans = 0

        def dfs(i, j):
            if i < 0 or i >= m or j < 0 or j >= n or grid[i][j] == 0:
                return 0

            val = grid[i][j]
            grid[i][j] = 0

            val += dfs(i+1, j)
            val += dfs(i-1, j)
            val += dfs(i, j+1)
            val += dfs(i, j-1)

            return val

        for i in range(m):
            for j in range(n):
                if grid[i][j] > 0:
                    total = dfs(i, j)
                    if total % k == 0:
                        ans += 1

        return ans
