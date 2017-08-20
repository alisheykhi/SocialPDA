class SwarmPDAFunction():


    def __init__(self):
        pass

    def transposition (self,position = [], lambda_tuple = (), *args):
        position[lambda_tuple[0]],position[lambda_tuple[1]] = position[lambda_tuple[1]],position[lambda_tuple[0]]
        return position

    def truncation (self, r, velocityList= [], *args):
        del velocityList[int(r*len(velocityList)):]
        return velocityList

    def concatenation (self, velocityList1= [], velocityList2= [] , *args):
        return velocityList1+velocityList2

    def displacement (self, positionList= [], velocityList = [] , * args ):
        vel = []
        while velocityList:
            vel.append(velocityList.pop())
        for _ in range(0,len(vel)):
            self.transposition(positionList ,vel.pop())
        return positionList

    def subtraction (self, positionList1 = [], positionList2 = [], *args ):
        velocityList = []
        flag = [False] * len(positionList1)
        pos1 = positionList1[:]
        pos2 = positionList2[:]
        for i, posx in enumerate(pos1):
            for j, posy in enumerate(pos2):
                if not flag[j] and posx == posy:
                    velocityList.append((posx,j))
                    flag[j] = True
        return self.__selectionSort(velocityList)

    def __selectionSort(self,alist):
        lambda_tuple =[]
        for fillslot in range(len(alist)-1,0,-1):
            positionOfMax=0
            for location in range(1,fillslot+1):
                if alist[location][1]>alist[positionOfMax][1]:
                    positionOfMax = location
            if fillslot != positionOfMax :
                alist[fillslot],alist[positionOfMax] = alist[positionOfMax],alist[fillslot]
                lambda_tuple.append((fillslot,positionOfMax))
        return lambda_tuple




