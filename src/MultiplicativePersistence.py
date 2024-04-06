"""
Minimum Multiplicative Persistences.

https://oeis.org/A003001

Copyright 2020 Alex Blandin
"""

from functools import reduce
from itertools import combinations_with_replacement
from operator import mul
from time import time

# Helper Functions


def tf(func, *args, **kwargs):  # time func  # noqa: ANN001, ANN002, ANN003, ANN201, D103
  start = time()
  r = func(*args, **kwargs)
  end = time()
  print(func.__name__, human_time(end - start))
  return r


# Convert single digit to 2
def digit2(x: int):  # noqa: ANN201, D103
  value = x << 1
  return (
    "0001020304050607080910111213141516171819"
    "2021222324252627282930313233343536373839"
    "4041424344454647484950515253545556575859"
    "6061626364656667686970717273747576777879"
    "8081828384858687888990919293949596979899"[value : value + 2]
  )


# Convert an int to a str 2 digits at a time, currently really slow bc str copies etc, do in a bytearray and use "pointer math" kinda  # noqa: E501
def int_to_str(x: int):  # noqa: ANN201, D103
  buf = []
  while x >= 100:  # noqa: PLR2004
    x, m = divmod(x, 100)
    buf.append(digit2(m))
  if x < 10:  # noqa: PLR2004
    buf.append(chr(ord("0") + x))
  else:
    buf.append(digit2(x))
  return "".join(reversed(buf))


def human_time(t: float, *, seconds: bool = True) -> str:  # dumb but "decently" formatted  # noqa: D103
  return (
    f"{int(t // 60)}m {human_time((int(t) % 60) + (t - int(t)), seconds=True)}"
    if t > 60  # noqa: PLR2004
    else f"{t:.3f}s"
    if t > 0.1 and seconds  # noqa: PLR2004
    else f"{t * 1000:.3f}ms"
    if t > 0.0001  # noqa: PLR2004
    else f"{t * 1000000:.3f}us"
  )


# Method demonstrated below, as a function
# goal = how many steps
# until = maximum length of the number in base 10
def persistence(goal=11, until=64) -> str:  # noqa: ANN001, D103
  for ndigits in range(2, until + 1):  # number of digits
    for front in ["26", "2", "3", "6", ""]:
      backfill = ndigits - len(front)
      for back in combinations_with_replacement("789", backfill):  # fill the rest
        reduced = front + "".join(back)
        steps = 0
        while len(reduced) > 1:  # multiply digits together
          reduced = str(reduce(mul, map(int, reduced), 1))
          steps += 1
        if steps == goal:
          return f"p({goal}) = {front}{"".join(back)}"
  return f"Sorry, nothing under {until + 1} digits"


# Above method but doing the reduce mul map int manually, so a fair bit faster
def faststr(goal=11, until=64) -> str:  # noqa: ANN001, D103
  for ndigits in range(2, until + 1):  # number of digits
    for front in ["26", "2", "3", "6", ""]:
      backfill = ndigits - len(front)
      for back in combinations_with_replacement("789", backfill):  # fill the rest
        reduced = front + "".join(back)
        steps = 0
        while len(reduced) > 1:  # multiply digits together
          acc = 1
          for digit in reduced:
            acc *= ord(digit) - 48
          reduced = str(acc)  # 48 == ord("0")
          steps += 1
        if steps == goal:
          return f"p({goal}) = {front}{"".join(back)}"
  return f"Sorry, nothing under {until + 1} digits"


def faststr2(goal=11, until=64) -> str:  # noqa: ANN001, D103
  for ndigits in range(2, until + 1):  # number of digits
    for front in ["26", "2", "3", "6", ""]:
      backfill = ndigits - len(front)
      for back in combinations_with_replacement("789", backfill):  # fill the rest
        reduced = front + "".join(back)
        steps = 0
        while len(reduced) > 1:  # multiply digits together
          acc = 1
          for digit in reduced:
            acc *= ord(digit) - 48
          reduced = int_to_str(acc)  # 48 == ord("0")
          steps += 1
        if steps == goal:
          return f"p({goal}) = {front}{"".join(back)}"
  return f"Sorry, nothing under {until + 1} digits"


# The same method but using integers rather than strings, gets real slow with big numbers
def fastint(goal=11, until=64) -> str:  # noqa: ANN001, D103
  for ndigits in range(2, until + 1):
    for front in ["26", "2", "3", "6", ""]:
      backfill = ndigits - len(front)
      for back in combinations_with_replacement("789", backfill):
        reduced = int(f"{front}{"".join(back)}")
        steps = 0
        while reduced > 9:  # noqa: PLR2004
          acc = 1
          while reduced > 0:  # the slow part for big N, could try more "fixed function" divmod 10 using bitshifts
            reduced, mod = divmod(reduced, 10)
            # ...
            acc *= mod
          reduced = acc
          steps += 1
        if steps == goal:
          return f"p({goal}) = {front}{"".join(back)}"
  return f"Sorry, nothing under {until + 1} digits"


"""
cpython 3.10.0
  persistence 4m 32.478s
  faststr 4m 25.585s
  faststr2 7m 29.267s

cpython 3.10.0 + pyjion 1.0.0 + .NET 6.0.0
  persistence 4m 24.683s
  faststr 5m 1.913s
  faststr2 9m 4.650s

pypy 3.7.4 (7.3.2-alpha0)
  persistence 1m 48.924s
  faststr 1m 41.711s
  faststr2 3m 28.306s
"""


def main() -> None:  # noqa: D103
  print()
  print("Generating multiplicative persistences")
  print("See https://youtu.be/Wim9WJeDTHQ")
  print("More info @ https://oeis.org/A003001")
  print("Source @ https://repl.it/@alexblandin/Multiplicative-Persistence")
  print()

  low = 3  # lowest persistance
  high = 12  # 12 and higher are unknown but suspected to NOT have solutions
  until = 200  # pypy exhausts in 43s, cpython in 2m 26s for goal=12
  for goal in range(low, high + 1):
    print(f"Finding the smallest number with persistence {goal}...")
    start = time()
    for ndigits in range(2, until + 1):  # number of digits
      for front in ["26", "2", "3", "6", ""]:
        backfill = ndigits - len(front)
        for back in combinations_with_replacement("789", backfill):  # fill the rest
          reduced = int(f"{front}{"".join(back)}")
          steps = 0
          while reduced > 9:  # noqa: PLR2004
            acc = 1
            while reduced > 0:
              reduced, mod = divmod(reduced, 10)
              acc *= mod
            reduced = acc
            steps += 1
          if steps == goal:
            end = time()  # found it
            reduced = front + "".join(back)
            print(f"{reduced} has persistence {goal}, via:")
            while len(reduced) > 1:
              reduced = str(reduce(mul, [int(digit) for digit in reduced], 1))
              print(reduced, end="\n" if len(reduced) > 1 else "")
            print(f", {steps} steps found in {human_time(end - start)}\n")
            break
        else:
          continue
        break
      else:
        continue
      break
    else:
      end = time()
      print(f"Nothing with (up to) {until} digits for {goal} steps, used {human_time(end - start)}\n")


if __name__ == "__main__":
  # main()
  goal, until = 12, 200
  tf(persistence, goal, until)
  tf(faststr, goal, until)
  tf(faststr2, goal, until)
  # tf(fastint, goal, until)
