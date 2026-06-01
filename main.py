import tkinter as tk
import random

# 1. Initialize the Main Window
root = tk.Tk()
root.title("Catch the Cat - Avoid the Hazards!")
root.resizable(False, False)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# 2. Create the Game Canvas
canvas = tk.Canvas(root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, bg="black")
canvas.pack()

# 3. Game Variables
player_x, player_y = 400, 300
player_speed = 25
score = 0
game_active = True  # Tracks if the game is running or over

cat_x = random.randint(50, SCREEN_WIDTH - 50)
cat_y = random.randint(50, SCREEN_HEIGHT - 50)

# 4. Obstacle Setup (Slower Bouncing Hazards)
obstacles = []
num_obstacles = 3
obstacle_size = 25

for i in range(num_obstacles):
    obs_x = random.randint(100, SCREEN_WIDTH - 100)
    obs_y = random.randint(100, SCREEN_HEIGHT - 100)
    
    # CHANGED: Lower numbers (1.5 to 2.5) make the obstacles move much slower
    dx = random.choice([-2.5, -1.5, 1.5, 2.5])
    dy = random.choice([-2.5, -1.5, 1.5, 2.5])
    
    # Draw the obstacle as a bright neon red box
    obj = canvas.create_rectangle(obs_x, obs_y, obs_x + obstacle_size, obs_y + obstacle_size, fill="#ff1744", outline="")
    obstacles.append([obs_x, obs_y, dx, dy, obj])

# 5. Drawing the Player (Mario Style)
def draw_player(x, y):
    canvas.delete("player_sprite") 
    canvas.create_rectangle(x+5, y+15, x+35, y+40, fill="#0d47a1", outline="", tags="player_sprite") # Body
    canvas.create_rectangle(x, y+15, x+5, y+30, fill="#d32f2f", outline="", tags="player_sprite")   # Arms
    canvas.create_rectangle(x+35, y+15, x+40, y+30, fill="#d32f2f", outline="", tags="player_sprite")
    canvas.create_oval(x+10, y+5, x+30, y+22, fill="#ffcc80", outline="", tags="player_sprite")     # Head
    canvas.create_rectangle(x+8, y, x+32, y+8, fill="#d32f2f", outline="", tags="player_sprite")    # Cap
    canvas.create_rectangle(x+5, y+6, x+35, y+10, fill="#d32f2f", outline="", tags="player_sprite")

# 6. Drawing the Cat
def draw_cat(x, y):
    canvas.delete("cat_sprite") 
    canvas.create_line(x+30, y+20, x+42, y+5, fill="#ffb74d", width=4, tags="cat_sprite") # Tail
    canvas.create_oval(x, y+10, x+32, y+30, fill="#ffb74d", outline="", tags="cat_sprite") # Body
    canvas.create_oval(x+15, y+2, x+32, y+18, fill="#ffb74d", outline="", tags="cat_sprite") # Head
    canvas.create_polygon(x+16, y+4, x+22, y-4, x+24, y+4, fill="#e65100", tags="cat_sprite") # Ears
    canvas.create_polygon(x+24, y+4, x+30, y-4, x+32, y+4, fill="#e65100", tags="cat_sprite")
    canvas.create_oval(x+21, y+5, x+25, y+9, fill="white", tags="cat_sprite") # Eyes
    canvas.create_oval(x+26, y+5, x+30, y+9, fill="white", tags="cat_sprite")
    canvas.create_oval(x+22, y+6, x+24, y+8, fill="black", tags="cat_sprite")
    canvas.create_oval(x+27, y+6, x+29, y+8, fill="black", tags="cat_sprite")

# Initial Render
draw_player(player_x, player_y)
draw_cat(cat_x, cat_y)

# Scoreboard text
score_text = canvas.create_text(60, 20, text=f"Score: {score}", fill="#ffeb3b", font=("Arial", 16, "bold"))

# 7. Function to Teleport Cat
def move_cat():
    global cat_x, cat_y
    cat_x = random.randint(40, SCREEN_WIDTH - 40)
    cat_y = random.randint(40, SCREEN_HEIGHT - 40)
    draw_cat(cat_x, cat_y)

# 8. Main Game Loop
def update_game():
    global score, game_active
    
    # If a collision already caused a Game Over, stop updating entirely
    if not game_active:
        return

    # Move and bounce obstacles
    for obs in obstacles:
        x, y, dx, dy, obj = obs
        
        x += dx
        y += dy
        
        if x <= 0 or x >= SCREEN_WIDTH - obstacle_size:
            dx = -dx
        if y <= 0 or y >= SCREEN_HEIGHT - obstacle_size:
            dy = -dy
            
        obs[0], obs[1], obs[2], obs[3] = x, y, dx, dy
        canvas.coords(obj, x, y, x + obstacle_size, y + obstacle_size)
        
        # CHANGED: Collision Detection for GAME OVER
        # If an obstacle hits the player's coordinate box area:
        if abs((player_x + 20) - (x + obstacle_size/2)) < 28 and abs((player_y + 20) - (y + obstacle_size/2)) < 28:
            game_active = False
            # Display big red Game Over text right in the middle
            canvas.create_text(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 
                               text="GAME OVER", fill="#ff1744", 
                               font=("Arial", 40, "bold"))
            canvas.create_text(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50, 
                               text=f"Final Score: {score}", fill="white", 
                               font=("Arial", 20))
            return # Exit the game loop completely

    # Collision Check: Player catching the Cat
    if abs((player_x + 20) - (cat_x + 16)) < 35 and abs((player_y + 20) - (cat_y + 15)) < 35:
        score += 1
        canvas.itemconfig(score_text, text=f"Score: {score}")
        move_cat()
        
    root.after(16, update_game)

# 9. Keyboard Controls
def move_player(event):
    global player_x, player_y
    
    # CHANGED: If the game is over, ignore keyboard presses
    if not game_active:
        return
        
    if event.keysym == "Left" and player_x > 0:
        player_x -= player_speed
    elif event.keysym == "Right" and player_x < SCREEN_WIDTH - 40:
        player_x += player_speed
    elif event.keysym == "Up" and player_y > 0:
        player_y -= player_speed
    elif event.keysym == "Down" and player_y < SCREEN_HEIGHT - 40:
        player_y += player_speed
        
    draw_player(player_x, player_y)

# 10. Bind Keys and Boot Engine
root.bind("<Left>", move_player)
root.bind("<Right>", move_player)
root.bind("<Up>", move_player)
root.bind("<Down>", move_player)

root.after(16, update_game)
root.mainloop()