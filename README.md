# ROS Game Control System

A ROS-based game system with multiple nodes for user information collection, game control, and result display.

## 🎲 Game Description

Navigate in maze from the starting position **(1,1)** to the target position **(8,8)** using arrow keys. The game features a scoring system based on efficiency - fewer moves result in a higher score. The system implements a three-phase game structure: **Welcome**, **Game**, and **Final** phases.

-----

## 🤖 Nodes

The system consists of five interconnected ROS nodes:

  * **info\_user** - Collects player information (name, username, age) via terminal input
  * **game\_node** - Main game logic implementing three phases (Welcome, Game, Final)
  * **control\_node** - Keyboard input for movement control using arrow keys
  * **control\_node\_bygame** - Automated control for testing/demonstration
  * **result\_node** - Displays final results with player information and score

-----

## Topics

  * **user\_information** (`game_control/user_msg`) - Player profile data
  * **keyboard\_control** (`std_msgs/String`) - Movement commands (UP/DOWN/LEFT/RIGHT)
  * **result\_information** (`std_msgs/Int64`) - Final score

-----

## ✉️ Custom Message

**`user_msg.msg`:**

```
string name
string username
int64 age
```

-----

## 📦 Dependencies

### Required ROS Packages:

  * **rospy** - Python client library for ROS
  * **std\_msgs** - Standard message types
  * **message\_generation** - For compiling custom messages
  * **message\_runtime** - For using custom messages at runtime

### System Dependencies:

  * **Python 3** - Programming language
  * **termios, tty, select** - Standard Python libraries for terminal input
  * **ROS Noetic** (or your ROS distribution) - Robot Operating System

### No External Dependencies Needed:

  * **pygame is NOT required** - Using standard Linux terminal input for keyboard control

-----

## 🔧 Installation Instructions

### Step 1: Install ROS Dependencies

```bash
# Install ROS base packages (if not already installed)
sudo apt-get update
sudo apt-get install ros-${ROS_DISTRO}-ros-base

# Install required ROS packages
sudo apt-get install ros-${ROS_DISTRO}-rospy
sudo apt-get install ros-${ROS_DISTRO}-std-msgs
sudo apt-get install ros-${ROS_DISTRO}-message-generation
sudo apt-get install ros-${ROS_DISTRO}-message-runtime
```

### Step 2: Create and Build the Workspace

```bash
# Create workspace
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws
catkin_make

# Source the workspace
source devel/setup.bash
echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc
```

### Step 3: Create the Package

```bash
cd ~/catkin_ws/src
catkin_create_pkg game_control rospy std_msgs message_generation message_runtime
cd game_control

# Create directory structure
mkdir msg scripts
```

### Step 4: Add Custom Message and Node Files

1.  Create `msg/user_msg.msg` with the custom message structure.
2.  Add all Python node files to the `scripts/` directory.
3.  Make scripts executable:
    ```bash
    chmod +x scripts/*.py
    ```

### Step 5: Build the Package

```bash
cd ~/catkin_ws
catkin_make
source devel/setup.bash
```

-----

## 🚀 How to Run the System

### Running Order and Expected Behavior

Start nodes in this order (each in separate terminals):

#### Terminal 1: ROS Core (Required First)

```bash
cd ~/catkin_ws
source devel/setup.bash
roscore
```

  * **Expected:** ROS master starts, ready for other nodes

#### Terminal 2: Result Node (Start Early)

```bash
cd ~/catkin_ws
source devel/setup.bash
rosrun game_control result_node.py
```

  * **Expected:**
      * `"Result node initialized - Waiting for game results..."`
      * Will display final results when game completes

#### Terminal 3: Game Node

```bash
cd ~/catkin_ws
source devel/setup.bash
rosrun game_control game_node.py
```

  * **Expected:**
      * `"Game node initialized - Waiting for user information..."`
      * Will transition through Welcome $\to$ Game $\to$ Final phases

#### Terminal 4: Control Node (Manual Play)

```bash
cd ~/catkin_ws
source devel/setup.bash
rosrun game_control control_node.py
```

  * **Expected:**
      * `"Control node started - Use arrow keys to move"`
      * `"Press 'q' to quit"`
      * Shows "Movement: UP/DOWN/LEFT/RIGHT" when arrow keys pressed

#### Terminal 5: Info User Node (Start Last)

```bash
cd ~/catkin_ws
source devel/setup.bash
rosrun game_control info_user.py
```

  * **Expected:**
      * Prompts for name, username, and age
      * Publishes user information and exits

-----

## 🎮 Game Flow and What to Expect

### Phase 1: Welcome Phase

  * **Triggered by:** User info from `info_user` node
  * **Expected Output:** Welcome message with user details and game instructions
  * **Transition:** Automatically to Game phase

### Phase 2: Game Phase

  * **Triggered by:** Movement commands from `control_node`
  * **Expected Output:**
      * Position updates: `"Position: (x, y) | Moves: count"`
      * Movement confirmations
  * **Win Condition:** Reach position (3,3)
  * **Transition:** Automatically to Final phase when target reached

### Phase 3: Final Phase

  * **Triggered by:** Reaching target position (3,3)
  * **Expected Output:**
      * Score calculation message
      * Score published to `result_information` topic
  * **Final Results:** Displayed in `result_node` terminal

-----

## 🏆 Expected Final Output

In the `result_node` terminal, you should see:

```text
🎊 === FINAL GAME RESULTS === 🎊
    Player: [Name]
    Username: @[username]
    Age: [age]
    Final Score: [score]
    Rating: [performance rating]
=================================
```

-----

## 🛠️ Troubleshooting

### Common Issues:

  * **"Package not found"**: Run `source devel/setup.bash` in each terminal
  * **Arrow keys not working**: Ensure `control_node` terminal is focused
  * **Nodes not communicating**: Verify `roscore` is running and all nodes started in correct order
  * **Build errors**: Check `CMakeLists.txt` and `package.xml` for correct syntax

### Verification Commands:

```bash
# Verify package recognition
rospack find game_control

# Verify custom message
rosmsg list | grep user_msg

# Check active topics
rostopic list

# Monitor specific topics
rostopic echo /user_information
rostopic echo /keyboard_control
rostopic echo /result_information
```

-----

## 📡 Node Communication Overview

```text
info_user (user data) → user_information topic → game_node & result_node
control_node (movement) → keyboard_control topic → game_node
game_node (score) → result_information topic → result_node
```

