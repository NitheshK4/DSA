class Solution:
    def smallestIndex(self, nums: List[int]) -> int:
        for i in range(len(nums)):
            num=nums[i]
            dig_sum=0
            while num>0:
                dig_sum+=num%10
                num//=10
            if dig_sum==i:
                return i
        return -1