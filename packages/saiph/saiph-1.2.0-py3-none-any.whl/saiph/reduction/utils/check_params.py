from typing import Any

import pandas as pd
from numpy.typing import NDArray


def fit_check_params(nf: int, col_weights: NDArray[Any], df: pd.DataFrame) -> None:
    if nf <= 0:
        raise ValueError("nf", "The number of components must be positive.")

    if nf > min(pd.get_dummies(df).shape):
        raise ValueError(
            f"Expected number of components <= {min(pd.get_dummies(df).shape)}, got {nf} instead."
        )

    if len(col_weights) != df.shape[1]:
        raise ValueError(
            "col_weights",
            f"Expected weight parameter size {str(df.shape[1])}, got {len(col_weights)} instead.",
        )
