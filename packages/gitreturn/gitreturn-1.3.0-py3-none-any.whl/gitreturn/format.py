import re

def worktree(string):
    return re.sub(r'/', '_', string)
