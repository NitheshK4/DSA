class Solution:
    def longestPalindrome(self, s: str) -> str:
        ans=""
        n=len(s)
        for i in range(n):
            for j in range(i,n):
                x=s[i:j+1]
                if x==x[::-1] and len(x)>len(ans):
                    ans=x
        return ans