class Solution:
    def superPow(self, a: int, b: list[int]) -> int:
        ans=1
        for x in b:
            ans=(ans**10*a**x)%1337
        return ans
        