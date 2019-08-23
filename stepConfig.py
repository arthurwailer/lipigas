def step_th():
    memo_integers = {'RunCounterStatus': 4002,
                     'height': 4007,
                     'temperatura': 40010,
                     'volumen': 40011}
 
    default_config = {'method': 'TCP',
                      'bitstop': 1,
                      'bytesize': 8,
                      'parity': 'N',
                      'baudrate': 9600,
                      'timeout': 3,
                      'nper':1}
 
    return {'memo_Integers': memo_integers,
            'default_config': default_config}