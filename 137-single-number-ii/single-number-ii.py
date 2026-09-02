class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        #res=[]
        for num in nums:
            if nums.count(num)==1:
                return num