
import heapq

class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)
        small, large = [], []
        active = set()
        side = {}
        ls = rs = 0
        lsum = rsum = 0

        def clean(heap, low):
            while heap:
                i = heap[0][1]
                if i not in active:
                    heapq.heappop(heap)
                else:
                    break

        def add(i):
            nonlocal ls, rs, lsum, rsum
            v = nums[i]
            clean(small, True)
            if not small or v <= -small[0][0]:
                heapq.heappush(small, (-v, i))
                side[i] = 0
                ls += 1
                lsum += v
            else:
                heapq.heappush(large, (v, i))
                side[i] = 1
                rs += 1
                rsum += v
            active.add(i)

        def remove(i):
            nonlocal ls, rs, lsum, rsum
            v = nums[i]
            active.remove(i)
            if side[i] == 0:
                ls -= 1
                lsum -= v
            else:
                rs -= 1
                rsum -= v

        def balance():
            nonlocal ls, rs, lsum, rsum
            clean(small, True)
            clean(large, False)

            while ls > rs + 1:
                clean(small, True)
                v, i = heapq.heappop(small)
                v = -v
                heapq.heappush(large, (v, i))
                side[i] = 1
                ls -= 1
                rs += 1
                lsum -= v
                rsum += v

            while ls < rs:
                clean(large, False)
                v, i = heapq.heappop(large)
                heapq.heappush(small, (-v, i))
                side[i] = 0
                rs -= 1
                ls += 1
                rsum -= v
                lsum += v

        def get_cost():
            clean(small, True)
            m = -small[0][0]
            return m * ls - lsum + rsum - m * rs

        costs = []
        for i in range(x):
            add(i)

        balance()
        costs.append(get_cost())

        for i in range(x, n):
            remove(i - x)
            balance()
            add(i)
            balance()
            costs.append(get_cost())

        INF = 10**18
        dp = [[INF] * (k + 1) for _ in range(n + 1)]
        dp[0][0] = 0

        for i in range(n):
            for j in range(k + 1):
                dp[i + 1][j] = min(dp[i + 1][j], dp[i][j])

                if j < k and i + x <= n:
                    dp[i + x][j + 1] = min(
                        dp[i + x][j + 1],
                        dp[i][j] + costs[i]
                    )

        return dp[n][k]
