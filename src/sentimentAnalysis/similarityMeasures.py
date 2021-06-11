class SimilarityClass:
    thresholds = []
    items = []
    def __init__(self, thresholds = [.6, .7, .8, .9, .95], items = ['item1a10K', 'etc']):
        self.thresholds = thresholds
        self.items = items

    #item = [item, threshold, [avgs], [prices one q out, y out, 2 y out]]
    def addTuple(data):
        for item in data[1]:
            
