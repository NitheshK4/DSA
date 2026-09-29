class Solution:
    def minPathSum(self, grid: list[list[int]]) -> int:
        r=len(grid)
        c=len(grid[0])
        for i in range(r):
            for j in range(c):
                if i==0 and j==0:
                    continue 
                if i==0:
                    grid[i][j]+=grid[i][j-1]
                elif j==0:
                    grid[i][j]+=grid[i-1][j]
                else:
                    grid[i][j]+=min(grid[i][j-1],grid[i-1][j])
        return grid[-1][-1]
