class Solution:
    def isPowerOfFour(self, n: int) -> bool:
        for i in range(31):
            ans=4**i
            if ans==n:
                return True
        return False