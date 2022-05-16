import re

def search_filter(data, params):
    search_pat = re.compile(r'^search_(?P<search_target>\w+( \w+)*)$')

    search_val = None
    search_target = None

    for (param_key, param_val) in params.items():
            search_m = search_pat.match(param_key)
            if search_m:
                search_val = param_val
                search_target = search_m.group('search_target')
                break

    if search_val and search_target:
        try:
            return data[data[search_target].str.contains(search_val, flags=re.IGNORECASE)]
        except:
            pass

    return data

def ordering_filter(data, params):
    ordering = params.get('ordering')
    ordering_fields = []
    ordering_ascending = []

    if ordering:
        ordering_pat = re.compile(r'^(?P<ascending>-{0,1})(?P<order>\w+( \w+)*)$')
        for order in ordering.split(','):
            order = order.strip()
            ordering_m = ordering_pat.match(order)
            if len(order) > 0 and ordering_m:
                order = ordering_m.group('order')
                ascending = ordering_m.group('ascending')
                ordering_fields.append(order)
                ordering_ascending.append(not bool(ascending))

        if ordering_fields and ordering_ascending:
            try:
                return data.sort_values(by=ordering_fields, ascending=ordering_ascending)
            except:
                pass

    return data

def columns_filter(data, params):
    columns = params.get('columns')
    cols_pat = re.compile(r"((?<=')[\w., ]+(?=')|[\w. ]+)")
    if columns:
        try:
            columns = cols_pat.findall(columns)
            return data[columns]
        except:
            pass
    
    return data

def attribute_filter(data, params):

    # get a string and return its corresponding value in python
    # on this case it can be one of the ff:
    # int = number ~ 1,2,3
    # string = str ~ 'abcd'
    # array = int,string,..., : 1,'abcd','def',3,4 
    def get_py_value(s):
        try:
            value = int(s)
        except:
            value = s
            arr_val_pat = re.compile(r'^\w+( \w+)*(,\w+( \w+)*)+$')
            arr_val_m = arr_val_pat.match(value)
            if arr_val_m:
                value = value.split(',')
        
        return value
    
    attr_pat = re.compile(r'^__(?P<method>\w+)__(?P<param>\w+)$')

    attrs = {}

    for (key, val) in params.items():
        attr_m = attr_pat.match(key)

        if attr_m:
            method = attr_m.group('method')
            param = attr_m.group('param')
            attr_val = {
                param: get_py_value(val),
            }
            attrs_val = attrs.setdefault(method, attr_val)

            if attrs_val:
                attrs_val.setdefault(param, get_py_value(val))
                attrs[method] = attrs_val

    for (method, kwargs) in attrs.items():
        try:
            data = getattr(data, method)(**kwargs)
        except:
            pass
    return data