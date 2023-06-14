import numpy as np

def main():
    vec = np.array([1, 2, 3])

    print(np.where(vec==3)[0])

if __name__=="__main__":
    main()