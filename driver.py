import graph as g
import matplotlib.pyplot as plt
import numpy as np

def main():
    steps = np.linspace(0,1,25)
    bot1results = []
    bot2results = []
    bot3results = []
    bot4results = []
    
    for q in steps:
        print("Simulating for q = {q:.2f}".format(q=q))
        bot1results.append(g.simulateBot1(100,q))
        bot2results.append(g.simulateBot2(100,q))
        bot3results.append(g.simulateBot3(100,q))
        bot4results.append(g.simulateBot4(100,q))

    bot1 = plt.scatter(steps, bot1results, marker="x")
    bot2 = plt.scatter(steps, bot2results, marker="x")
    bot3 = plt.scatter(steps, bot3results, marker="x")
    bot4 = plt.scatter(steps, bot4results, marker="o")
    plt.legend((bot1, bot2, bot3, bot4),
               ("Bot 1", "Bot 2", "Bot 3", "Bot 4"),
               loc='lower left',
               ncol=2,
               fontsize=8)
    plt.show()
    
if __name__ == "__main__":
    main()