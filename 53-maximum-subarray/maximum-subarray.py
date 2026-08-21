class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        cur=nums[0]
        ms=nums[0]
        for num in nums[1:]:
            cur=max(num,cur+num)
            ms=max(cur,ms)
        return ms