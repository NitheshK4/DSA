# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def maxPathSum(self, root: TreeNode | None) -> int:
        ans=float(-inf)
        def dfs(node):
            nonlocal ans
            if not node:
                return 0
            left=max(0,dfs(node.left))
            right=max(0,dfs(node.right))
            ans=max(ans,node.val+left+right)
            return node.val+max(left,right)
        dfs(root)
        return ans