
class Trie(object):

    def __init__(self, metadata=None, key: str=""):
        self.metadata = metadata
        self.key = key # eg. "01110101"
        self.branch = [None, None]
        self.size = 0 # only counts the leaves

    def __repr__(self) -> str:
        # "(branch[0].key / self.key \ branch[1].key)"
        rep = "("
        if self.branch[0] is not None:
            rep += self.branch[0].key + " / "
        rep += self.key
        if self.branch[1] is not None:
            rep += " \ " + self.branch[1].key
        return rep+")"
                
    # add the provided key to the trie
    # returns True on success and False on failure (usually
    # when the key is already in the trie)
    def add(self, key: str, metadata=None) -> bool:
        if self.branch[int(key[len(self.key)])] is not None:
            # branch already exists
            branch = self.branch[int(key[len(self.key)])]

            minLen = min(len(key), len(branch.key))
            if key[:minLen] == branch.key[:minLen]:
                if len(key)==len(branch.key):
                    # key already in the trie, cannot insert it
                    return False
                else:
                    # key is a branch of branch
                    #
                    #     11  +insert(111001)  *111* +insert(111001)
                    #    /  \                  /   \
                    # 110  *111*     -->     1110  1111

                    success = branch.add(key=key, metadata=metadata)
            else:
                # insert between two nodes in the trie
                # 
                #   11 +insert(111001)     11 self
                #  / \                    / \
                #     \       -->          1110 mid
                #      \                  /    \
                #     111011     key 111001 111011 branch

                for i in range(minLen):
                    if branch.key[i]!=key[i]:
                        # first bit where branch.key and key diverge

                        # create mid Trie node
                        mid = Trie(key=branch.key[:i])
                        # define mid branches
                        mid.branch[int(key[i])] = Trie(metadata=metadata, key=key)
                        mid.branch[1-int(key[i])] = branch
                        # set its size
                        mid.size = branch.size + 1
                        # update self branch to mid
                        self.branch[int(key[len(self.key)])] = mid
                        success=True

                        break
        else:
            # self doesn't have the appropriate branch
            # only useful for root node
            #
            #    . +insert(001)  .            . +insert(110)   .
            #         -->       /     OR     /      -->       / \
            #                 001          001              001 110

            self.branch[int(key[len(self.key)])] = Trie(metadata=metadata, key=key)
            success=True

        if success:
            self.size+=1
        return success
                
    # returns True if key in trie and False otherwise
    def find(self, key: str) -> bool:
        if len(self.key) >= len(key):
            if self.key == key:
                if self.metadata is None:
                    return True
                else:
                    return self.metadata
            else:
                return False
        elif self.branch[int(key[len(self.key)])] is not None:
            return self.branch[int(key[len(self.key)])].find(key)
        else:
            return False

    # returns a list of the n closest keys in the Trie to the given key
    def n_closest(self, key:str, n:int) -> list[str]:
        if self.branch[0] == self.branch[1] == None:
            # leaf of the trie
            if self.metadata is None:
                return [self.key]
            else:
                return [self.metadata]
        
        nclosest = []
        if self.branch[int(key[len(self.key)])] is not None:
            # get n closest on the closest branch
            nclosest += self.branch[int(key[len(self.key)])].n_closest(key, n)
        if len(nclosest) < n and self.branch[1-int(key[len(self.key)])] is not None:    
            # if we don't have n keys yet, get the difference from the other branch
            nclosest += self.branch[1-int(key[len(self.key)])].n_closest(key, n-len(nclosest))
        return nclosest


