import csv
import random
import math
def getdata():
    with open('DelayData.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        num=0
        variable = []
        data = []
        for row in csv_reader:
            if num == 0:
                variable = row
            else:
                data.append(row)
            num+=1
        return variable,data
def get_sample(variables,data,var_analysis):
    all_sample = []
    number = []
    for i in var_analysis:
        for j in range(len(variables)):
            if variables[j] == i:
                number.append(j)
                break

    for item in data:
        now = []
        for i in number:
            now.append(item[i])
        all_sample.append(now)
    return all_sample
def distance(X,Y):
    sum=0
    for i in range(len(X)):
        sum += ((float)(X[i])-(float)(Y[i]))**2
    return math.sqrt(sum)
def water(sample):
    res = []
    for item in sample:
        for i in item:
            if i == 'NaN':
                break
        else:
            res.append(item)
    print(len(sample),len(res))
    return res
def KMeans(sample,k):
    choice = random.sample(sample,k)
    T = 100
    while(T>=0):
        print("{} times left".format(T))
        T-=1
        belong = []
        for i in range(len(choice)):
            belong.append(0)
        #print(belong)
        sum = []
        for i in range(len(choice)):
            sum.append([])
            for j in range(len(choice[0])):
                sum[i].append(0)
        #print(sum)
        for i in range(len(sample)):
            dis = -1
            pos = -1
            for j in range(len(choice)):
                if dis == -1:
                    dis = distance(sample[i],choice[j])
                    pos = j
                elif dis>distance(sample[i],choice[j]):
                    dis = distance(sample[i], choice[j])
                    pos = j
            belong[pos]+=1
            for j in range(len(choice[0])):
                sum[pos][j]+=(float)(sample[i][j])
        #print(sum)
        #print(belong)
        new_choice = []
        for item in range(len(sum)):
            now = []
            for i in sum[item]:
                now.append(i/belong[item])
            new_choice.append(now)
        #print(new_choice)
        choice = new_choice
    print(choice)
    return choice

def display(sample,result):
    with open('result.txt','w') as file:

        maxdis = []
        to = []
        for i in range(len(result)):
            maxdis.append(0)
        for i in range(len(sample)):
            dis = -1
            pos = -1
            for j in range(len(result)):
                if dis == -1:
                    dis = distance(sample[i], result[j])
                    pos = j
                elif dis > distance(sample[i], result[j]):
                    dis = distance(sample[i], result[j])
                    pos = j
            maxdis[pos] = max(maxdis[pos],dis)
            to.append(pos)
        print(maxdis)
        final = 0
        for i in range(len(sample)):
            if distance(sample[i],result[to[i]]) < 0.6*maxdis[to[i]]:
                final += 1
        file.write('{} {}\n'.format(final, len(result)))
        for i in range(len(sample)):
            if distance(sample[i],result[to[i]]) < 0.6*maxdis[to[i]]:
                file.write('{} {} {}\n'.format(sample[i][0],sample[i][1],to[i]))

if __name__ == '__main__':
    variables,data = getdata()
    print("Get Data Successfully!")
    var_analysis = ['dayofmonth', 'dayofweek', 'scheduledhour', 'numflights', 'depdelay','arrdelay']
    var_analysis = ['windspeedsquare','arrdelay']
    all_sample = get_sample(variables,data,var_analysis)
    print("Get Sample Successfully!")
    all_sample = water(all_sample)
    print("Get valid Sample!")
    result = KMeans(all_sample,5)
    display(all_sample,result)