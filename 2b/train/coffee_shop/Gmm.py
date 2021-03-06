import matplotlib.pyplot as plt
import random
import sys
import math
# from mpmath import mpf, mpc, mp
import numpy as np

CLASS_SIZE=500
K=8
D=2



def transposeMatrix(m):
    return np.array(m).T.tolist()
    # return map(list,zip(*m))  

def getMatrixMinor(m,i,j):
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

def getMatrixDeternminant(m):
    #base case for 2x2 matrix
    if len(m) == 2:
        return m[0][0]*m[1][1]-m[0][1]*m[1][0]

    determinant = 0
    for c in range(len(m)):
        determinant += ((-1)**c)*m[0][c]*getMatrixDeternminant(getMatrixMinor(m,0,c))
    return determinant

def inverseMatrix(m):
    determinant = getMatrixDeternminant(m)
    #special case for 2x2 matrix:
    if len(m) == 2:
        return [[m[1][1]/determinant, -1*m[0][1]/determinant],
                [-1*m[1][0]/determinant, m[0][0]/determinant]]

    #find matrix of cofactors
    cofactors = []
    for r in range(len(m)):
        cofactorRow = []
        for c in range(len(m)):
            minor = getMatrixMinor(m,r,c)
            cofactorRow.append(((-1)**(r+c)) * getMatrixDeternminant(minor))
        cofactors.append(cofactorRow)
    cofactors = transposeMatrix(cofactors)
    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] = cofactors[r][c]/determinant
    return cofactors



# def inverseMatrix(cov_matrix_b):
# 	det = (cov_matrix_b[0][0]*cov_matrix_b[1][1]) - (cov_matrix_b[0][1]*cov_matrix_b[1][0])
# 	inv_matrix=[[0 for i in range(2)]for j in range(2)]
# 	inv_matrix[0][1] = -1*cov_matrix_b[0][1]
# 	inv_matrix[1][0] = -1*cov_matrix_b[1][0]
 
# 	inv_matrix[0][0] = cov_matrix_b[1][1]
# 	inv_matrix[1][1] = cov_matrix_b[0][0];

# 	for i in range(D):
# 		for j in range(D):
# 			inv_matrix[i][j] /= det;
# 	return inv_matrix

# def calcDet(matrix):
# 	det = (matrix[0][0]*matrix[1][1]) - (matrix[0][1]*matrix[1][0])        
# 	return det





def Distribution(x,Sigma,Mean):
	# print("Sigma = ",Sigma)
	SigmaInverse=inverseMatrix(Sigma)
	# print("SigmaInverse = ",SigmaInverse)
	# print("x = ",x)
	# print("Mean = ",Mean)	
	mean=[[0 for x in range(D)]for y in range(1)]
    
    for i in range(D):
        mean[0][i]=x[i]-Mean[i]
	# print("mean=",mean)
	
	# t=[((mean[0]*SigmaInverse[0][0])+(mean[1]*SigmaInverse[1][0])), ((mean[0]*SigmaInverse[0][1])+(mean[1]*SigmaInverse[1][1]))]
	
	t=[[0 for x in range(D)]for y in range(1)]

    for i in range(len(mean)):
       # iterate through columns of Y
       for j in range(len(SigmaInverse[0])):
           # iterate through rows of Y
           for k in range(len(SigmaInverse)):
               t[i][j] += mean[i][k] * SigmaInverse[k][j]

    w0 = 0.0
    print(t)
    for i in range(D):
       # iterate through columns of Y
       w0 += mean[0][i]*t[0][i]   
    # print(result)



	w0/=2
	# print("w0pehle=",w0)
	w0=-w0
	# print("w0=",w0)
	w0=(math.exp(w0))
	# print("w0 after exp",w0)
	w0/=(pow(2*math.pi,D/2)*pow(getMatrixDeternminant(Sigma),0.5))
	# print(w0)
	return (w0)


def main():
	clusterCentres=[[0 for x in range(D)]for y in range(K)]
	dSet=[[0 for x in range(D+1)]for y in range(CLASS_SIZE)]
	
	f=open("Class3afterKmeans.txt","r")
	for i in range(K):
		line=next(f)
		line=line.split()
		for j in range(D):
			clusterCentres[i][j]=float(line[j])
		print(clusterCentres[i])

	for i in range(CLASS_SIZE):
		line=next(f)
		line=line.split()
		for j in range(D):
			dSet[i][j]=float(line[j])
		dSet[i][D]=int(line[D])
		print(dSet[i])
	f.close()

		

	Pi=[0 for x in range(K)]
	for i in range(CLASS_SIZE):
		Pi[dSet[i][D]]+=1
		# print(dSet[i][D])

	Sigma=[[[0 for x in range(D)]for y in range(D)]for z in range(K)]
	for i in range(CLASS_SIZE):
		for j in range(D):
			for k in range(D):
				Sigma[dSet[i][D]][j][k]+=((dSet[i][j]-clusterCentres[dSet[i][D]][j])*(dSet[i][k]-clusterCentres[dSet[i][D]][k]))
		# print(Sigma[i])
	
	
	for i in range (K):
		for j in range(D):
			for k in range(D):
				Sigma[i][j][k]/=Pi[i]
		
	for i in range(K):
		Pi[i]/=CLASS_SIZE
	# print("Pi",Pi)
	# print("Sigma=",Sigma)

	Gamma=[[0 for x in range(K)]for y in range(CLASS_SIZE)]
	Total=[0 for x in range(CLASS_SIZE)]

	oldCost=-1
	diff=20
	counter=1
	while diff>0.001:
		#Recalculating gamma
		for i in range(CLASS_SIZE):
			Total[i]=0
			for j in range(K):
				temp=(Pi[j]* Distribution(dSet[i],Sigma[j],clusterCentres[j]))
				Total[i]+=temp
			for j in range(K):
				Gamma[i][j]=(Pi[j]*Distribution(dSet[i],Sigma[j],clusterCentres[j]))/(Total[i])
			# print(Gamma[i]," ",dSet[i][D])

		#Recalulating Effective N for each cluster
		EffectiveN=[0 for i in range(K)]
		for i in range(CLASS_SIZE):
			for j in range(K):
				EffectiveN[j]+=Gamma[i][j]
		
		# print("EffectiveN",EffectiveN)

		#Recalculating mean i.e ClusterCenteres
		for i in range(K):
			numerator=[0 for i in range(D)]
			for j in range(CLASS_SIZE):
				for k in range(D):
					numerator[k]+=(Gamma[j][i]*dSet[j][k])
			for k in range(D):
				clusterCentres[i][k]=numerator[k]/EffectiveN[i]			
		
		# print("ClusterCenters",clusterCentres)

		#Recalculating Sigma
		for i in range(K):
			numerator=[[0 for i in range(D)] for j in range(D)]
			for j in range(CLASS_SIZE):
				temp=[0 for k in range(D)]
				for k in range(D):
					temp[k]=dSet[j][k]-clusterCentres[i][k]	
				for k in range(D):
					for l in range(D):
						numerator[k][l]+=(Gamma[j][i]*temp[k]*temp[l])
			for j in range(D):
				for k in range(D):
					Sigma[i][j][k]=numerator[j][k]/EffectiveN[i]
			# print(Sigma[i])
		#Recalculating Pi k

		# print("Sigma",Sigma)

		for i in range(K):
			Pi[i]=EffectiveN[i]/CLASS_SIZE
		
		# print("New Pi",Pi)

		#Calculatin new Cost


		newCost=0
		for i in range(CLASS_SIZE):
			PikDistribution=0
			for j in range(K):
				PikDistribution+=(Pi[k]*Distribution(dSet[i],Sigma[j],clusterCentres[j]))
			newCost+=math.log(PikDistribution)	
		# print(newCost)
		diff=abs(oldCost-newCost)
		oldCost=newCost
		print(diff)
		counter+=1

	file=open("Class3afterGMM.txt","w")
	for i in range(K):
		for j in range(D):
			file.write("%f "%(clusterCentres[i][j]))	
		file.write("\n")
	
	for i in range(K):
		for j in range(D):
			for k in range(D):
				file.write("%f "%(Sigma[i][j][k]))	
		file.write("\n")
	
	for i in range(K):
		file.write("%f "%(Pi[i]))
		file.write("\n")

	file.close

	return
	


	#Plotting
	for i in range(CLASS_SIZE):
		print(dSet[i][0]," ",dSet[i][1])
		maxx=0
		clusterrr=0
		for j in range(K):
			if Gamma[i][j]>maxx:
				maxx=Gamma[i][j]
				clusterrr=j
		if clusterrr==0:
			plt.plot(dSet[i][0],dSet[i][1],'bo')
		elif clusterrr==1:
			plt.plot(dSet[i][0],dSet[i][1],'go')
		elif clusterrr==2:
			plt.plot(dSet[i][0],dSet[i][1],'ro')
		elif clusterrr==3:
			plt.plot(dSet[i][0],dSet[i][1],'co')
		elif clusterrr==4:
			plt.plot(dSet[i][0],dSet[i][1],'mo')
		elif clusterrr==5:
			plt.plot(dSet[i][0],dSet[i][1],'yo')
		elif clusterrr==6:
			plt.plot(dSet[i][0],dSet[i][1],'ko')
		elif clusterrr==7:
			plt.plot(dSet[i][0],dSet[i][1],'wo')
		# elif clusterrr==8:
		# 	plt.plot(dSet[i][0],dSet[i][1],'')
		# elif clusterrr==9:
		# 	plt.plot(dSet[i][0],dSet[i][1],'')
		# elif clusterrr==10:
		# 	plt.plot(dSet[i][0],dSet[i][1],)
		# elif clusterrr==11:
		# 	plt.plot(dSet[i][0],dSet[i][1],)
		# elif clusterrr==12:
		# 	plt.plot(dSet[i][0],dSet[i][1],)
		# elif clusterrr==13:
		# 	plt.plot(dSet[i][0],dSet[i][1],)
		# elif clusterrr==14:
		# 	plt.plot(dSet[i][0],dSet[i][1],)
		# elif clusterrr==15:
		# 	plt.plot(dSet[i][0],dSet[i][1],)
		# elif clusterrr==16:
		# 	plt.plot(dSet[i][0],dSet[i][1],)
		# elif clusterrr==17:
		# 	plt.plot(dSet[i][0],dSet[i][1],)
		# elif clusterrr==18:
		# 	plt.plot(dSet[i][0],dSet[i][1],)
		# elif clusterrr==19:
		# 	plt.plot(dSet[i][0],dSet[i][1],)
		# elif clusterrr==20:
		# 	plt.plot(dSet[i][0],dSet[i][1],lor=" #75f740 ")
		# elif clusterrr==21:
		# 	plt.plot(dSet[i][0],dSet[i][1],color=" #75f740 ")
		# elif clusterrr==22:
		# 	plt.plot(dSet[i][0],dSet[i][1],color=" #75f740 ")
		# elif clusterrr==23:
		# 	plt.plot(dSet[i][0],dSet[i][1],color=" #75f740 ")
		# elif clusterrr==24:
		# 	plt.plot(dSet[i][0],dSet[i][1],color=" #75f740 ")
		# elif clusterrr==25:
		# 	plt.plot(dSet[i][0],dSet[i][1],color=" #75f740 ")
		# elif clusterrr==26:
		# 	plt.plot(dSet[i][0],dSet[i][1],color=" #75f740 ")
		# elif clusterrr==27:
		# 	plt.plot(dSet[i][0],dSet[i][1],color=" #75f740 ")
		# elif clusterrr==28:
		# 	plt.plot(dSet[i][0],dSet[i][1],color=" #75f740 ")
		# elif clusterrr==29:
		# 	plt.plot(dSet[i][0],dSet[i][1],color=" #75f740 ")
		# elif clusterrr==30:
		# 	plt.plot(dSet[i][0],dSet[i][1],color=" #75f740 ")
		# elif clusterrr==31:
		# 	plt.plot(dSet[i][0],dSet[i][1],color=" #75f740 ")
		
	plt.savefig('afterGMM.png')	




if __name__== "__main__":
	main()