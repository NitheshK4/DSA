class Solution:
    def getCommon(self, nums1: list[int], nums2: list[int]) -> int:
        com=list(set(nums1)& set(nums2))
        if len(com)==0:
            return -1
        com.sort()
        return com[0]