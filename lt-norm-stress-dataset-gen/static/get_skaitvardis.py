from json import load
from enum import IntEnum

class Number(IntEnum):
    NAME = 0
    TEN_POWER_NAME = 1

class Stress(IntEnum):
    No = 0
    ASCII = 1

stress_dict = {
    Stress.No : 'raw/skaitvardziai.json',
    Stress.ASCII : 'raw/skaitvardziai.stressed.json'
}

all_number_names_ = {}
number_names_forms = {}
unique_number_names_ending_paths = {}

def get_variations(stress=Stress.No):
    return get_all_number_names(stress)['Variations']

def get_all_number_names(stress=Stress.No):
    if stress not in all_number_names_:            
        with open(stress_dict[stress], 'r', encoding='utf-8') as fp:
            all_number_names_[stress] = load(fp)

    return all_number_names_[stress]

def offset_from_var(variations, **kwargs):
    offset = 0
    values = {}
    rkeys = list(variations.keys())
    rkeys.reverse()

    for key in variations.keys():
        values[key] = variations[key][0]

    for key, value in kwargs.items():
        values[key] = value

    l = 1
    for i in range(len(rkeys)):
        key = rkeys[i]
        value = values[key]

        offset += variations[key].index(value) * l
        l *= len(variations[key])

    return offset

def get_number_complex_name(value, category_type=None,
    category_subtype=None, number=None, gender='vyr. g.', case='vard.', stress=Stress.No):

    all_number_names = get_all_number_names(stress)
    default_category_type = all_number_names['Default']
    default_category_subtype = all_number_names[default_category_type]['Default']

    def get_number_names(category_type, category_subtype, stress):
        number_names = {int(k):v for k,v in all_number_names[category_type][category_subtype]['Names'].items()}
        ten_power_names = {int(k):v for k,v in all_number_names[category_type][category_subtype]['Ten Power Names'].items()}

        return number_names, ten_power_names

    number_names_ = get_number_names(default_category_type, default_category_subtype, stress)
    default_number_names, default_ten_power_names = number_names_

    number_splits = get_number_splits(value, default_number_names.keys(), default_ten_power_names.keys())
    variations = get_variations(stress)
    last_name_index = len(number_splits) - 1

    default_gender = 'vyr. g.'
    default_number = 'vns'
    default_case = 'vard.'

    if not category_type:
        category_type = default_category_type

    if not category_subtype:
        category_subtype = default_category_subtype
    
    number_names_ = get_number_names(category_type, category_subtype, stress)
    number_names, ten_power_names = number_names_

    gender = default_gender if not gender else gender
    case = default_case if not case else case
    number = default_number if not number else number

    for i in range(len(number_splits)):
        tmp_gender = default_gender
        tmp_number = default_number
        tmp_number_2 = 'dgs'
        tmp_case = default_case if category_type != 'Kiekiniai' else case

        split_value, split_type = number_splits[i]        

        if split_type == Number.NAME:
            if i == last_name_index:
                tmp_case = case
                tmp_gender = gender
                tmp_number = number
            elif i == last_name_index - 1 and number_splits[-1][1] != Number.NAME:
                tmp_number = number
                tmp_case = case

            if i < len(number_splits) - 1:
                _, next_split_type = number_splits[i+1]
                if next_split_type == Number.NAME:
                    tmp_case = 'vard.'

            if split_value > 1 and not category_type == 'Kelintiniai':
                tmp_number = 'dgs'

            if split_value <= 9:
                tmp_number_2 = 'vns'

        elif split_type == Number.TEN_POWER_NAME:
            if i > 0:
                prev_split_value, prev_split_type, _, _, _, _ = number_splits[i-1]
                if prev_split_type == Number.TEN_POWER_NAME:
                    tmp_number = 'dgs'
                    tmp_case = 'kilm.'
                else:
                    if prev_split_value != 1:
                        tmp_number = 'dgs'
                        if prev_split_value > 9:
                            tmp_case = 'kilm.'

            if i == last_name_index:
                tmp_gender = gender
                if category_type == 'Kelintiniai':
                    tmp_number = number
                    tmp_case = case
                    
        else:
            raise Exception()

        number_splits[i] = (split_value, split_type, tmp_gender, tmp_number, tmp_number_2, tmp_case)
    
    tmp_number_splits = []
    for i in range(len(number_splits)):
        split_value, split_type = number_splits[i][:2]
        if split_type == Number.NAME:
                if split_value == 1:
                    if i + 1 < len(number_splits) and i == 0:
                        next_split_type = number_splits[i+1][1]
                        if next_split_type == Number.TEN_POWER_NAME:
                            continue
        tmp_number_splits.append(number_splits[i])
    number_splits = tmp_number_splits
    last_name_index = len(number_splits) - 1
        
    for i in range(len(number_splits)):
        split_value, split_type, split_gender, split_number, _, split_case = number_splits[i]
        if i == last_name_index:
            name = number_names[split_value] if split_type == Number.NAME else ten_power_names[split_value]
        else:
            if split_type == Number.NAME:
                if split_value == 1:
                    if i + 1 < len(number_splits) and i == 0:
                        _, next_split_type, _, _, _ = number_splits[i+1]
                        if next_split_type == Number.TEN_POWER_NAME:
                            continue

                name = default_number_names[split_value]
            else:
                name = default_ten_power_names[split_value]

        offset = offset_from_var(variations, number=split_number, gender=split_gender, case=split_case)
        
        normalized_name = name[0] + name[offset + 1]
        extra = (name[0], name[offset + 1])

        number_splits[i] += extra + (normalized_name,)

    number_splits_ = []
    for i in range(len(number_splits) - 1):
        if (not(number_splits[i][0] == 1 and 
            number_splits[i][1] == Number.NAME and 
            number_splits[i + 1][1] == Number.TEN_POWER_NAME)):

            number_splits_.append(number_splits[i])
    
    number_splits_.append(number_splits[-1])
    
    return ' '.join([split[-1] for split in number_splits_]), number_splits_

def get_number_splits(value, number_name_keys, ten_powers_name_keys):
    num_splits = []
    if value == 0:
        num_splits.append((0, Number.NAME))
    else:
        num_pow_splits = {}
        for p in sorted(ten_powers_name_keys, reverse=True):
            d = pow(10, p)
            num_pow_splits[p] = value // d
            value = value % d

        for p in sorted(ten_powers_name_keys, reverse=True):
            if num_pow_splits[p] == 0:
                continue
            
            if p == 1:
                if num_pow_splits[p] == 1:
                    value = 10 + num_pow_splits[0] 
                    num_splits.append((value, Number.NAME))
                    break
                else:
                    value = num_pow_splits[p] * 10
                    num_splits.append((value, Number.NAME))
                    continue
            
            if num_pow_splits[p] in number_name_keys:
                num_splits.append((num_pow_splits[p], Number.NAME))
            else:
                num_splits += get_number_splits(num_pow_splits[p], number_name_keys, ten_powers_name_keys)

            if p > 1:
                num_splits.append((p, Number.TEN_POWER_NAME))

    return num_splits
    
def get_number_forms(stress=Stress.No):  
    global number_names_forms  

    def iterate_numbers(number_names=get_all_number_names(stress),path=[]):
        if len(path) > 3:
            raise Exception()

        if isinstance(number_names, dict):
            if ('Names' in number_names and 
                'Ten Power Names' in number_names):
    
                names = list(number_names['Names'].items())
                for i in range(len(names)):
                    value, endings = names[i]
                    for j in range(1, len(endings[1:])):
                        ending = endings[j]
                        yield int(value), ending, endings[0] + ending, list(path + [i,j])

                ten_names = list(number_names['Ten Power Names'].items())
                for i in range(len(ten_names)):
                    value, endings = ten_names[i]
                    for j in range(1, len(endings[1:])):
                        ending = endings[j]
                        yield pow(10, int(value)), ending, endings[0] + ending, list(path + [i,j])
            else:
                for modifier, sub_number_names in number_names.items():
                    for _ in iterate_numbers(sub_number_names, path + [modifier]):
                        yield _
        
        elif isinstance(number_names, list):
            for element in number_names:
                for _ in iterate_numbers(element):
                    yield _
    
    if stress not in number_names_forms:
        number_names_forms_ = {}
        number_names_ending_counter = {}
        
        for value, ending, name, path in iterate_numbers():
            path = '/'.join([str(_) for _ in path])
            if value not in number_names_forms_:
                number_names_forms_[value] = {}
                number_names_ending_counter[value] = {}

            number_names_forms_[value][path] = (name, ending)

            if ending not in number_names_ending_counter[value]:
                number_names_ending_counter[value][ending] = [path, set([])]
            number_names_ending_counter[value][ending][1].add(name)
        
        unique_number_names_ending_paths_ = {}
        for value, endings in number_names_ending_counter.items():
            unique_number_names_ending_paths_[value] = []
            for ending, v in endings.items():
                if len(v[1]) == 1:
                    unique_number_names_ending_paths_[value].append(v[0])

        number_names_forms[stress] = dict(number_names_forms_)
        unique_number_names_ending_paths[stress] = dict(unique_number_names_ending_paths_)

    return number_names_forms[stress], unique_number_names_ending_paths[stress]

def test():
    num_name, _ = get_number_complex_name(
        value=4900000,
        category_type="Kiekiniai",
        category_subtype="Pagrindiniai",
        number="dgs",
        case="vard."
    )

    assert('keturi milijonai devyni šimtai tūkstančių' == num_name)

    num_name, _ = get_number_complex_name(
        value=4900000,
        category_type="Kiekiniai",
        category_subtype="Pagrindiniai",
        number="dgs",
        case="kilm."
    )

    assert('keturių milijonų devynių šimtų tūkstančių' == num_name)

    num_name, _ = get_number_complex_name(
        value=4900000,
        category_type="Kiekiniai",
        category_subtype="Pagrindiniai",
        number="dgs",
        case="naud."
    )

    assert('keturiems milijonams devyniems šimtams tūkstančių' == num_name)

    test_data = [
        (6349000, "Kiekiniai", "Pagrindiniai", None, "mot. g.", 'kilm.', 'šešių milijonų trijų šimtų keturiasdešimt devynių tūkstančių'),
        (21, "Kiekiniai", "Pagrindiniai", 'dgs', "mot. g.", 'kilm.', 'dvidešimt vienų'),
        (21, "Kelintiniai", "Neįvardžiuotiniai", "dgs", "mot. g.", 'vard.', 'dvidešimt pirmos'),
        (6349000, "Kiekiniai", "Pagrindiniai", "vns", "mot. g.", 'vard.', 'šeši milijonai trys šimtai keturiasdešimt devyni tūkstančiai'),
    ]
    for i in range(len(test_data)):
        val, cat_type, cat_subtype, number, gender, case, name = test_data[i]

        num_name, _ = get_number_complex_name(
            value=val, category_type=cat_type,
            category_subtype=cat_subtype,
            number=number, gender=gender, case=case
        )

        assert(name == num_name)
    
    pairs0 = [
        (1100, 'tūkstantis šimtųjų'),
        (2003, 'du tūkstančiai trečiųjų'),
        (1, 'pirmųjų'),
        (11, 'vienuoliktųjų'),
        (101, 'šimtas pirmųjų'),
        (10, 'dešimtųjų'),
        (100, 'šimtųjų'),
        (1000, 'tūkstantųjų'),
        (119, 'šimtas devynioliktųjų'),
        (11002, 'vienuolika tūkstančių antrųjų'),
        (1000001, 'milijonas pirmųjų'),
        (102340010050, 'šimtas du milijardai trys šimtai keturiasdešimt milijonų dešimt tūkstančių penkiasdešimtųjų')]

    for value, name in pairs0:
        num_name, _ = get_number_complex_name(
            value=value,
            category_type="Kelintiniai",
            category_subtype="Įvardžiuotiniai",
            number="dgs",
            case="kilm.")

        assert(name == num_name)
        
if __name__ == '__main__':
    test()

    a = get_number_forms(Stress.No)
    
    
    num_name, _ = get_number_complex_name(
        value=6349000, category_type="Kiekiniai",
        category_subtype="Pagrindiniai",
        gender="mot. g.", case='vard.'
      )
    assert(num_name == 'šeši milijonai trys šimtai keturiasdešimt devyni tūkstančiai')

    number_name, _ = get_number_complex_name(
        value=1, category_type='Kelintiniai',
        category_subtype='Įvardžiuotiniai', gender='mot. g.',
        number='vns', case='kilm.', stress=Stress.No
    )
    assert(number_name == 'pirmosios')


    number_name, _ = get_number_complex_name(
        value=133, category_type='Kelintiniai',
        category_subtype='Įvardžiuotiniai', gender='vyr. g.',
        number='dgs', case='vard.', stress=Stress.No
    )
    assert(number_name == 'šimtas trisdešimt tretieji')
