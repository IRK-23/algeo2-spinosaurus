from PIL import Image
import numpy as np
import json
import os
from typing import Tuple
from ..algorithms.eigenvalue import vector_length
from ..algorithms.svd import truncated_svd

class PCA:
	def __init__(self, k):
		self.N_ENTRIES = 523
		self.IMG_WIDTH = 200
		self.IMG_HEIGHT = 300
		self.k = k
		self.u = None
		self.uMatrix = None
		self.coeffMatrix = None

	def fit(self, data_dir: str = "data"):
		mapper_path = os.path.join(data_dir, "mapper.json")
		with open(mapper_path, 'r', encoding='utf-8') as f:
			mapper = json.load(f)
		cover_paths = [entry["cover"] for entry in mapper.values()]

		# RGB flattened
		# datasetMatrix = np.zeros((self.IMG_WIDTH * self.IMG_HEIGHT * 3, self.N_ENTRIES))
		# for x in range(min(self.N_ENTRIES, len(cover_paths))):
		# 	img_path = os.path.join(data_dir, cover_paths[x])
		# 	img = Image.open(img_path).convert('RGB').resize((self.IMG_WIDTH, self.IMG_HEIGHT))
		# 	imageMatrix = np.array(img)
		# 	datasetMatrix[:, x] = imageMatrix.flatten()

		# Grayscale (PIL built-in)
		# datasetMatrix = np.zeros((self.IMG_WIDTH * self.IMG_HEIGHT, self.N_ENTRIES))
		# for x in range(min(self.N_ENTRIES, len(cover_paths))):
		# 	img_path = os.path.join(data_dir, cover_paths[x])
		# 	img = Image.open(img_path).convert('L').resize((self.IMG_WIDTH, self.IMG_HEIGHT))
		# 	imageMatrix = np.array(img)
		# 	datasetMatrix[:, x] = imageMatrix.flatten()

		# Grayscale (manual)
		datasetMatrix = np.zeros((self.IMG_WIDTH * self.IMG_HEIGHT, self.N_ENTRIES))
		for x in range(min(self.N_ENTRIES, len(cover_paths))):
			img_path = os.path.join(data_dir, cover_paths[x])
			img = Image.open(img_path).convert('RGB').resize((self.IMG_WIDTH, self.IMG_HEIGHT))
			imageMatrix = np.array(img)
			iter = 0
			for y in imageMatrix:
				for z in y:
					datasetMatrix[iter, x] = 0.2126 * z[0] + 0.7152 * z[1] + 0.0722 * z[2]
					iter += 1

		self.u = np.mean(datasetMatrix, axis=1)
		datasetMatrix = datasetMatrix.T
		for x in range(datasetMatrix.shape[0]):
			datasetMatrix[x] -= self.u
		datasetMatrix = datasetMatrix.T
		self.uMatrix = truncated_svd(datasetMatrix, self.k)[0]
		self.coeffMatrix = np.zeros((self.N_ENTRIES, self.k))
		for x in range(self.N_ENTRIES):
			self.coeffMatrix[x] = np.matmul(self.uMatrix.T, datasetMatrix.T[x])

		return self

	def process_uploaded_image(self, image_path):
		# RGB flattened
		# img = Image.open(image_path).convert('RGB').resize((self.IMG_WIDTH, self.IMG_HEIGHT))
		# imageMatrix = np.array(img)
		# img_vector = imageMatrix.flatten()

		# Grayscale (PIL built-in)
		# img = Image.open(image_path).convert('L').resize((self.IMG_WIDTH, self.IMG_HEIGHT))
		# imageMatrix = np.array(img)
		# img_vector = imageMatrix.flatten()

		# Grayscale (manual)
		img = Image.open(image_path).convert('RGB').resize((self.IMG_WIDTH, self.IMG_HEIGHT))
		imageMatrix = np.array(img)
		img_vector = np.zeros(self.IMG_WIDTH * self.IMG_HEIGHT)
		iter = 0
		for y in imageMatrix:
			for z in y:
				img_vector[iter] = 0.2126 * z[0] + 0.7152 * z[1] + 0.0722 * z[2]
				iter += 1

		img_vector = img_vector - self.u
		img_coeffs = np.matmul(self.uMatrix.T, img_vector)
		return img_coeffs

	def find_similar_to_uploaded(self, image_path, n=5) -> Tuple[np.ndarray, np.ndarray]:
		img_coeffs = self.process_uploaded_image(image_path)
		dArray = np.zeros((self.N_ENTRIES, 2))
		for x in range(self.N_ENTRIES):
			dArray[x, 0] = vector_length(img_coeffs - self.coeffMatrix[x])
			dArray[x, 1] = x
		indices = dArray[:, 0].argsort()
		sorted_dArray = dArray[indices]
		out_indices = np.zeros(n)
		out_distances = np.zeros(n)
		for i in range(n):
			out_indices[i] = sorted_dArray[i, 1]
			out_distances[i] = sorted_dArray[i, 0]
		return out_indices, out_distances

	def calculate_pca(self, idx, n) -> np.ndarray:
		dArray = np.zeros((self.N_ENTRIES, 2))
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

	def save(self, output_dir: str):
		os.makedirs(output_dir, exist_ok=True)
		np.save(os.path.join(output_dir, 'u.npy'), self.u)
		np.save(os.path.join(output_dir, 'uMatrix.npy'), self.uMatrix)
		np.save(os.path.join(output_dir, 'coeffMatrix.npy'), self.coeffMatrix)

	def load(self, input_dir: str):
		self.u = np.load(os.path.join(input_dir, 'u.npy'))
		self.uMatrix = np.load(os.path.join(input_dir, 'uMatrix.npy'))
		self.coeffMatrix = np.load(os.path.join(input_dir, 'coeffMatrix.npy'))
		return self

