import numpy as np

import edge_detect as ed

def main():
    data = np.zeros(shape=(5,5), dtype=float)

    for i in range(5):
        data[2][i] = 0.25
        data[3][i] = 1
        data[4][i] = 1

    print data.tolist()
    print 'hey'
    print data.shape


    print ed.compute_gradient(data, 5, 5, 2, 2, -1, -1)

    print ed.second_stage(data, 5, 5, 2, 2)

    edges = ed.first_stage(data, 5, 5)
    print edges.tolist()


if __name__ == '__main__':
    main()
