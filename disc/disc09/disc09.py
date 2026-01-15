#Q1
import asyncio

async def wait_for(seconds):
    await asyncio.sleep(seconds)

async def go():
    await asyncio.gather(wait_for(5), wait_for(3), wait_for(4))

asyncio.run(go())
#Q1

#Q2
class Status:
    """A Status represents whether some operation is complete.

    >>> s = Status()
    >>> s.is_done()
    False
    >>> s.done()
    >>> s.is_done()
    True
    """
    def __init__(self):
        self._event = asyncio.Event()

    def is_done(self) -> bool:
        return self._event.is_set()

    def done(self):
        self._event.set()
#Q2

#Q3
import sys

async def get_user_input(status: Status) -> str:
    # Read one line of user input
    # Using "await" means that we're giving up control
    # and letting other coroutines run while we wait for
    # user input.
    result = await asyncio.to_thread(sys.stdin.readline)
    status.done() # Update status
    return result
#Q3

#Q4
async def timer(status: Status, period):
    """Print a message every period seconds until status.is_done()."""
    time_passed = 0
    while not status.is_done():
        if time_passed == 1:
            print('1 second has passed...')
        else:
            print(f'{time_passed} seconds have passed...')
        time_passed += period
        await asyncio.sleep(period)
    return time_passed
#Q4

#Q5
async def wwpd(challenge: str):
    """Run a WWPD interface.

    >>> simulate_user_input(5, 2.5) # simulate a user entering 5 after 2.5 seconds
    >>> asyncio.run(wwpd('2 + 3'))
    What is 2 + 3
    0 seconds have passed...
    1 second has passed...
    2 seconds have passed...
    5
    The user waited 3 seconds to correctly respond with 5

    >>> simulate_user_input(6, 1.5) # simulate a user entering 6 after 1.5 seconds
    >>> asyncio.run(wwpd('2 + 3'))
    What is 2 + 3
    0 seconds have passed...
    1 second has passed...
    6
    The user waited 2 seconds to incorrectly respond with 6
    """
    print('What is', challenge)
    status = Status()
    seconds, response = await asyncio.gather(
        timer(status, 1),
        get_user_input(status)
    )
    # Get the correct answer, and compare it to the user input.
    correct_answer = eval(challenge)
    if str(correct_answer) == response.strip():
        print(f'The user waited {seconds} seconds to correctly respond with {response}')
    else:
        print(f'The user waited {seconds} seconds to incorrectly respond with {response}')

def simulate_user_input(response, time):
    """Simulate a user response after an amount of time. This is just for testing."""
    async def f(status):
        await asyncio.sleep(time)
        status.done()
        print(response)
        return str(response)
    global get_user_input
    get_user_input = f
#Q5

#Q6
def get_next_expression(expressions, first) -> str:
    """ Return the lowest index expression in expressions that's not in first,
        or an empty string if all expressions are in first.

    >>> get_next_expression(['1 + 1', '[1, 2] + [5, 6]'], {})
    '1 + 1'
    >>> get_next_expression(['1 + 1', '[1, 2] + [5, 6]'], {'1 + 1': 'John'})
    '[1, 2] + [5, 6]'
    >>>
    >>> get_next_expression(['1 + 1'], {'1 + 1': 'John'})
    ''
    """
    for expr in expressions:
        if expr not in first:
            return expr
    return ''

async def run_challenges(name: str, get_result, expressions: list[str], first: dict[str, str]):
    expression = get_next_expression(expressions, first)
    while expression:
        result = await get_result(expression)

        correct_answer = str(eval(expression))
        if result.strip() == correct_answer:
            print(f"-- Good job {name}; you correctly evaluated '{expression}' --")
            if expression not in first:
                first[expression] = name
        else:
            print(f"-- Not quite {name}. Try to evaluate '{expression}' again! --")
        expression = get_next_expression(expressions, first)

async def get_input_from_user(expression):
    print('What does the following Python expression evaluate to', expression)
    return await asyncio.to_thread(sys.stdin.readline)

async def get_input_from_computer(expression: str):
    """Return the result of evaluating the expression, after 0.3 seconds."""
    await asyncio.sleep(0.3)
    return str(eval(expression))

async def run_challenge(player: str):
    """ Return a dictionary mapping each expression to the player name that evaluated it first.
        One player reads from stdin using the get_input_from_user coroutine and has name player, and the other
        is named 'computer' and gets input using get_input_from_computer."""
    expressions = ['1 + 1', '[1, 2].append([5, 6])', '[1, 2] + [5, 6]']
    first = {}
    await asyncio.gather(
        run_challenges(player, get_input_from_user, expressions, first),
        run_challenges('computer', get_input_from_computer, expressions, first),
    )
    return first
#Q6