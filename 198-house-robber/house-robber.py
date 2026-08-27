class Solution:
    def rob(self, nums: List[int]) -> int:
        a=0
        b=0
        for num in nums:
            temp=max(a+num,b)
            a=b
            b=temp
        return b