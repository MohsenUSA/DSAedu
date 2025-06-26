# Contributing to DSA Learning Adventure

Thank you for your interest in contributing to DSA Learning Adventure! This document provides guidelines and information for contributors.

## Table of Contents
1. [Getting Started](#getting-started)
2. [Development Setup](#development-setup)
3. [Contributing Guidelines](#contributing-guidelines)
4. [Code Standards](#code-standards)
5. [Adding New Levels](#adding-new-levels)
6. [Testing](#testing)
7. [Submitting Changes](#submitting-changes)
8. [Community Guidelines](#community-guidelines)

## Getting Started

### Ways to Contribute
- **Bug Reports**: Report issues and bugs
- **Feature Requests**: Suggest new features or improvements
- **Code Contributions**: Implement new features or fix bugs
- **Documentation**: Improve guides and documentation
- **Level Design**: Create new DSA learning levels
- **Testing**: Help test new features and find issues
- **UI/UX**: Improve visual design and user experience

### Before You Start
1. Check existing issues to avoid duplicates
2. Read through the documentation to understand the project
3. Set up the development environment
4. Run the test suite to ensure everything works

## Development Setup

### Prerequisites
- Python 3.7 or higher
- Git for version control
- Text editor or IDE (VS Code, PyCharm recommended)

### Setup Steps
```bash
# 1. Fork and clone the repository
git clone https://github.com/yourusername/DSAedu.git
cd DSAedu

# 2. Create virtual environment
python3 -m venv dsa_game_env
source dsa_game_env/bin/activate  # On Windows: dsa_game_env\Scripts\activate

# 3. Install dependencies
pip install pygame

# 4. Run tests to verify setup
python3 test_game.py

# 5. Run the game
./run_game.sh
```

### Development Tools
- **Linting**: Use `flake8` or `pylint` for code quality
- **Formatting**: Use `black` for consistent code formatting
- **Type Checking**: Use `mypy` for type hint validation

## Contributing Guidelines

### Issue Reporting
When reporting bugs or requesting features:

#### Bug Reports
```markdown
**Bug Description**
Clear description of the issue

**Steps to Reproduce**
1. Step one
2. Step two
3. Step three

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS: [e.g., macOS 12.0]
- Python Version: [e.g., 3.9.0]
- PyGame Version: [e.g., 2.6.1]

**Screenshots**
If applicable, add screenshots
```

#### Feature Requests
```markdown
**Feature Description**
Clear description of the proposed feature

**Educational Value**
How does this help users learn DSA concepts?

**Implementation Ideas**
Any thoughts on how to implement this

**Alternatives Considered**
Other approaches you've considered
```

### Pull Request Process
1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Make** your changes
4. **Test** your changes thoroughly
5. **Commit** with clear messages
6. **Push** to your fork
7. **Submit** a pull request

### Commit Message Format
```
type(scope): brief description

Longer description if needed

Fixes #issue-number
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(levels): add linked list level with traversal mechanics

fix(queue): resolve crash when processing empty queue

docs(api): update BaseLevel class documentation
```

## Code Standards

### Python Style Guide
Follow PEP 8 with these specific guidelines:

#### Naming Conventions
```python
# Classes: PascalCase
class ArrayLevel(BaseLevel):
    pass

# Functions and variables: snake_case
def handle_event(self, event):
    selected_index = 0

# Constants: UPPER_SNAKE_CASE
SCREEN_WIDTH = 1024
MAX_ATTEMPTS = 3

# Private methods: leading underscore
def _internal_method(self):
    pass
```

#### Documentation
```python
class NewLevel(BaseLevel):
    """
    Level N: Brief description of the level concept.
    
    This level teaches [DSA concept] through [game mechanics].
    Players learn [specific learning objectives].
    """
    
    def __init__(self):
        """Initialize level with default settings."""
        super().__init__(time_limit=60)
        # Implementation
    
    def handle_event(self, event):
        """
        Process player input events.
        
        Args:
            event (pygame.Event): Input event to process
        """
        # Implementation
```

#### Type Hints
```python
from typing import List, Tuple, Optional

def add_high_score(self, name: str, score: int) -> None:
    """Add a new high score entry."""
    pass

def get_high_scores(self) -> List[Tuple[str, int]]:
    """Return list of high score entries."""
    return self.high_scores
```

### Code Organization

#### File Structure
```python
# Imports
import pygame
import sys
from typing import List
from enum import Enum

# Constants
SCREEN_WIDTH = 1024
COLORS = {...}

# Classes
class GameClass:
    pass

# Functions
def utility_function():
    pass

# Main execution
if __name__ == "__main__":
    main()
```

#### Class Structure
```python
class LevelClass(BaseLevel):
    """Class docstring."""
    
    def __init__(self):
        """Constructor."""
        # Initialize parent
        super().__init__(time_limit)
        
        # Initialize attributes
        self.attribute = value
    
    # Public methods
    def public_method(self):
        """Public method docstring."""
        pass
    
    # Private methods
    def _private_method(self):
        """Private method docstring."""
        pass
    
    # Abstract method implementations
    def handle_event(self, event):
        """Handle input events."""
        pass
    
    def update(self):
        """Update game logic."""
        return "playing"
    
    def draw(self, screen):
        """Render graphics."""
        pass
```

## Adding New Levels

### Level Design Process
1. **Concept**: Choose a DSA concept to teach
2. **Mechanics**: Design interactive gameplay mechanics
3. **Difficulty**: Determine appropriate difficulty level
4. **Visual Design**: Plan graphics and animations
5. **Implementation**: Code the level
6. **Testing**: Verify educational value and fun factor

### Level Implementation Template
```python
class NewLevel(BaseLevel):
    """
    Level N: [DSA Concept] - [Brief Description]
    
    Learning Objectives:
    - Objective 1
    - Objective 2
    - Objective 3
    """
    
    def __init__(self):
        super().__init__(time_limit=60)  # Adjust time limit
        
        # Initialize level-specific data
        self.data_structure = []
        self.target = None
        self.player_actions = []
        
        # Generate level content
        self._generate_level()
    
    def _generate_level(self):
        """Generate random level content."""
        # Create random data, targets, etc.
        pass
    
    def handle_event(self, event):
        """Process player input."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self._handle_action()
            # Add other controls
    
    def _handle_action(self):
        """Process player action."""
        # Implement game mechanics
        # Update score based on correctness
        pass
    
    def update(self):
        """Update level state."""
        if self.is_time_up():
            return "failed"
        
        # Check win condition
        if self._check_completion():
            return "completed"
        
        return "playing"
    
    def _check_completion(self):
        """Check if level is completed."""
        # Implement completion logic
        return False
    
    def draw(self, screen):
        """Render level graphics."""
        screen.fill(BLACK)
        self.draw_hud(screen)
        
        # Draw instructions
        self._draw_instructions(screen)
        
        # Draw data structure visualization
        self._draw_data_structure(screen)
        
        # Draw player interface
        self._draw_interface(screen)
    
    def _draw_instructions(self, screen):
        """Draw level instructions."""
        # Implement instruction display
        pass
    
    def _draw_data_structure(self, screen):
        """Draw visual representation of data structure."""
        # Implement visualization
        pass
    
    def _draw_interface(self, screen):
        """Draw player interaction interface."""
        # Implement UI elements
        pass
```

### Registering New Levels
```python
# In levels.py - Add to factory function
def get_level_instance(level_num):
    if level_num == 1:
        return ArrayLevel()
    elif level_num == 2:
        return StackLevel()
    # ... existing levels
    elif level_num == 5:  # New level
        return NewLevel()
    else:
        raise ValueError(f"Level {level_num} not implemented yet!")

# In dsa_game.py - Add to level definitions
self.levels = {
    # ... existing levels
    5: {"name": "New Level Name", "time_limit": 60, "difficulty": "Medium"},
}
```

### Level Design Guidelines

#### Educational Principles
- **Clear Learning Objective**: Each level should teach one main concept
- **Progressive Difficulty**: Build on previous knowledge
- **Immediate Feedback**: Show results of actions immediately
- **Visual Learning**: Use graphics to illustrate concepts
- **Active Learning**: Require player interaction, not passive observation

#### Gameplay Mechanics
- **Intuitive Controls**: Easy to learn, hard to master
- **Fair Challenge**: Difficult but achievable
- **Multiple Attempts**: Allow learning from mistakes
- **Time Pressure**: Create urgency without frustration
- **Score Incentives**: Reward efficient solutions

#### Visual Design
- **Consistent Style**: Match existing retro aesthetic
- **High Contrast**: Ensure accessibility
- **Clear Feedback**: Visual responses to all actions
- **Animated Elements**: Bring data structures to life
- **Color Coding**: Use consistent color meanings

## Testing

### Test Categories

#### Unit Tests
Test individual components in isolation:
```python
def test_array_level_creation():
    """Test ArrayLevel initialization."""
    level = ArrayLevel()
    assert len(level.array) == 10
    assert level.target in level.array
    assert level.selected_index == 0

def test_stack_operations():
    """Test stack push/pop operations."""
    level = StackLevel()
    level.push(5)
    assert level.stack[-1] == 5
    level.pop()
    assert len(level.stack) == 0
```

#### Integration Tests
Test component interactions:
```python
def test_level_completion():
    """Test level completion flow."""
    game = DSAGame()
    game.start_level(1)
    # Simulate winning the level
    result = game.current_level_instance.update()
    assert result in ["playing", "completed", "failed"]
```

#### Manual Testing Checklist
- [ ] Game launches without errors
- [ ] All menus navigate correctly
- [ ] Each level can be completed
- [ ] Each level can be failed (time up)
- [ ] Scores are calculated correctly
- [ ] High scores persist between sessions
- [ ] All controls work as expected
- [ ] Graphics render correctly
- [ ] No performance issues (60 FPS)

### Running Tests
```bash
# Automated tests
python3 test_game.py

# Manual testing
./run_game.sh

# Performance testing
# Monitor frame rate and memory usage during gameplay
```

### Test-Driven Development
When adding new features:
1. Write tests first (if possible)
2. Implement feature to pass tests
3. Refactor while keeping tests passing
4. Add additional tests for edge cases

## Submitting Changes

### Pull Request Checklist
- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] No merge conflicts
- [ ] Feature is complete and tested
- [ ] Screenshots included (for visual changes)

### Pull Request Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Testing
- [ ] Unit tests pass
- [ ] Manual testing completed
- [ ] No performance regressions

## Screenshots
(If applicable)

## Additional Notes
Any additional information for reviewers
```

### Review Process
1. **Automated Checks**: Code style and tests
2. **Peer Review**: Code quality and design
3. **Testing**: Functionality verification
4. **Documentation**: Ensure docs are updated
5. **Merge**: After approval from maintainers

## Community Guidelines

### Code of Conduct
- **Be Respectful**: Treat all contributors with respect
- **Be Inclusive**: Welcome contributors of all backgrounds
- **Be Constructive**: Provide helpful feedback
- **Be Patient**: Remember everyone is learning
- **Be Professional**: Keep discussions focused on the project

### Communication Channels
- **GitHub Issues**: Bug reports and feature requests
- **Pull Requests**: Code discussions
- **Discussions**: General questions and ideas

### Getting Help
- **Documentation**: Check existing docs first
- **Issues**: Search existing issues
- **Discussions**: Ask questions in discussions
- **Code**: Read through existing code for examples

### Recognition
Contributors will be recognized in:
- **README**: Contributor list
- **Releases**: Release notes
- **Credits**: In-game credits screen (planned)

## Educational Impact

### Learning Objectives
When contributing, consider:
- **Pedagogical Value**: Does this help students learn?
- **Engagement**: Is it fun and motivating?
- **Accessibility**: Can learners of different levels use it?
- **Real-world Relevance**: Does it connect to practical applications?

### Target Audience
- **Students**: Learning DSA for the first time
- **Interview Candidates**: Preparing for technical interviews
- **Educators**: Teaching DSA concepts
- **Professionals**: Refreshing knowledge

---

Thank you for contributing to DSA Learning Adventure! Your efforts help make computer science education more accessible and engaging for learners worldwide.

**Built using Amazon Q Developer CLI for AWS Games Challenge June 2025**
