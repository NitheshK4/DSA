class Solution:
    def maxArea(self, height: List[int]) -> int:
        n=len(height)
        l=0
        r=n-1
        ma=0
        while l<r:
            w=r-l
            h=min(height[l],height[r])
            a=w*h
            ma=max(ma,a)
            if height[l]>height[r]:
                r-=1
            else:
                l+=1
        return ma
