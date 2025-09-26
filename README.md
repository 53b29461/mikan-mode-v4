# Mikan Mode

Mikan Mode implements the learning algorithm from the mikan English vocabulary app for Anki. This add-on provides an efficient repetition-based learning method with flexible set sizes and enhanced functionality.

## ✨ Features

### 🎛️ Flexible Session Settings
- **Configurable set sizes**: 3-10 cards per set (default: 5)
- **Adjustable session length**: 1-100 sets (default: 6)
- **Real-time calculation**: Total cards automatically calculated and displayed
- **Smart repetition**: Cards marked as "unknown" go to the back of the queue, while "known" cards are removed

### ⏱️ Accurate Learning Time Tracking
- **Session-based measurement**: Tracks actual learning time from start to finish
- **Realistic statistics**: Average time per card calculated and recorded in Anki
- **No artificial timers**: Uses real learning duration instead of fixed values

### 🔙 Undo Functionality
- **Back button**: Return to previous cards with "Back (B)" button
- **Keyboard shortcut**: Press "B" key to go back
- **State restoration**: Automatically restores card completion status and answers
- **Smart display**: Back button only appears when applicable

### 🖥️ Adaptive Interface
- **Resizable window**: Drag to adjust window size to your preference
- **Minimum size protection**: Prevents window from becoming too small (600x400)
- **Responsive layout**: UI elements adjust properly to different window sizes
- **Intuitive controls**: Large, clearly labeled buttons with keyboard shortcuts

## 🔄 How it works

1. **Session Setup**: Choose your preferred cards per set (3-10) and number of sets (1-100)
2. **Card Selection**: Uses Anki's scheduling algorithm to select due cards, new cards, and learning cards
3. **Random Shuffle**: Selected cards are shuffled randomly for varied learning
4. **Set-based Learning**: Cards are presented in your configured set size
5. **Smart Repetition**: For each set:
   - Cards marked as "unknown" (1 key) go to the back of the queue
   - Cards marked as "known" (Space/2/3/4 keys) are removed from the queue
   - Continue until all cards in the set are marked as "known"
6. **Progress Through Sets**: Move to the next set once current set is complete
7. **Session Completion**: Finish when all sets are completed with accurate time tracking

## 🚀 Usage

### Getting Started
1. Go to **Tools → Mikan Mode**
2. Configure your session:
   - **Cards per set**: Choose 3-10 cards (default: 5)
   - **Number of sets**: Choose 1-100 sets (default: 6)
   - **Total cards**: Automatically calculated and displayed
3. Click **Start** to begin the session

### During Learning
Use keyboard shortcuts or click buttons to respond:

**Question Phase:**
- **Space/Enter**: Show answer
- **B**: Go back to previous card (if available)
- **Esc**: Exit session

**Answer Phase:**
- **Space/Enter**: Mark as known (Good)
- **1**: Mark as unknown (Again) - card goes to back of queue
- **2**: Mark as known (Hard)
- **3**: Mark as known (Good)
- **4**: Mark as known (Easy)
- **B**: Go back to previous card
- **Esc**: Exit session

### Window Controls
- **Resize**: Drag window edges or corners to adjust size
- **Minimum size**: Window cannot be smaller than 600x400 for usability

## 📦 Installation

### Method 1: Download from GitHub Releases
1. Visit [Releases](https://github.com/53b29461/mikan-mode-v4/releases)
2. Download **mikan_mode_v4.ankiaddon** from the latest release
3. Open Anki
4. Go to **Tools → Add-ons → Install from file**
5. Select the downloaded .ankiaddon file
6. Restart Anki
7. Access via **Tools → Mikan Mode**

### Method 2: AnkiWeb (when available)
1. Open Anki
2. Go to **Tools → Add-ons → Get Add-ons**
3. Search for "Mikan Mode"
4. Click **Install**
5. Restart Anki

## System Requirements

- Anki 2.1.50 or later
- Tested on Anki 2.1.66+

## License

This add-on is released under the MIT License.

## Support

For bug reports and feature requests, please visit the GitHub repository or AnkiWeb page.

## 📋 Version History

### 1.0.0 (2024-09-26)
- **Flexible session settings**: Configurable cards per set (3-10) and number of sets (1-100)
- **Accurate time tracking**: Session-based learning time measurement with realistic Anki statistics
- **Undo functionality**: Back button with keyboard shortcut (B key) and state restoration
- **Resizable interface**: Adaptive window sizing with minimum size protection
- **Enhanced keyboard shortcuts**: Complete set of navigation and response shortcuts
- **Smart card selection**: Uses Anki's scheduling algorithm for optimal learning
- **Real-time progress tracking**: Visual feedback with detailed progress information
- **Robust error handling**: Comprehensive error management and user feedback
- **Ready for distribution**: Complete .ankiaddon package with proper metadata

### Development Features
- Modern Qt-based interface with proper event handling
- Efficient data structures for card queue management
- Clean separation of concerns between UI, session, and queue management
- Comprehensive documentation and development setup