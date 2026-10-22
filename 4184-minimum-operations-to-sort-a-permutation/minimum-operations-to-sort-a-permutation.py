
class Solution:
    def minOperations(self, nums: List[int]) -> int:
        n = len(nums)
        zero = nums.index(0)

        def check(step):
            for i in range(1, n):
                a = (zero + (i - 1) * step) % n
                b = (zero + i * step) % n
                if nums[a] > nums[b]:
                    return False
            return True

        ans = float('inf')

        if check(1):
            ans = min(ans, zero, n - zero + 2)

        if check(-1):
            ans = min(ans, zero + 2, n - zero)

        return -1 if ans == float('inf') else ans
