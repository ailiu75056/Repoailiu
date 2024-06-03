#functions for caluclating values for operations
from offset import Offset
from datetime import datetime

#allocateOffset takes the list of offsets available and list of offsets already allocated, the purchase amount, the price of the offset per KG, and the customer id and returns a tuple of the offsets allocated, the remaining amount, and a 
#tuple indicating the list of offsets allocated to the customer, the reamining amount, if the purchase was successfully fulled allocated
#offsetAllocation should be a list of tuples with the offset id, customerID, and amount assigned, and datetime
def allocateOffset(offsetList:list, purchaseAmount:float, offsetPriceKG:float, offsetAllocation:list, customerId: str) -> tuple:
    remainingAmount = purchaseAmount/offsetPriceKG #amount to be assigned starts at the purchase amount converted to KG
    
    avaiableOffsets = [(x.id, x.offsetKG - sum([x for x in offsetAllocation if x[0] == x.id])) for x in offsetList]
    def efficientAllocation():
        i = min(avaiableOffsets, key=lambda amt:abs(amt-remainingAmount)) # the offset with the amount of unallocated offset closest to the remaining amount
        return (i[0],i[1])
    
    while remainingAmount > 0:
        offsetID, offsetKG = efficientAllocation()
        offsetAllocated= []
        if remainingAmount > sum([x[1] for x in avaiableOffsets]): #check if available offset stock is less than the remaining amount
            return (offsetAllocated, remainingAmount,False)
        if offsetKG > remainingAmount:
            offsetAllocation.append((offsetID, remainingAmount, customerId, datetime.now()))
            offsetAllocated.append((offsetID))
            remainingAmount = 0
            return (offsetAllocated, remainingAmount,True) #return the offset allocated and the remaining amount of 0
        else:
            offsetAllocation.append((offsetID, offsetKG, customerId, datetime.now()))
            remainingAmount -= offsetKG
            continue #continue to the next iteration of the loop to allocate the remaining amount

    return None