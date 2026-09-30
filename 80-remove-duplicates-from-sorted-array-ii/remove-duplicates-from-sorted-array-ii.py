
class Solution:
    def removeDuplicates(self, nums: list[int]) -> int:
        
        counts=Counter(nums)
        k=0
        for num in nums:
            if counts[num]>2:
                counts[num]-=1
            else:
                nums[k]=num
                k+=1
        return k