class Solution:
    def singleNumber(self, nums: List[int]) -> List[int]:
        res=[]
        for num in nums:
            if nums.count(num)==1:
                res.append(num)
        return res