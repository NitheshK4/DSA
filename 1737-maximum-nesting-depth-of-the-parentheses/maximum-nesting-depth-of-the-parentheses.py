class Solution:
    def maxDepth(self, s: str) -> int:
        dpt=0
        ans=0
        for i in s:
            if i=="(":
                dpt+=1
                ans=max(ans,dpt)
            else:
                if i==")":
                    dpt-=1
        return ans