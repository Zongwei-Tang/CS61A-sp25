"""Typing test implementation"""

from utils import (
    lower,
    split,
    remove_punctuation,
    lines_from_file,
    count,
    deep_convert_to_tuple,
)
from ucb import main, interact, trace
from datetime import datetime
import random


###########
# Phase 1 #
###########


def pick(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which the SELECT function returns True.
    If there are fewer than K such paragraphs, return an empty string.

    Arguments:
        paragraphs: a list of strings representing paragraphs
        select: a function that returns True for paragraphs that meet its criteria
        k: an integer

    >>> ps = ['hi', 'how are you', 'fine']
    >>> s = lambda p: len(p) <= 4
    >>> pick(ps, s, 0)
    'hi'
    >>> pick(ps, s, 1)
    'fine'
    >>> pick(ps, s, 2)
    ''
    """
    # BEGIN PROBLEM 1
    "*** YOUR CODE HERE ***"
    x = 0
    for i in range(len(paragraphs)):
        if select(paragraphs[i]):
            if x == k:
                return paragraphs[i]
            x += 1
    return ''
    # END PROBLEM 1


def about(keywords):
    """Return a function that takes in a paragraph and returns whether
    that paragraph contains one of the words in keywords.

    Arguments:
        keywords: a list of keywords

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> pick(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> pick(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in keywords]), "keywords should be lowercase."

    # BEGIN PROBLEM 2
    "*** YOUR CODE HERE ***"
    def helper(x):
        x = x.lower()
        x = remove_punctuation(x)
        x = x.split()
        for i in x:
            if i in keywords:
                return True
        return False
    return helper
    # END PROBLEM 2


def accuracy(typed, source):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    compared to the corresponding words in SOURCE.

    Arguments:
        typed: a string that may contain typos
        source: a model string without errors

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    >>> accuracy('', '')
    100.0
    """
    typed_words = split(typed)
    source_words = split(source)
    # BEGIN PROBLEM 3
    "*** YOUR CODE HERE ***"
    count = 0
    i = 0
    if len(typed_words) == 0 and len(source_words) == 0:
        return 100.0
    if len(typed_words) == 0 or len(source_words) == 0:
        return 0.0
    while i < len(typed_words) and i < len(source_words):
        if typed_words[i] == source_words[i]:
            count += 1
        i += 1
    return count / len(typed_words) * 100
    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string.

    Arguments:
        typed: an entered string
        elapsed: an amount of time in seconds

    >>> wpm('hello friend hello buddy hello', 15)
    24.0
    >>> wpm('0123456789',60)
    2.0
    """
    assert elapsed > 0, "Elapsed time must be positive"
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"
    return len(typed) / 5 / (elapsed / 60)
    # END PROBLEM 4


################
# Phase 4 (EC) #
################


def memo(f):
    """A general memoization decorator."""
    cache = {}

    def memoized(*args):
        immutable_args = deep_convert_to_tuple(args)  # convert *args into a tuple representation
        if immutable_args not in cache:
            result = f(*immutable_args)
            cache[immutable_args] = result
            return result
        return cache[immutable_args]

    return memoized


def memo_diff(diff_function):
    """A memoization function."""
    cache = {}

    def memoized(typed, source, limit):
        # BEGIN PROBLEM EC
        tuple1 = (typed, source)
        if tuple1 in cache and limit <= cache[tuple1][1]:
            return cache[tuple1][0]
        cache[tuple1] = (diff_function(typed, source, limit), limit)
        return cache[tuple1][0]
        # END PROBLEM EC

    return memoized


###########
# Phase 2 #
###########

@memo
def autocorrect(typed_word, word_list, diff_function, limit):
    """Returns the element of WORD_LIST that has the smallest difference
    from TYPED_WORD based on DIFF_FUNCTION. If multiple words are tied for the smallest difference,
    return the one that appears closest to the front of WORD_LIST. If the
    lowest difference is greater than LIMIT, return TYPED_WORD instead.

    Arguments:
        typed_word: a string representing a word that may contain typos
        word_list: a list of strings representing source words
        diff_function: a function quantifying the difference between two words
        limit: a number

    >>> ten_diff = lambda w1, w2, limit: 10 # Always returns 10
    >>> autocorrect("hwllo", ["butter", "hello", "potato"], ten_diff, 20)
    'butter'
    >>> first_diff = lambda w1, w2, limit: (1 if w1[0] != w2[0] else 0) # Checks for matching first char
    >>> autocorrect("tosting", ["testing", "asking", "fasting"], first_diff, 10)
    'testing'
    """
    # BEGIN PROBLEM 5
    "*** YOUR CODE HERE ***"
    if typed_word in word_list:
        return typed_word
    mini = diff_function(typed_word, word_list[0], limit)
    result = word_list[0]
    for i in range(1, len(word_list)):
        if diff_function(typed_word, word_list[i], limit) < mini:
            mini = diff_function(typed_word, word_list[i], limit)
            result = word_list[i]
    if mini <= limit:
        return result
    return typed_word
    
    # END PROBLEM 5


def furry_fixes(typed, source, limit):
    """A diff function for autocorrect that determines how many letters
    in TYPED need to be substituted to create SOURCE, then adds the difference in
    their lengths to this value and returns the result.

    Arguments:
        typed: a starting word
        source: a string representing a desired goal word
        limit: a number representing an upper bound on the number of chars that must change

    >>> big_limit = 10
    >>> furry_fixes("nice", "rice", big_limit)    # Substitute: n -> r
    1
    >>> furry_fixes("range", "rungs", big_limit)  # Substitute: a -> u, e -> s
    2
    >>> furry_fixes("pill", "pillage", big_limit) # Don't substitute anything, length difference of 3.
    3
    >>> furry_fixes("roses", "arose", big_limit)  # Substitute: r -> a, o -> r, s -> o, e -> s, s -> e
    5
    >>> furry_fixes("rose", "hello", big_limit)   # Substitute: r->h, o->e, s->l, e->l, length difference of 1.
    5
    """
    # BEGIN PROBLEM 6
    if limit < 0:
        return 0
    if not typed:
        return len(source)
    if not source:
        return len(typed)
    if typed[0] == source[0]:
        return furry_fixes(typed[1:], source[1:], limit)
    else:
        return 1 + furry_fixes(typed[1:], source[1:], limit - 1)
    # END PROBLEM 6

@memo_diff
def minimum_mewtations(typed, source, limit):
    """A diff function for autocorrect that computes the edit distance from TYPED to SOURCE.
    This function takes in a string TYPED, a string SOURCE, and a number LIMIT.

    Arguments:
        typed: a starting word
        source: a string representing a desired goal word
        limit: a number representing an upper bound on the number of edits

    >>> big_limit = 10
    >>> minimum_mewtations("cats", "scat", big_limit)       # cats -> scats -> scat
    2
    >>> minimum_mewtations("purng", "purring", big_limit)   # purng -> purrng -> purring
    2
    >>> minimum_mewtations("ckiteus", "kittens", big_limit) # ckiteus -> kiteus -> kitteus -> kittens
    3
    """
    if limit < 0: # Base cases should go here, you may add more base cases as needed.
        # BEGIN
        return float('inf')
        # END
    if typed == source:
        return 0
    if not typed:
        return len(source)
    if not source:
        return len(typed)
    if limit == 0:
        return float('inf')
    if abs(len(typed) - len(source)) > limit:
        return float('inf')
    # Recursive cases should go below here
    if typed[0] == source[0]:
        return minimum_mewtations(typed[1:], source[1:], limit)
    else:
        add = minimum_mewtations(typed, source[1:], limit - 1)
        remove = minimum_mewtations(typed[1:], source, limit - 1)
        substitute = minimum_mewtations(typed[1:], source[1:], limit - 1)
        # BEGIN
        a = min(add, remove, substitute)
        if a != float('inf'):
            return 1 + min(add, remove, substitute)
        return float('inf')
        # END
    """
    Below is the most optimized version written by Claude. Only this version can pass the test for Problem EC.

    if limit < 0:
        return float('inf')  # Changed from 0 - this is crucial!
    
    # Base case: strings are already equal
    if typed == source:
        return 0
    
    # Base case: if limit is 0 but strings aren't equal, it's impossible
    if limit == 0:
        return float('inf')  # Can't make any more edits
    
    # Base case: one or both strings are empty
    if not typed:
        # Need to add all characters from source
        return len(source) if len(source) <= limit else float('inf')
    if not source:
        # Need to remove all characters from typed
        return len(typed) if len(typed) <= limit else float('inf')
    
    # Optimization: if the difference in lengths already exceeds limit, impossible
    if abs(len(typed) - len(source)) > limit:
        return float('inf')
    
    # Recursive cases
    if typed[0] == source[0]:
        # CRITICAL OPTIMIZATION: When first characters match,
        # the optimal solution MUST be to keep them and recurse on the rest.
        # We should NOT try add/remove/substitute operations here!
        return minimum_mewtations(typed[1:], source[1:], limit)
    else:
        # Only when first characters differ do we try all three operations
        # Add: insert source[0] at the beginning of typed
        add_cost = minimum_mewtations(typed, source[1:], limit - 1)
        
        # Remove: remove typed[0]
        remove_cost = minimum_mewtations(typed[1:], source, limit - 1)
        
        # Substitute: replace typed[0] with source[0]
        substitute_cost = minimum_mewtations(typed[1:], source[1:], limit - 1)
        
        # Find the minimum cost among valid operations
        min_cost = min(add_cost, remove_cost, substitute_cost)
        
        # If all operations lead to invalid paths, return infinity
        if min_cost == float('inf'):
            return float('inf')
        
        return 1 + min_cost
    """

# Ignore the line below
minimum_mewtations = count(minimum_mewtations)


def final_diff(typed, source, limit):
    """A diff function that takes in a string TYPED, a string SOURCE, and a number LIMIT.
    If you implement this function, it will be used.
    Tbh i dont understand why the test will add ', ", or () in typed/source😅
    """
    typed = typed.lower()
    source = source.lower()
    
    # 步骤2：全面的字符清理 - 移除所有非字母字符
    def clean_text_for_keyboard_check(text):
        """
        为键盘相邻性检查清理文本
        只保留字母字符，移除所有标点符号、数字、特殊字符
        """
        cleaned_chars = []
        for char in text:
            if char.isalpha():  # 只保留字母
                cleaned_chars.append(char)
            # 可以选择保留空格，取决于你的需求
            # elif char.isspace():
            #     cleaned_chars.append(char)
        return ''.join(cleaned_chars)
    
    # 应用清理函数
    typed = clean_text_for_keyboard_check(typed)
    source = clean_text_for_keyboard_check(source)
    keyboard_adjacent = {
    # 第一行：QWERTYUIOP
    'q': ['w', 'a'],                    # q只与w(右)和a(下)相邻
    'w': ['q', 'e', 'a', 's'],          # w与q(左)、e(右)、a(左下)、s(下)相邻
    'e': ['w', 'r', 's', 'd'],          # e与w(左)、r(右)、s(左下)、d(下)相邻
    'r': ['e', 't', 'd', 'f'],          # r与e(左)、t(右)、d(左下)、f(下)相邻
    't': ['r', 'y', 'f', 'g'],          # t与r(左)、y(右)、f(左下)、g(下)相邻
    'y': ['t', 'u', 'g', 'h'],          # y与t(左)、u(右)、g(左下)、h(下)相邻
    'u': ['y', 'i', 'h', 'j'],          # u与y(左)、i(右)、h(左下)、j(下)相邻
    'i': ['u', 'o', 'j', 'k'],          # i与u(左)、o(右)、j(左下)、k(下)相邻
    'o': ['i', 'p', 'k', 'l'],          # o与i(左)、p(右)、k(左下)、l(下)相邻
    'p': ['o', 'l'],                    # p与o(左)和l(下)相邻
    
    # 第二行：ASDFGHJKL
    'a': ['q', 'w', 's', 'z'],          # a与q(上)、w(右上)、s(右)、z(下)相邻
    's': ['a', 'w', 'e', 'd', 'z', 'x'], # s与a(左)、w(左上)、e(上)、d(右)、z(左下)、x(下)相邻
    'd': ['s', 'e', 'r', 'f', 'x', 'c'], # d与s(左)、e(左上)、r(上)、f(右)、x(左下)、c(下)相邻
    'f': ['d', 'r', 't', 'g', 'c', 'v'], # f与d(左)、r(左上)、t(上)、g(右)、c(左下)、v(下)相邻
    'g': ['f', 't', 'y', 'h', 'v', 'b'], # g与f(左)、t(左上)、y(上)、h(右)、v(左下)、b(下)相邻
    'h': ['g', 'y', 'u', 'j', 'b', 'n'], # h与g(左)、y(左上)、u(上)、j(右)、b(左下)、n(下)相邻
    'j': ['h', 'u', 'i', 'k', 'n', 'm'], # j与h(左)、u(左上)、i(上)、k(右)、n(左下)、m(下)相邻
    'k': ['j', 'i', 'o', 'l', 'm'],     # k与j(左)、i(左上)、o(上)、l(右)、m(下)相邻
    'l': ['k', 'o', 'p', 'm'],          # l与k(左)、o(左上)、p(上)、m(下)相邻
    
    # 第三行：ZXCVBNM
    'z': ['a', 's', 'x'],               # z与a(上)、s(右上)、x(右)相邻
    'x': ['z', 's', 'd', 'c'],          # x与z(左)、s(左上)、d(上)、c(右)相邻
    'c': ['x', 'd', 'f', 'v'],          # c与x(左)、d(左上)、f(上)、v(右)相邻
    'v': ['c', 'f', 'g', 'b'],          # v与c(左)、f(左上)、g(上)、b(右)相邻
    'b': ['v', 'g', 'h', 'n'],          # b与v(左)、g(左上)、h(上)、n(右)相邻
    'n': ['b', 'h', 'j', 'm'],          # n与b(左)、h(左上)、j(上)、m(右)相邻
    'm': ['n', 'j', 'k', 'l']           # m与n(左)、j(左上)、k(上)、l(右上)相邻
    }
    if limit < 0: # Base cases should go here, you may add more base cases as needed.
        # BEGIN
        return 0
        # END
    if not typed:
        return len(source)
    if not source:
        return len(typed)
    # Recursive cases should go below here
    if typed[0] == source[0]:
        return final_diff(typed[1:], source[1:], limit)
    else:
        add = 1 + final_diff(source[0] + typed, source, limit - 1)
        remove = 1 + final_diff(typed[1:], source, limit - 1)
        substitute = 1 + final_diff(source[0] + typed[1:], source, limit - 1)
        if typed[0] in keyboard_adjacent[source[0]]:
            substitute = 0.5 + final_diff(source[0] + typed[1:], source, limit - 0.5)
        if len(source) > 1 and source[0] == source[1]:
            add = 0.5 + final_diff(source[0] + typed, source, limit - 0.5)
            remove = 0.5 + final_diff(typed[1:], source, limit - 0.5)
        if len(typed) > 1 and len(source) > 1 and typed[0] == source[1] and typed[1] == source[0]:
            substitute = 1 + final_diff(source[0] + source[1] + typed[2:], source, limit - 1)
        # BEGIN
        return min(add, remove, substitute)


FINAL_DIFF_LIMIT = 6  # REPLACE THIS WITH YOUR LIMIT


###########
# Phase 3 #
###########


def report_progress(typed, source, user_id, upload):
    """Upload a report of your id and progress so far to the multiplayer server.
    Returns the progress so far.

    Arguments:
        typed: a list of the words typed so far
        source: a list of the words in the typing source
        user_id: a number representing the id of the current user
        upload: a function used to upload progress to the multiplayer server

    >>> print_progress = lambda d: print('ID:', d['id'], 'Progress:', d['progress'])
    >>> # The above function displays progress in the format ID: __, Progress: __
    >>> print_progress({'id': 1, 'progress': 0.6})
    ID: 1 Progress: 0.6
    >>> typed = ['how', 'are', 'you']
    >>> source = ['how', 'are', 'you', 'doing', 'today']
    >>> report_progress(typed, source, 2, print_progress)
    ID: 2 Progress: 0.6
    0.6
    >>> report_progress(['how', 'aree'], source, 3, print_progress)
    ID: 3 Progress: 0.2
    0.2
    """
    # BEGIN PROBLEM 8
    "*** YOUR CODE HERE ***"
    for i in range(len(typed)):
        if typed[i] != source[i]:
            progress = i / len(source)
            upload({'id': user_id, 'progress': progress})
            return progress
    progress = len(typed) / len(source)
    upload({'id': user_id, 'progress': progress})
    return progress
    # END PROBLEM 8


def time_per_word(words, timestamps_per_player):
    """Return a dictionary {'words': words, 'times': times} where times
    is a list of lists that stores the durations it took each player to type
    each word in words.

    Arguments:
        words: a list of words, in the order they are typed.
        timestamps_per_player: A list of lists of timestamps including the time
                          each player started typing, followed by the time each
                          player finished typing each word.

    >>> p = [[75, 81, 84, 90, 92], [19, 29, 35, 36, 38]]
    >>> result = time_per_word(['collar', 'plush', 'blush', 'repute'], p)
    >>> result['words']
    ['collar', 'plush', 'blush', 'repute']
    >>> result['times']
    [[6, 3, 6, 2], [10, 6, 1, 2]]
    """
    tpp = timestamps_per_player  # A shorter name (for convenience)
    # BEGIN PROBLEM 9
    times = []  # You may remove this line
    for i in range(len(tpp)):
        result = []
        for j in range(1, len(tpp[i])):
            result.append(tpp[i][j] - tpp[i][j - 1])
        times.append(result)
    # END PROBLEM 9
    return {'words': words, 'times': times}


def fastest_words(words_and_times):
    """Return a list of lists indicating which words each player typed fastest.
    In case of a tie, the player with the lower index is considered to be the one who typed it the fastest.

    Arguments:
        words_and_times: a dictionary {'words': words, 'times': times} where
        words is a list of the words typed and times is a list of lists of times
        spent by each player typing each word.

    >>> p0 = [5, 1, 3]
    >>> p1 = [4, 1, 6]
    >>> fastest_words({'words': ['Just', 'have', 'fun'], 'times': [p0, p1]})
    [['have', 'fun'], ['Just']]
    >>> p0  # input lists should not be mutated
    [5, 1, 3]
    >>> p1
    [4, 1, 6]
    """
    check_words_and_times(words_and_times)  # verify that the input is properly formed
    words, times = words_and_times['words'], words_and_times['times']
    player_indices = range(1, len(times))  # contains an *index* for each player
    word_indices = range(len(words))    # contains an *index* for each word
    # BEGIN PROBLEM 10
    "*** YOUR CODE HERE ***"
    result = [[] for _ in range(len(times))] # Dont use [[] * len(times)]! It will cause bug because when you change one list in that list all lists would be changed.
    for i in word_indices:
        mini = 0
        for j in player_indices:
            if times[j][i] < times[mini][i]:
                mini = j
        result[mini].append(words[i])
    return result
    # END PROBLEM 10


def check_words_and_times(words_and_times):
    """Check that words_and_times is a {'words': words, 'times': times} dictionary
    in which each element of times is a list of numbers the same length as words.
    """
    assert 'words' in words_and_times and 'times' in words_and_times and len(words_and_times) == 2
    words, times = words_and_times['words'], words_and_times['times']
    assert all([type(w) == str for w in words]), "words should be a list of strings"
    assert all([type(t) == list for t in times]), "times should be a list of lists"
    assert all([isinstance(i, (int, float)) for t in times for i in t]), "times lists should contain numbers"
    assert all([len(t) == len(words) for t in times]), "There should be one word per time."


def get_time(times, player_num, word_index):
    """Return the time it took player_num to type the word at word_index,
    given a list of lists of times returned by time_per_word."""
    num_players = len(times)
    num_words = len(times[0])
    assert word_index < len(times[0]), f"word_index {word_index} outside of 0 to {num_words-1}"
    assert player_num < len(times), f"player_num {player_num} outside of 0 to {num_players-1}"
    return times[player_num][word_index]


enable_multiplayer = True  # Change to True when you're ready to race.

##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file("data/sample_paragraphs.txt")
    random.shuffle(paragraphs)
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        source = pick(paragraphs, select, i)
        if not source:
            print("No more paragraphs about", topics, "are available.")
            return
        print("Type the following paragraph and then press enter/return.")
        print("If you only type part of it, you will be scored only on that part.\n")
        print(source)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print("Goodbye.")
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print("Words per minute:", wpm(typed, elapsed))
        print("Accuracy:        ", accuracy(typed, source))

        print("\nPress enter/return for the next paragraph or type q to quit.")
        if input().strip() == "q":
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse

    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument("topic", help="Topic word", nargs="*")
    parser.add_argument("-t", help="Run typing test", action="store_true")

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)

