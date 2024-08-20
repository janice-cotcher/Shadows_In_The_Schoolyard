# Shadows in the Schoolyard

## Project Overview

"Shadows in the Schoolyard" is an interactive text-based adventure game developed as an example for the Computer Science 30 curriculum. This game puts players in the role of Veronica "Ronnie" Malone, a teenage private investigator, as she and her friends unravel a mysterious disappearance and confront supernatural forces in their town.

## Game Features

- Text-based interface with typewriter-style text display
- Multiple locations to explore, each with various rooms and characters
- Inventory system for collecting and using items
- Puzzle-solving elements, including a cipher to decode
- Decision-making that affects the game's progression
- Three distinct acts, each with increasing complexity and stakes

## Educational Context

This project aligns with several key outcomes from the Saskatchewan Computer Science 30 curriculum:

### CS30-CP1: Explore computer programming concepts and constructs

- The game demonstrates the use of variables, data types, control structures, and functions.
- Object-oriented programming concepts are applied through the use of classes for locations, rooms, and inventory items.

### CS30-CP2: Extend understanding of procedural programming and modular design

- The game is structured into multiple Python files (e.g., project.py, map.py, inventory.py) to demonstrate modular design.
- Functions are used extensively to handle different game actions and locations.

### CS30-FP1: Explore additional areas of emphasis in computer science

- The project incorporates file I/O for reading and writing game data (e.g., CSV files for priest information).
- Basic cryptography concepts are introduced through the cipher puzzle.

### CS30-FP2: Design, build and evaluate a significant computer science project

- The game represents a comprehensive project that combines multiple programming concepts and techniques.
- It includes user input validation, error handling, and a test suite for quality assurance.

## Requirements

The project dependencies are listed in the `requirements.txt` file. To install these dependencies:

1. Ensure you have Python 3.x and pip installed on your system.
2. Navigate to the project directory in your terminal or command prompt.
3. Run the following command:

   ```
   pip install -r requirements.txt
   ```

This will install all the necessary packages to run the game and its tests.

## How to Run the Game

1. Ensure you have installed the required dependencies (see Requirements section).
2. Navigate to the project directory in your terminal or command prompt.
3. Run the game using the command: `python project.py`

## Testing

The project includes a comprehensive test suite (test_project.py) to ensure the game's functionality. To run the tests:

1. Ensure you have installed the required dependencies, which include pytest.
2. In the project directory, run the command: `pytest test_project.py`

## Future Enhancements

- Implement a save/load game feature
- Add more complex puzzles and branching narratives
- Incorporate simple ASCII art for visual elements
- Develop a graphical user interface (GUI) version of the game

## Conclusion

"Shadows in the Schoolyard" not only provides an engaging gaming experience but also serves as a practical application of key computer science concepts. Through its development, students can gain hands-on experience with programming constructs, software design principles, and project management skills essential for success in computer science.