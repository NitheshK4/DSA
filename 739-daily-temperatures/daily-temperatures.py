class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        n=len(temperatures)
        ans=[0]*n
        stk=[]
        for i,t in enumerate(temperatures):
            while stk and stk[-1][1]<t:
                stk_i,stk_t=stk.pop()
                ans[stk_i]=i-stk_i
            stk.append([i,t])
        return ans