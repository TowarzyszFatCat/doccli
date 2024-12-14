def gen_rating(score):
    bar = '●' * (score // 10) + '○' * (10 - score // 10)
    return f"Średnia ocen: [{bar}] {score}%"
