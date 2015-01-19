def readfile(filename):
	lines = [line for line in file(filename)]

	colnames = lines[0].strip().split('\t')[1:]
	rownames = []
	data = []
	for line in lines[1:]:
		p = line.strip().split('\t')
		rownames.append(p[0])
		data.append([float(x) for x in p[1:]])
	return rownames,colnames,data

from math import sqrt
def pearson(v1,v2):
	sum1 = sum(v1)
	sum2 = sum(v2)

	sum1sq = sum([pow(v,2) for v in v1])
	sum2sq = sum([pow(v,2) for v in v2])

	pSum = sum([v1[i]*v2[i] for i in range(len(v1))])

	num = pSum - (sum1*sum2/len(v1))
	den = sqrt((sum1sq-pow(sum1,2)/len(v1))*(sum2sq-pow(sum2,2)/len(v1)))
	if den == 0 :return 0

	return 1.0 - num/den


class bicluster:
	def __init__(self,vec,left = None,right = None,distance = 0.0,id = None):
		self.left = left
		self.right = right
		self.vec = vec
		self.id = id
		self.distance = distance

def hcluster(rows,distance = pearson):
	distances = {}
	currentclustid = -1

	# Clusters are initially just the rows
	clust = [bicluster(rows[i],id = i) for i in range(len(rows))]

	while len(clust) > 1:
		lowestpair = (0,1)
		closest = distance(clust[0].vec,clust[1].vec)

		# loop through every pair looking for the smallest distance
		for i in range(len(clust)):
			for j in range(i + 1,len(clust)):
				if (clust[i].id,clust[j].id) not in distances:
					distances[(clust[i].id,clust[j].id)] = distance(clust[i].vec,clust[j].vec)

				d = distances[(clust[i].id,clust[j].id)]
				if d < closest:
					closest = d
					lowestpair = (i,j)

		# calculate the average of the two clusters
		mergevec = [(clust[lowestpair[0]].vec[i]+clust[lowestpair[1]].vec[i])/2.0 for i in range(len(clust[0].vec))]

		# create the new cluster
		newcluster = bicluster(mergevec,left = clust[lowestpair[0]],right = clust[lowestpair[1]],
								distance = closest,id = currentclustid)

		currentclustid -= 1
		del clust[lowestpair[1]]
		del clust[lowestpair[0]]
		clust.append(newcluster)

	return clust[0]

def printclust(clust,labels = None,n = 0):
	# indent to make a hierarchy layout
	for i in range(n):print ' ',
	if clust.id < 0:
		# negative id means that this is branch
		print "-"
	else:
		# positive id means that this is an endpoint
		if labels == None: print clust.id
		else:print labels[clust.id]

	# now print the right and left branches
	if clust.left!=None: printclust(clust.left,labels=labels,n=n+1)
	if clust.right!=None: printclust(clust.right,labels=labels,n=n+1)



import random

def kcluster(rows,distance = pearson, k = 4):
	# Determine the minimum and maximum values for each point
	ranges=[(min([row[i] for row in rows]),max([row[i] for row in rows])) for i in range(len(rows[0]))]

	# Create k randomly placed centroids
	clusters=[[random.random()*(ranges[i][1]-ranges[i][0])+ranges[i][0] for i in range(len(rows[0]))] for j in range(k)]

	lastmatches=None
	for t in range(100):
		print 'Iteration %d' % t
		bestmatches=[[] for i in range(k)]
	
		# Find which centroid is the closest for each row
		for j in range(len(rows)):
			row=rows[j]
			bestmatch=0
			for i in range(k):
				d=distance(clusters[i],row)
				if d<distance(clusters[bestmatch],row): bestmatch=i
			bestmatches[bestmatch].append(j)

		# If the results are the same as last time, this is complete
		if bestmatches==lastmatches: break
		lastmatches=bestmatches
	
		# Move the centroids to the average of their members
		for i in range(k):
			avgs=[0.0]*len(rows[0])
			if len(bestmatches[i])>0:
				for rowid in bestmatches[i]:
					for m in range(len(rows[rowid])):
						avgs[m]+=rows[rowid][m]
			for j in range(len(avgs)):
				avgs[j]/=len(bestmatches[i])
			clusters[i]=avgs
	
	return bestmatches





