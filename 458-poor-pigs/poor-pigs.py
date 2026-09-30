class Solution:
    def poorPigs(self, buckets: int, minutesToDie: int, minutesToTest: int) -> int:
        rounds=minutesToTest//minutesToDie
        pig=0
        stage=1
        while stage<buckets:
            stage*=rounds+1
            pig+=1
        return pig
