# Galaga Remix

A modern remake of the classic Galaga arcade game built with Pygame.

## Description

Galaga Remix is a Python-based recreation of the iconic Galaga arcade game. It features:
- Smooth ship movement and rotation
- Mouse-controlled aiming
- Dynamic bullet trajectories
- Classic Galaga-style gameplay mechanics

## Prerequisites

- Python 3.6 or higher
- Pygame
- Git (for cloning the repository)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/GalagaRemixPygame.git
   cd GalagaRemixPygame
   ```

2. Set up a virtual environment:
   ```bash
   # Using venv (recommended)
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Or using conda
   conda create -n galaga python=3.8
   conda activate galaga
   ```

3. Install required packages:
   ```bash
   pip install pygame
   ```

## How to Play

1. Run the game:
   ```bash
   python main.py
   ```

2. Controls:
   - WASD: Move ship
   - Mouse: Aim
   - Left Click: Fire

## Project Structure

- `main.py`: Game entry point and main loop
- `ShipController.py`: Player ship movement and controls
- `BulletController.py`: Bullet creation and management
- `Sprites.py`: Base sprite class and utility functions
- `Constants.py`: Game configuration and constants
- `GameField.py`: Game state management

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License.