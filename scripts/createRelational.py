import pandas as pd
from itertools import product
from pymort.loader import load
from pathlib import Path
import pickle

def getSelectUltimate(metaDF: pd.DataFrame) -> pd.DataFrame:
    '''
    Given a pandas DataFrame of MetaData, return the values metadata
    '''
    selects = []
    ults = []
    for x in metaDF.index.values:
        xtbml = load(x)
        select = xtbml.Tables[0].Values
        select['id'] = x
        selects.append(select)

        ult = xtbml.Tables[1].Values
        ult['id'] = x
        ults.append(ult)
    
    ultsDF = pd.concat(ults)
    ultsDF.reset_index(inplace=True)
    ultsDF.set_index(['id', 'Age'], inplace=True)
    ultsDF.sort_index(inplace=True)

    selDF = pd.concat(selects)
    selDF.reset_index(inplace=True)
    selDF.set_index(['id', 'Age', 'Duration'], inplace=True)
    selDF.sort_index(inplace=True)
    
    return selDF, ultsDF

def getMeta() -> pd.DataFrame:
    df = pd.concat([get2015VBT(), get2017CSO()])
    df = df[['id', 'study', 'grouping', 'loading', 'age_basis', 'gender', 'risk']]
    df.set_index('id', inplace=True)
    df.sort_index(inplace=True)
    return df

# There is no easy way to automate this
def get2017CSO() -> pd.DataFrame:
    loading = []
    risk = []
    gender = []
    age_basis = []
    grouping = []
    ids = []
    # LOADED COMPOSITE GENDER BLENDED
    loading.extend(['loaded']*10)
    grouping.extend(['composite']*10)
    risk.extend([None]*10)
    gender.extend([f"{percent}% male" for percent in [20, 40, 50, 60, 80]] * 2)
    age_basis.extend(['ANB']*5 + ['ALB']*5)
    ids.extend(list(range(3277, 3287)))
    # LOADED COMPOSITE GENDER DISTINCT
    loading.extend(['loaded']*4)
    grouping.extend(['composite']*4)
    risk.extend([None]*4)
    gender.extend(['male', 'female']*2)
    age_basis.extend(['ANB']*2 + ['ALB']*2)
    ids.extend(range(3287, 3291))
    # LOADED SMOKER AND GENDER DISTINCT
    loading.extend(['loaded']*8)
    grouping.extend(['smoker distinct']*8)
    risk.extend((['nonsmoker']*2 + ['smoker']*2)*2)
    gender.extend(['male', 'female']*4)
    age_basis.extend(['ANB']*4 + ['ALB']*4)
    ids.extend(range(3291, 3299))
    # LOADED PREFERRED STRUCTURE
    loading.extend(['loaded']*20)
    grouping.extend(['preferred structure']*20)
    risk.extend((['ns s pref', 'ns pref', 'ns r']*2 + ['s pref', 's res']*2)*2)
    gender.extend(((['male']*3 + ['female']*3) + (['male']*2 + ['female']*2))*2)
    age_basis.extend(['ANB']*10 + ['ALB']*10)
    ids.extend(range(3299, 3319))
    # LOADED GENDER BLENDED
    pLoading, pSmoke, pBasis, pGender = list(zip(*product(['loaded'], ['nonsmoker', 'smoker'], ['ANB', 'ALB'], [f'{percent}% male' for percent in [20, 40, 50, 60, 80]])))
    loading.extend(pLoading)
    grouping.extend(['gender blended']*len(pLoading))
    risk.extend(pSmoke)
    gender.extend(pBasis)
    age_basis.extend(pGender)
    ids.extend(range(3319, 3339))
    # UNLOADED PREFERRED STRUCTURE
    loading.extend(['unloaded']*20)
    grouping.extend(['preferred structure']*20)
    risk.extend((['ns s pref', 'ns pref', 'ns r']*2 + ['s pref', 's res']*2)*2)
    gender.extend(((['male']*3 + ['female']*3) + (['male']*2 + ['female']*2))*2)
    age_basis.extend(['ANB']*10 + ['ALB']*10)
    ids.extend(range(3341, 3361))
    # UNLOADED COMPOSITE GENDER DISTINCT
    loading.extend(['unloaded']*4)
    grouping.extend(['composite']*4)
    risk.extend([None]*4)
    gender.extend(['male', 'female']*2)
    age_basis.extend(['ANB']*2 + ['ALB']*2)
    ids.extend(range(3361, 3365))
    # UNLOADED SMOKER AND GENDER DISTINCT
    loading.extend(['unloaded']*8)
    grouping.extend(['smoker distinct']*8)
    risk.extend((['nonsmoker']*2 + ['smoker']*2)*2)
    gender.extend(['male', 'female']*4)
    age_basis.extend(['ANB']*4 + ['ALB']*4)
    ids.extend(range(3365, 3373))

    cso2017 = {'loading': loading, 'grouping': grouping, 'risk': risk, 'gender': gender, 'age_basis': age_basis, 'id': ids}
    
    # load the dict as a pandas dataframe
    df2017 = pd.DataFrame(cso2017)
    df2017['study'] = "2017 CSO"
    return df2017

def get2015VBT() -> pd.DataFrame:
    risk = []
    grouping = []
    gender = []
    age_basis = []
    ids = []

    pGender, pBasis, pRisk =zip(*product(['female'], ['ALB', 'ANB'], [f"ns RR{x}" for x in [50, 60, 70, 80, 90, 100, 110, 125, 150, 175]]))
    gender.extend(pGender)
    grouping.extend(['RR']*20)
    risk.extend(pRisk)
    age_basis.extend(pBasis)
    ids.extend(range(3209, 3229))

    pGender, pBasis, pRisk =zip(*product(['female'], ['ALB', 'ANB'], [f"s RR{x}" for x in [75, 100, 125, 150]]))
    gender.extend(pGender)
    grouping.extend(['RR']*8)
    risk.extend(pRisk)
    age_basis.extend(pBasis)
    ids.extend(range(3229, 3237))

    pGender, pBasis, pRisk =zip(*product(['male'], ['ALB', 'ANB'], [f"ns RR{x}" for x in [50, 60, 70, 80, 90, 100, 110, 125, 150, 175]]))
    gender.extend(pGender)
    grouping.extend(['RR']*20)
    risk.extend(pRisk)
    age_basis.extend(pBasis)
    ids.extend(range(3237, 3257))

    pGender, pBasis, pRisk =zip(*product(['male'], ['ALB', 'ANB'], [f"s RR{x}" for x in [75, 100, 125, 150]]))
    gender.extend(pGender)
    grouping.extend(['RR']*8)
    risk.extend(pRisk)
    age_basis.extend(pBasis)
    ids.extend(range(3257, 3265))

    gender.extend(['male', 'female']*4)
    grouping.extend(['smoker distinct']*8)
    risk.extend((['ns']*2 + ['s']*2)*2)
    age_basis.extend(['ANB']*4 + ['ALB']*4)
    ids.extend(range(3265, 3273))

    gender.extend(['male', 'female']*2)
    grouping.extend(['unismoke']*4)
    risk.extend(['unismoke']*4)
    age_basis.extend(['ANB']*2 + ['ALB']*2)
    ids.extend(range(3273, 3277))

    # load the dict as a pandas dataframe
    vbt2015 = {'risk': risk, 'grouping': grouping, 'gender': gender, 'age_basis': age_basis, 'id': ids}
    df2015 = pd.DataFrame(vbt2015)
    df2015['study'] = '2015 VBT'
    return df2015

if __name__ == "__main__":
    meta = getMeta()
    sel, ult = getSelectUltimate(meta)
    with open(Path('pymort', 'pickled_tables', 'meta.pickle'), 'wb') as f:
        pickle.dump(meta, f)
    with open(Path('pymort', 'pickled_tables', 'sel.pickle'), 'wb') as f:
        pickle.dump(sel, f)
    with open(Path('pymort', 'pickled_tables', 'ult.pickle'), 'wb') as f:
        pickle.dump(ult, f)