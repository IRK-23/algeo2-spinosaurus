import numpy as np
from typing import Tuple


def vector_length(v: np.ndarray) -> float:
    return np.sqrt(np.dot(v, v))


def create_diagonal_matrix(diagonal_values: np.ndarray) -> np.ndarray:
    n = len(diagonal_values)
    matrix = np.zeros((n, n))
    for i in range(n):
        matrix[i, i] = diagonal_values[i]
    return matrix


def extract_diagonal(matrix: np.ndarray) -> np.ndarray:
    n = matrix.shape[0]
    return np.array([matrix[i, i] for i in range(n)])


def qr_decomposition(A: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    m, n = A.shape
    Q = np.zeros((m, n))
    R = np.zeros((n, n))

    for j in range(n):
        v = A[:, j].copy()

        for i in range(j):
            R[i, j] = np.dot(Q[:, i], A[:, j])
            v = v - R[i, j] * Q[:, i]

        R[j, j] = vector_length(v)
        if R[j, j] > 1e-10:
            Q[:, j] = v / R[j, j]
        else:
            Q[:, j] = v

    return Q, R


def qr_algorithm(A: np.ndarray, max_iter: int = 1000, tol: float = 1e-10) -> Tuple[np.ndarray, np.ndarray]: #aproksimasi
    n = A.shape[0]
    A_k = A.copy()
    Q_total = np.eye(n)

    for _ in range(max_iter):
        Q, R = qr_decomposition(A_k)
        A_k_new = R @ Q
        Q_total = Q_total @ Q

        diag_elements = extract_diagonal(A_k_new)
        diag_matrix = create_diagonal_matrix(diag_elements)
        off_diag = np.sum(np.abs(A_k_new - diag_matrix))
        if off_diag < tol:
            break

        A_k = A_k_new

    eigenvalues = extract_diagonal(A_k)
    eigenvectors = Q_total

    return eigenvalues, eigenvectors


