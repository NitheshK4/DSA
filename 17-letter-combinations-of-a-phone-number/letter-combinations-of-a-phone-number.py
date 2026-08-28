class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        if not digits:
            return None
        result=[""]
        phone={
            "2": "abc",
            "3":"def",
            "4":"ghi",
            "5":"jkl",
            "6":"mno",
            "7":"pqrs",
            "8":"tuv",
            "9":"wxyz"
        }
        for digit in digits:
            temp=[]
            for old in result:
                for x in phone[digit]:
                    temp.append(old+x)
            result=temp
        return result