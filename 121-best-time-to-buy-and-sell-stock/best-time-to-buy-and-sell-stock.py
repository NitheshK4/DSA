class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        min_p=prices[0]
        max_p=0
        for price in prices:
            if price<min_p:
                min_p=price

            profit=price-min_p

            if profit>max_p:
                max_p=profit
        return max_p