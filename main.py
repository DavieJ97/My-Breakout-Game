import turtle
import json
import random

class Break_Through_Game:
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.title("BreakThough Game(clone)")
        self.screen.tracer(0)
        self.screen.cv._rootwindow.state("zoomed")
        self.screen.bgcolor("black")
        self.screen.screensize(800, 600)
        with open("highscore.json", "r") as file:
            data = json.load(file) 
        self.high_score = data["Highscore"]
        self.lives = 3
        self.score = 0
        self.ball_speed = 10.0  # Initial speed multiplier
        self.speed_increment = 0.1  # Amount to increase the speed
        self.max_speed = 20.0  # Maximum speed limit
        self.countdown_turtle = turtle.Turtle()
        self.countdown_turtle.color("white")
        self.countdown_turtle.penup()
        self.countdown_turtle.hideturtle()
        self.draw_border()
        self.draw_lives()
        self.make_paddle()
        self.screen.listen()
        self.blocks = {}
        self.screen.update()
        self.welcome_screen()
    

    def countdown_timer(self):
        self.countdown_turtle.goto(0, 0)  # Center position
        
        self.countdown_value = 3  # Set the starting countdown value
        
        self.update_countdown()

    def update_countdown(self):
        if self.countdown_value > 0:
            self.countdown_turtle.clear()
            self.countdown_turtle.write(
                f"{self.countdown_value}", align="center", font=("Courier", 50, "bold")
            )
            self.countdown_value -= 1
            self.screen.ontimer(self.update_countdown, 1000)  # Call this method again after 1 second
        else:
            self.countdown_turtle.clear()
            self.playing = True
            self.make_ball()

    def welcome_screen(self):
        self.welcome_turtle = turtle.Turtle()
        self.welcome_turtle.color("white")
        self.welcome_turtle.pendown()
        self.welcome_turtle.write(f"Welcome\nStart\n", align="center", font=("Courier", 50, "bold"))
        self.welcome_turtle.write(f"Space to start", align="center", font=("Courier", 30, "bold"))
        self.welcome_turtle.penup()
        self.screen.onkeypress(self.start_game, "space")
        
    def random_direction(self):
        self.rand_dir = random.randint(30, 150)
        if self.rand_dir < 75 and self.rand_dir > 105:
            self.random_direction()
    
    def start_game(self):
        self.welcome_turtle.clear()
        self.welcome_turtle.hideturtle()
        self.create_all_blocks()
        self.countdown_timer()
        

    def create_all_blocks(self):
        self.create_block_row(250, "pink")
        self.create_block_row(200, "#CBC3E3")
        self.create_block_row(150, "aqua")

    def create_block_row(self, y, color):
        start_x = -325  # Starting x-coordinate for the row
        block_count = 7  # Number of blocks in the row
        
        for i in range(block_count):
            block = turtle.Turtle()
            block.shape("square")
            block.color(color)
            block.shapesize(stretch_wid=2, stretch_len=5)
            block.penup()
            
            # Calculate x-coordinate for each block
            x = start_x + i * 110  # Adjust spacing based on block size
            block.goto(x, y)
            
            block_id = f"block_{i+1}_{color}"  # Create a unique key for each block
            self.blocks[block_id] = {
                "turtle": block,
                "x": x, 
                "y": y, 
                "color": color
                }
        
    def make_paddle(self):
        self.paddle = turtle.Turtle()
        self.paddle.shape("square") 
        self.paddle.color("#FFFFC5")
        self.paddle.shapesize(stretch_wid=1, stretch_len=10)
        self.paddle.speed(0)
        self.paddle.penup()
        self.paddle.goto(0, -270) 

    def move_left(self):
        x = self.paddle.xcor()
        if x > -290:
            self.paddle.setx(x - 20)
    
    def move_right(self):
        x = self.paddle.xcor()
        if x < 290:
            self.paddle.setx(x + 20)

    def make_ball(self):
        self.ball = turtle.Turtle()
        self.ball.shape('circle')
        self.ball.color("white")
        self.ball.speed(1)
        self.ball.penup()
        self.ball.setpos(0,0)
        self.random_direction()
        self.ball.setheading(self.rand_dir)
        self.move_ball()

    def draw_lives(self):
        self.scoreBoard = turtle.Turtle()
        self.scoreBoard.color("white")
        self.scoreBoard.speed(0)
        self.scoreBoard.penup() 
        self.scoreBoard.goto(-350, 300)
        self.scoreBoard.write(f"balls left: {self.lives}", align="left", font=("Courier", 20, "italic"))
        self.scoreBoard.goto(-20, 300)
        self.scoreBoard.write(f"Highscore: {self.high_score}", align="left", font=("Courier", 20, "italic"))
        self.scoreBoard.goto(250, 300)
        self.scoreBoard.write(f"score: {self.score}", align="left", font=("Courier", 20, "italic"))
        self.scoreBoard.hideturtle()
        if self.score % 5 == 0 and self.score > 0:  # Every 5 points
                self.ball_speed = min(self.ball_speed + self.speed_increment, self.max_speed)
                print(f"Current ball speed: {self.ball_speed}")

    def draw_border(self):
        border = turtle.Turtle()
        border.speed(0)
        border.color("white")
        border.pensize(3)
        border.penup()
        border.goto(-400, 300)  # Top-left corner
        border.pendown()
        for _ in range(2):
            if _ == 1:
                border.penup()
                border.forward(800) 
                border.right(90)
                border.pendown()
            else:
                border.forward(800) 
                border.right(90)    
            border.forward(600)  
            border.right(90)
        border.hideturtle()

    def move_forward(self):
        self.ball.forward(self.ball_speed)
            
    def move_ball(self):
        if self.playing:
            self.screen.onkeypress(self.move_left, "Left")
            self.screen.onkeypress(self.move_right, "Right")
            self.screen.update()
            self.move_forward()
            self.check_collisiion()
            self.screen.ontimer(self.move_ball, 15)
            
    def check_collisiion(self):
        x,y = self.ball.position()
        px, py = self.paddle.position()
        delete_block_id = ""
        for block_id, position in self.blocks.items():
            if x < position["x"] + 52 and x > position["x"] -52 and y < position["y"] + 30 and y > position["y"] -30:
                block = self.blocks[block_id]["turtle"] 
                block.hideturtle()
                delete_block_id = block_id
                if abs(x - (position["x"]+52)) > abs(y - (position["y"]+30)):  # Side collision
                    self.change_direction("side")
                else:  # Top or bottom collision
                    self.change_direction("top")
                self.score += 1
                self.scoreBoard.clear()
                self.draw_lives()
        if delete_block_id in self.blocks:
            del self.blocks[delete_block_id]
        if self.blocks == {}:
            self.ball.hideturtle()
            self.ball.goto(-500, -500)
            self.create_all_blocks()
            self.playing = False
            self.countdown_timer()
        if x > 390 or x < -390:
            self.change_direction("side")
        if y > 290:
            self.change_direction("top")
        if x < px + 100 and x > px - 100 and y < py + 20 and y > py - 20:
            self.change_direction("top")
        elif y < py - 20:
            self.lost_ball()
                  

    def change_direction(self, wall):
        if wall == "side":
            new_heading = 180 - self.ball.heading()  # Reflect horizontally
            self.ball.setheading(new_heading)
        elif wall == "top":
            new_heading = 360 - self.ball.heading()  # Reflect vertically
            self.ball.setheading(new_heading)


        
    def game_over(self):
        self.new_high_score()
        game_over_text = turtle.Turtle()
        game_over_text.color("white")
        game_over_text.write(f"GAME OVER\n", align="center", font=("Courier", 50, "bold"))
        game_over_text.write(f"Highscore: {self.high_score}", align="left", font=("Courier", 20, "italic"))
        game_over_text.hideturtle()



    def lost_ball(self):
        self.ball.hideturtle()
        self.playing = False
        if self.lives != 0:
            self.ball_speed = 10.0
            self.lives -= 1
            self.scoreBoard.clear()
            self.draw_lives()
            self.countdown_timer()
        else:
            self.game_over()

    def new_high_score(self):
        if self.score > self.high_score:
            data = {"Highscore": self.score}
            with open("highscore.json", "w") as file:
                json.dump(data, file)
            self.high_score = self.score
            



Break_Through_Game()
turtle.done()