class Solution:
    def sumCounts(self, nums: list[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)

        tree = [0] * (4 * n)
        sq = [0] * (4 * n)
        lazy = [0] * (4 * n)

        def push(node, l, r):
            add = lazy[node]
            if add == 0 or l == r:
                return

            mid = (l + r) // 2

            for child, length in (
                (node * 2, mid - l + 1),
                (node * 2 + 1, r - mid)
            ):
                sq[child] += 2 * add * tree[child] + length * add * add
                tree[child] += length * add
                lazy[child] += add

            lazy[node] = 0

        def update(node, l, r, ql, qr):
            if ql <= l and r <= qr:
                length = r - l + 1
                sq[node] += 2 * tree[node] + length
                tree[node] += length
                lazy[node] += 1
                return

            push(node, l, r)
            mid = (l + r) // 2

            if ql <= mid:
                update(node * 2, l, mid, ql, qr)
            if qr > mid:
                update(node * 2 + 1, mid + 1, r, ql, qr)

            tree[node] = tree[node * 2] + tree[node * 2 + 1]
            sq[node] = sq[node * 2] + sq[node * 2 + 1]

        last = {}
        ans = 0

        for i, x in enumerate(nums):
            prev = last.get(x, -1)
            update(1, 0, n - 1, prev + 1, i)
            ans = (ans + sq[1]) % MOD
            last[x] = i

        return ans