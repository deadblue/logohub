__author__ = 'deadblue'

def must_atoi(s:str, def_value:int=0) -> int:
    try:
        return int(s, 10)
    except:
        return def_value
