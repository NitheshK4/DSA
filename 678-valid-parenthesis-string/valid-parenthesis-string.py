class Solution:
    def checkValidString(self, s: str) -> bool:
        leftmax,leftmin=0,0
        for ch in s:
            if ch == "(":
                leftmin+=1
                leftmax+=1
            elif ch==")":
                leftmax-=1
                leftmin-=1
            else:
                leftmax+=1
                leftmin-=1
            if leftmax<0:
                return False
            if leftmin<0:
                leftmin=0
        return leftmin==0