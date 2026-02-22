VOWELS = set('AEIOU')
CONSONANTS = set('BCDFGHJKLMNPQRSTVWXYZ')

# --- Slot Configuration ---
# Change these numbers to add more upgrade slots.
# Costs double with each subsequent slot. Guaranteed is always double the random.
AUTO_CONSONANT_SLOTS = 2   # starting cost $50
AUTO_VOWEL_SLOTS = 1       # starting cost $100
EXTRA_STRIKE_SLOTS = 2     # starting cost $250


def _generate_upgrades():
    upgrades = []

    # Auto consonant slots
    prev_id = None
    for i in range(AUTO_CONSONANT_SLOTS):
        cost = 50 * (2 ** i)
        random_id = f'auto_consonant_{i + 1}'
        guaranteed_id = f'auto_consonant_guaranteed_{i + 1}'
        slot_label = f' {i + 1}' if AUTO_CONSONANT_SLOTS > 1 else ''

        upgrades.append({
            'id': random_id,
            'label': f'Free Consonant{slot_label}',
            'description': 'A random consonant is revealed each round',
            'cost': cost,
            'requires': prev_id,
        })
        upgrades.append({
            'id': guaranteed_id,
            'label': f'Guaranteed Consonant{slot_label}',
            'description': 'Free consonant is guaranteed to be in the phrase',
            'cost': cost * 2,
            'requires': random_id,
        })
        prev_id = random_id

    # Auto vowel slots
    prev_id = None
    for i in range(AUTO_VOWEL_SLOTS):
        cost = 100 * (2 ** i)
        random_id = f'auto_vowel_{i + 1}'
        guaranteed_id = f'auto_vowel_guaranteed_{i + 1}'
        slot_label = f' {i + 1}' if AUTO_VOWEL_SLOTS > 1 else ''

        upgrades.append({
            'id': random_id,
            'label': f'Free Vowel{slot_label}',
            'description': 'A random vowel is revealed each round',
            'cost': cost,
            'requires': prev_id,
        })
        upgrades.append({
            'id': guaranteed_id,
            'label': f'Guaranteed Vowel{slot_label}',
            'description': 'Free vowel is guaranteed to be in the phrase',
            'cost': cost * 2,
            'requires': random_id,
        })
        prev_id = random_id

    # Extra strike slots
    prev_id = None
    for i in range(EXTRA_STRIKE_SLOTS):
        cost = 250 * (2 ** i)
        strike_id = f'extra_strike_{i + 1}'
        strike_num = i + 4  # Starts at the 4th strike

        upgrades.append({
            'id': strike_id,
            'label': f'{strike_num}th Strike' if strike_num != 5 else '5th Strike',
            'description': f'Gain a {strike_num}th strike before losing',
            'cost': cost,
            'requires': prev_id,
        })
        prev_id = strike_id

    return upgrades


UPGRADES = _generate_upgrades()

# --- Consumable Definitions ---
# Consumables are single use and applied immediately upon purchase mid-round.
CONSUMABLES = [
    {
        'id': 'reveal_consonant',
        'label': 'Reveal Consonant',
        'description': 'Reveals a random hidden consonant in the phrase',
        'cost': 25,
    },
    {
        'id': 'reveal_vowel',
        'label': 'Reveal Vowel',
        'description': 'Reveals a random hidden vowel in the phrase',
        'cost': 50,
    },
    {
        'id': 'eliminate_letters',
        'label': 'Eliminate 3 Letters',
        'description': 'Removes 3 wrong letters from the alphabet',
        'cost': 25,
    },
    {
        'id': 'free_guess',
        'label': 'Free Guess',
        'description': 'Next guess costs nothing, right or wrong',
        'cost': 50,
    },
    {
        'id': 'bonus_strike',
        'label': 'Bonus Strike',
        'description': 'Absorbs one wrong guess before a real strike',
        'cost': 75,
    },
]