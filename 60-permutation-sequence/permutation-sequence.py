class Solution:
    def getPermutation(self, n: int, k: int) -> str:
        nums=range(1,n+1)
        arr=list(permutations(nums))
        return "".join(map(str,arr[k-1]))