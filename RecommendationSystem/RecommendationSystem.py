import csv
import heapq
import requests
import string
import pandas as pd
import numpy as np


class HeapNode:
    """The class for creating our custom Heap Node"""
    def __init__(self, parent, target, cos):
        self.parent = parent
        self.target = target
        self.cos = cos

    # Functions that help us build the min heap
    def __lt__(self, other):
        """overloading the less than operator"""
        return self.cos < other.cos

    def __eq__(self, other):
        """overloads the equal to operator"""
        if other is None:
            return False
        if not isinstance(other, HeapNode):  # Safeguarding ourselves if other is not a HeapNode
            return False
        return self.cos == other.cos


class RecommendationEngine:

    def __init__(self, dataset_path, encoding='utf-8'):


        # Loading the dataset
        with open(dataset_path, encoding=encoding) as file:
            self.data = list(csv.DictReader(file))


        # Loading the stop words

        stop_words_df = pd.read_csv(
            "https://gist.githubusercontent.com/sebleier/554280/raw/7e0e4a1ce04c2bb7bd41089c9821dbcf6d0c786c/NLTK's%2520list%2520of%2520english%2520stopwords",
            names=['words'])
        self.stop_words = set(stop_words_df['words'].values)

        # Loading the punctuations

        self.punctuations = set(string.punctuation)

        # getting the top 500 words

        self.top_500_words = self.get_most_common_words()

        # getting the feature dictionary for each record

        self.list_features = self.create_feature_dict_each_record()



    def get_most_common_words(self):
        """get the 500 most common words which helps us in building our features"""
        try:
            most_common_words = {}

            for event in self.data: # iterating over each title
                for word in event['description'].split(" "):  # iterating over each word in the description
                    word = word.lower()  # standardizing the word

                    if word in self.punctuations or word in self.stop_words:  # if word is a punctuation or a stop word, we don't consider the word
                        continue
                    elif word == '–' or word == '—':
                        continue
                    else:
                        if word in most_common_words:  # check if word is in most common words
                            most_common_words[word] += 1
                        else:
                            most_common_words[word] = 1
            # get the top 500 words
            top_500_words = list(
                dict(sorted(most_common_words.items(), key=lambda item: item[1], reverse=True)).keys())[:500]

            return top_500_words
        except Exception as e:
            pass

    def create_feature_dict_each_record(self):
        try:
            """This function creates feature dictionary for each record"""
            list_features = []  # list that stores the value of features (top words) for each record

            for event in self.data:  # iterate over all the records
                features = {key: 0 for key in self.top_500_words}  # generate a feature dictionary where keys are top 500 words and values are 0

                for word in event['description'].split(" "): # iterate over each word in this title's description
                    word = word.lower() # standardize the word

                    if word in features:  # increment the number of occurences of this word in the feature dictionary
                        features[word] += 1
                list_features.append(features) # add the feature dictionary into the features list for all records
            return list_features

        except Exception as e:
            pass


    def get_cosine_similarity(self,arr1, arr2):
        try:
            """calculates cosine similarity b/w 2 vectors"""

            num = np.dot(arr1, arr2)   # The numerator of the division
            denom = (np.sqrt(np.dot(arr1, arr1)) * np.sqrt(np.dot(arr2, arr2))) # The denominator of the division

            if denom == 0 or denom == np.nan:  # safeguard against wrong division.
                return -10000

            cos = num/denom    # calculate the cosine simmilarity

            return cos


        except Exception as e:
            pass


    def get_parent_index_from_sid(self, sid):
        try:

            """calculates the index from the sid i.e. Title id"""
            index = int(sid[1:])-1
            return index

        except Exception as e:
            pass


    def get_recommendations(self, sid, num_recommendations):
        try:
            """main function to generate the recommendations"""

            parent_index = self.get_parent_index_from_sid(sid)   # get the index for this sid


            heap = []  # create min heap for this title

            arr1 = np.array(list(self.list_features[parent_index].values()))  # generate vector from values of this feature dictionary




            for index, event in enumerate(self.list_features):  # iterate over all the titles
                if index == parent_index: # same title, hence we can safely ignore this title.
                    continue
                else:
                    arr2 = np.array(list(self.list_features[index].values()))  # generator vector for 2nd title

                    cos = self.get_cosine_similarity(arr1,arr2)  # calculate the cosine simmilarity b/w the two vectors.

                    temp_heap_node = HeapNode(parent_index, index, cos)  # temperory heap node

                    heapq.heappush(heap, temp_heap_node)  # push the node into the heap

                    if len(heap) > num_recommendations:  # if the number of elements in the heap exceed the desired recommendations, remove the top. The top will
                        # always have the least cosine simmilarity. Hence others are better candidates for recommendatons.
                        front = heapq.heappop(heap)

                        del front  # delete this object to free up memory. It is not required anymore.
            return heap # return the recommendations
        except Exception as e:
            pass





