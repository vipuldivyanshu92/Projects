def cont_segments(l):
    queue = []
    result = []

    for e in l:
        if not queue:
            queue.append(e)
        else:
            if e == queue[-1]+1:
                queue.append(e)
            else:
                result.append(queue)
                queue = []
                queue.append(e)
    result.append(queue)

    return result

print(cont_segments([4, 5, 6, 10, 8, 9]))
