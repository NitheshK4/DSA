
class Solution:
    def minMoves(self, nums: List[int]) -> int:
        mini = min(nums)
        moves = 0

        for num in nums:
            moves += num - mini

        return moves
