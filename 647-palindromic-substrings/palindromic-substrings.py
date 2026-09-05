class Solution:
    def countSubstrings(self, s: str) -> int:
        count=0
        n=len(s)
        for i in range(n):
            for j in range(i,n):
                if s[i:j+1]==s[i:j+1][::-1]:
                    count+=1
        return count