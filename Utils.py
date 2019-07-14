class terminalColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def nameFromPath(path):
    reversedPath = path[::-1]
    name = ""
    for char in reversedPath:
        if char != '/' and char != '\\':
            name = name + char
        else:
            break
    return name[::-1]

def removeDuplicateInAcquisti(acquisti)
    retList = []
    for acquisto in acquisti:
        if acquisto.product_id  not in list(map(lambda el: el.product_id, retList)):
            retList.append(acquisto)
    return retList
