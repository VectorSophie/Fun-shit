def whereto(arr):
    if len(arr) < 3:
        return -1

    door = -1
    distance = -1
    index = -1

    for i in range(len(arr)):
        if arr[i] == 'd':
            door = i
            break

    if door == -1:
        return -1  

    newarr = [x for x in arr if x != 'd']

    for i in range(len(newarr) - 2):  
        currstall = sum(int(newarr[i + j]) for j in range(3))

        todoor = abs((arr.index(newarr[i])) - door)

        if todoor > distance:
            distance = todoor
            index = arr.index(newarr[i])

    return index

N = input().split() 
print(whereto(N))

