import multiprocessing.dummy as mp

def funky_functions (number):
    return number + 80

threads = mp.Pool(20)
print threads.map(funky_functions, range(100, 200))
