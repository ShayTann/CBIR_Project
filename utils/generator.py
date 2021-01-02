import random;

def generate_weights(weights_old=[1/3,1/3,1/3]):
    a = random.randint(1,3)  #Chose one random weights to start our changing
    x=0 #Temporary variables
    y=0
    z=0
    if a==1:
        # print('in 1')
        x=random.randint(1,20) 
        x=round(1/x,3) #Generate the first weight
        y=round(random.uniform(0.001,(1-x)),3) #Generate the second weight
        z=round(1-(x+y),3) #Generate the last weight by 1- sum(w1+w2 ) because we know we need to have 1 as sum of all weights
        f = open("utils\\weights.txt", "r") #We store the old weights generated for an input in a text file to avoid generate same weights twice
        for line in f.readlines():
            test = line.split(",")
            if x==float(test[0]) and y== float(test[1]) and z== float(test[2]):
                print('already exist')
                generate_weights() #In case its already generated we gonna re call this function to generate a different one
        f.close()
        

    elif a==2:
        # print('in 2')
        y=random.randint(1,20)
        y=round(1/y,3)
        x=round(random.uniform(0.001,(1-y)),3)
        z=round(1-(x+y),3)
        f = open("utils\\weights.txt", "r")
        for line in f.readlines():
            test =line.split(",")
            if x==float(test[0]) and y== float(test[1]) and z== float(test[2]):
                print('already exist')
                generate_weights()
        f.close()
        f.close()

    else:
        # print('in 3')
        z=random.randint(1,20)
        z=round(1/z,3)
        y=round(random.uniform(0.001,(1-z)),3)
        x=round(1-(z+y),3)
        f = open("utils\\weights.txt", "r")
        for line in f.readlines():
            test =line.split(",")
            if x==float(test[0]) and y== float(test[1]) and z== float(test[2]):
                print('already exist')
                generate_weights()
        f.close()
  
    f = open("utils\\weights.txt", "a") #Finally we gonna write the new weights generated in the text file then return them as a list
    f.write(str(x)+','+str(y)+','+str(z)+'\n')
    weights = [x,y,z]
    f.close
    return weights
    
def reset_weights() : #This function we'll be used in the index view to reset the weights text file every time we have a new upload
    open("utils\\weights.txt", "w").close()
    
if __name__ == "__main__":#Just for the test
    generate_weights()
    reset_weights()