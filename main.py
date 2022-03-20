from RecommendationSystem.RecommendationSystem import RecommendationEngine
import heapq


def get_index(sid):
    index = int(sid[1:]) - 1
    return index

if __name__ == '__main__':
    path = 'data\\netflix_titles.csv'  # path to the dataset

    re = RecommendationEngine(path)  # Recommendation Engine object

    input_index = 's10'   # input title

    recommendations = re.get_recommendations(input_index, 5)  # generate recommendations for this file


    # displaying the original title and its description
    print("original file")

    print(re.data[get_index(input_index)]['title'])
    print(re.data[get_index(input_index)]['description'])

    # displaying the recommendations and their descriptions
    result= []
    while len(recommendations) > 0:
        top = heapq.heappop(recommendations)
        result.append(re.data[top.target])


    print("--------------------------------------------------------------------")

    print("Recommendations: ")

    for res in result[::-1]:
        print(res['title'])
        print(res['description'])
        print("///////////////////////////////////////////")