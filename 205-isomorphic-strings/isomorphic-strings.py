class Solution:
    def isIsomorphic(self, s: str, t: str) -> bool:
        m1=[]
        m2=[]
        for char in s:
            m1.append(s.index(char))
        for char in t:
            m2.append(t.index(char))
        if m1==m2:
            return True
        return False