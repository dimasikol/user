def sort_heap(lst):
    def heapify(data,size,i):
        largest = i
        left = largest*2+1
        right = largest*2+2
        if left<size and data[left]>data[largest]:
            largest = left
        if right<size and data[right]>data[largest]:
            largest = right

        if largest!=i:
            data[largest],data[i] = data[i],data[largest]
            heapify(data,size,largest)
    for i in range(len(lst)-1,-1,-1):
        heapify(lst,len(lst),i)
    for k in range(len(lst)-1,-1,-1):
        heapify(lst,k,0)
        lst[0],lst[k] = lst[k],lst[0]

    return lst


def sort_shell(lst):
    middle = len(lst)//2
    while middle:
        for i in range(middle, len(lst)):
            index = i
            temp = lst[index]
            while index >= middle and lst[index-middle] > temp:
                lst[index] = lst[index-middle]
                index = index-middle
            lst[index] = temp
        middle //= 2
    return lst


def sort_merge(lst):
    def merge(lst1,lst2):
        res = []
        while lst1 and lst2:
            if lst1[0]>lst2[0]:
                res.append(lst2.pop(0))
            else:
                res.append(lst1.pop(0))
        return res + lst1 + lst2

    if len(lst)<=1:
        return lst
    return merge(sort_merge(lst[:len(lst)//2]),sort_merge(lst[len(lst)//2:]))


def sort_quick(lst):
    if len(lst)==2:
        return [min(lst),max(lst)]
    if len(lst)<=1:
        return lst
    r = lst[len(lst)//2]
    l,m,h = [], [], []
    for i in lst:
        if i<r:
            l.append(i)
        elif i==r:
            m.append(i)
        else:
            h.append(i)
    return sort_quick(l)+m+sort_quick(h)


def sort_gnome(lst):
    i = 1
    j = 2
    while i<len(lst):
        if lst[i-1] < lst[i]:
            i = j
            j += 1
        else:
            lst[i-1], lst[i] = lst[i], lst[i-1]
            i -= 1
        if i == 0:
            i = j
            j += 1
    return lst


def sort_shake(lst):
    left = 0
    right = len(lst)-1
    while left < right:
        left_index = left
        right_index = right
        for i in range(left, right):
            if lst[left] > lst[i]:
                lst[left], lst[i] = lst[i], lst[left]
        left += 1
        for i in range(right, left, -1):
            if lst[right] > lst[i]:
                lst[right], lst[i] = lst[i], lst[right]
        right -= 1
    return lst


def sort_selection(lst):

    for i in range(len(lst)):
        index = i
        flag = False
        for k in range(i+1, len(lst)):
            if lst[k] < lst[index]:
                index = k
                flag = True
        if flag:
            lst[index],lst[i] = lst[i],lst[index]
    return lst


def sort_insertion(lst):
    for i in range(1, len(lst)):
        index = 0
        temp = lst[i]
        while index < i and lst[index]<temp:
            index += 1
        lst.insert(index,lst.pop(i))
    return lst


def sort_bubble(lst):
    flag = True
    while flag:
        flag = False
        for i in range(len(lst)-1):
            if lst[i]>lst[i+1]:
                lst[i+1],lst[i] = lst[i],lst[i+1]
                flag = True
    return lst


if __name__ == '__main__':
    d = [5,3,22,45,1,4,2,-3,2,55,1,0,-33]
    r = sort_shake(d)
    print(r)