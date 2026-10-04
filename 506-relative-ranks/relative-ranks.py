class Solution:
    def findRelativeRanks(self, score: list[int]) -> list[str]:
        original = score[:]
        score.sort(reverse=True)

        rank = []

        for i in range(len(score)):
            if i == 0:
                rank.append("Gold Medal")
            elif i == 1:
                rank.append("Silver Medal")
            elif i == 2:
                rank.append("Bronze Medal")
            else:
                rank.append(str(i + 1))

        return [rank[score.index(x)] for x in original]