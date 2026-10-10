class Solution:
    def minSumSquareDiff(self, nums1, nums2, k1, k2):
        diff = [abs(a - b) for a, b in zip(nums1, nums2)]
        k = k1 + k2

        if sum(diff) <= k:
            return 0

        left, right = 0, max(diff)

        while left < right:
            mid = (left + right) // 2
            need = sum(max(d - mid, 0) for d in diff)

            if need > k:
                left = mid + 1
            else:
                right = mid

        for i in range(len(diff)):
            if diff[i] > left:
                k -= diff[i] - left
                diff[i] = left

        for i in range(len(diff)):
            if k > 0 and diff[i] == left and left > 0:
                diff[i] -= 1
                k -= 1

        return sum(d * d for d in diff)