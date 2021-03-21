
def validate(data):
    required = ['title', 'on_discount', 'discount_price', 'price']
    for key in required:
        if key not in data:
            return {'error': '{} is required'.format(key), }
    type_check = ['title', 'on_discount', 'discount_price',
                  'price', 'description', 'image_path']
    type_val = [str, bool, int, int, str, str]
    for i in range(len(type_check)):
        if type_check[i] in data:
            if type(data[type_check[i]]) != type_val[i]:
                return {'error': 'data type of {} is not {}'.format(type_check[i], type_val[i])}
    return {'msg': 'sucessfully validate'}
