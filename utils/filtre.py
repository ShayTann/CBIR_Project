import random;

def filterr():
    a= random.randint(1,3) 
    x=0
    y=0
    z=0
    if a==1:
        print('in 1')
        x=random.randint(1,20)
        x=round(1/x,3)
        y=round(random.uniform(0.001,(1-x)),3)
        z=round(1-(x+y),3)
        f = open("tst.txt", "r")
        for line in f.readlines():
            test =line.split(",")
            if z==float(test[2]):
                print('already exist')
                filterr()
        f.close()
        

    elif a==2:
        print('in 2')
        y=random.randint(1,20)
        y=round(1/y,3)
        x=round(random.uniform(0.001,(1-y)),3)
        z=round(1-(x+y),3)
        f = open("tst.txt", "r")
        for line in f.readlines():
            test =line.split(",")
            if z==float(test[2]):
                print('already exist')
                filterr()
        f.close()
        f.close()

    else:
        print('in 3')
        z=random.randint(1,20)
        z=round(1/z,3)
        y=round(random.uniform(0.001,(1-z)),3)
        x=round(1-(z+y),3)
        f = open("tst.txt", "r")
        for line in f.readlines():
            test =line.split(",")
            if z==float(test[2]):
                print('already exist')
                filterr()
        f.close()
  
    f = open("tst.txt", "a")
    f.write(str(x)+','+str(y)+','+str(z)+'\n')
    f.close

    

if __name__ == "__main__":
    filterr()