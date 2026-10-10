def calculate_health_score(stars, forks, issues):

    score = 50

    score += min(stars // 1000, 25)

    score += min(forks // 500, 15)

    score += min(issues // 100, 10)

    score = min(score, 100)

    if score >= 85:
        status = "Excellent"

    elif score >= 70:
        status = "Good"

    elif score >= 50:
        status = "Average"

    else:
        status = "Needs Improvement"

    return score, status