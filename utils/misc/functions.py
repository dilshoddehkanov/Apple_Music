def split_list(lst):
    for i in range(0, len(lst), 5):
        yield lst[i:i + 5]
