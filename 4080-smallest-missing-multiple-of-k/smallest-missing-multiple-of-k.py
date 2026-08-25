class Solution:
    def missingMultiple(self, nums: List[int], k: int) -> int:
        nums=set(nums)
        for i in range(1,len(nums)+2):
            x=k*i
            if x not in nums:
                return x
            