def quicksort(cards):
    if len(cards)  < 2:
        print(cards)
    else:
        pivot = cards[0]
        less = [i for i in cards[1:] if i <= pivot]
        greater = [i for i in cards[1:] if i >= pivot]
        print(quicksort(less), [pivot], quicksort(greater))


data=[10,7,9,4,2,5,11,20,12]
print(
    data
)
quicksort(data)
