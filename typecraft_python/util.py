def batch(iterable, n=1):
    length = len(iterable)
    for next_index in range(0, length, n):
        yield iterable[next_index:min(next_index + n, length)]
