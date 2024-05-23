from flask import Flask, render_template, request, redirect, url_for, jsonify
import uuid

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for session management

# Global dictionary to store scoreboards
scoreboards = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scorecard', methods=['GET'])
def scorecard():
    guid = str(uuid.uuid4())
    team1 = request.args.get('team1', 'Team 1')
    score1 = request.args.get('score1', '0')
    team2 = request.args.get('team2', 'Team 2')
    score2 = request.args.get('score2', '0')
    logo1 = request.args.get('logo1', '')
    logo2 = request.args.get('logo2', '')
    color1 = request.args.get('color1', '#FF0000')
    color2 = request.args.get('color2', '#0000FF')
    to1 = request.args.get('to1', '0')
    fo1 = request.args.get('fo1', '0')
    to2 = request.args.get('to2', '0')
    fo2 = request.args.get('fo2', '0')
    time = request.args.get('time', '00:00')
    period = request.args.get('period', '1')
    possession = request.args.get('possession', 'none')
    possession_icon = request.args.get('possession_icon', 'fas fa-basketball-ball')

    scoreboard = {
        'team1': team1,
        'score1': score1,
        'team2': team2,
        'score2': score2,
        'logo1': logo1,
        'logo2': logo2,
        'color1': color1,
        'color2': color2,
        'to1': to1,
        'fo1': fo1,
        'to2': to2,
        'fo2': fo2,
        'time': time,
        'period': period,
        'possession': possession,
        'possession_icon': possession_icon
    }

    scoreboards[guid] = scoreboard
    return redirect(url_for('display_scorecard', guid=guid))

@app.route('/scorecard/<guid>', methods=['GET'])
def display_scorecard(guid):
    scoreboard = scoreboards.get(guid)
    if not scoreboard:
        return 'Scoreboard not found', 404
    return render_template('scorecard.html', guid=guid, **scoreboard)

@app.route('/scoreboard_data/<guid>', methods=['GET'])
def scoreboard_data(guid):
    scoreboard = scoreboards.get(guid)
    if not scoreboard:
        return jsonify({'error': 'Scoreboard not found'}), 404
    return jsonify(scoreboard)

@app.route('/control/<guid>', methods=['GET'])
def control_panel(guid):
    scoreboard = scoreboards.get(guid)
    if not scoreboard:
        return 'Scoreboard not found', 404
    return render_template('control_panel.html', guid=guid, **scoreboard)

@app.route('/update/<guid>', methods=['POST'])
def update_scorecard(guid):
    scoreboard = scoreboards.get(guid)
    if not scoreboard:
        return 'Scoreboard not found', 404

    for key in request.form:
        scoreboard[key] = request.form[key]
    
    scoreboards[guid] = scoreboard
    return jsonify(success=True)

@app.route('/destroy/<guid>', methods=['GET'])
def destroy_scorecard(guid):
    scoreboards.pop(guid, None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
