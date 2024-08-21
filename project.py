from typing import List, Dict

from act_one import act_one, intro_text
from act_two import act_two
from act_three import act_three


def main():
    cache: List[Dict[str, str]] = []
    intro_text()
    cache = act_one(cache)
    print()
    cache, basement_visit, solve_code = act_two(cache)
    print()
    act_three(cache, basement_visit, solve_code)


if __name__ == "__main__":
    main()
