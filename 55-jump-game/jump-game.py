class Solution:
    def canJump(self, nums: List[int]) -> bool:
        res=0
        n=len(nums)
        for i in range(n):
            if i>res:
                return False
            res=max(res,i+nums[i])
        return True