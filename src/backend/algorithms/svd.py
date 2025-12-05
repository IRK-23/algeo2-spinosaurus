import numpy as np
from typing import Tuple
from .eigenvalue import qr_algorithm, create_diagonal_matrix


def svd(A: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    m, n = A.shape

    ATA = A.T @ A

    eigenvalues, eigenvectors = qr_algorithm(ATA)

    idx = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]

    eigenvalues = np.maximum(eigenvalues, 0)

    singular_values = np.sqrt(eigenvalues)

    # right singular vectors (eigenvector A^T * A)
    V = eigenvectors

    # rank (nonzero)
    rank = np.sum(singular_values > 1e-7)

    # left singular vectors
    # U = A * V * (sigma)^(-1)
    U = np.zeros((m, rank))
    for i in range(rank):
        if singular_values[i] > 1e-7:
            U[:, i] = (A @ V[:, i]) / singular_values[i]

    sigma_matrix = create_diagonal_matrix(singular_values[:rank])
    V = V[:, :rank]

    return U, sigma_matrix, V.T


def truncated_svd(A: np.ndarray, k: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    U, sigma, VT = svd(A)

    # top k components
    k = min(k, min(U.shape[1], sigma.shape[0], VT.shape[0]))

    U_k = U[:, :k]
    sigma_k = sigma[:k, :k] if sigma.ndim == 2 else create_diagonal_matrix(sigma[:k])
    V_k = VT[:k, :]

    return U_k, sigma_k, V_k



