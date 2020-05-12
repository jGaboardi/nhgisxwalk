"""IDs and ID components of geographic code descriptions in a pandas.DataFrame.
"""


from .__code_components import *
import numpy
import pandas
from io import StringIO


def code_cols(geog, year):
    """Geography ID coded columns.  ############################################# This maybe only needs to support BGP...
                                    ############################################# All other geography IDs can easily
                                    ############################################# be obtained...
    
    Parameters
    ----------
    
    geog : str
         The specified census geography. This will support
         ["blk", "bgp", "bgr", "trt", "cty",...] in the future.
    
    year : str
        The specified census year. This will support
        ["1990", "2000", "2010", "2020"] in the future.
    
    Returns
    -------
    
    cols : list
        The correct ordering of columns to create the geography ID.
    
    """
    # ensure `year` is a str
    year = str(year)

    if geog == "bgp":
        if year == "1990":
            cols = [
                "STATEA",
                "COUNTYA",
                "CTY_SUBA",
                "PLACEA",
                "TRACTA",
                "CDA",  ###################################### swap out "CD103A"
                "AIANHHA",
                "RES_TRSTA",
                "ANRCA",
                "URB_AREAA",
                "URBRURALA",
                "BLCK_GRPA",
            ]
        if year == "2000":
            # Geographic level: Block Group (by State--County--County Subdivision--Place/Remainder--Census Tract--Urban/Rural)
            cols = [
                "STATEA",
                "COUNTYA",
                "CTY_SUBA",
                "PLACEA",
                "TRACTA",
                "URBRURALA",
                "BLCK_GRPA",
            ]

    return cols


def blk_id():
    """######################################################################### Probably don't need this?
    """

    pass


def bgp_id(df, order, cname="_GJOIN", tzero=["STATEA", "COUNTYA"], nhgis=True):
    """Recreate BGPs GISJOIN/GEOID.
    
    Parameters
    ----------
    
    df : pandas.DataFrame
        The input dataframe.
    
    order : list-like
        The correct ordering of columns.
    
    cname : str
        The name for the new column.
    
    tzeros : list
        The columns to add trailing zero. ``nhgis`` must be ``True``.
    
    nhgis : bool
        Set to ``True`` to add 'G' and trailing zeros.
        See `GISJOIN identifiers <https://www.nhgis.org/user-resources/geographic-crosswalks>`_.
    
    Returns
    -------
    
    df : pandas.DataFrame
        The input ``df`` with new column.
    
    """

    def _gjoin(x):
        """Internal GISJOIN/GEOID generator."""

        # container for ID components
        join_id_vals = []
        for o in order:

            # if the val associated with `o` is a numpy.float
            v = getattr(x, o)

            try:
                # handle NaN values
                if not numpy.isnan(v):
                    _id_val = str(v)
                else:
                    _id_val = ""

            # if the val associated with `o` is a str
            except TypeError:
                _id_val = str(v)

            # trailing zero for NHGIS
            if nhgis and o in tzero:
                _id_val += "0"
            # append ID component to ID list
            join_id_vals.append(_id_val)

        id_str = "".join(join_id_vals)
        if nhgis:
            # G prefix for GISJOIN and concatentate ID components
            id_str = "G" + id_str

        return id_str

    # recreate GISJOIN ID (_GJOIN, [or other])
    df[cname] = [_gjoin(record) for record in df.itertuples()]

    return df


def bkg_id(year, _id, nhgis):
    """Extract the block group ID from the block ID.
    
    Parameters
    ----------
    
    year : str
        The census collection year.
    
    _id : str
        The block GISJOIN/GEOID.
    
    nhgis : bool
        Set to ``True`` to add 'G' and trailing zeros.
        See `GISJOIN identifiers <https://www.nhgis.org/user-resources/geographic-crosswalks>`_.
    
    Returns
    -------
    
    block_group_id : str
        The block group GISJOIN/GEOID.
    
    """

    # 1990 -- Block Group (by State--County--Census Tract)
    block_group_id = None
    pass


def trt_id(year, _id, nhgis):
    """Extract the tract ID from the block ID.
    
    Parameters
    ----------
    
    year : str
        The census collection year.
    
    _id : str
        The block GISJOIN/GEOID.
    
    nhgis : bool
        Set to ``True`` to add 'G' and trailing zeros.
        See `GISJOIN identifiers <https://www.nhgis.org/user-resources/geographic-crosswalks>`_.
    
    Returns
    -------
    
    tract_id : str
        The tract GISJOIN/GEOID.
    
    """

    if year == "2010":
        indexer = 14
        if not nhgis:
            indexer = "?"
        # slice out tract ID
        tract_id = _id[:indexer]
    else:
        msg = "Census year %s is not currently supported." % year
        raise RuntimeError(msg)

    return tract_id


def cty_id():
    """
    """

    pass


def id_from(target_func, target_year, source, nhgis, vectorized):
    """Create target IDs from source IDs.
    
    Parameters
    ----------
    
    target_func : function or method
        The function or method for generating requested target IDs.
    
    target_year : str
        The original target ID year.
    
    source : iterable
        The original source IDs.
    
    vectorized : bool
        Potential speedup when set to ``True``. Default is ``True``.
    
    Returns
    -------
    
    result : iterable
        The generated target IDs.
    
    """

    # generate IDs from source geographies to target geographies
    if vectorized:
        result = numpy.vectorize(target_func)(target_year, source, nhgis)
    else:
        result = [target_func(target_year, rec, nhgis) for rec in source]

    return result


def id_code_components(year, geo):
    """Fetch the raw-string of the components used to create the specified
    year+geography ID, and return in a dataframe.
    
    Parameters
    ----------
    
    year : str
        The specified census year.
    
    geo : str
        The specified census geography.
    
    Returns
    -------
    
    df : pandas.DataFrame
        A dataframe of two columns: "Variable", "Description". The
        "Variable" column is tabular name of the component that is
        explained in "Description".
    
    """

    if year == "1990":
        if geo == "blk":
            components = blk1990
        if geo == "bgp":
            components = bgp1990
        if geo == "bkg":
            raise AttributeError()
            # components
        if geo == "trt":
            raise AttributeError()
            # components
        if geo == "cty":
            raise AttributeError()
            # components

    if year == "2000":
        if geo == "blk":
            components = blk2000
        if geo == "bgp":
            components = bgp2000
            # components
        if geo == "bkg":
            raise AttributeError()
            # components
        if geo == "trt":
            raise AttributeError()
            # components
        if geo == "cty":
            raise AttributeError()
            # components

    if year == "2010":
        if geo == "blk":
            raise AttributeError()
            # components
        if geo == "bgp":
            raise AttributeError()
            # components
        if geo == "bkg":
            raise AttributeError()
            # components
        if geo == "trt":
            components = trt2010
        if geo == "cty":
            raise AttributeError()
            # components

    # create ID components dataframe
    df = pandas.read_csv(StringIO(components), header=None)
    df.index.name = geo + year
    df.columns = ["Variable", "Description"]

    return df


def _add_ur_code_blk2000(df):
    """ Special case function to give 2000 blocks an Urban/Rural
    identifier for 2000 Block Group Parts
    
    Parameters
    ----------
    
    df : pandas.DataFrame
        The input dataframe.
    
    Returns
    -------
    
    df : pandas.DataFrame
        The input ``df`` with new column.
    
    """

    # generate Urban/Rural identifier
    df["URBRURALA"] = df["FXT001"].map(lambda x: "U" if x > 0 else "R")
    # reorder columns
    cols = df.columns
    reorder_cols = list(cols[:12]) + list(cols[-1:]) + list(cols[12:-1])
    df = df[reorder_cols]

    return df
