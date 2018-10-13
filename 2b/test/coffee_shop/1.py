#testing
import os
from PIL import Image
import math
import random

def print_pixel_mat(pix,w,h):
	for i in range(w):
		for j in range(h):
			print(pix[i][j],end=" ")
		print()

def copy(pix_stable,pix,w,h):
	for i in range(w):
		for j in range(h):
			pix_stable[i][j] = pix[i,j];

def make_stable(pix,w,h):
	w_d = math.ceil(w/32)
	h_d = math.ceil(h/32) 
	w_r = w%32
	h_r = h%32
	pix_stable = [[[0 for i in range(3)] for j in range(h_d*32)] for k in range(w_d*32)]
	copy(pix_stable,pix,w,h)
	print(len(pix_stable)," ",len(pix_stable[0]))
	# print_pixel_mat(pix_stable,w_d*32,h_d*32)
	# pix_stable = pix;
	l=w-w_r;
	b=h-h_r;
	i=0
	if(h_r!=0):
		while(i<(w)):
			j=h_r
			k=0
			while(j<32):
				pix_stable[i][b+j] = pix_stable[i][b+k] 
				j+=1
				k+=1
			i+=1;

	j=0
	if(w_r!=0):
		while(j<(h_d*32)):
			i=w_r
			k=0
			while(i<32):
				pix_stable[l+i][j] = pix_stable[l+k][j] 
				i+=1
				k+=1
			j+=1;
	# print_pixel_mat(pix_stable,w_d*32,h_d*32)
	return pix_stable;

def extract_image_features(img_name,train):
	im = Image.open(img_name + '.jpg') # Can be many different formats.
	pix = im.load()
	w = im.size[0]
	h = im.size[1]
	print(w,"----",h)
	pix_stable = make_stable(pix,w,h)
	w = len(pix_stable)
	h = len(pix_stable[0])
	print(((w*h)/(32*32)));
	i=j=0
	l=b=0
	file = open(img_name + ".txt",'w')
	while(l<w):
		b=0
		while(b<h):
			s=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
			# print(l,"---",b)
			for i in range(32):
				for j in range(32):	
					r = int((pix_stable[i+l][j+b][0])/32)
					g = int((pix_stable[i+l][j+b][1])/32)
					br = int((pix_stable[i+l][j+b][2])/32)
					s[r]+=1
					s[8+g]+=1
					s[16+br]+=1
			b=b+32
			string=""
			for x in range(24):
				string += str(s[x])
				if(x<23):
					string += " "

				# file.write(str([x]));
				# file.write(" ")
				# train.write(str(s[x]));
				# train.write(" ")
			# string = string[:-1]
			file.write(string)
			file.write("\n")
			train.write(string)
			train.write("\n")
			# print(s);
			# print(b)
		l=l+32;


def dist_cal(x,y):
	sum = 0
	for i in range(len(x)):
		sum += ((x[i]-y[i])*(x[i]-y[i]))
	return sum

def split_line_int(line):
	line = line.split()
	for j in range(24):
		line[j] = float(line[j])
	return line;

def dist(cluster,x):
	dist = 0;
	for i in range(24):
		diff = x[i]-cluster[i]
		dist+= diff ** 2
	return dist

def which_cluster(clusters,x):
	point =0
	min=0;
	for i in range(32):
		if(i==0):
			min = dist(clusters[i],x);
			point = i;
		else:
			if(min>dist(clusters[i],x)):
				min = dist(clusters[i],x);
				point = i;
	return point;

def make_output():

	cluster_file = open("clusters.txt",'r')
	lines_in_clusters = cluster_file.readlines()
	clusters = [[0 for x in range(24)] for y in range(32)]
	for i in range(len(lines_in_clusters)):
		clusters[i] = lines_in_clusters[i];
		clusters[i] = clusters[i].split();
		for j in range(24):
			clusters[i][j] = float(clusters[i][j])

	files = os.listdir()
	output = open('output.txt','w')
	count = [0 for i in range(32)]
	for f in files:
		if f.endswith("jpg"):
			f = os.path.splitext(f)[0]
			file = open(f + ".txt",'r')
			lines = file.readlines()
			size = len(lines)
			for i in range(size):
				x = split_line_int(lines[i]);
				cluster_point = which_cluster(clusters,x)
				count[cluster_point]+=1
			output.write(f)
			output.write(" - ")
			output.write(str(size))
			output.write(" - ")
			s = ""
			for i in range(32):
				if(i<31):
					s+=str(count[i]) + " "
				else:
					s+=str(count[i])
				count[i]=0
			output.write(s);
			output.write("\n");

def k_cluster_apply():
	train = open("train.txt",'r')
	lines = train.readlines()
	size = len(lines)
	random_k_points = random.sample(range(0, size-1), 32)
	print(random_k_points)
	clusters = [[0.0 for x in range(24)] for y in range(32)]
	for i in range(32):
		clusters[i] = lines[random_k_points[i]];
		clusters[i] = clusters[i].split();
		for j in range(24):
			clusters[i][j] = float(clusters[i][j])
			print(clusters[i][j],end=' ')
		print();

	counter = 0
	size_each_cluster = [0.0 for x in range(32)]
	update_clusters = [[0.0 for x in range(24)] for y in range(32)]
	cluster_point=0
	x = [0 for i in range(24)]
	flag=1
	diff = 0.0 
	cost_prev_j=0.0
	cost_cur_j=0.0

	print(size);
	# while(flag>0 or diff>0.001):
	# 	cost_cur_j=0
	# 	print(counter)
	# 	for i in range(32):
	# 		size_each_cluster[i]=0.0;
	# 	for i in range(32):
	# 		for j in range(24):
	# 			update_clusters[i][j]=0.0;

	# 	for i in range(size):
	# 		x = split_line_int(lines[i])
	# 		cluster_point = which_cluster(clusters,x)
	# 		cost_cur_j += dist(clusters[cluster_point],x)
	# 		# print(i,"-------",cluster_point)
	# 		size_each_cluster[cluster_point]+=1;
	# 		for j in range(24):
	# 			update_clusters[cluster_point][j] += x[j];

	# 	total=0
	# 	for i in range(32):
	# 		total += size_each_cluster[i];
	# 	print("total = ", total," --- ",size_each_cluster)

	# 	for i in range(32):
	# 		for j in range(24):
	# 			# t = 5.0/(size_each_cluster[i])
	# 			if size_each_cluster[i]!=0:
	# 				update_clusters[i][j] /= size_each_cluster[i]
	# 			else:
	# 				update_clusters[i][j]=0 
	# 			clusters[i][j] = update_clusters[i][j];

	# 	print(cost_prev_j, "   ", cost_cur_j)
	# 	diff = abs( cost_prev_j-cost_cur_j )
	# 	print("diff = ",diff)
	# 	flag-=1
	# 	# if(flag==1):
	# 	cost_prev_j = cost_cur_j
	# 	# else:

	# 	flag=0
	# 	counter+=1

	# print(clusters)
	cluster_file = open("clusters.txt",'w')
	for i in range(32):
		s=""
		for j in range(24):
			s+=str(clusters[i][j])
			if(j<23):
				s+=" "
		cluster_file.write(s)
		cluster_file.write("\n")

	make_output()

def main():
	directory = os.getcwd()
	files = os.listdir()
	i=0
	# train = open("train.txt",'w')
	# for f in files:
	# 	if f.endswith("jpg"):
	# 		f = os.path.splitext(f)[0]
	# 		print(i,"----",f);
	# 		extract_image_features(f,train);
	# 		i+=1;

	k_cluster_apply();


if __name__== "__main__":
	main()