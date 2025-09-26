# Mikan Mode

Mikan Mode implements the learning algorithm from the mikan English vocabulary app for Anki. This add-on provides an efficient repetition-based learning method using 5-card sets.

## Features

- **5-card set learning**: Cards are presented in groups of 5
- **Smart repetition**: Cards marked as "unknown" go to the back of the queue, while "known" cards are removed
- **Session-based learning**: Configure session size (default: 100 cards)
- **Keyboard shortcuts**: Fast navigation with Space, 1, 2, 3, and Esc keys
- **Progress tracking**: Visual feedback on current progress and completion status
- **Anki integration**: Learning results are properly recorded in Anki's statistics

## How it works

1. Select cards from your deck using Anki's scheduling algorithm
2. Shuffle the selected cards randomly
3. Present them in sets of 5 cards
4. For each set:
   - Cards marked as "unknown" (1 key) go to the back of the queue
   - Cards marked as "known" (Space/2/3 keys) are removed from the queue
   - Continue until all 5 cards in the set are marked as "known"
5. Move to the next set of 5 cards
6. Complete the session when all cards are finished

## Usage

1. Go to **Tools → Mikan Mode**
2. Set your preferred session size (5-500 cards)
3. Click **Start** to begin the session
4. Use keyboard shortcuts or buttons to respond:
   - **Space/Enter**: Show answer → Mark as known
   - **1**: Mark as unknown (answer visible)
   - **2/3**: Mark as known (answer visible)
   - **Esc**: Exit session

## Installation

1. Download the .ankiaddon file
2. Open Anki
3. Go to Tools → Add-ons → Install from file
4. Select the downloaded .ankiaddon file
5. Restart Anki

## System Requirements

- Anki 2.1.50 or later
- Tested on Anki 2.1.66+

## License

This add-on is released under the MIT License.

## Support

For bug reports and feature requests, please visit the GitHub repository or AnkiWeb page.

## Version History

### 1.0.0
- Initial release
- 5-card set learning algorithm
- Keyboard shortcuts
- Session management
- Progress tracking
- Anki statistics integration