
class Solution:
    def sortableIntegers(self, nums: List[int]) -> int:
        n = len(nums)
        pref = [0] * (n + 1)
        suff = [float('inf')] * (n + 1)

        for i in range(n):
            pref[i + 1] = max(pref[i], nums[i])

        for i in range(n - 1, -1, -1):
            suff[i] = min(suff[i + 1], nums[i])

        drop = [0] * n
        for i in range(1, n):
            drop[i] = drop[i - 1] + (nums[i - 1] > nums[i])

        ans = 0
        for k in range(1, n + 1):
            if n % k:
                continue

            ok = True
            for i in range(0, n, k):
                j = i + k - 1
                d = drop[j] - drop[i]
                d += nums[j] > nums[i]

                if d > 1 or pref[i] > suff[i]:
                    ok = False
                    break

            if ok:
                ans += k

        return ans
