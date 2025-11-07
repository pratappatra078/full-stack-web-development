from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/roll', methods=['GET'])
def roll_dice():
    dice_value = random.randint(1, 6)
    return jsonify({
        'value': dice_value,
        'message': f'You rolled a {dice_value}!'
    })


if __name__ == '__main__':
    app.run(debug=True)
