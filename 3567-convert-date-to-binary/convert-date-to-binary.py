class Solution:
    def convertDateToBinary(self, date: str) -> str:
        year,month,day=date.split('-')
        return bin(int(year))[2:]+'-'+bin(int(month))[2:]+'-'+bin(int(day))[2:]