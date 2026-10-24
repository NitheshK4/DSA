class Solution:
    def countDaysTogether(self, a: str, b: str, c: str, d: str) -> int:
        days = [31,28,31,30,31,30,31,31,30,31,30,31]

        def f(s):
            m, day = map(int, s.split("-"))
            return sum(days[:m-1]) + day

        return max(0, min(f(b), f(d)) - max(f(a), f(c)) + 1)