from app.main import canonical,compare_facts,validated_facts,mock_extract

def test_equivalent_units():
    assert canonical('thickness','1.2 cm','cm') == ('12','mm')
    assert canonical('thickness','12 mm','mm') == ('12','mm')

def test_evidence_rejects_fake_quote():
    assert validated_facts([{'property':'thickness','raw_value':'12 mm','page':1,'exact_quote':'not here'}],['Thickness: 12 mm'])==[]

def test_diff_and_missing_are_distinct():
    o={'property':'thickness','normalized_value':'12','raw_value':'12 mm'}
    n={'property':'thickness','normalized_value':'14','raw_value':'14 mm'}
    assert compare_facts([o],[n])[0]['state']=='changed'
    assert compare_facts([o],[])[0]['state']=='unresolved'

def test_mock_extract():
    facts=validated_facts(mock_extract(['Product: TD-PANEL\nThickness: 12 mm\nUsage conditions: Class 1']),['Product: TD-PANEL\nThickness: 12 mm\nUsage conditions: Class 1'])
    assert len(facts)==3
