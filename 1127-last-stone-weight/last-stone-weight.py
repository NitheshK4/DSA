class Solution:
    def lastStoneWeight(self, stones: List[int]) -> int:
        while len(stones)>1:
            stones.sort()
            a=stones.pop()
            b=stones.pop()
            if a!=b:
                stones.append(a-b)
        return stones[0] if stones else 0
        