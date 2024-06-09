import numpy as np
from custom_inherit import doc_inherit
from skcriteria.preprocessing import SKCMatrixAndWeightTransformerABC


class SafeVectorScaler(SKCMatrixAndWeightTransformerABC):
    """Scaler based on the norm of the vector.

    This class modifies the original VectorScaler to handle cases where the norm of a vector (column)
    might be zero, by setting such norms to 1 to prevent division by zero errors.

    If the scaler is configured to work with 'matrix', each value
    of each criterion is divided by the norm of the vector defined by the values
    of that criterion. If it is configured to work with 'weights',
    each value of weight is divided by the vector defined by the values of the weights.
    """

    @doc_inherit(SKCMatrixAndWeightTransformerABC._transform_weights)
    def _transform_weights(self, weights):
        """Transforms the weights by scaling to have a unit norm,
        using the same method as for matrix columns.
        """
        weights = np.asarray(weights, dtype=float)
        norms = np.linalg.norm(weights, None, axis=None)
        norms[norms == 0] = 1  # Prevent division by zero
        return weights / norms

    @doc_inherit(SKCMatrixAndWeightTransformerABC._transform_matrix)
    def _transform_matrix(self, matrix):
        """Transforms the decision matrix by scaling each column to have a unit norm,
        including handling columns with zero norm.
        """
        matrix = np.asarray(matrix, dtype=float)
        norms = np.linalg.norm(matrix, None, axis=0)
        norms[norms == 0] = 1  # Prevent division by zero by replacing zero norms with 1
        return matrix / norms
