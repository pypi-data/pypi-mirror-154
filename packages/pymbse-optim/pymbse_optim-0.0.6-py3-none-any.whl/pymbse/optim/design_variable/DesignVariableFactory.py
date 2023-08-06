from typing import List

import pandas as pd

from pymbse.optim.design_variable.GeneticDesignVariable import GeneticDesignVariable


def init_genetic_design_variables_with_csv(csv_path: str) -> List[GeneticDesignVariable]:
    """

    :param csv_path:
    :return:
    """
    # todo: add description of columns in the dataframe
    design_variables_df = pd.read_csv(csv_path)
    return init_genetic_design_variables_with_df(design_variables_df)


def init_genetic_design_variables_with_df(design_variables_df):
    genetic_design_variables = []
    for _, row in design_variables_df.iterrows():
        gen_dv = GeneticDesignVariable(**row)
        genetic_design_variables.append(gen_dv)

    return genetic_design_variables
