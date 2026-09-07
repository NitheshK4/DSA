class Solution:
    def jump(self, nums: List[int]) -> int:
        jump=0
        far=0
        end=0
        for i in range(len(nums)-1):
            far=max(far,i+nums[i])
            if i==end:
                jump+=1
                end=far
        return jump