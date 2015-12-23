from functools import lru_cache
import uuid


@lru_cache(maxsize=2048)
def levenshtein(query, ref):
    # Recursive levenshtein distance
    if not query:
        return len(ref)
    if not ref:
        return len(query)
    if query[0] == ref[0]:
        return levenshtein(query[1:], ref[1:])

    d1 = levenshtein(query[1:], ref)
    d2 = levenshtein(query[1:], ref[1:])
    d3 = levenshtein(query, ref[1:])

    return min(d1, d2, d3) + 1


def get_near_matches(query, existing, distance=3):
    matches = []
    for e in existing:
        if levenshtein(query, e) <= distance:
            matches.append(e)
    return matches


def at_least_distance(query, existing, distance=3):
    for e in existing:
        if levenshtein(query, e) < distance:
            return False
    return True


def create_ids(n, id_length, failure_threshold=0.99):
    uuids = []
    hrids = []
    failures = 0
    trys = 1
    while len(hrids) < n and failures/trys < failure_threshold:
        trys += 1
        uuid_ = uuid.uuid4()
        hrid = uuid_.hex[-id_length:]
        if at_least_distance(hrid, hrids):
            uuids.append(uuid_)
            hrids.append(hrid)
            yield (uuid_, hrid)
        else:
            failures += 1
