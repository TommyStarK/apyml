from hashlib import sha256 as sha

def merkle_root(array: list) -> str:
    def merkle(hashes: list) -> list:
        if not len(hashes):
            raise RuntimeError(f'Unprocessable dataframe. Cannot retrieve columns name. Got {hashes}')
        if len(hashes) > 1:
            if len(hashes)%2==0:
                def reducer(r: list) -> list:
                    i = 0
                    res = []
                    while i+1 < len(r):
                        res.append(sha(str(r[i]).encode('utf-8')+str(r[i+1]).encode('utf-8')).hexdigest())
                        i+=2
                    return res
                return merkle(reducer(hashes))
            else:
                return merkle([merkle(hashes[:len(hashes)-1]), hashes[len(hashes)-1]])
        return sha(str(hashes[0]).encode('utf-8')).hexdigest()
    return merkle(array)
