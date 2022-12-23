from collections import defaultdict, deque
import bisect
from copy import deepcopy

def color(A, to_color, left, right):
    # color to_color[left:right] inclusive with the value A[left]; use only for small cases 
    # due to added complexity
    B = deepcopy(to_color)
    to_color[left:right + 1] = [A[left]] * (right - left + 1)
    print(f"{B} ->\n{to_color}")
    print("---")
    return

def helper(A, mp, left, right, colored):
    # Solve the minimum number of days to color A[left:right] inclusive, correctly
    if left > right:                            # empty
        return 0
    if left == right:                           # exactly one job => one day
        if colored:                             # visualizer
            color(A, colored, left, right)
        return 1
        
    val = A[left]
    tail_leftmost_occ = left                    # get rightmost index of consecutive equal values
                                                # that starts at index left
    while tail_leftmost_occ < right and A[tail_leftmost_occ] == A[tail_leftmost_occ + 1]:
        tail_leftmost_occ += 1
        
    rightmost_occ = bisect.bisect_right(mp[val], right) - 1 # ceil; rightmost instance of value 
                                                            # between A[left:right] inclusive
    if rightmost_occ == -1:                     # no other instance exists => no intermediate coloring
        return 1 + helper(A, mp, tail_leftmost_occ + 1, right, colored)
        
    res = 0
    rightmost_occ = mp[val][rightmost_occ]      # index back into A
    tail_rightmost_occ = rightmost_occ          # analogous to left side
    while tail_rightmost_occ > tail_leftmost_occ and A[tail_rightmost_occ] == A[tail_rightmost_occ - 1]:
        tail_rightmost_occ -= 1
    
    if colored:                                 # color this chunk
        color(A, colored, left, rightmost_occ)
        
    res += 1 + helper(A, mp, tail_leftmost_occ + 1, tail_rightmost_occ - 1, colored) # inner part is not uniform; color it recursively
    if rightmost_occ < right:                   # work on portion to the right of our chunk 
                                                # before the right boundary
        res += helper(A, mp, rightmost_occ + 1, right, colored)
        
    return res
    
def solve(A, visual=False):
    """
    Problem: Given an array of target colors A, define an operation on an array as coloring
    any length subarray with some fixed color. What is the minimum number of operations needed 
    to color a blank array of zeroes to the target, A?
    
    Below solves in O(N * log(N)) time via a greedy two pointer approach with recursion
    Basically, work from left and right; fix the leftmost index and look for the rightmost
    instance of that value, then color that block uniformly with A[left], then work your way
    inwards. Handle any remaining portion between the rightmost instance and the rest of the
    array recursively on its own.
    
    Questions:
    1. Is this correct?
    2. Can we solve in O(N)?
    """
    if not A:
        return 0
        
    mp = defaultdict(lambda : deque()) # map unique values to their indices, organized as a 
                                       # double-ended queue. May use list instead. Originally
                                       # used deque to achieve O(N) solution but algorithm didn't
                                       # handle some cases correctly
    for i, a in enumerate(A):
        mp[a].append(i)
        
    visualizer = [0] * len(A) if visual else None
    return helper(A, mp, 0, len(A) - 1, visualizer)
    
def main():
    for A in [
        [1, 1, 1, 1],
        [1, 1, 2, 2],
        [1, 2, 1, 2],
        [1, 2, 3, 4, 1, 4, 3, 2, 1, 6],
        [1, 2, 3, 4, 1, 4, 3, 2, 1, 6, 1, 2, 3, 4, 1, 4, 3, 2, 1, 6],
    ]:
        print("TARGET")
        print(A)
        print("----")
        ans = solve(A, visual=True)
        print(f"Answer: {ans}")
        print("==========")
        
    return

if __name__ == "__main__":
    main()
