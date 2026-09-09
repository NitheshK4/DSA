# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        res=[]
        q=collections.deque([root]) #add the tree value in queue
        while q:  #check if root is null
            rs=None
            lenq=len(q)
            for i in range(len(q)):
                node=q.popleft()  #take one node the left most
                if node:
                    rs=node
                    q.append(node.left) #add left chile from root node
                    q.append(node.right)#add rightchild form root node
            if rs:
                res.append(rs.val)
        return res