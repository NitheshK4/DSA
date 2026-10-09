class Solution:
    def minInsertions(self, s: str) -> int:
        ans=0
        r=0
        for c in s:
            if c=="(":
                if r%2==1:
                    ans+=1
                    r-=1
                r+=2
            else:
                r-=1
            if r<0:
                ans+=1
                r=1
        return ans+r