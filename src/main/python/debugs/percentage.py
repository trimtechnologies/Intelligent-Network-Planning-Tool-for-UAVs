def percentage(percent: float, whole: float) -> float:
    return (percent * whole) / 100.0


altura = 56

percentage15 = percentage(15, altura)
percentage30 = percentage(30, altura)

print(altura - percentage30)
print(altura - percentage15)
print(altura)
print(altura + percentage15)
print(altura + percentage30)
