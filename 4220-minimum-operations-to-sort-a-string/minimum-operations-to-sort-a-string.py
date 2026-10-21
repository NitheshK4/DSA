class Solution:
    def minOperations(self, s: str) -> int:
        if s==''.join(sorted(s)):
            return 0
        if len(s)==2:
            return -1
        mn,mx=min(s),max(s)
        if s[0]==mn or s[-1]==mx:
            return 1
        if mn in s[1:-1] or mx in s[1:-1]:
            return 2
        return 3
        
