class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        r=[[]]
        for num in nums:
            new=[]
            for subset in r:
                new.append(subset+[num])
            r+=new
        return r
            