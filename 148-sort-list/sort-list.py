# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def sortList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        result=[]
        current=head
        while current is not None:
            result.append(current.val)
            current=current.next
        result.sort()
        
        current=head
        i=0
        while current is not None:
            current.val=result[i]
            current=current.next
            i+=1
        return head