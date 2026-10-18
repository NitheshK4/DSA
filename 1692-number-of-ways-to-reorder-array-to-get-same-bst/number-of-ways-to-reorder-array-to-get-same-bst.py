class Solution:
    def numOfWays(self, nums: list[int]) -> int:
        MOD = 10**9 + 7

        def solve(arr):
            if len(arr) <= 2:
                return 1

            left = [x for x in arr[1:] if x < arr[0]]
            right = [x for x in arr[1:] if x > arr[0]]

            n = len(left) + len(right)
            k = min(len(left), len(right))
            ways = 1

            for i in range(k):
                ways = ways * (n - i) // (i + 1)

            return ways * solve(left) * solve(right) % MOD

        return (solve(nums) - 1) % MOD