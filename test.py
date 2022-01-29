import multiprocessing as mp
from utils import timing

def f(x):
    a = 1
    for j in range(100000):
        a += j

@timing
def serial(n):
    for j in range(n):
        f(j)

@timing
def process(n):
    process_list = []
    for j in range(n):
        p = mp.Process(target=f, args=[j])
        p.start()
        process_list.append(p)
    for process in process_list:
        process.join()

@timing
def parpool(n):
    with mp.Pool(mp.cpu_count()) as pool:
        pool.map(f, range(n))

@timing
def parpoolApply(n):
    with mp.Pool(mp.cpu_count()) as pool:
        for j in range(n):
            pool.apply(f, (j,))


if __name__ == "__main__":
    n = 200
    serial(n)
    process(n)
    parpool(n)
    parpoolApply(n)
