from pymort import MortXML

def test_PyXML():
    xml = MortXML(3279)

    contentClassification = xml.ContentClassification
    assert contentClassification.TableIdentity == 3279
    assert contentClassification.ProviderDomain == "soa.org"
    assert contentClassification.ProviderName == "American Academy of Actuaries along with the Society of Actuaries"
    assert contentClassification.TableReference == """Joint American Academy of Actuaries' Life Experience Committee and Society of Actuaries Preferred Mortality Oversight Group CSO Development Subgroup, "Report on the 2017 CSO  and on the 2017 CSO Preferred Structure Table Development", American Academy of Actuaries, (2015). Appendix K. Accessed: February, 2016 from https://www.soa.org/resources/experience-studies/2015/2017-cso-tables/"""
    assert contentClassification.ContentType == "CSO / CET"
    assert contentClassification.TableName == "2017 Loaded CSO Composite Gender-Blended 50% Male ANB"
    assert contentClassification.TableDescription == "2017 Loaded CSO Composite Gender-Blended, Male, 50%, Age Nearest Birthday. Minimum Age: 0. Maximum Age: 95."
    assert contentClassification.Comments == "The 2017 Commissioners Standard Ordinary Tables (CSO) are a series of mortality tables developed for regulatory uses including CRVM, net premium reserves and non-forfeiture determination. The tables were based on life insurance mortality experience from 2002 to 2009, projected with improvement to 2017.  The tables include a margin to cover the variation of individual company’s mortality around the industry mean. Table uploaded: 02/2016. Select rates at ages 0-17 for certain durations and ultimate rates at ages 18-27, 29, 30, 32 and 37 were modified 09/2016. Data verified: 07/2018."
    assert contentClassification.KeyWords == ["Select", "CSO/CET", "United States of America"]

    # Tests for the select table
    meta0 = xml.Tables[0].MetaData
    assert meta0.ScalingFactor == 0.
    assert meta0.DataType == "Floating Point"
    assert meta0.Nation == "United States of America"
    assert meta0.TableDescription == "2017 Loaded CSO Composite Gender-Blended, Male, 50%, Select and Ultimate Table. Basis: Age Nearest Birthday. Minimum Select Age: 0. Maximum Select Age: 95."
    
    assert meta0.AxisDefs[0].ScaleType == "Age"
    assert meta0.AxisDefs[0].AxisName == "Age"
    assert meta0.AxisDefs[0].MinScaleValue == 0
    assert meta0.AxisDefs[0].MaxScaleValue == 95
    assert meta0.AxisDefs[0].Increment == 1

    assert meta0.AxisDefs[1].ScaleType == "Ordinal Date"
    assert meta0.AxisDefs[1].AxisName == "Duration"
    assert meta0.AxisDefs[1].MinScaleValue == 1
    assert meta0.AxisDefs[1].MaxScaleValue == 25
    assert meta0.AxisDefs[1].Increment == 1

    values0 = xml.Tables[0].Values
    assert .00029 == list(values0.loc[0, 1])[0]
    assert .00072 == list(values0.loc[5, 23])[0]

    # Tests for the ultimate table
    meta1 = xml.Tables[1].MetaData
    assert meta1.ScalingFactor == 0.
    assert meta1.DataType == "Floating Point"
    assert meta1.Nation == "United States of America"
    assert meta1.TableDescription == "2017 Loaded CSO Composite Gender-Blended, Male, 50%, Select and Ultimate Table. Basis: Age Nearest Birthday. Minimum Ultimate Age: 0. Maximum Ultimate Age: 120"

    assert meta1.AxisDefs[0].ScaleType == "Age"
    assert meta1.AxisDefs[0].AxisName == "Age"
    assert meta1.AxisDefs[0].MinScaleValue == 0
    assert meta1.AxisDefs[0].MaxScaleValue == 120
    assert meta1.AxisDefs[0].Increment == 1
    
    values1 = xml.Tables[1].Values
    assert .00029 == values1.loc[0]["vals"]
    assert .00248 == values1.loc[50]["vals"]