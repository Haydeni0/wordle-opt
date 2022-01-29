from wordleFunctions import *
from bestWord import *
import sys
import time

if __name__ == "__main__":
    n = 1000
    print(algScore(bestWord1, n)[0]/n)
    print(algScore(bestWord2, n)[0]/n)