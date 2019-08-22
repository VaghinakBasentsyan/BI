from sklearn.svm import SVC

def create_model(*args, **kwargs):
    return SVC(gamma='scale', probability=True, kernel='rbf')



if __name__ == "__main__":
    X = [[0, 0], [1, 1]]
    Y = [0, 1]
    clf = create_model()

    a = clf.fit(X, Y)
    b = clf.predict([[2., 2.]])
    print(b)

