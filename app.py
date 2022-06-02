from flask import Flask, request, render_template
import pickle

app = Flask(__name__)

file = open('bodyfatmodel.pkl', 'rb')
model = pickle.load(file)
file.close()


@app.route("/", methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        my_dict = request.form
        try:
            density = float(my_dict['density'])
            chest = float(my_dict['chest'])
            abdomen = float(my_dict['abdomen'])
            weight = float(my_dict['weight'])
            hip = float(my_dict['hip'])
        except ValueError:
            return render_template('home.html')
        else:
            input_features = [[density, chest, abdomen, weight, hip]]
            prediction = model.predict(input_features)[0].round(2)
            print(input_features[0], prediction)
            return render_template('home.html', string=f'{prediction}')
    return render_template('home.html')


if __name__ == "__main__":
    app.run(debug=True)
