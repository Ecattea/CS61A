# Q1: Draw 
def draw(hand, positions):
    """Remove and return the items at positions from hand.

    >>> hand = ['A', 'K', 'Q', 'J', 10, 9]
    >>> draw(hand, [2, 1, 4])
    ['K', 'Q', 10]
    >>> hand
    ['A', 'J', 9]
    """
    return list(reversed( [hand.pop(i) for i in reversed(sorted(positions))] ))
# Q1: Draw

# Q2: Keyboard
LOWERCASE_LETTERS = 'abcdefghijklmnopqrstuvwxyz'

class CapsLock:
    def __init__(self):
        self.pressed = 0

    def press(self):
        self.pressed += 1

class Button:
    """A button on a keyboard.

    >>> f = lambda c: print(c, end='')  # The end='' argument avoids going to a new line
    >>> k, e, y = Button('k', f), Button('e', f), Button('y', f)
    >>> s = e.press().press().press()
    eee
    >>> caps = Button.caps_lock
    >>> t = [x.press() for x in [k, e, y, caps, e, e, k, caps, e, y, e, caps, y, e, e]]
    keyEEKeyeYEE
    >>> u = Button('a', print).press().press().press()
    A
    A
    A
    """
    caps_lock = CapsLock()

    def __init__(self, letter, output):
        assert letter in LOWERCASE_LETTERS
        self.letter = letter
        self.output = output
        self.pressed = 0

    def press(self):
        """Call output on letter (maybe uppercased), then return the button that was pressed."""
        self.pressed += 1
        if self.caps_lock.pressed % 2 != 0:
            self.output(self.letter.upper())
        else:
            self.output(self.letter)
        return self

class Keyboard:
    """A keyboard.

    >>> Button.caps_lock.pressed = 0  # Reset the caps_lock key
    >>> bored = Keyboard()
    >>> bored.type('hello')
    >>> bored.typed
    ['h', 'e', 'l', 'l', 'o']
    >>> bored.keys['l'].pressed
    2

    >>> Button.caps_lock.press()
    >>> bored.type('hello')
    >>> bored.typed
    ['h', 'e', 'l', 'l', 'o', 'H', 'E', 'L', 'L', 'O']
    >>> bored.keys['l'].pressed
    4
    """
    def __init__(self):
        self.typed = []
        self.keys = {c: Button(c, self.typed.append) for c in LOWERCASE_LETTERS}

    def type(self, word):
        """Press the button for each letter in word."""
        assert all([w in LOWERCASE_LETTERS for w in word]), 'word must be all lowercase'
        for letter in word:
            self.keys[letter].press()
        
# Q2: Keyboard

# Q3: Bear
class Eye:
    """An eye.

    >>> Eye().draw()
    '0'
    >>> print(Eye(False).draw(), Eye(True).draw())
    0 -
    """
    def __init__(self, closed=False):
        self.closed = closed

    def draw(self):
        if self.closed:
            return '-'
        else:
            return '0'

class Bear:
    """A bear.

    >>> Bear().print()
    ? 0o0?
    """
    def __init__(self):
        self.nose_and_mouth = 'o'

    def next_eye(self):
        return Eye()

    def print(self):
        left, right = self.next_eye(), self.next_eye()
        print('? ' + left.draw() + self.nose_and_mouth + right.draw() + '?')

class SleepyBear(Bear):
    """A bear with closed eyes.

    >>> SleepyBear().print()
    ? -o-?
    """
    def next_eye(self):
        return Eye(True)

class WinkingBear(Bear):
    """A bear whose left eye is different from its right eye.

    >>> WinkingBear().print()
    ? -o0?
    """
    def __init__(self):
        super().__init__()
        self._next_closed = True

    def next_eye(self):
        eye, self._next_closed = Eye(self._next_closed), not self._next_closed
        return eye
# Q3: Bear

# Q4: Counter
class Counter:
    """Counts how many times inc has been called on itself or any of its spawn.

    >>> total = Counter()
    >>> odd, even = total.spawn(), total.spawn()
    >>> one, three = odd.spawn(), odd.spawn()
    >>> for c in [one, even, three, even, odd, even]:
    ...     c.inc()
    >>> [c.count for c in [one, three, even, odd, total]]
    [1, 1, 3, 3, 6]
    """
    def __init__(self, parent=None):
        self.parent = parent
        self.count = 0

    def inc(self):
        self.count += 1
        if self.parent is not None:
            self.parent.inc()

    def spawn(self):
        return Counter(self)
# Q4: Counter

# Q5: MissDict
class MissDict:
    """Has a dict, gets a list of values for an iterable of keys, and counts keys that are not in the dict.

    >>> double = MissDict({1: 2, 2: 4, 3: 6, 5: 10})
    >>> half = MissDict({2: 1.0, 3: 1.5, 4: 2.0})
    >>> double.get([1, 3, 5, 2, 4])  # No value for key 4 (1 miss)
    [2, 6, 10, 4]
    >>> double.get([5, 4, 3, 0, 4])  # No value for keys 0 or either 4 (3 misses)
    [10, 6]
    >>> half.get([1, 3, 5, 2, 4])    # No value for keys 1 or 5 (2 misses)
    [1.5, 1.0, 2.0]
    >>> print(double)
    4/6 of the misses
    """
    misses = Counter()
    def __init__(self, d):
        assert isinstance(d, dict)
        self.d = d
        self.misses = MissDict.misses.spawn()

    def get(self, keys):
        result = []
        for k in keys:
            if k in self.d:
                result.append(self.d[k])
            else:
                self.misses.inc()
        return result

    def __str__(self):
        return f'{self.misses.count}/{MissDict.misses.count} of the misses'
# Q5: MissDict
