#functions for caluclating values for operations
from offset import Offset
from datetime import datetime

#allocateOffset takes the list of offsets available and list of offsets already allocated, the purchase amount, the price of the offset per KG, and the customer id and returns a tuple of the offsets allocated, the remaining amount, and a 
#tuple indicating the list of offsets allocated to the customer, the reamining amount, if the purchase was successfully fulled allocated
#offsetAllocation should be a list of tuples with the offset id, customerID, and amount assigned, and datetime
def allocateOffset(offsetList:list, purchaseAmount:float, offsetPriceKG:float, offsetAllocation:list, customerId: str) -> tuple:
    remainingAmountKG = purchaseAmount/offsetPriceKG #amount to be assigned starts at the purchase amount converted to KG
    
    avaiableOffsets = [(x.id, x.offsetKG - sum([x for x in offsetAllocation if x[0] == x.id])) for x in offsetList]
    def efficientAllocation():
        i = min(avaiableOffsets, key=lambda amt:abs(amt-remainingAmountKG)) # the offset with the amount of unallocated offset closest to the remaining amount
        return (i[0],i[1])
    
    while remainingAmountKG > 0:
        offsetID, offsetKG = efficientAllocation()
        offsetAllocated= []
        if remainingAmountKG > sum([x[1] for x in avaiableOffsets]): #check if available offset stock is less than the remaining amount
            return (offsetAllocated, remainingAmountKG*offsetPriceKG,False)
        if offsetKG > remainingAmountKG:
            offsetAllocation.append((offsetID, remainingAmountKG*offsetPriceKG, customerId, datetime.now()))
            offsetAllocated.append((offsetID))
            remainingAmountKG = 0
            return (offsetAllocated, remainingAmountKG*offsetPriceKG,True) #return the offset allocated and the remaining amount of 0
        else:
            offsetAllocation.append((offsetID, offsetKG, customerId, datetime.now()))
            remainingAmountKG -= offsetKG
            continue #continue to the next iteration of the loop to allocate the remaining amount

    return None