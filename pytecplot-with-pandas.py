import pandas
import tecplot

def pandas_to_zone(df,dataset,zone_name='pandas'):
    """Adds a zone and populates the variables from a pandas dataframe.
    Make sure the column keys match the variable names.
    See also zone_to_pandas().
    """
    dfzone = dataset.add_ordered_zone(zone_name,df.shape[0])
    for k in df.keys():
        kglob = k[:k.find('[')] + '[[]' + k[k.find('[')+1:k.find(']')] + '[]]' + k[k.find(']')+1:]
        dfzone.values(kglob)[:] = df[k].values
    return dataset


def zone_to_pandas(zone, variables, df_index=None):
    """Exports the variables in a zone to a pandas dataframe.
    variables should be, eg., the iterable result of dataset.variables()
    See also pandas_to_zone(). Please use caution when working with large
    datasets.
    """
    vardict = {var.name : zone.values(var.index)[:] for var in variables}
    df = pd.DataFrame(vardict,index=df_index)
    return df
