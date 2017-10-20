from network2 import *
import re
import random
import string

#nw = Network([2,3,2])
#print(nw.feedforward(np.zeros((2,1))))

#print(1.0/(1.0+np.exp(np.zeros((2,1)))))

#import mnist_loader

#training_data, validation_data, test_data = mnist_loader.load_data_wrapper()

f = open("prenoms.txt","r")

train = False

def gennames(net):
    compteur = 0
    while compteur < 50:
        st = ''.join(random.choice(string.ascii_lowercase) for _ in range(random.randint(3,12)))
        result = asknet(net,st)
        if result[0]>result[1]+0.999:
            if not st in lines:
                st = st[0].upper()+st[1:]
                print(st)
                compteur+=1
            
def asknet(net,st):
    testing = np.zeros((26*12,1), dtype=np.float32)
    for j in range(min(12,len(st))):
        num = ord(st[j])-97
        if num<0 or num>25:
            continue

        testing[26*j+num][0] = 1
    result = net.feedforward(testing)
    return result

def correct(lns):
    for i in range(len(lns)):
        lns[i] = re.sub("\n","", lns[i])
        lns[i] = lns[i].lower()

lines = f.readlines()
correct(lines)
n = len(lines)

training = [(np.zeros((26*12,1), dtype=np.float32),np.zeros((2,1), dtype=np.float32)) for i in range(n)]

for i in range(n):
    for j in range(min(12,len(lines[i]))):
        num = ord(lines[i][j])-97
        if num<0 or num>25:
            continue

        training[i][0][26*j+num][0] = 1
    training[i][1][0][0] = 1
#print(training[0])

n2 = n*2

training2 = [(np.zeros((26*12,1), dtype=np.float32),np.zeros((2,1), dtype=np.float32)) for i in range(n2)]



net = Network([26*12,150,300,150,2])

if 1==1:
    for i in range(len(net.weights)):
        twei = np.loadtxt('weights'+str(i)+'.txt')
        tbia = np.loadtxt('biases'+str(i)+'.txt')
        for j in range(len(net.weights[i])):
            net.weights[i][j] = twei[j]
            net.biases[i][j] = tbia[j]

while 2==0:
    st = raw_input()
    rep = asknet(net,st)
    print(rep[0]-rep[1])

#_data[:1000]

for _ in range(1000):
    training2 = [(np.zeros((26*12,1), dtype=np.float32),np.zeros((2,1), dtype=np.float32)) for i in range(n2)]
    for i in range(len(training2)):
        le = lines[0]
        while le in lines:
            le = ''.join(random.choice(string.ascii_lowercase) for _ in range(random.randint(3,12)))
        for j in range(min(12,len(le))):
            num = ord(le[j])-97
            if num<0 or num>25:
                continue

            training2[i][0][26*j+num][0] = 1
        training2[i][1][1][0] = 1#-i%2+1



    testing_data = [(training[i][0],0) for i in range(n)]
    testing_data.extend([(training2[i][0],1) for i in range(len(training2))])

    training_data =  [training[i] for i in range(n)]
    training_data.extend(training2)

    #print(testing_data[-1])
    if train:
        random.shuffle(training_data)
        net.SGD(training_data, 5, 30, 0.3,1,None,False,False,True,True)
        for i in range(len(net.weights)):
            np.savetxt('weights'+str(i)+'.txt', net.weights[i], fmt='%.40f')
            np.savetxt('biases'+str(i)+'.txt', net.biases[i], fmt='%.40f')
    else:
        raw_input()
    gennames(net)


