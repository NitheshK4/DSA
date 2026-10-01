class Solution:
    def isValid(self, s: str) -> bool:
        mapping = {')': '(', '}': '{', ']': '['}
        stack = []

        for c in s:
            if c in mapping.values():
                stack.append(c)
            elif c in mapping:
                if not stack or mapping[c] != stack.pop():
                    return False
        return not stack