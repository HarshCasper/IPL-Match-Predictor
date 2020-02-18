import flask
import pickle
import pandas as pd
import numpy as np

with open(f'model/ipl_model.pkl', 'rb') as f:
    model = pickle.load(f)

app = flask.Flask(__name__, template_folder='templates')

@app.route('/', methods=["GET", "POST"])
def main():
    if flask.request.method == 'GET':
        return(flask.render_template('main.html'))

    if flask.request.method == 'POST':
        city = flask.request.form['city']
        Home = flask.request.form['Home']
        Away = flask.request.form['Away']
        toss_winner = flask.request.form['toss_winner']
        toss_decision = flask.request.form['toss_decision']
        venue = flask.request.form['venue']

        if toss_winner == 'Home Team':
            toss_winner = Home
        else:
            toss_winner = Away

        input_variables = pd.DataFrame([[city, Home, Away, toss_winner, toss_decision, venue]], columns=['city', 'Home', 'Away', 'toss_winner',
        'toss_decision', 'venue'], dtype=object)

        input_variables.Home.replace(['Sunrisers Hyderabad', 'Mumbai Indians', 'Gujarat Lions',
                      'Rising Pune Supergiant', 'Royal Challengers Bangalore',
                      'Kolkata Knight Riders', 'Delhi Capitals', 'Kings XI Punjab',
                      'Chennai Super Kings', 'Rajasthan Royals', 'Deccan Chargers',
                      'Kochi Tuskers Kerala', 'Pune Warriors', 'Rising Pune Supergiants'],
                      np.arange(0, 14), inplace=True)
        input_variables.Away.replace(['Sunrisers Hyderabad', 'Mumbai Indians', 'Gujarat Lions',
                      'Rising Pune Supergiant', 'Royal Challengers Bangalore',
                      'Kolkata Knight Riders', 'Delhi Capitals', 'Kings XI Punjab',
                      'Chennai Super Kings', 'Rajasthan Royals', 'Deccan Chargers',
                      'Kochi Tuskers Kerala', 'Pune Warriors', 'Rising Pune Supergiants'],
                      np.arange(0, 14), inplace=True)
        #input_variables['toss_winner'] = np.where(input_variables['toss_winner'] == 'Home Team', input_variables['Home'], input_variables['Away'])
        input_variables.toss_winner.replace(['Sunrisers Hyderabad', 'Mumbai Indians', 'Gujarat Lions',
                             'Rising Pune Supergiant', 'Royal Challengers Bangalore',
                             'Kolkata Knight Riders', 'Delhi Capitals', 'Kings XI Punjab',
                             'Chennai Super Kings', 'Rajasthan Royals', 'Deccan Chargers',
                             'Kochi Tuskers Kerala', 'Pune Warriors', 'Rising Pune Supergiants'],
                              np.arange(0, 14), inplace=True)
        input_variables.toss_decision.replace(['bat', 'field'], [0, 1], inplace=True)
        input_variables.city.replace(['Hyderabad', 'Pune', 'Rajkot', 'Indore', 'Bangalore', 'Mumbai',
        'Kolkata', 'Delhi', 'Chandigarh', 'Kanpur', 'Jaipur', 'Chennai',
        'Cape Town', 'Port Elizabeth', 'Durban', 'Centurion',
        'East London', 'Johannesburg', 'Kimberley', 'Bloemfontein',
        'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala', 'Kochi',
        'Visakhapatnam', 'Raipur', 'Ranchi', 'Abu Dhabi', 'Sharjah'],
        np.arange(0, 30), inplace=True)
        input_variables.venue.replace(['Rajiv Gandhi International Stadium, Uppal',
        'Maharashtra Cricket Association Stadium',
        'Saurashtra Cricket Association Stadium', 'Holkar Cricket Stadium',
        'M Chinnaswamy Stadium', 'Wankhede Stadium', 'Eden Gardens',
        'Feroz Shah Kotla',
        'Punjab Cricket Association IS Bindra Stadium, Mohali',
        'Green Park', 'Punjab Cricket Association Stadium, Mohali',
        'Sawai Mansingh Stadium', 'MA Chidambaram Stadium, Chepauk',
        'Dr DY Patil Sports Academy', 'Newlands', "St George's Park",
        'Kingsmead', 'SuperSport Park', 'Buffalo Park',
        'New Wanderers Stadium', 'De Beers Diamond Oval',
        'OUTsurance Oval', 'Brabourne Stadium',
        'Sardar Patel Stadium, Motera', 'Barabati Stadium',
        'Vidarbha Cricket Association Stadium, Jamtha',
        'Himachal Pradesh Cricket Association Stadium', 'Nehru Stadium',
        'Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium',
        'Subrata Roy Sahara Stadium',
        'Shaheed Veer Narayan Singh International Stadium',
        'JSCA International Stadium Complex', 'Sheikh Zayed Stadium',
        'Sharjah Cricket Stadium'],
        np.arange(0, 34), inplace=True)
        prediction = model.predict(input_variables)
        prediction = pd.DataFrame(prediction, columns=['Winners'])
        prediction = prediction["Winners"].map({0:'Sunrisers Hyderabad', 1:'Mumbai Indians', 2:'Gujarat Lions',
                      3:'Rising Pune Supergiant', 4:'Royal Challengers Bangalore',
                      5:'Kolkata Knight Riders', 6:'Delhi Capitals', 7:'Kings XI Punjab',
                      8:'Chennai Super Kings', 9:'Rajasthan Royals', 10:'Deccan Chargers',
                      11:'Kochi Tuskers Kerala', 12:'Pune Warriors', 13:'Rising Pune Supergiants'})
        return flask.render_template('main.html', original_input={'city':city, 'Home':Home, 'Away':Away, 'toss_winner':toss_winner, 'toss_decision':toss_decision,
                                     'venue':venue},
                                    result=prediction[0],
                                    )

if __name__=='__main__':
    app.run(debug="True")
