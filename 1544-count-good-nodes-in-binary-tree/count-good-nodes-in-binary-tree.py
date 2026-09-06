# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def goodNodes(self, root: TreeNode) -> int:
        def dfs(node,mx):
            if not node:
                return 0
            if node.val>=mx:
                ans=1
            else:
                ans=0
            mx=max(node.val,mx)
            return ans + dfs(node.left,mx) + dfs(node.right,mx)
        return dfs (root,root.val)