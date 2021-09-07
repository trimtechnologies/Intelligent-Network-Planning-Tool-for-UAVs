def percentage(percent: float, whole: float) -> float:
    return (percent * whole) / 100.0


height = 56

percentage15 = percentage(15, height)
percentage30 = percentage(30, height)

print(height - percentage30)
print(height - percentage15)
print(height)
print(height + percentage15)
print(height + percentage30)
