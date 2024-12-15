def gen_rating(score):
    if isinstance(score, int):
        bar = '●' * (score // 10) + '○' * (10 - score // 10)
        return f"[{bar}] | {score}%"
    else:
        return 'Średnia ocen: [Brak]'
