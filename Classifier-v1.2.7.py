import os
import codecs
import math
from operator import itemgetter

class classifier:

    def __init__(self, trainingdata, filteringwords):
    
        self.StW = {}
        self.lexicon = {}
        self.probability = {}
        self.totals = {}
               
        categories = os.listdir(trainingdata)
        self.categories = categories
        wordstodelete = []
        for i in self.categories:
            (self.probability[i],
             self.totals[i]) = self.training(trainingdata, i)
        
        lengthvocabulary = len(self.lexicon)
        print "RUNNING THE PROBABILITY ANALYSIS"
        c = 0
        for i in self.categories:
            c += 1
            print c, i
            t = self.totals[i]
            vocablen = lengthvocabulary
            d = t + vocablen
            s = self.lexicon
            sp = self.probability[i]
            for word in s:
                if word in sp:
                    nk = sp[word]
                else:
                    nk = 1
                sp[word] = (float(nk + 1) / d)

        print "******THE MACHINE IS TRAINED NOW******\n\n"

        f = open(filteringwords)
        for k in f:
            self.StW[k.strip()] = 1
        f.close()

    

    def training(self, trainingdata, i):
        wordcounts = {}
        presentdirectory = trainingdata + i
        def splitting(something):
            return something.split()
        data = os.listdir(presentdirectory)
        def stripping(something):
            return something.strip('":?".;\/')
        totalwords = 0
        pd = presentdirectory
        def lowering(something):
            return something.lower()
        for j in data:
            filedata = pd + '/' + j
            dataFileToTrain = codecs.open(filedata, 'r', 'iso8859-1')
            
            for eachline in dataFileToTrain:
                tokens = splitting(eachline)
                for eachtokens in tokens:
                    eachtokens = stripping(eachtokens)
                    eachtokens = lowering(eachtokens)
                    
                    for eachtoken in tokens:
                        if eachtoken <> '' and not eachtokens in self.StW:
                            default_val = 0
                            self.lexicon.setdefault(eachtokens, default_val)
                            self.lexicon[eachtokens] += 1
                    for eachtoken in tokens:
                         if eachtoken <> '' and not eachtokens in self.StW:
                            default_val = 0
                            wordcounts.setdefault(eachtokens, default_val)
                            wordcounts[eachtokens] += 1
                            totalwords += 1
            dataFileToTrain.close()
        return(wordcounts, totalwords)

    def test(self, testingdirectory):
        def accuracytest(testD, i):
            def classification(filename):
                def splitting(something):
                    return something.split()
                def stripping(something):
                    return something.strip('":?".;\/')
                def lowering(something):
                    return something.lower()
                output = {}
                out = output
                cat = self.categories
                fn = filename
                
                for i in cat:
                    out[i] = 0
                testtextfile = codecs.open(fn, 'r', 'iso8859-1')
                for everyline in testtextfile:
                    tokenization = splitting(everyline)
                    for eachtoken in tokenization:
                        eachtoken = stripping(eachtoken)
                        eachtoken = lowering(eachtoken)
                        lexicon = self.lexicon
                        if eachtoken in lexicon:
                            for i in cat:
                                prob = self.probability[i]
                                if prob[eachtoken] == 0:
                                    """print("%s %s" % (i, eachtoken))"""
                                out[i] += math.log(prob[eachtoken])
        
                testtextfile.close()
                out = list(out.items())
                out.sort(key=itemgetter(1), reverse = True)
                return out [0][0]
            
            docs = os.listdir(testD)
            total = 0
            accurate = 0
            for j in docs:
                total += 1
                result = classification(testD + j)
                if result == i:
                    accurate += 1
            return (accurate, total)
            
        categories = self.categories
        entire = 0
        match = 0
        for totalfilesincategories in categories:
            data = testingdirectory + totalfilesincategories + '/'
            (matchedcat, entirecat) = accuracytest(data, totalfilesincategories)
            match += matchedcat
            entire += entirecat
        print("\n\nClassification accuracy : %f%% (%i files to test)" %
              ((float(match) / entire) * 100, entire))


testingdirectory = ("/home/neelabh/Documents/Dr. Huang/Machine Learning/20_newsgroups/20_newsgroups_testing/")
trainingdirectory = ("/home/neelabh/Documents/Dr. Huang/Machine Learning/20_newsgroups/20_newsgroups_training/")
cls = classifier(trainingdirectory,  "/home/neelabh/Documents/Dr. Huang/Machine Learning/20_newsgroups/filteringwords.txt")
print("results")
cls.test(trainingdirectory)

    
    

    
    

    




