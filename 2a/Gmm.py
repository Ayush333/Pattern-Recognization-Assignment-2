import matplotlib.pyplot as plt
import random
import sys
import math
from mpmath import mpf, mpc, mp

CLASS_SIZE=2488
K=8
D=2



def inverseMatrix(cov_matrix_b):
	det = (cov_matrix_b[0][0]*cov_matrix_b[1][1]) - (cov_matrix_b[0][1]*cov_matrix_b[1][0])
	inv_matrix=[[0 for i in range(2)]for j in range(2)]
	inv_matrix[0][1] = -1*cov_matrix_b[0][1]
	inv_matrix[1][0] = -1*cov_matrix_b[1][0]
 
	inv_matrix[0][0] = cov_matrix_b[1][1]
	inv_matrix[1][1] = cov_matrix_b[0][0];

	for i in range(D):
		for j in range(D):
			inv_matrix[i][j] /= det;
	return inv_matrix

def calcDet(matrix):
	det = (matrix[0][0]*matrix[1][1]) - (matrix[0][1]*matrix[1][0])        
	return det

def Distribution(x,Sigma,Mean):
	mp.dps=200
	# print("Sigma = ",Sigma)
	SigmaInverse=inverseMatrix(Sigma)
	# print("SigmaInverse = ",SigmaInverse)
	# print("x = ",x)
	# print("Mean = ",Mean)	
	mean=[0 for i in range(D)]
	for i in range(D):
		mean[i]=x[i]-Mean[i]
	# print("mean=",mean)
	t=[((mean[0]*SigmaInverse[0][0])+(mean[1]*SigmaInverse[1][0])), ((mean[0]*SigmaInverse[0][1])+(mean[1]*SigmaInverse[1][1]))]
	w0=((t[0]*mean[0])+(t[1]*mean[1]))/2
	# print("w0pehle=",w0)
	w0=-w0
	# print("w0=",w0)
	w0=(math.exp(w0))
	# print("w0 after exp",w0)
	w0/=(pow(2*math.pi,D/2)*pow(calcDet(Sigma),0.5))
	# print(w0)
	return (w0)


def main():
	mp.dps=200
	clusterCentres=[[0 for x in range(D)]for y in range(K)]
	dSet=[[0 for x in range(D+1)]for y in range(CLASS_SIZE)]
	
	f=open("Class2after8means.txt","r")
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

	oldCost=-1000000000000000
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
			# print(Gamma[i])
		# print("EffectiveN",EffectiveN)
		

		#Recalculating Sigma
		for i in range(K):
			numerator=[[0 for x in range(D)] for y in range(D)]
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
			# print(i," ",Sigma[i])

		if Sigma[0][0][1]==0 and Sigma[0][1][0]==0 and Sigma[0][1][1]==0:
			break
		
		#Recalculating mean i.e ClusterCenteres
		for i in range(K):
			numerator=[0 for i in range(D)]
			for j in range(CLASS_SIZE):
				for k in range(D):
					numerator[k]+=(Gamma[j][i]*dSet[j][k])
			for k in range(D):
				clusterCentres[i][k]=numerator[k]/EffectiveN[i]			
		
		# print("ClusterCenters",clusterCentres)


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
				PikDistribution+=(Pi[j]*Distribution(dSet[i],Sigma[j],clusterCentres[j]))
			newCost+=math.log(PikDistribution)	
		# print(newCost)
		diff=newCost-oldCost
		oldCost=newCost
		print("diff=",diff)
		counter+=1


		file=open("Class2afterGMM8c.txt","w")
		for i in range(K):
			for j in range(D):
				print(clusterCentres[i][j],end=" ")
				file.write(str(clusterCentres[i][j]))
				file.write(" ")	
			print()
			file.write("\n")
			# print("\n")

		for i in range(K):
			for j in range(D):
				for k in range(D):
					file.write(str(Sigma[i][j][k]))
					file.write(" ")		
					print(Sigma[i][j][k],end=" ")
			print()
			file.write("\n")
			# print("\n")
		
		for i in range(K):
			file.write(str(Pi[i]))
			file.write("\n")
			print(Pi[i])
			# print("\n")



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