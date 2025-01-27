import unittest
import pytest

import numpy as np
import scipy.sparse as sps
import porepy as pp


class TestSparseMath(unittest.TestCase):
    def zero_1_column(self):
        A = sps.csc_matrix(
            (np.array([1, 2, 3]), (np.array([0, 2, 1]), np.array([0, 1, 2]))),
            shape=(3, 3),
        )
        pp.matrix_operations.zero_columns(A, 0)
        self.assertTrue(np.all(A.A == np.array([[0, 0, 0], [0, 0, 3], [0, 2, 0]])))
        self.assertTrue(A.nnz == 3)
        self.assertTrue(A.getformat() == "csc")

    def zero_2_columns(self):
        A = sps.csc_matrix(
            (np.array([1, 2, 3]), (np.array([0, 2, 1]), np.array([0, 1, 2]))),
            shape=(3, 3),
        )
        pp.matrix_operations.zero_columns(A, np.array([0, 2]))
        self.assertTrue(np.all(A.A == np.array([[0, 0, 0], [0, 0, 0], [0, 2, 0]])))
        self.assertTrue(A.nnz == 3)
        self.assertTrue(A.getformat() == "csc")

    def test_zero_columns(self):
        # Test slicing of csr_matrix
        A = sps.csc_matrix(np.array([[0, 0, 0], [1, 0, 0], [0, 0, 3]]))

        A0_t = sps.csc_matrix(np.array([[0, 0, 0], [0, 0, 0], [0, 0, 3]]))
        A2_t = sps.csc_matrix(np.array([[0, 0, 0], [1, 0, 0], [0, 0, 0]]))
        A0_2_t = sps.csc_matrix(np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]]))
        A0 = A.copy()
        A2 = A.copy()
        A0_2 = A.copy()
        pp.matrix_operations.zero_columns(A0, np.array([0], dtype=int))
        pp.matrix_operations.zero_columns(A2, 2)
        pp.matrix_operations.zero_columns(A0_2, np.array([0, 1, 2]))

        self.assertTrue(np.sum(A0 != A0_t) == 0)
        self.assertTrue(np.sum(A2 != A2_t) == 0)
        self.assertTrue(np.sum(A0_2 != A0_2_t) == 0)

    def test_zero_columns_assert(self):
        A = sps.csr_matrix(np.array([[0, 0, 0], [1, 0, 0], [0, 0, 3]]))
        try:
            pp.matrix_operations.zero_columns(A, 1)
        except ValueError:
            return None
        self.assertTrue(False)

    # ----------Zero out rows---------------
    def zero_1_row(self):
        A = sps.csr_matrix(
            (np.array([1, 2, 3]), (np.array([0, 2, 1]), np.array([0, 1, 2]))),
            shape=(3, 3),
        )
        pp.matrix_operations.zero_rows(A, 0)
        self.assertTrue(np.all(A.A == np.array([[0, 0, 0], [0, 0, 3], [0, 2, 0]])))
        self.assertTrue(A.nnz == 3)
        self.assertTrue(A.getformat() == "csr")

    def zero_2_rows(self):
        A = sps.csr_matrix(
            (np.array([1, 2, 3]), (np.array([0, 2, 1]), np.array([0, 1, 2]))),
            shape=(3, 3),
        )
        pp.matrix_operations.zero_rows(A, np.array([0, 2]))
        self.assertTrue(np.all(A.A == np.array([[0, 0, 0], [0, 0, 0], [0, 2, 0]])))
        self.assertTrue(A.nnz == 3)
        self.assertTrue(A.getformat() == "csr")

    def test_zero_rows(self):
        A = sps.csr_matrix(np.array([[0, 0, 0], [1, 0, 0], [0, 0, 3]]))

        A0_t = sps.csr_matrix(np.array([[0, 0, 0], [1, 0, 0], [0, 0, 3]]))
        A2_t = sps.csr_matrix(np.array([[0, 0, 0], [1, 0, 0], [0, 0, 0]]))
        A0_2_t = sps.csr_matrix(np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]]))
        A0 = A.copy()
        A2 = A.copy()
        A0_2 = A.copy()
        pp.matrix_operations.zero_rows(A0, np.array([0], dtype=int))
        pp.matrix_operations.zero_rows(A2, 2)
        pp.matrix_operations.zero_rows(A0_2, np.array([0, 1, 2]))

        self.assertTrue(np.sum(A0 != A0_t) == 0)
        self.assertTrue(np.sum(A2 != A2_t) == 0)
        self.assertTrue(np.sum(A0_2 != A0_2_t) == 0)

    def test_zero_rows_assert(self):
        A = sps.csc_matrix(np.array([[0, 0, 0], [1, 0, 0], [0, 0, 3]]))
        try:
            pp.matrix_operations.zero_rows(A, 1)
        except ValueError:
            return None
        self.assertTrue(False)

    # ------------------- get slicing indices ------------------
    def test_csr_slice(self):
        # Test slicing of csr_matrix
        A = sps.csr_matrix(np.array([[0, 0, 0], [1, 0, 0], [0, 0, 3]]))

        cols_0 = pp.matrix_operations.slice_indices(A, np.array([0]))
        cols_1 = pp.matrix_operations.slice_indices(A, 1)
        cols_2 = pp.matrix_operations.slice_indices(A, 2)
        cols_split = pp.matrix_operations.slice_indices(A, np.array([0, 2]))
        cols0_2 = pp.matrix_operations.slice_indices(A, np.array([0, 1, 2]))

        self.assertTrue(cols_0.size == 0)
        self.assertTrue(cols_1 == np.array([0]))
        self.assertTrue(cols_2 == np.array([2]))
        self.assertTrue(np.all(cols_split == np.array([2])))
        self.assertTrue(np.all(cols0_2 == np.array([0, 2])))

    def test_csc_slice(self):
        # Test slicing of csr_matrix
        A = sps.csc_matrix(np.array([[0, 0, 0], [1, 0, 0], [0, 0, 3]]))
        rows_0 = pp.matrix_operations.slice_indices(A, np.array([0], dtype=int))
        rows_1 = pp.matrix_operations.slice_indices(A, 1)
        rows_2 = pp.matrix_operations.slice_indices(A, 2)
        cols_split = pp.matrix_operations.slice_indices(A, np.array([0, 2]))
        rows0_2 = pp.matrix_operations.slice_indices(A, np.array([0, 1, 2]))

        self.assertTrue(rows_0 == np.array([1]))
        self.assertTrue(rows_1.size == 0)
        self.assertTrue(rows_2 == np.array([2]))
        self.assertTrue(np.all(cols_split == np.array([1, 2])))
        self.assertTrue(np.all(rows0_2 == np.array([1, 2])))

    # ------------------ Test sliced_mat() -----------------------
    def test_sliced_mat_columns(self):
        # Test slicing of csr_matrix

        # original matrix
        A = sps.csc_matrix(np.array([[0, 0, 0], [1, 0, 0], [0, 0, 3]]))

        # expected results
        A0_t = sps.csc_matrix(np.array([[0, 0], [0, 0], [0, 3]]))
        A1_t = sps.csc_matrix(np.array([[0, 0], [1, 0], [0, 0]]))
        A2_t = sps.csc_matrix(np.array([[0], [0], [3]]))
        A3_t = sps.csc_matrix(np.array([[], [], []]))
        A4_t = sps.csc_matrix(np.array([[0, 0], [1, 0], [0, 3]]))

        A5_t = sps.csc_matrix(np.array([[0, 0], [0, 0], [0, 0]]))

        A0 = pp.matrix_operations.slice_mat(A, np.array([1, 2], dtype=int))
        A1 = pp.matrix_operations.slice_mat(A, np.array([0, 1]))
        A2 = pp.matrix_operations.slice_mat(A, 2)
        A3 = pp.matrix_operations.slice_mat(A, np.array([], dtype=int))
        A4 = pp.matrix_operations.slice_mat(A, np.array([0, 2], dtype=int))
        A5 = pp.matrix_operations.slice_mat(A, np.array([1, 1], dtype=int))

        self.assertTrue(np.sum(A0 != A0_t) == 0)
        self.assertTrue(np.sum(A1 != A1_t) == 0)
        self.assertTrue(np.sum(A2 != A2_t) == 0)
        self.assertTrue(np.sum(A3 != A3_t) == 0)
        self.assertTrue(np.sum(A4 != A4_t) == 0)
        self.assertTrue(np.sum(A5 != A5_t) == 0)

    def test_sliced_mat_rows(self):
        # Test slicing of csr_matrix
        A = sps.csr_matrix(np.array([[0, 0, 0], [1, 0, 0], [0, 0, 3]]))

        A0_t = sps.csr_matrix(np.array([[1, 0, 0], [0, 0, 3]]))
        A1_t = sps.csr_matrix(np.array([[0, 0, 0], [1, 0, 0]]))
        A2_t = sps.csr_matrix(np.array([[0, 0, 3]]))
        A3_t = sps.csr_matrix(np.atleast_2d(np.array([[], [], []])).T)
        A4_t = sps.csr_matrix(np.array([[0, 0, 0], [0, 0, 3]]))
        A5_t = sps.csr_matrix(np.array([[1, 0, 0], [1, 0, 0]]))

        A0 = pp.matrix_operations.slice_mat(A, np.array([1, 2], dtype=int))
        A1 = pp.matrix_operations.slice_mat(A, np.array([0, 1]))
        A2 = pp.matrix_operations.slice_mat(A, 2)
        A3 = pp.matrix_operations.slice_mat(A, np.array([], dtype=int))
        A4 = pp.matrix_operations.slice_mat(A, np.array([0, 2], dtype=int))
        A5 = pp.matrix_operations.slice_mat(A, np.array([1, 1], dtype=int))

        self.assertTrue(np.sum(A0 != A0_t) == 0)
        self.assertTrue(np.sum(A1 != A1_t) == 0)
        self.assertTrue(np.sum(A2 != A2_t) == 0)
        self.assertTrue(np.sum(A3 != A3_t) == 0)
        self.assertTrue(np.sum(A4 != A4_t) == 0)
        self.assertTrue(np.sum(A5 != A5_t) == 0)

    # ------------------ Test stack_mat() -----------------------
    def test_stack_mat_columns(self):
        # Test slicing of csr_matrix
        A = sps.csc_matrix(np.array([[0, 0, 0], [1, 0, 0], [0, 0, 3]]))

        B = sps.csc_matrix(np.array([[0, 2], [3, 1], [1, 0]]))

        A_t = sps.csc_matrix(
            np.array([[0, 0, 0, 0, 2], [1, 0, 0, 3, 1], [0, 0, 3, 1, 0]])
        )

        pp.matrix_operations.stack_mat(A, B)

        self.assertTrue(np.sum(A != A_t) == 0)

    def test_stack_empty_mat_columns(self):
        # Test slicing of csr_matrix
        A = sps.csc_matrix(np.array([[0, 0, 0], [1, 0, 0], [0, 0, 3]]))

        B = sps.csc_matrix(np.array([[], [], []]))

        A_t = A.copy()
        pp.matrix_operations.stack_mat(A, B)
        self.assertTrue(np.sum(A != A_t) == 0)
        B_t = A.copy()
        pp.matrix_operations.stack_mat(B, A)
        self.assertTrue(np.sum(B != B_t) == 0)

    def test_stack_mat_rows(self):
        # Test slicing of csr_matrix
        A = sps.csr_matrix(np.array([[0, 0, 0], [1, 0, 0], [0, 0, 3]]))

        B = sps.csr_matrix(np.array([[0, 2, 2], [3, 1, 3]]))

        A_t = sps.csr_matrix(
            np.array([[0, 0, 0], [1, 0, 0], [0, 0, 3], [0, 2, 2], [3, 1, 3]])
        )

        pp.matrix_operations.stack_mat(A, B)

        self.assertTrue(np.sum(A != A_t) == 0)

    def test_stack_empty_mat_rows(self):
        # Test slicing of csr_matrix
        A = sps.csr_matrix(np.array([[0, 0, 0], [1, 0, 0], [0, 0, 3]]))

        B = sps.csr_matrix(np.array([[], [], []]).T)

        A_t = A.copy()
        pp.matrix_operations.stack_mat(A, B)
        self.assertTrue(np.sum(A != A_t) == 0)
        B_t = A.copy()
        pp.matrix_operations.stack_mat(B, A)
        self.assertTrue(np.sum(B != B_t) == 0)

    # ------------------ Test merge_matrices() -----------------------

    def test_merge_mat_split_columns(self):
        # Test slicing of csr_matrix
        A = sps.csc_matrix(np.array([[0, 0, 0], [1, 0, 0], [0, 0, 3]]))

        B = sps.csc_matrix(np.array([[0, 2], [3, 1], [1, 0]]))

        A_t = sps.csc_matrix(np.array([[0, 0, 2], [3, 0, 1], [1, 0, 0]]))

        pp.matrix_operations.merge_matrices(
            A, B, np.array([0, 2], dtype=int), matrix_format="csc"
        )

        self.assertTrue(np.sum(A != A_t) == 0)

    def test_merge_mat_columns(self):
        # Test slicing of csr_matrix
        A = sps.csc_matrix(np.array([[0, 0, 0], [1, 0, 0], [0, 0, 3]]))

        B = sps.csc_matrix(np.array([[0, 2], [3, 1], [1, 0]]))

        A_t = sps.csc_matrix(np.array([[0, 0, 2], [1, 3, 1], [0, 1, 0]]))

        pp.matrix_operations.merge_matrices(
            A, B, np.array([1, 2], dtype=int), matrix_format="csc"
        )

        self.assertTrue(np.sum(A != A_t) == 0)

    def test_merge_mat_split_columns_same_pos(self):
        # Test slicing of csr_matrix
        A = sps.csc_matrix(np.array([[0, 0, 0], [1, 0, 0], [0, 0, 3]]))

        B = sps.csc_matrix(np.array([[0, 2], [3, 1], [1, 0]]))

        try:
            pp.matrix_operations.merge_matrices(
                A, B, np.array([0, 0], dtype=int), matrix_format="csc"
            )
        except ValueError:
            pass

    def test_merge_mat_split_rows(self):
        # Test slicing of csr_matrix
        A = sps.csr_matrix(np.array([[0, 0, 0], [1, 0, 0], [0, 0, 3]]))

        B = sps.csr_matrix(np.array([[0, 2, 2], [3, 1, 3]]))

        A_t = sps.csr_matrix(np.array([[0, 2, 2], [1, 0, 0], [3, 1, 3]]))

        pp.matrix_operations.merge_matrices(
            A, B, np.array([0, 2], dtype=int), matrix_format="csr"
        )

        self.assertTrue(np.sum(A != A_t) == 0)

    def test_merge_mat_rows(self):
        # Test slicing of csr_matrix
        A = sps.csr_matrix(np.array([[0, 0, 0], [1, 0, 0], [0, 0, 3]]))

        B = sps.csr_matrix(np.array([[0, 2, 2], [3, 1, 3]]))

        A_t = sps.csr_matrix(np.array([[0, 2, 2], [3, 1, 3], [0, 0, 3]]))

        pp.matrix_operations.merge_matrices(
            A, B, np.array([0, 1], dtype=int), matrix_format="csr"
        )

        self.assertTrue(np.sum(A != A_t) == 0)

    # Tests of csr_matrix_from_blocks
    def test_csr_matrix_from_single_block(self):

        block_size = 2
        arr = np.arange(block_size ** 2).reshape((block_size, block_size))

        known = np.array([[0, 1], [2, 3]])
        value = pp.matrix_operations.csr_matrix_from_blocks(
            arr.ravel("c"), block_size, 1
        )

        self.assertTrue(np.allclose(known, value.toarray()))

        # Larger block
        block_size = 3
        arr = np.arange(block_size ** 2).reshape((block_size, block_size))

        known = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8]])
        value = pp.matrix_operations.csr_matrix_from_blocks(
            arr.ravel("c"), block_size, 1
        )

        self.assertTrue(np.allclose(known, value.toarray()))

    # Tests of csr_matrix_from_blocks
    def test_csr_matrix_from_two_blocks(self):

        block_size = 2
        num_blocks = 2
        full_arr = np.arange((num_blocks * block_size) ** 2).reshape(
            (num_blocks * block_size, num_blocks * block_size)
        )

        arr = np.array(
            [full_arr[:block_size, :block_size], full_arr[block_size:, block_size:]]
        )

        known = np.array([[0, 1, 0, 0], [4, 5, 0, 0], [0, 0, 10, 11], [0, 0, 14, 15]])
        value = pp.matrix_operations.csr_matrix_from_blocks(
            arr.ravel("c"), block_size, num_blocks
        )

        self.assertTrue(np.allclose(known, value.toarray()))

    def test_csr_matrix_from_array(self):

        block_size = 2
        num_blocks = 2
        arr = np.array([1, 2, 3, 4, 5, 6, 7, 8])

        known = np.array([[1, 2, 0, 0], [3, 4, 0, 0], [0, 0, 5, 6], [0, 0, 7, 8]])
        value = pp.matrix_operations.csr_matrix_from_blocks(arr, block_size, num_blocks)

        self.assertTrue(np.allclose(known, value.toarray()))

    # Tests of csr_matrix_from_blocks
    def test_csc_matrix_from_array(self):

        block_size = 2
        num_blocks = 2
        arr = np.array([1, 2, 3, 4, 5, 6, 7, 8])

        known = np.array([[1, 3, 0, 0], [2, 4, 0, 0], [0, 0, 5, 7], [0, 0, 6, 8]])
        value = pp.matrix_operations.csc_matrix_from_blocks(arr, block_size, num_blocks)

        self.assertTrue(np.allclose(known, value.toarray()))


@pytest.mark.parametrize(
    "mat", [np.arange(6).reshape((3, 2)), np.arange(6).reshape((2, 3))]
)
def test_optimized_storage(mat):
    # Check that the optimized sparse storage chooses format according to whether the
    # matrix has more columns or rows or oposite.

    # Convert input matrix to sparse storage. For the moment, the matrix format is chosen
    # according to the number of rows and columns only, thus the lack of true sparsity
    # does not matter.
    A = sps.csc_matrix(mat)

    optimized = pp.matrix_operations.optimized_compressed_storage(A)

    if A.shape[0] > A.shape[1]:
        assert optimized.getformat() == "csc"
    else:
        assert optimized.getformat() == "csr"


if __name__ == "__main__":
    unittest.main()
