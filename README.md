# Retro Chase Game (Python & Tkinter)

A lightweight, standalone 2D arcade game built entirely using Python's native GUI framework. The player controls a Mario-inspired character to chase an orange cat while dodging moving, bouncing speed hazards.

## Features
* **Dynamic Frame Rate Loop:** Built using asynchronous time handlers (`root.after`) running at 60 frames per second.
* **Algorithmic Asset Generation:** To keep the game 100% lightweight and dependency-free, character and enemy sprites are built algorithmically using multi-layered vector geometric polygons.
* **Collision Engine:** Integrates custom absolute distance bounding-box checks to handle catch triggers and game-over states instantly.

## How to Play and Run
No external installations or pip packages required!
1. Clone this repository or download the `main.py` file.
2. Run the file using your terminal:
```bash
   python main.py
