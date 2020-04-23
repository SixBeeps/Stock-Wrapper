from Classes.LogisticRegression import LogisticRegression
from Classes.JSONReader import JSONReader
from Classes.Stocks import Stocks

stocks = Stocks("autumn2k@gmail.com", "Mary0707$2")

data = stocks.get_data(['UAL'], 'day')
features, labels = stocks.get_training_data(['UAL'], '3month')
testFeatures, testLabels = stocks.get_training_data(['DAL'], '3month')

regression = LogisticRegression(features, labels, options={'learning_rate': 1, 'iterations': 80, 'batchsize': 10})
regression.train()

accuracy = regression.test(testFeatures, testLabels).numpy().tolist()
print(accuracy)

# store data as json
data = {}
data["accuracy"] = accuracy
data["weights"] = regression.weights.numpy().tolist()

JSONReader.write_file('stock.txt', data)