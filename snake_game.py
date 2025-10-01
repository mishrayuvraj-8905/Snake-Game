import turtle
import time
import random
import sqlite3

# Database setup for high score
conn = sqlite3.connect('snake_highscore.db')
cursor = conn.cursor()
cursor.execute(
    '''CREATE TABLE IF NOT EXISTS scores (id INTEGER PRIMARY KEY, score INTEGER)'''
)
conn.commit()

def get_high_score():
    cursor.execute('SELECT MAX(score) FROM scores')
    result = cursor.fetchone()
    return result[0] if result[0] is not None else 0

def update_high_score(score):
    current_high = get_high_score()
    if score > current_high:
        cursor.execute('INSERT INTO scores (score) VALUES (?)', (score,))
        conn.commit()

# Game window setup
window = turtle.Screen()
window.title("Python Turtle Snake Game")
window.bgcolor("black")
window.setup(width=600, height=600)
window.tracer(0)  # Turns off the screen updates for smooth animation

# Snake head
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("white")
head.penup()
head.goto(0, 0)
head.direction = "stop"

# Food
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0, 100)

segments = []

# Score
score = 0
high_score = get_high_score()

# Pen for score display
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("cyan")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Courier", 24, "normal"))


# Functions to control the snake
def go_up():
    if head.direction != "down":
        head.direction = "up"
        
def go_down():
    if head.direction != "up":
        head.direction = "down"
        
def go_left():
    if head.direction != "right":
        head.direction = "left"
        
def go_right():
    if head.direction != "left":
        head.direction = "right"
        

def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)
        
    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)
        
    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)
        
    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)


# Keyboard bindings
window.listen()
window.onkeypress(go_up, "Up")
window.onkeypress(go_down, "Down")
window.onkeypress(go_left, "Left")
window.onkeypress(go_right, "Right")


# Main game loop
def game_loop():
    global score, high_score
    
    window.update()
    
    # Check for collision with border
    if (
        head.xcor() > 290 or head.xcor() < -290 or
        head.ycor() > 290 or head.ycor() < -290
    ):
        time.sleep(1)
        head.goto(0, 0)
        head.direction = "stop"
        
        # Hide segments
        for segment in segments:
            segment.goto(1000, 1000)
        segments.clear()
        
        # Update high score in DB
        update_high_score(score)
        
        score = 0
        pen.clear()
        high_score = get_high_score()
        pen.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Courier", 24, "normal"))
    
    # Check for collision with food
    if head.distance(food) < 20:
        # Move food to random spot
        x = random.randint(-14, 14) * 20
        y = random.randint(-14, 14) * 20
        food.goto(x, y)
        
        # Add new segment
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("grey")
        new_segment.penup()
        segments.append(new_segment)
        
        # Increase score
        score += 10
        if score > high_score:
            high_score = score
        
        pen.clear()
        pen.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Courier", 24, "normal"))
    
    # Move snake segments in reverse order
    for i in range(len(segments) - 1, 0, -1):
        x = segments[i - 1].xcor()
        y = segments[i - 1].ycor()
        segments[i].goto(x, y)
    
    # Move first segment to head's old position
    if segments:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x, y)
    
    move()
    
    # Check for collision with body segments
    for segment in segments:
        if segment.distance(head) < 20:
            time.sleep(1)
            head.goto(0, 0)
            head.direction = "stop"
            
            for segment in segments:
                segment.goto(1000, 1000)
            segments.clear()
            
            update_high_score(score)
            
            score = 0
            pen.clear()
            high_score = get_high_score()
            pen.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Courier", 24, "normal"))
            break
    
    # Repeat the game loop every 100 ms for smooth gameplay
    window.ontimer(game_loop, 100)

# Start the game loop
game_loop()

window.mainloop()

# Close the DB connection on exit
conn.close()
