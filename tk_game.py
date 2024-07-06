import tkinter as tk
import random

class Player:
    def __init__(self, name):
        self.name = name
        self.runs = 0
        self.balls_faced = 0
        self.wickets_taken = 0

    def __str__(self):
        return f"{self.name} - Runs: {self.runs}, ({self.balls_faced} balls, {self.wickets_taken} wkts)"

class Batsman(Player):
    def __init__(self, name):
        super().__init__(name)

class Bowler(Player):
    def __init__(self, name):
        super().__init__(name)

class AIOpponent:
    def decide_action(self):
        return random.choice(["defend", "attack", "single", "double", "boundary", "out"])

class CricketGame:
    def __init__(self, team1, team2, overs, update_gui, update_score):
        self.team1 = team1
        self.team2 = team2
        self.overs = overs
        self.current_batsman = None
        self.current_bowler = None
        self.ai = AIOpponent()
        self.innings = 1
        self.current_over = 0
        self.score = [0, 0]
        self.wickets = [0, 0]
        self.update_gui = update_gui
        self.update_score = update_score
    
    def play_ball(self):
        action = self.ai.decide_action()
        self.update_gui(f"AI chose to: {action}")

        if action == "defend":
            self.update_gui(f"{self.current_batsman.name} defended the ball.")
        elif action == "attack":
            runs = random.choice([0, 1, 2, 3, 4, 6])
            self.current_batsman.runs += runs
            self.score[self.innings - 1] += runs
            self.update_gui(f"{self.current_batsman.name} scored {runs} runs.")
        elif action == "single":
            self.current_batsman.runs += 1
            self.score[self.innings - 1] += 1
            self.update_gui(f"{self.current_batsman.name} scored a single run.")
        elif action == "double":
            self.current_batsman.runs += 2
            self.score[self.innings - 1] += 2
            self.update_gui(f"{self.current_batsman.name} scored a double run.")
        elif action == "boundary":
            runs = random.choice([4, 6])
            self.current_batsman.runs += runs
            self.score[self.innings - 1] += runs
            self.update_gui(f"{self.current_batsman.name} scored {runs} runs.")
        elif action == "out":
            self.wickets[self.innings - 1] += 1
            self.update_gui(f"{self.current_batsman.name} out.")
        
        self.update_score(self.score[0], self.wickets[0], self.score[1], self.wickets[1], self.current_over)
        
        # Check if second team has surpassed the first team's score + 1
        if self.innings == 2 and self.score[1] > self.score[0]:
            self.update_gui(f"Team 2 wins by {10 - self.wickets[1]} wickets.")
            self.update_gui("Game over.")
            self.play_over_button.config(state=tk.DISABLED)
            return False
        return True
    
    def play_over(self):
        for ball in range(6):
            if not self.play_ball():
                return False

            self.update_gui(f"Current score: {self.score[self.innings - 1]}/{self.wickets[self.innings - 1]}")

            if self.wickets[self.innings - 1] >= 10:
                self.update_gui("All players are out")
                return False
        return True
    
    def start_game(self):
        self.innings = 1
        self.current_over = 0
        self.current_batsman = Batsman("Batsman " + str(self.innings))
        self.current_bowler = Bowler("Bowler " + str(self.innings))
        self.update_gui("Game started.")
        self.update_score(0, 0, 0, 0, 0)
    
    def play_next_over(self):
        if self.current_over < self.overs:
            self.current_over += 1
            self.update_gui(f"Over {self.current_over}")
            if not self.play_over():
                self.end_innings()
        else:
            self.end_innings()
    
    def end_innings(self):
        self.update_gui(f"End of Innings {self.innings}. Final Score: {self.score[self.innings - 1]}/{self.wickets[self.innings - 1]}")
        
        if self.innings == 1:
            self.innings = 2
            self.current_over = 0
            self.current_batsman = Batsman("Batsman " + str(self.innings))
            self.current_bowler = Bowler("Bowler " + str(self.innings))
            self.update_gui("Starting second innings.")
            self.update_score(self.score[0], self.wickets[0], 0, 0, 0)
        else:
            if self.score[0] > self.score[1]:
                self.update_gui(f"Team 1 wins by {self.score[0] - self.score[1]} runs.")
            else:
                self.update_gui(f"Team 2 wins by {10 - self.wickets[1]} wickets.")
            self.update_gui("Game over.")
            self.play_over_button.config(state=tk.DISABLED)

class CricketGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cricket Game")

        # Create frames for scores
        self.frame_scores = tk.Frame(root)
        self.frame_scores.pack()

        # Create labels for team 1's scores
        self.team1_label = tk.Label(self.frame_scores, text="Team 1")
        self.team1_label.grid(row=0, column=0)

        self.team1_score_label = tk.Label(self.frame_scores, text="Score: 0")
        self.team1_score_label.grid(row=1, column=0)

        self.team1_wickets_label = tk.Label(self.frame_scores, text="Wickets: 0")
        self.team1_wickets_label.grid(row=2, column=0)

        # Create labels for team 2's scores
        self.team2_label = tk.Label(self.frame_scores, text="Team 2")
        self.team2_label.grid(row=0, column=1)

        self.team2_score_label = tk.Label(self.frame_scores, text="Score: 0")
        self.team2_score_label.grid(row=1, column=1)

        self.team2_wickets_label = tk.Label(self.frame_scores, text="Wickets: 0")
        self.team2_wickets_label.grid(row=2, column=1)

        # Create label for overs
        self.overs_label = tk.Label(root, text="Overs: 0")
        self.overs_label.pack()

        self.text = tk.Text(root, height=20, width=50)
        self.text.pack()

        self.start_button = tk.Button(root, text="Start Game", command=self.start_game)
        self.start_button.pack()

        self.play_over_button = tk.Button(root, text="Play Over", command=self.play_over, state=tk.DISABLED)
        self.play_over_button.pack()

    def update_gui(self, message):
        self.text.insert(tk.END, message + "\n")
        self.text.see(tk.END)

    def update_score(self, team1_score, team1_wickets, team2_score, team2_wickets, overs):
        self.team1_score_label.config(text=f"Score: {team1_score}")
        self.team1_wickets_label.config(text=f"Wickets: {team1_wickets}")
        self.team2_score_label.config(text=f"Score: {team2_score}")
        self.team2_wickets_label.config(text=f"Wickets: {team2_wickets}")
        self.overs_label.config(text=f"Overs: {overs}")

    def start_game(self):
        self.team1 = [Batsman(f"Batsman{i + 1}") for i in range(11)]
        self.team2 = [Bowler(f"Bowler{i + 1}") for i in range(11)]
        self.overs = 2

        self.game = CricketGame(self.team1, self.team2, self.overs, self.update_gui, self.update_score)
        self.game.start_game()

        self.play_over_button.config(state=tk.NORMAL)

    def play_over(self):
        self.game.play_next_over()

def main():
    root = tk.Tk()
    app = CricketGameGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
