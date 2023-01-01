import dpath.util


def get_data_from_dict():
    d = {
        'a': 1,
        'b': {
            'ba': {
                'bax': 999,
            }
        }
    }
    path = '/a'
    print(dpath.util.get(d, path))

    path = '/b'
    print(dpath.util.get(d, path))

    path = '/b/ba'
    print(dpath.util.get(d, path))

    path = '/b/ba/bax'
    print(dpath.util.get(d, path))


def get_data_from_list():
    d = [
        {
            'c': 3,
            'd': [
                'e',
                'f',
                'g',
            ]
        },
        'bbb',
        {
            'h': [
                'i',
                {
                    'j': {
                        'ja': 543,
                    },
                },
                'k',
            ]
        },
    ]
    path = '/0'
    print(dpath.util.get(d, path))

    path = '/0/d'
    print(dpath.util.get(d, path))

    path = '/0/d/1'
    print(dpath.util.get(d, path))

    path = '/2/h/1/j'
    print(dpath.util.get(d, path))


if __name__ == '__main__':
    # get_data_from_dict()
    get_data_from_list()
