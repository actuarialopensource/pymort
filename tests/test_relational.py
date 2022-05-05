from pymort import Relational

def test_relational():
    
    db = Relational()

    assert list(db.metadata.loc[3209]) == ["2015_VBT", "relative_risk ALB", "female", "nonsmoker RR50"]
    assert list(db.select.loc[3226, 20, 9])[0] == .00034
    assert list(db.ultimate.loc[3372, 50])[0] == .00308