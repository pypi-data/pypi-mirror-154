def nth(n):
    suffixes = {1: "st", 2: "nd", 3: "rd"}

    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = suffixes.get(n % 10, "th")

    return f"{n}{suffix}"
