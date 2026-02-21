# Changelog

## v1.3

### New Features
- Puzzle difficulty system using a formula based on unique letters, letter rarity (Scrabble values), average word length, and number of words
- Puzzles are now filtered by difficulty based on the player's current streak — harder puzzles unlock as the streak grows
- "What Are You Doing?" category receives adjusted difficulty scoring since I, N, and G are effectively free letters due to every puzzle ending in ING

### Difficulty Gates
| Streak | Max Difficulty | Approx Puzzles Available |
|---|---|---|
| 0–2 | 200 | ~54 |
| 3–4 | 350 | ~127 |
| 5–6 | 500 | ~174 |
| 7–8 | 700 | ~208 |
| 9+ | No limit | 274 |

### Content
- Removed accented characters from all puzzles — English characters only

---

## v1.2

### New Features
- Passive upgrades system that unlocks based on win streak
- Upgrades button centered at the top of the screen opens an upgrade menu
- Upgrade menu shows streak requirement and upgrade name
- Enter key closes any open popup or the upgrades menu

### Upgrades
| Streak | Upgrade |
|---|---|
| 3 | Free Consonant (random from alphabet) |
| 5 | Free Consonant upgraded to guaranteed match in phrase |
| 7 | 4th Strike |
| 9 | Free Vowel (random from alphabet) |
| 11 | Free Vowel upgraded to guaranteed match in phrase |
| 13 | 5th Strike |

### Content
- Expanded all categories to 25 puzzles each
- Renamed Person → Proper Name
- Renamed Place → Proper Place for famous real-world landmarks
- Added new Place category for ambiguous everyday locations (e.g. Pond in the Park, Back Corner Booth)
- Added new Occupation category
- Total puzzle count increased from 115 to 275 across 11 categories

---

## v1.1

### New Features
- Win and lose popups now display the secret phrase
- Streak counter in the top left tracks consecutive wins
- Losing displays your final streak count in the popup
- Topic category displays centered below the phrase
- Long phrases now wrap across multiple lines

### Changes
- Guessed letters in the alphabet are now darker grey
- Removed borders from the streak, topic, and alphabet letter displays
- Play Again button updated to white outline with black background and white text

### Content
- Added 15 new "What Are You Doing?" puzzles
- Total puzzle count increased from 100 to 115

---

## v1.0

### New Features
- Word guessing gameplay with keyboard input
- Letter slots reveal on correct guess
- 3 strike system with red X indicators in the top right
- Full alphabet displayed at the bottom of the screen
- Topic category displayed in the top left
- Win and lose popups with Play Again button
- Streak counter tracking consecutive wins
- Multi-word phrases with spaces displayed as gaps
- 100 puzzles across 8 categories: Thing, Place, Person, Phrase, Before & After, Food & Drink, Event, Around the House