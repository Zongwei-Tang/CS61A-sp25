passphrase = 'abc'

def midsem_survey(p):
    """
    You do not need to understand this code.
    >>> midsem_survey(passphrase)
    '2bf925d47c03503d3ebe5a6fc12d479b8d12f14c0494b43deba963a0'
    """
    import hashlib
    return hashlib.sha224(p.encode('utf-8')).hexdigest()


class VendingMachine:
    """A vending machine that vends some product for some price.

    >>> v = VendingMachine('candy', 10)
    >>> v.vend()
    'Nothing left to vend. Please restock.'
    >>> v.add_funds(15)
    'Nothing left to vend. Please restock. Here is your $15.'
    >>> v.restock(2)
    'Current candy stock: 2'
    >>> v.vend()
    'Please add $10 more funds.'
    >>> v.add_funds(7)
    'Current balance: $7'
    >>> v.vend()
    'Please add $3 more funds.'
    >>> v.add_funds(5)
    'Current balance: $12'
    >>> v.vend()
    'Here is your candy and $2 change.'
    >>> v.add_funds(10)
    'Current balance: $10'
    >>> v.vend()
    'Here is your candy.'
    >>> v.add_funds(15)
    'Nothing left to vend. Please restock. Here is your $15.'

    >>> w = VendingMachine('soda', 2)
    >>> w.restock(3)
    'Current soda stock: 3'
    >>> w.restock(3)
    'Current soda stock: 6'
    >>> w.add_funds(2)
    'Current balance: $2'
    >>> w.vend()
    'Here is your soda.'
    """
    def __init__(self, product, price):
        """Set the product and its price, as well as other instance attributes."""
        self.product = product
        self.price = price
        self.inventory = 0
        self.balance = 0

    def restock(self, n):
        """Add n to the stock and return a message about the updated stock level.

        E.g., Current candy stock: 3
        """
        self.inventory += n
        return f'Current {self.product} stock: {self.inventory}'

    def add_funds(self, n):
        """If the machine is out of stock, return a message informing the user to restock
        (and return their n dollars).

        E.g., Nothing left to vend. Please restock. Here is your $4.

        Otherwise, add n to the balance and return a message about the updated balance.

        E.g., Current balance: $4
        """
        if self.inventory == 0:
            return f'Nothing left to vend. Please restock. Here is your ${n}.'
        self.balance += n
        return f'Current balance: ${self.balance}'

    def vend(self):
        """Dispense the product if there is sufficient stock and funds and
        return a message. Update the stock and balance accordingly.

        E.g., Here is your candy and $2 change.

        If not, return a message suggesting how to correct the problem.

        E.g., Nothing left to vend. Please restock.
              Please add $3 more funds.
        """
        if self.inventory == 0:
            return 'Nothing left to vend. Please restock.'
        elif self.balance < self.price:
            return f'Please add ${self.price - self.balance} more funds.'
        elif self.balance == self.price:
            self.inventory -= 1
            self.balance = 0
            return f'Here is your {self.product}.'
        else:
            self.inventory -= 1
            a = self.balance - self.price
            self.balance = 0
            return f'Here is your {self.product} and ${a} change.'



def store_digits(n):
    """Stores the digits of a positive number n in a linked list.

    >>> s = store_digits(1)
    >>> s
    Link(1)
    >>> store_digits(2345)
    Link(2, Link(3, Link(4, Link(5))))
    >>> store_digits(876)
    Link(8, Link(7, Link(6)))
    >>> store_digits(2450)
    Link(2, Link(4, Link(5, Link(0))))
    >>> store_digits(20105)
    Link(2, Link(0, Link(1, Link(0, Link(5)))))
    >>> # a check for restricted functions
    >>> import inspect, re
    >>> cleaned = re.sub(r"#.*\\n", '', re.sub(r'"{3}[\s\S]*?"{3}', '', inspect.getsource(store_digits)))
    >>> print("Do not use str or reversed!") if any([r in cleaned for r in ["str", "reversed"]]) else None
    """
    if n < 10:
        return Link(n)
    result = store_digits(n // 10)
    a = result
    while a.rest:
        a = a.rest
    a.rest = Link(n % 10)
    return result



def deep_map_mut(func, s):
    """Mutates a deep link s by replacing each item found with the
    result of calling func on the item. Does NOT create new Links (so
    no use of Link's constructor).

    Does not return the modified Link object.

    >>> link1 = Link(3, Link(Link(4), Link(5, Link(6))))
    >>> print(link1)
    <3 <4> 5 6>
    >>> # Disallow the use of making new Links before calling deep_map_mut
    >>> Link.__init__, hold = lambda *args: print("Do not create any new Links."), Link.__init__
    >>> try:
    ...     deep_map_mut(lambda x: x * x, link1)
    ... finally:
    ...     Link.__init__ = hold
    >>> print(link1)
    <9 <16> 25 36>
    """
    "*** YOUR CODE HERE ***"
    if not s:
        return
    if isinstance(s.first, Link):
        deep_map_mut(func, s.first)
    else:
        s.first = func(s.first)
    deep_map_mut(func, s.rest)



def two_list(vals, counts):
    """
    Returns a linked list according to the two lists that were passed in. Assume
    vals and counts are the same size. Elements in vals represent the value, and the
    corresponding element in counts represents the number of this value desired in the
    final linked list. Assume all elements in counts are greater than 0. Assume both
    lists have at least one element.
    >>> a = [1, 3]
    >>> b = [1, 1]
    >>> c = two_list(a, b)
    >>> c
    Link(1, Link(3))
    >>> a = [1, 3, 2]
    >>> b = [2, 2, 1]
    >>> c = two_list(a, b)
    >>> c
    Link(1, Link(1, Link(3, Link(3, Link(2)))))
    """
    def helper(vals, counts, result):
        if not vals or not counts:
            return result.rest
        end = result
        while end.rest:
            end = end.rest
        for _ in range(counts[0]):
            end.rest = Link(vals[0])
            end = end.rest
        return helper(vals[1:], counts[1:], result)
    return helper(vals, counts, Link(None))


# 2022 sp MT2
def roll(self):
    value = self.values[self.index]
    self.index = (self.index + 1) % len(self.values)
    return value

def next_player(self):
    yield from self.players
    yield from self.next_player()

def get_scores_except(self, player):
    return [pl.score for pl in self.players if pl != player]

def roll_dice(self, num_rolls):
    outcomes = [self.dice.roll() for x in range(num_rolls)]
    ones = [outcome == 1 for outcome in outcomes]
    return 1 if any(ones) else sum(outcomes)

def play(self):
    player_gen = self.next_player()
    while max(self.get_scores()) < self.goal:
        player = next(player_gen)
        other_scores = self.get_scores_except(player)
        num_rolls = player.strategy(player.score, other_scores)
        outcome = self.roll_dice(num_rolls)
        player.score += outcome
    return self.get_scores()

def __init__(self, values, when_broken):
    super().__init__(values)
    self.when_broken = when_broken
    self.is_broken = False

def roll(self):
    if self.is_broken:
        self.is_broken = not self.is_broken
        return self.when_broken
    else:
        self.is_broken = not self.is_broken
        return super().roll()
    

# Fall 2020
def __init__(self, s):
    self.n = len(s)
    self.common = most_common(s)
    self.others = {i: s[i] for i in range(self.n) if s[i] != self.common}

def item(self, i):
    if i >= self.n:
        return 'out of range'
    elif i in self.others:
        return self.others[i]
    else:
        return self.common
    
def items(self):
    return [self.item(i) for i in range(self.n)]


# Fall 2019
def __str__(self):
    return self.edit.apply(str(self.previous))

def apply(self, t):
    return t[:self.i] + self.c + t[self.i:]

def apply(self, t):
    return t[:self.i] + t[self.i + self.c]


# Fall 2020
def wins(states, k):
    if k <= 0:
        yield Link.empty
    if states:
        first = states[0].electors
        for win in wins(states[1:], k - first):
            yield Link(states[0].code, win)
        yield from wins(states[1:], k)

def must_win(states, k):
    def contains(s, x):
        return (s is not Link.empty) and (x == s.first or contains(s.rest, x))
    return [s.code for s in states if all([contains(w, s.code) for w in wins(states, k)])]

def is_minimal(state_codes, k):
    votes_in_favor = [State.electors[i] for i in state_codes]
    total_possible_votes = sum(State.electors.values())
    def win_margin(n):
        return n - (total_possible_votes - n)
    if win_margin(sum(votes_in_favor)) < k:
        return False
    in_favor_no_smallest = sum(votes_in_favor) - min(votes_in_favor)
    return win_margin(in_favor_no_smallest) < k


# Fall 2018
def replace(s, t, i, j):
    if i > 1:
        replace(s.rest, t, i - 1, j - 1)
    else:
        for k in range(j - i):
            s.rest = s.rest.rest
        end = t
        while end.rest:
            end = end.rest
        s.rest, end.rest = t, s.rest


# Spring 2017
def link_insert(lnklst, value, before):
    if not lnklst:
        return Link.empty
    elif lnklst.first == before:
        return Link(value, lnklst)
    else:
        return Link(lnklst.first, link_insert(lnklst.rest, value, before))



class Link:
    """A linked list.

    >>> s = Link(1)
    >>> s.first
    1
    >>> s.rest is Link.empty
    True
    >>> s = Link(2, Link(3, Link(4)))
    >>> s.first = 5
    >>> s.rest.first = 6
    >>> s.rest.rest = Link.empty
    >>> s                                    # Displays the contents of repr(s)
    Link(5, Link(6))
    >>> s.rest = Link(7, Link(Link(8, Link(9))))
    >>> s
    Link(5, Link(7, Link(Link(8, Link(9)))))
    >>> print(s)                             # Prints str(s)
    <5 7 <8 9>>
    """
    empty = ()

    def __init__(self, first, rest=empty):
        assert rest is Link.empty or isinstance(rest, Link)
        self.first = first
        self.rest = rest

    def __repr__(self):
        if self.rest is not Link.empty:
            rest_repr = ', ' + repr(self.rest)
        else:
            rest_repr = ''
        return 'Link(' + repr(self.first) + rest_repr + ')'

    def __str__(self):
        string = '<'
        while self.rest is not Link.empty:
            string += str(self.first) + ' '
            self = self.rest
        return string + str(self.first) + '>'

