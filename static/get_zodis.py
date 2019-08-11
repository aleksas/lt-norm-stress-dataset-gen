from json import load
from static.get_skaitvardis import offset_from_var, Stress

stress_dict = {
    Stress.No : 'raw/zodziai.json',
    Stress.ASCII : 'raw/zodziai.stressed.json'
}

all_names_ = {}

def get_cases(stress=Stress.No):
    return get_all_names(stress)['Variations']['case']

def get_variations(stress=Stress.No):
    return get_all_names(stress)['Variations']

def get_all_names(stress=Stress.No):
    if stress not in all_names_:            
        with open(stress_dict[stress], 'r', encoding='utf-8') as fp:
            all_names_[stress] = load(fp)

    return all_names_[stress]

def get_complex_name(value, category_type=None,
    number='vns', case='vard.', stress=Stress.No):

    value = str(value)

    all_names = get_all_names(stress)

    default_category_type = all_names['Default']

    if not category_type:
        category_type = default_category_type

    names = all_names[category_type]

    variations = get_variations(stress)
    
    offset = offset_from_var(variations, number=number, case=case)

    if not names[value][0] and not names[value][offset + 1]:
        return None
    return names[value][0] + names[value][offset + 1]

if __name__ == '__main__':
    names = get_complex_name(
        value=1,
        category_type="Month",
        case="kilm.",
        number="dgs",
        stress=Stress.ASCII)
        
    assert('vasa~rių' == names)

    names = get_complex_name(
        value='diena',
        category_type="All",
        case="kilm.",
        number="dgs",
        stress=Stress.ASCII)

    assert('dienų~' == names)
        