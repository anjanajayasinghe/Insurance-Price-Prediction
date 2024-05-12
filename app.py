from flask import Flask, render_template, request
import pickle
import numpy as np

# setup application
app = Flask(__name__,template_folder='template')

def prediction(lst):
    filename = 'model/predictor.pickle'
    with open(filename, 'rb') as file:
        model = pickle.load(file)
    pred_value = model.predict([lst])
    return pred_value

@app.route('/', methods=['POST', 'GET'])
def index():
    # return "Hello World"
    pred_value = 0
    if request.method == 'POST':
        age = request.form['age']
        sex = request.form['sex']
        bmi = request.form['bmi']
        children = request.form['children']
        region = request.form['region']
        smoke = request.form.getlist('smoke')
        
        feature_list = []

        feature_list.append(int(age))
        feature_list.append(float(bmi))
        feature_list.append(len(smoke))
        feature_list.append(int(sex))

        children_list = ['0','1','2','3','4','5']
        region_list = ["southeast","southwest","northwest","northeast"]
        def traverse_list(lst, value):
            for item in lst:
                if item == value:
                    feature_list.append(1)
                else:
                    feature_list.append(0)
        

        traverse_list(children_list, children)
        traverse_list(region_list, region)
        print(feature_list)
        pred_value = prediction(feature_list)
        pred_value = np.round(pred_value[0],2)
        pred_value
    return render_template('index.html', pred_value=pred_value)


if __name__ == '__main__':
    app.run(debug=True)