class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        if not nums:
            return [-1,-1]
        def binsearch(find_left):
            left=0
            right=len(nums)-1
            ans=-1
            while left<=right:
                mid=(left+right)//2
                if nums[mid]<target:
                    left=mid+1
                elif nums[mid]>target:
                    right=mid-1
                else:
                    ans=mid
                    if find_left:
                        right=mid-1
                    else:
                        left=mid+1
            return ans
        return [binsearch(True),binsearch(False)]