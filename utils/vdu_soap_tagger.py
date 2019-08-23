from requests import post
from re import compile 
from html import unescape

re_result = compile(r'Nudaugiareiksmintas tekstas:.*<br>.*<br>(.*)<\/form>')
re_tag = compile(r'<([^<>]+)>')
re_param = compile(r'([^ =]+)(="([^"]+)")?')

def stress_text(text, version='8.0'):    
    data = {
        'tekstas': text,
        'tageris': 'Dirbti'
    }

    response = post("http://donelaitis.vdu.lt/~airenas/Kirtis/tag.php", data)

    if response.status_code != 200:
        raise Exception(response.reason)

    text = response.content.decode("utf-8")
    m = re_result.search(text)
    if not m:
        raise Exception('Bad response')

    result = unescape(m.group(1)).strip()

    elements = []

    for tag in re_tag.finditer(result):
        element = {}
        for param in re_param.finditer(tag.group(1)):
            element[param.group(1)] = param.group(3)
        elements.append(element)
    
    return elements

print (stress_text('Laba diena draugai! Kaip jums sekasi? Vienas, du, trys.'))
print (stress_text('namo'))
print (stress_text('Šioje vietoje trūksta namo!'))
print (stress_text('Einam namo!'))