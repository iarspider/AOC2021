import numpy as np

mysin = [0, 1, 0, -1]
mycos = [1, 0, -1, 0]

matrices = []


def Rx(theta):
    return np.matrix([[1, 0, 0],
                      [0, mycos[theta], -mysin[theta]],
                      [0, mysin[theta], mycos[theta]]])


def Ry(theta):
    return np.matrix([[mycos[theta], 0, mysin[theta]],
                      [0, 1, 0],
                      [-mysin[theta], 0, mycos[theta]]])


def Rz(theta):
    return np.matrix([[mycos[theta], -mysin[theta], 0],
                      [mysin[theta], mycos[theta], 0],
                      [0, 0, 1]])


def generate_matrices():
    matrices = []
    for ax in range(4):
        for ay in range(4):
            for az in range(4):
                rx = Rx(ax)
                ry = Ry(ay)
                rz = Rz(az)

                matrices.append(rx * ry * rz)
                matrices.append(rx * rz * ry)
                matrices.append(ry * rx * rz)
                matrices.append(ry * rz * rx)
                matrices.append(rz * ry * rx)
                matrices.append(rz * rx * ry)

    excl = []
    for i in range(len(matrices)):
        if i in excl:
            continue

        for j in range(i + 1, len(matrices)):
            if np.array_equal(matrices[i], matrices[j]):
                excl.append(j)

    for i in reversed(sorted(excl)):
        matrices.pop(i)

    print("Geneated", len(matrices), "matrices")
    return matrices

def rotate(v, i):
    return np.dot(matrices[i], v)
