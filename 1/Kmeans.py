import matplotlib.pyplot as plt
import random
import sys

def distance(pointA,pointB):
	return(((pointA[0]-pointB[0])*(pointA[0]-pointB[0]))+((pointA[1]-pointB[1])*(pointA[1]-pointB[1])))


def main():
	print("Reading")
	#Reading file 1
	dSet=[[0 for x in range(3)]for y in range(1500)]
	f=open("Class1.txt","r")
	fl=f.readlines()
	i=0
	for lines in fl:
		lines=lines.split()
		for j in range(2):
			dSet[i][j]=float(lines[j])
		i+=1
	f.close()
	#Reading file 2
	f=open("Class2.txt","r")
	fl=f.readlines()
	#dSet=[[0 for x in range(2)]for y in range(1500)]
	i=500
	for lines in fl:
		lines=lines.split()
		for j in range(2):
			dSet[i][j]=float(lines[j])
		i+=1
	f.close()
	#Reading file 3
	f=open("Class3.txt","r")
	fl=f.readlines()
	#dSet=[[0 for x in range(2)]for y in range(1500)]
	i=1000
	for lines in fl:
		lines=lines.split()
		for j in range(2):
			dSet[i][j]=float(lines[j])
		i+=1
	f.close()

	K=3

	clusterCentres=[[0 for x in range(2)]for y in range(K)]
	newclusterCentres=[[0 for x in range(3)]for y in range(K)]
	
	for x in range(K):
		r=random.randint(1,1501)
		print(r)
		clusterCentres[x][0]=dSet[r][0]
		clusterCentres[x][1]=dSet[r][1]
		

	oldCost=sys.maxsize
	diff=20
	counter=1
	while diff>0.001:
		for x in range(1500):
			min=sys.maxsize
			for y in range(K):
				if distance(clusterCentres[y],dSet[x])<min:
					min=distance(clusterCentres[y],dSet[x])
					dSet[x][2]=y
				# print(distance(clusterCentres[y],dSet[x]))
			# print(dSet[x][2])		
		
		for x in range(1500):
			newclusterCentres[dSet[x][2]][2]+=1
			newclusterCentres[dSet[x][2]][0]+=dSet[x][0]
			newclusterCentres[dSet[x][2]][1]+=dSet[x][1]
		for x in range(K):
			clusterCentres[x][0]=newclusterCentres[x][0]/newclusterCentres[x][2]
			clusterCentres[x][1]=newclusterCentres[x][1]/newclusterCentres[x][2]	
		
		newCost=0
		for x in range(1500):
			newCost+=distance(dSet[x],clusterCentres[dSet[x][2]])
		print(newCost)
		diff=oldCost-newCost
		oldCost=newCost
		print(diff)

		for i in range(1500):
			print(dSet[i][0]," ",dSet[i][1])
			if dSet[i][2]==0:
				plt.plot(dSet[i][0],dSet[i][1],'ro')
			elif dSet[i][2]==1:
				plt.plot(dSet[i][0],dSet[i][1],'go')
			elif dSet[i][2]==2:
				plt.plot(dSet[i][0],dSet[i][1],'bo')
		print("Saving ",counter)
		plt.savefig(str(counter)+".png")
		counter+=1



	print("Plotting")

	for i in range(1500):
		print(dSet[i][0]," ",dSet[i][1])
		if dSet[i][2]==0:
			plt.plot(dSet[i][0],dSet[i][1],'ro')
		elif dSet[i][2]==1:
			plt.plot(dSet[i][0],dSet[i][1],'go')
		elif dSet[i][2]==2:
			plt.plot(dSet[i][0],dSet[i][1],'bo')
	plt.show()




if __name__== "__main__":
  main()