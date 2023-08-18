from flask import Flask, request, jsonify
import pandas as pd
from surprise import dump,Dataset,Reader
import json
import pickle

app = Flask(__name__)

@app.route('/', methods=['GET'])
def popularity():
    try: 

        data = pd.read_csv(r"C:\Users\Jaskirat Singh\Python files\Flipkart grid\Not-FlipKart\backend + model\filtered.csv")
        data = data[['pid','product_name','brand','description','retail_price']].head(12)
        result = data.to_json(indent=6,orient="records")
        parsed = json.loads(result)
        # parsed.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')

        return parsed
    
    except FileNotFoundError:
        return jsonify({"error": "Data file not found"}), 404
    


# Get recommendations for the users based on SVD (Singular Value Decomposition)

def prediction(userId,svd):
    
    # function to add the Predicted rating in with other data
    def addrating(x):
        for row in top_predictions:
            if x == row[1]:
                return row[3]
    
    # the number of recommendation to give for particular user
    items_to_recommend = 30
    data = pd.read_csv(r"C:\Users\Jaskirat Singh\Python files\Flipkart grid\Not-FlipKart\backend + model\filtered.csv")
    prod_auth_pt = pickle.load(open(r"C:\Users\Jaskirat Singh\Python files\Flipkart grid\Not-FlipKart\backend + model\pivot_table.pkl",'rb'))
    # prediction for each product for the particular user
    predictions = [svd.predict(userId,itemid,rating) for itemid,rating in prod_auth_pt[userId].items()]
    
    
    # Sort the predictions based on the estimated rating (`est`) in descending order and selects the top `items_to_recommend` items as the recommendations.
    top_predictions = sorted(predictions, key=lambda x: x.est, reverse=True)[:items_to_recommend]
    

    # get only the ProductId and Predicted Rating fro each of the top Item
    topitemsId = [row[1] for row in top_predictions]
    
    # here we add the predicted rating column in to dataframe

    recommended_items = data[data['pid'].isin(topitemsId)][['pid','product_name','brand','description','retail_price']].drop_duplicates(subset='pid')
    recommended_items['predictedRating'] = recommended_items['pid'].apply(addrating)
    
    
    return recommended_items

@app.route('/api/collaborative', methods=['GET'])
def collaborative():
    try:
        _,svd = dump.load(r"C:\Users\Jaskirat Singh\Python files\Flipkart grid\Not-FlipKart\backend + model\svd.pkl")
        User = int(request.args.get('userid'))
        recommendedItems = prediction(User,svd)
        result = recommendedItems.to_json(orient="records",indent=6)
        parse = json.loads(result)
        return parse

    except FileNotFoundError:
        return jsonify({"error": "Data file not found"}), 404
        # except:
        #     return jsonify({"error": "User not found"})
    

def recommend(Id,cosine_sim):

    filtered = pd.read_csv(r"C:\Users\Jaskirat Singh\Python files\Flipkart grid\Not-FlipKart\backend + model\filtered.csv")
    indices = pd.Series(filtered.index, index=filtered['pid']) # Mapping title with the index
    
    try:
        # Get the index of the given 'title' in the 'indices' list or dictionary

        index = indices[Id]
    
        # Get the cosine similarity of the given title with all other titles
        similarity = list(enumerate(cosine_sim[index]))
        
        # Sort the similarity scores in descending order
        similarity = sorted(similarity, key=lambda x: x[1], reverse=True)
        
        # Get the top 30 similar titles (excluding the given title itself)
        scores = similarity[1:6]
        
        # Get the original indices of the top 30 similar titles
        org_index = [i[0] for i in scores]

        similar_titles = filtered[['pid','product_name','brand','description','retail_price']].iloc[org_index].copy()
        
        similar_titles['similarity'] = [i[1] for i in scores]
        # Return a DataFrame with the 'productId', 'name', and 'description' columns of the similar titles
        return similar_titles
    
    except:
        pass

@app.route('/api/contentbased', methods=['GET'])
def contentbased():
    try:
        with open(r"C:\Users\Jaskirat Singh\Python files\Flipkart grid\Not-FlipKart\backend + model\cosine_sim_tfidf.pkl", 'rb') as f:
            data = pickle.load(f)
            Id = str(request.args.get('id'))
            recommendations = recommend(Id,data)
            
            result = recommendations.to_json(orient="records",indent=6)
            parsed = json.loads(result)
        return parsed
    
    except FileNotFoundError:
        return jsonify({"error": "Data file not found"}), 404
    except:
        return jsonify({"error": "Item Id not found"}), 404
    

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
