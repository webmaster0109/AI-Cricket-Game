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
    def __init__(self, team1, team2, overs):
        self.team1 = team1
        self.team2 = team2
        self.overs = overs
        self.current_batsman = None
        self.current_bowler = None
        self.ai = AIOpponent()
        self.innings = 1
        self.score = [0, 0]
        self.wickets = [0, 0]
    
    def play_ball(self):
        action = self.ai.decide_action()
        print(f"AI chose to: {action}")

        if action == "defend":
            print(f"{self.current_batsman.name} defended the ball.")
        elif action == "attack":
            runs = random.choice([0, 1, 2, 3, 4, 6])
            self.current_batsman.runs += runs
            self.score[self.innings - 1] += runs
            print(f"{self.current_batsman.name} scored {runs} runs.")
        elif action == "single":
            self.current_batsman.runs += 1
            self.score[self.innings - 1] += 1
            print(f"{self.current_batsman.name} scored a single run.")
        elif action == "double":
            self.current_batsman.runs += 2
            self.score[self.innings - 1] += 2
            print(f"{self.current_batsman.name} scored a double runs.")
        elif action == "boundary":
            runs = random.choice([4, 6])
            self.current_batsman.runs += runs
            self.score[self.innings - 1] += runs
            print(f"{self.current_batsman.name} scored {runs} runs.")
        elif action == "out":
            self.wickets[self.innings - 1] += 1
            print(f"{self.current_batsman.name} out.")
    
    def play_over(self):
        for ball in range(6):
            self.play_ball()
            print(f"Current score: {self.score[self.innings - 1]}/{self.wickets[self.innings - 1]}")

            if self.wickets[self.innings - 1] >= 10:
                print("All players are out")
                break
    
    def start_game(self):
        for innings in range(2):
            self.innings = innings + 1
            self.current_batsman = Batsman("Batsman " + str(self.innings))
            self.current_bowler = Bowler("Bowler " + str(self.innings))
            for over in range(self.overs):
                print(f"Over {over + 1}")
                self.play_over()
                if self.wickets[self.innings - 1] >= 10:
                    break
            print(f"End of Innings {self.innings}. Final Score: {self.score[self.innings - 1]}/{self.wickets[self.innings - 1]}")
        
        if self.score[0] > self.score[1]:
            print(f"{self.team1} wins by {self.score[0] - self.score[1]} runs.")
        else:
            print(f"{self.team2} wins by {self.score[1] - self.score[0]} runs.")

def main():
    team1 = [Batsman(f"Batsman{i + 1}") for i in range(11)]
    team2 = [Bowler(f"Bowler{i + 1}") for i in range(11)]
    overs = 2

    game = CricketGame(team1, team2, overs)
    game.start_game()

if __name__ == "__main__":
    main()