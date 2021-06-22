import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({'font.size': 14})

import sys
if len(sys.argv) != N:
    print("""
Usage: python ...
""")

    sys.exit()
#end if

def main():
    row, col = 1,1
    fig, ax = plt.subplots(row,col, figsize=(8*col,7*row))  
    ax.plot(x,y)
    ax.set(
        title='chart',
        ylim=(0, 1),
        xlim=(0, 1),
        xlabel="x",
        ylabel="y")
    ax.legend()

    plt.show()
    #fig.savefig('Fig1.png')
    plt.close()

if __name__ == "__main__":

    main()

