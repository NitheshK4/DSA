# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def rotateRight(self, head: ListNode | None, k: int) -> ListNode | None:
        arr=[]
        while head:
            arr.append(head.val)
            head=head.next
        if not arr:
            return None
        k=k%len(arr)
        arr=arr[-k:]+arr[:-k]
        ##put the values back to list
        dummy=ListNode(0)
        curr=dummy
        for x in arr:
            curr.next=ListNode(x)
            curr=curr.next
        return dummy.next