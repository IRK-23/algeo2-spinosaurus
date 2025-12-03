from PIL import Image
import numpy as np
from typing import Tuple
from .eigenvalue import vector_length
from .svd import truncated_svd

class PCA:
	def __init__(self, k):
		self.N_ENTRIES = 523
		self.IMG_WIDTH = 200
		self.IMG_HEIGHT = 300
		self.k = k
		self.datasetMatrix = np.zeros((self.IMG_WIDTH * self.IMG_HEIGHT, self.N_ENTRIES))
		for x in range(self.N_ENTRIES):
			img = Image.open("sample.jpg") #placeholder
			imageMatrix = np.array(img)
			iter = 0
			for y in imageMatrix.T:
				for z in y:
					self.datasetMatrix[iter, x] = 0.0722 * z[0] + 0.7152 * z[1] + 0.2126 * z[2] #BGR
					iter += 1
		
		u = np.zeros(self.IMG_WIDTH * self.IMG_HEIGHT)
		for x in range(self.N_ENTRIES):
			for y in range(self.IMG_WIDTH * self.IMG_HEIGHT):
				u[y] += self.datasetMatrix[y, x]
		u /= self.N_ENTRIES
		self.datasetMatrix = self.datasetMatrix.T
		for x in range(self.datasetMatrix.shape[0]):
			self.datasetMatrix[x] -= u
		self.datasetMatrix = self.datasetMatrix.T
		self.uMatrix = truncated_svd(datasetMatrix, self.k)[0]
		self.coeffMatrix = np.zeros((self.N_ENTRIES, self.k))
		for x in range(self.N_ENTRIES):
			self.coeffMatrix[x] = np.matmul(self.uMatrix.T, self.datasetMatrix.T[x])

	def calculate_pca(self, idx, n) -> np.ndarray:
		dArray = np.zeros(self.N_ENTRIES, 2)
		xArray = self.coeffMatrix[idx]
		for x in range(self.N_ENTRIES):
			dArray[x, 0] = vector_length(xArray - self.coeffMatrix[x])
			dArray[x, 1] = x
		indices = dArray[:, 0].argsort()
		sorted_dArray = dArray[indices]
		out = np.zeros(n)
		i = 0
		iter = 0
		while i < n:
			if sorted_dArray[iter, 1] != idx:
				out[i] = sorted_dArray[iter, 1]
				i += 1
			iter += 1
		return out