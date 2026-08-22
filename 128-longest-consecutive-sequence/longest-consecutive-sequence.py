class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        nums=sorted(set(nums))
        lon=1
        cur=1
        if not nums:
            return 0
        for i in range(1,len(nums)):
            if nums[i]==nums[i-1]+1:
                cur+=1
            else:
                lon=max(lon,cur)
                cur=1
        return max(lon,cur)