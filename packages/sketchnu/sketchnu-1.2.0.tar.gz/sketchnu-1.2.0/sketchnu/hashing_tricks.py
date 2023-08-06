"""
Sketchnu has Numba implementations of sketch algorithms and other useful functions 
that utilize hash functions.

Copyright (C) 2022 Matthew Hendrey

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from numba import njit, types, float32, uint32, int64, uint64
import numpy as np
from typing import List, Iterable

from sketchnu.hashes import fasthash64


@njit(uint64(uint64))
def splitmix64(index):
    """
    Fast, simple function for taking an integer and returning a random number. Function
    used in Java random number generator.

    Parameters
    ----------
    index : uint64

    Returns
    -------
    uint64
    """
    z = index + uint64(0x9E3779B97F4A7C15)
    z = (z ^ (z >> uint64(30))) * uint64(0xBF58476D1CE4E5B9)
    z = (z ^ (z >> uint64(27))) * uint64(0x94D049BB133111EB)

    return z ^ (z >> uint64(31))


@njit(float32[:, :](float32[:], int64[:], int64[:], int64))
def random_projection(
    data: np.ndarray, indices: np.ndarray, indptr: np.ndarray, d: int
):
    """
    Randomly project a sparse matrix (standard CSR representation) to a dense vector by
    effectively multiplying by a random matrix whose elements are -1 or 1. The
    projection matrix is never stored in memory. Instead the elements are generated as
    needed using splitmix64(). **Note** Projection dimension, `d`, is rounded to a
    multiple of 64 since we generate random bits in batches of 64.

    The column indices for row i are stored in indices[indptr[i]:indptr[i+1]] and the
    corresponding values are stored in data[indptr[i]:indptr[i+1]].

    Parameters
    ----------
    data : np.ndarray, shape=(nnz,), dtype=float32
        The values of the nonzero elements in the sparse csr_matrix where nnz = number
        of nonzero elements
    indices : np.ndarray, shape=(nnz,), dtype=int64
        The column indices of the nonzero elements in the sparse csr_matrix
    indptr : np.ndarray, shape=(n_rows+1,), dtype=int64
        Pointers into `data` and `indices` to indicate where the rows start and stop.
        If you have just a single record, then indtpr=[0, len(data)]
    d : int
        Output dimension of dense vectors.
    
    Returns
    -------
    X : np.ndarray, shape=(n_rows, d), dtype=float32
        Dense 2-d array containing the randomly projected dense vectors for each row of
        the input sparse matrix.
    """
    assert data.shape == indices.shape, f"Shape of data and indices do not match"
    assert data.ndim == 1, f"data and indices must be 1-d"
    assert indptr.ndim == 1, f"indptr must be 1-d"

    d = max(64, d // 64 * 64)
    n_rows = indptr.shape[0] - 1
    X = np.zeros((n_rows, d), float32)

    # Iterate through the rows
    for row_id in range(n_rows):
        # Get the slices that correspond to just row_id
        index = indices[indptr[row_id] : indptr[row_id + 1]]
        value = data[indptr[row_id] : indptr[row_id + 1]]
        # Accumulate the matrix-vector project one column at a time
        for i in range(index.size):
            # Incrementally generate a column of the random matrix, 64 bits at a time
            # Multiply it by the corresponding element of the sparse vector
            # Accumulate the result in the dense projection vector
            n_chunks = d // 64
            for chunk in range(n_chunks):
                bits = splitmix64(index[i] * n_chunks + chunk)
                for bitpos in range(64):
                    sign = ((bits >> bitpos) & 1) * 2 - 1
                    X[row_id, chunk * 64 + bitpos] += sign * value[i]

    return X
