from static.get_skaitvardis import Stress

def remove_stress(text, stress=Stress.ASCII):
    if stress==Stress.No:
        return text
    elif stress==Stress.ASCII:
        for _ in '~^`':
            text = text.replace(_, '')
        return text
    else:
        raise NotImplementedError()