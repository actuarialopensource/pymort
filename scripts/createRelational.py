import pandas as pd
from itertools import product
from pymort import PyXML
from pathlib import Path
import pickle


def getSelectUltimate(metaDF: pd.DataFrame) -> pd.DataFrame:
    """
    Given a pandas DataFrame of MetaData, return the values metadata
    """
    selects = []
    ults = []
    for x in metaDF.index.values:
        xtbml = PyXML(x)
        select = xtbml.Tables[0].Values
        select["id"] = x
        selects.append(select)

        ult = xtbml.Tables[1].Values
        ult["id"] = x
        ults.append(ult)

    ultsDF = pd.concat(ults)
    ultsDF.reset_index(inplace=True)
    ultsDF.set_index(["id", "Age"], inplace=True)
    ultsDF.sort_index(inplace=True)

    selDF = pd.concat(selects)
    selDF.reset_index(inplace=True)
    selDF.set_index(["id", "Age", "Duration"], inplace=True)
    selDF.sort_index(inplace=True)

    return selDF, ultsDF


def getMeta() -> pd.DataFrame:
    df = pd.concat([get2015VBT(), get2017CSO()])
    df = df[["id", "study", "grouping", "gender", "risk"]]
    df.set_index("id", inplace=True)
    df.sort_index(inplace=True)
    return df


# There is no easy way to automate this
def get2017CSO() -> pd.DataFrame:
    grouping = []
    risk = []
    gender = []
    age_basis = []
    ids = []
    # LOADED COMPOSITE GENDER BLENDED
    grouping.extend(["loaded composite gender_blended"] * 10)
    risk.extend(["composite"] * 10)
    gender.extend([f"{percent}%_male" for percent in [20, 40, 50, 60, 80]] * 2)
    age_basis.extend(["ANB"] * 5 + ["ALB"] * 5)
    ids.extend(list(range(3277, 3287)))
    # LOADED COMPOSITE GENDER DISTINCT
    grouping.extend(["loaded composite gender_distinct"] * 4)
    risk.extend(["composite"] * 4)
    gender.extend(["male", "female"] * 2)
    age_basis.extend(["ANB"] * 2 + ["ALB"] * 2)
    ids.extend(range(3287, 3291))
    # LOADED SMOKER AND GENDER DISTINCT
    grouping.extend(["loaded smoker_distinct gender_distinct"] * 8)
    risk.extend((["nonsmoker"] * 2 + ["smoker"] * 2) * 2)
    gender.extend(["male", "female"] * 4)
    age_basis.extend(["ANB"] * 4 + ["ALB"] * 4)
    ids.extend(range(3291, 3299))
    # LOADED PREFERRED STRUCTURE
    grouping.extend(["loaded preferred_structure gender_distinct"] * 20)
    risk.extend(
        (
            ["nonsmoker super_preferred", "nonsmoker preferred", "nonsmoker residual"]
            * 2
            + ["smoker preferred", "smoker residual"] * 2
        )
        * 2
    )
    gender.extend(
        ((["male"] * 3 + ["female"] * 3) + (["male"] * 2 + ["female"] * 2)) * 2
    )
    age_basis.extend(["ANB"] * 10 + ["ALB"] * 10)
    ids.extend(range(3299, 3319))
    # LOADED GENDER BLENDED
    pGrouping, pSmoke, pBasis, pGender = list(
        zip(
            *product(
                ["loaded smoker_distinct gender_blended"],
                ["nonsmoker", "smoker"],
                ["ANB", "ALB"],
                [f"{percent}%_male" for percent in [20, 40, 50, 60, 80]],
            )
        )
    )
    grouping.extend(pGrouping)
    risk.extend(pSmoke)
    gender.extend(pGender)
    age_basis.extend(pBasis)
    ids.extend(range(3319, 3339))
    # UNLOADED PREFERRED STRUCTURE
    grouping.extend(["unloaded preferred_structure gender_distinct"] * 20)
    risk.extend(
        (
            ["nonsmoker super_preferred", "nonsmoker preferred", "nonsmoker residual"]
            * 2
            + ["smoker preferred", "smoker residual"] * 2
        )
        * 2
    )
    gender.extend(
        ((["male"] * 3 + ["female"] * 3) + (["male"] * 2 + ["female"] * 2)) * 2
    )
    age_basis.extend(["ANB"] * 10 + ["ALB"] * 10)
    ids.extend(range(3341, 3361))
    # UNLOADED COMPOSITE GENDER DISTINCT
    grouping.extend(["unloaded composite gender_distinct"] * 4)
    risk.extend(["composite"] * 4)
    gender.extend(["male", "female"] * 2)
    age_basis.extend(["ANB"] * 2 + ["ALB"] * 2)
    ids.extend(range(3361, 3365))
    # UNLOADED SMOKER AND GENDER DISTINCT
    grouping.extend(["unloaded smoker_distinct gender_distinct"] * 8)
    risk.extend((["nonsmoker"] * 2 + ["smoker"] * 2) * 2)
    gender.extend(["male", "female"] * 4)
    age_basis.extend(["ANB"] * 4 + ["ALB"] * 4)
    ids.extend(range(3365, 3373))

    # Put the age basis as part of the grouping. Not all tables have an age basis so it shouldn't be a column.
    grouping = [" ".join(group_basis) for group_basis in zip(grouping, age_basis)]

    cso2017 = {"grouping": grouping, "risk": risk, "gender": gender, "id": ids}

    # load the dict as a pandas dataframe
    df2017 = pd.DataFrame(cso2017)
    df2017["study"] = "2017_CSO"
    return df2017


def get2015VBT() -> pd.DataFrame:
    risk = []
    grouping = []
    gender = []
    age_basis = []
    ids = []

    pGender, pBasis, pRisk = zip(
        *product(
            ["female"],
            ["ALB", "ANB"],
            [f"nonsmoker RR{x}" for x in [50, 60, 70, 80, 90, 100, 110, 125, 150, 175]],
        )
    )
    gender.extend(pGender)
    grouping.extend(["relative_risk"] * 20)
    risk.extend(pRisk)
    age_basis.extend(pBasis)
    ids.extend(range(3209, 3229))

    pGender, pBasis, pRisk = zip(
        *product(
            ["female"], ["ALB", "ANB"], [f"smoker RR{x}" for x in [75, 100, 125, 150]]
        )
    )
    gender.extend(pGender)
    grouping.extend(["relative_risk"] * 8)
    risk.extend(pRisk)
    age_basis.extend(pBasis)
    ids.extend(range(3229, 3237))

    pGender, pBasis, pRisk = zip(
        *product(
            ["male"],
            ["ALB", "ANB"],
            [f"nonsmoker RR{x}" for x in [50, 60, 70, 80, 90, 100, 110, 125, 150, 175]],
        )
    )
    gender.extend(pGender)
    grouping.extend(["relative_risk"] * 20)
    risk.extend(pRisk)
    age_basis.extend(pBasis)
    ids.extend(range(3237, 3257))

    pGender, pBasis, pRisk = zip(
        *product(
            ["male"], ["ALB", "ANB"], [f"smoker RR{x}" for x in [75, 100, 125, 150]]
        )
    )
    gender.extend(pGender)
    grouping.extend(["relative_risk"] * 8)
    risk.extend(pRisk)
    age_basis.extend(pBasis)
    ids.extend(range(3257, 3265))

    gender.extend(["male", "female"] * 4)
    grouping.extend(["smoker_distinct"] * 8)
    risk.extend((["nonsmoker"] * 2 + ["smoker"] * 2) * 2)
    age_basis.extend(["ANB"] * 4 + ["ALB"] * 4)
    ids.extend(range(3265, 3273))

    gender.extend(["male", "female"] * 2)
    grouping.extend(["unismoke"] * 4)
    risk.extend(["unismoke"] * 4)
    age_basis.extend(["ANB"] * 2 + ["ALB"] * 2)
    ids.extend(range(3273, 3277))

    # put the age_basis as part of the grouping
    grouping = [" ".join(group_basis) for group_basis in zip(grouping, age_basis)]

    # load the dict as a pandas dataframe
    vbt2015 = {"risk": risk, "grouping": grouping, "gender": gender, "id": ids}
    df2015 = pd.DataFrame(vbt2015)
    df2015["study"] = "2015_VBT"
    return df2015


if __name__ == "__main__":
    meta = getMeta()
    sel, ult = getSelectUltimate(meta)
    with open(Path("pymort", "pickled_tables", "meta.pickle"), "wb") as f:
        pickle.dump(meta, f)
    with open(Path("pymort", "pickled_tables", "sel.pickle"), "wb") as f:
        pickle.dump(sel, f)
    with open(Path("pymort", "pickled_tables", "ult.pickle"), "wb") as f:
        pickle.dump(ult, f)
