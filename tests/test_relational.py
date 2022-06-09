from pymort import Relational, getIdGroup
import pytest

def test_relational():
    
    db = Relational()

    assert list(db.metadata.loc[3209]) == ["2015_VBT", "relative_risk ALB", "female", "nonsmoker RR50"]
    assert list(db.select.loc[3226, 20, 9])[0] == .00034
    assert list(db.ultimate.loc[3372, 50])[0] == .00308

def test_getIdGroup():
    with pytest.raises(KeyError):
        #  Table with id of 1 is not in the Relational().metadata pandas table
        getIdGroup(1)
    idGroup = getIdGroup(3265)
    assert idGroup.study == "2015_VBT"
    assert idGroup.grouping == "smoker_distinct ANB"
    assert idGroup.ids == [3265, 3266, 3267, 3268]
    