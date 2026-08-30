class Solution:
    def wordPattern(self, pattern: str, s: str) -> bool:
        words=s.split()
        if len(pattern)!=len(words):
            return False
        m1=[]
        m2=[]
        for char in pattern:
            m1.append(pattern.index(char))
        for word in words:
            m2.append(words.index(word))
        return m1==m2