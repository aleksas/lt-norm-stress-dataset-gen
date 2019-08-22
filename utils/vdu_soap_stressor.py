from zeep import Client

_stress_map = {
    '&#x0300;': '`',
    '&#x0301;': '^',
    '&#x0303;': '~'
}

def stress_text(text, version='8.0'):    
    data = {
        'in':text,
        'Versija':version,
        'WP':''
    }

    client = Client('http://donelaitis.vdu.lt/Kirtis/KServisas.php?wsdl')
    result = client.service.kirciuok(data)

    for k,v in _stress_map.items():
        result['out'] = result['out'].replace(k, v)

    assert (result['Info'] == None)
    assert (result['Klaida'] == None)

    return result['out']


print (stress_text('Laba diena draugai! Kaip jums sekasi? Vienas, du, trys.'))
print (stress_text('namo'))
print (stress_text('Šioje vietoje trūksta namo!'))
print (stress_text('Einam namo!'))