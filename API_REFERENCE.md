# DSA Learning Adventure - API Reference

## Core Classes

### DSAGame Class

Main game controller that manages the overall game state and flow.

#### Constructor
```python
DSAGame()
```
Initializes the game with default settings, loads high scores, and sets up the display.

#### Key Methods

##### `run()`
Main game loop that handles events, updates game state, and renders frames.
- **Returns**: None
- **Side Effects**: Runs until game is closed

##### `handle_menu_events(event)`
Processes input events when in menu state.
- **Parameters**: `event` (pygame.Event) - Input event to process
- **Returns**: None

##### `handle_level_select_events(event)`
Processes input events when in level selection state.
- **Parameters**: `event` (pygame.Event) - Input event to process
- **Returns**: None

##### `handle_game_over_events(event)`
Processes input events when in game over state.
- **Parameters**: `event` (pygame.Event) - Input event to process
- **Returns**: None

##### `start_level(level_num)`
Initializes and starts a specific level.
- **Parameters**: `level_num` (int) - Level number to start (1-4)
- **Returns**: None
- **Side Effects**: Changes game state to PLAYING

##### `add_high_score(name, score)`
Adds a new high score to the leaderboard.
- **Parameters**: 
  - `name` (str) - Player name
  - `score` (int) - Score achieved
- **Returns**: None
- **Side Effects**: Updates high_scores.txt file

##### `draw_menu()`
Renders the main menu screen.
- **Returns**: None
- **Side Effects**: Draws to screen surface

##### `draw_level_select()`
Renders the level selection screen.
- **Returns**: None
- **Side Effects**: Draws to screen surface

##### `draw_scoreboard()`
Renders the high scores screen.
- **Returns**: None
- **Side Effects**: Draws to screen surface

##### `draw_game_over()`
Renders the game over screen.
- **Returns**: None
- **Side Effects**: Draws to screen surface

#### Properties

##### `state`
Current game state (GameState enum).
- **Type**: GameState
- **Values**: MENU, LEVEL_SELECT, PLAYING, GAME_OVER, SCOREBOARD

##### `score`
Current total score across all levels.
- **Type**: int
- **Range**: 0 to unlimited

##### `high_scores`
List of high score entries.
- **Type**: List[Tuple[str, int]]
- **Format**: [(name, score), ...]
- **Max Length**: 10 entries

---

### BaseLevel Class (Abstract)

Abstract base class for all game levels.

#### Constructor
```python
BaseLevel(time_limit)
```
- **Parameters**: `time_limit` (int) - Time limit in seconds

#### Abstract Methods

##### `handle_event(event)`
Process player input for this level.
- **Parameters**: `event` (pygame.Event) - Input event
- **Returns**: None
- **Must Override**: Yes

##### `update()`
Update level logic and check win/lose conditions.
- **Returns**: str - "playing", "completed", or "failed"
- **Must Override**: Yes

##### `draw(screen)`
Render level graphics.
- **Parameters**: `screen` (pygame.Surface) - Display surface
- **Returns**: None
- **Must Override**: Yes

#### Implemented Methods

##### `get_remaining_time()`
Calculate remaining time for the level.
- **Returns**: float - Seconds remaining (0 if time up)

##### `is_time_up()`
Check if time limit has been reached.
- **Returns**: bool - True if time is up

##### `get_score()`
Calculate final score including time bonus.
- **Returns**: int - Total score for level

##### `draw_hud(screen)`
Draw heads-up display with time and score.
- **Parameters**: `screen` (pygame.Surface) - Display surface
- **Returns**: None

#### Properties

##### `time_limit`
Time limit for the level in seconds.
- **Type**: int

##### `score`
Current score for this level.
- **Type**: int

##### `completed`
Whether the level has been completed.
- **Type**: bool

##### `failed`
Whether the level has failed.
- **Type**: bool

---

### ArrayLevel Class

Level 1: Array manipulation and linear search.

#### Constructor
```python
ArrayLevel()
```
Creates array level with random array and target.

#### Methods

##### `generate_new_target()`
Selects a new target element from the array.
- **Returns**: None
- **Side Effects**: Updates target and resets attempts

##### `check_selection()`
Validates player's current selection.
- **Returns**: None
- **Side Effects**: Updates score and attempts

#### Properties

##### `array`
Array of integers to search through.
- **Type**: List[int]
- **Length**: 10 elements
- **Range**: 1-50

##### `target`
Current target value to find.
- **Type**: int

##### `selected_index`
Currently selected array index.
- **Type**: int
- **Range**: 0 to len(array)-1

##### `attempts`
Number of selection attempts made.
- **Type**: int
- **Max**: 3 per target

---

### StackLevel Class

Level 2: Stack operations and sequence building.

#### Constructor
```python
StackLevel()
```
Creates stack level with random target sequence.

#### Methods

##### `push(value)`
Push a value onto the stack.
- **Parameters**: `value` (int) - Value to push (1-9)
- **Returns**: None
- **Side Effects**: Updates stack and operations log

##### `pop()`
Pop the top value from the stack.
- **Returns**: None
- **Side Effects**: Updates stack and operations log

##### `check_progress()`
Check if stack matches target sequence.
- **Returns**: None
- **Side Effects**: Updates score and progress tracking

##### `reset_progress()`
Reset progress tracking when stack is modified.
- **Returns**: None

#### Properties

##### `stack`
Current stack contents.
- **Type**: List[int]
- **Order**: Bottom to top

##### `target_sequence`
Sequence that must be built on stack.
- **Type**: List[int]
- **Length**: 5 elements
- **Range**: 1-9

##### `operations`
Log of recent operations.
- **Type**: List[str]
- **Format**: ["PUSH 1", "POP 2", ...]

##### `sequence_matches`
Indices of matched sequence elements.
- **Type**: List[int]

---

### QueueLevel Class

Level 3: Queue management and FIFO operations.

#### Constructor
```python
QueueLevel()
```
Creates queue level with customer processing goal.

#### Methods

##### `add_customer()`
Add a new customer to the queue.
- **Returns**: None
- **Side Effects**: Increments customer_id, adds to queue

##### `process_customer()`
Process the next customer in queue (FIFO).
- **Returns**: None
- **Side Effects**: Removes from queue, adds to processed

#### Properties

##### `queue`
Current queue of customers.
- **Type**: List[int]
- **Order**: First to last (FIFO)
- **Max Length**: 15 (to prevent overflow)

##### `processed`
List of processed customers.
- **Type**: List[int]

##### `customer_id`
Next customer ID to assign.
- **Type**: int
- **Auto-increment**: Yes

##### `target_processed`
Number of customers to process for completion.
- **Type**: int
- **Default**: 10

---

### BinarySearchLevel Class

Level 4: Binary search algorithm implementation.

#### Constructor
```python
BinarySearchLevel()
```
Creates binary search level with sorted array and target.

#### Methods

##### `search_left()`
Search the left half of current range.
- **Returns**: None
- **Side Effects**: Updates search range and comparisons

##### `search_right()`
Search the right half of current range.
- **Returns**: None
- **Side Effects**: Updates search range and comparisons

##### `check_found()`
Check if current middle element is the target.
- **Returns**: None
- **Side Effects**: Updates found status and score

##### `update_mid()`
Recalculate middle index for current range.
- **Returns**: None

#### Properties

##### `array`
Sorted array to search through.
- **Type**: List[int]
- **Length**: 15 elements
- **Range**: 1-100 (sorted)

##### `target`
Value to find in the array.
- **Type**: int

##### `left`
Left boundary of search range.
- **Type**: int

##### `right`
Right boundary of search range.
- **Type**: int

##### `mid`
Current middle index.
- **Type**: int

##### `comparisons`
Number of comparisons made.
- **Type**: int
- **Max**: 4 (log₂(15))

##### `found`
Whether target has been found.
- **Type**: bool

---

## Utility Functions

### `get_level_instance(level_num)`
Factory function to create level instances.
- **Parameters**: `level_num` (int) - Level number (1-4)
- **Returns**: BaseLevel - Appropriate level instance
- **Raises**: ValueError - If level number is invalid

---

## Constants

### Colors
```python
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
```

### Display Settings
```python
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60
```

### Game States
```python
class GameState(Enum):
    MENU = 1
    LEVEL_SELECT = 2
    PLAYING = 3
    GAME_OVER = 4
    SCOREBOARD = 5
```

---

## Event Handling

### Keyboard Controls

#### Global Controls
- `ESC` - Return to previous screen/main menu
- `Q` - Quit game (from main menu)

#### Menu Controls
- `SPACE` - Start game
- `S` - View scoreboard

#### Level Selection
- `1-4` - Select level

#### Array Level
- `LEFT/RIGHT` - Navigate array
- `SPACE` - Select element

#### Stack Level
- `1-9` - Push number
- `SPACE` - Pop from stack

#### Queue Level
- `A` - Add customer
- `SPACE` - Process customer

#### Binary Search Level
- `LEFT` - Target is smaller
- `RIGHT` - Target is larger
- `SPACE` - Found target

#### Game Over
- `R` - Retry level
- `SPACE` - Level select
- `ESC` - Main menu

---

## File I/O

### High Scores File (`high_scores.txt`)
Format: `name,score` per line
```
PLAYER,1500
CPU,1000
RETRO,800
```

### Loading High Scores
```python
def load_high_scores(self):
    try:
        with open('high_scores.txt', 'r') as f:
            scores = []
            for line in f:
                name, score = line.strip().split(',')
                scores.append((name, int(score)))
            return sorted(scores, key=lambda x: x[1], reverse=True)[:10]
    except FileNotFoundError:
        return [("CPU", 1000), ("PLAYER", 800), ("RETRO", 600)]
```

### Saving High Scores
```python
def save_high_scores(self):
    with open('high_scores.txt', 'w') as f:
        for name, score in self.high_scores:
            f.write(f"{name},{score}\n")
```

---

## Error Handling

### Common Exceptions
- `FileNotFoundError` - High scores file missing (handled gracefully)
- `ValueError` - Invalid level number in factory function
- `pygame.error` - Display or audio initialization issues

### Error Recovery
- Missing high scores file creates default scores
- Invalid input events are ignored
- Level creation failures return to menu

---

## Performance Considerations

### Frame Rate Management
- Target: 60 FPS
- Use `pygame.time.Clock.tick(60)` for consistent timing

### Memory Usage
- Minimal texture loading
- Reuse pygame surfaces where possible
- Clean up resources on level transitions

### Optimization Tips
- Limit particle effects count
- Use efficient collision detection
- Minimize string operations in render loop

---

This API reference provides detailed information about all classes, methods, and functions in the DSA Learning Adventure game. Use this as a guide for understanding the codebase and extending functionality.
