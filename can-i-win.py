# https://www.reddit.com/r/leetcode/comments/17j583f/can_i_win_problem/
from collections import defaultdict
PICK = []
IS_FIRST = False

def solve(target, N):
    global PICK
    PICK = []
    remaining = tuple(list(range(1, N + 1)))
    remaining_sum = sum(range(1, N + 1))
    assert remaining_sum >= target
    memo = {}
    res = helper(target, remaining, memo)
    pairs = sorted(memo.keys(), reverse=True)
    """
    prev = None
    for pair in pairs:
        if prev != pair[0]:
            print()
        
        print(f"{pair}: {memo[pair]}", end=" ")
        prev = pair[0]
        
    print()
    """
    memo2 = defaultdict(lambda : [])
    for k, v in memo.items():
        t, pool = k
        does_win, picked = v
        memo2[t].append((does_win, pool, picked))
        
    trace(memo2, target)
    return res
    
def trace(memo, remain):
    if remain <= 0:
        return
    
    global PICK
    last = None
    for does_win, pool, picked in memo[remain]:
        if picked in PICK:
            continue
        
        if does_win:
            # print(f"At {memo[remain]} we can win if we pick {picked}")
            PICK.append(picked)
            return trace(memo, remain - picked)
    
        last = (does_win, pool, picked)
        
    last_picked = last[2]
    PICK.append(last_picked)
    return trace(memo, remain - last_picked)

def helper(target, remaining, memo):
    pair = (target, remaining)
    if pair in memo:
        return memo[pair]
        
    if max(remaining) >= target: # current player wins
        memo[pair] = (True, max(remaining))
        return memo[pair]
        
    res = False, min(remaining) # assume we lose
    for idx in range(len(remaining)):
        left = remaining[:idx]
        right = remaining[idx+1:]
        val = remaining[idx]
        opp, opp_pick = helper(target - val, left + right, memo)
        if not opp:
            res = (True, val)
            break
        
    memo[pair] = res
    return memo[pair]
    
x = solve(40, 10)
print(x)
print(PICK)
print(sum(PICK))
