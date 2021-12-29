import pdb
from flask import Flask, request, redirect, session, render_template, jsonify
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_sauce'
boggle_game = Boggle()

@app.route('/')
def show_game():
  """Generate board on front end, keep track of total games played"""
  gameBoard = boggle_game.make_board()
  session['game_board'] = gameBoard
  totalGames = session.get("totalGamesPlayed", 0)
  highScore = session.get("highScore", 0)

  return render_template('index.html', gameBoard = gameBoard, totalGames = totalGames, highScore = highScore)

@app.route("/check-word")
def check_word():
  """Check if word is in dictionary."""
  word = request.args["word"]
  board = session["game_board"]
  response = boggle_game.check_valid_word(board, word)

  return jsonify({'result': response})

@app.route("/post-score", methods=["POST"])
def post_score():
  """Keep track of number of games & score to save in server"""
  score = request.json["score"]

  # Track number of games played to display to user
  totalGamesPlayed = session.get("totalGamesPlayed", 0)
  session["totalGamesPlayed"] = totalGamesPlayed +1 

# Track highscore to display to user
  highScore = session.get("highScore", 0)
  session["highScore"] = max(score, highScore)

  return jsonify(score = score, highscore = highScore)
