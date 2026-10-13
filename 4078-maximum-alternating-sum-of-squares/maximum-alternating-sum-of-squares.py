class Solution:
    def maxAlternatingSum(self, nums: List[int]) -> int:
        nums.sort(key=lambda x: x*x)
        ans = 0
        for i in range(len(nums)):
            if i < len(nums)//2:
                ans -= nums[i]*nums[i]
            else:
                ans += nums[i]*nums[i]
        return ans