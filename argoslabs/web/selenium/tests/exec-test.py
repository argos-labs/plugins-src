try:
    params = {
#        'name': 'abc',
    }

    script_f = 'exec-test.txt'
    with open(script_f) as ifp:
        script = ifp.read()

    exec(script, globals(), locals())
    globals().update(locals())

    # noinspection PyUnresolvedReferences
    do_start(**params)
except Exception as err:
    print(str(err))
