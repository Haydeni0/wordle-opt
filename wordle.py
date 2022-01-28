from wordleFunctions import *
from bestWord import *
import sys
import time


if __name__ == "__main__":
    n = 200
    # print(algScore(bestWord1, n))
    # print(algScore(bestWord2, n))

    tic = time.time()
    print(algScoreParpool(bestWord1, n))
    toc = time.time()
    print(f"Time take: {toc - tic :.4f} seconds.")

    tic = time.time()
    print(algScoreParpoolMap(bestWord1, n))
    toc = time.time()
    print(f"Time take: {toc - tic :.4f} seconds.")

    tic = time.time()
    print(algScore(bestWord1, n))
    toc = time.time()
    print(f"Time take: {toc - tic :.4f} seconds.")