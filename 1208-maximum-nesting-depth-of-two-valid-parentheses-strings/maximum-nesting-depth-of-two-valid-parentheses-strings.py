class Solution:
    def maxDepthAfterSplit(self, seq: str) -> list[int]:
        d=0
        ans=[]
        for c in seq:
            if c=="(":
                d+=1
            ans.append(d%2)
            if c==')':
                d-=1
        return ans