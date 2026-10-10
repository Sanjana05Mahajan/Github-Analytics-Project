
from flask import Flask, render_template, request, jsonify

from github_api import get_repository
from analytics import calculate_health_score
from database import create_database, save_repository, get_history

app = Flask(__name__)

# Create the database table when the application starts.
create_database()


def api_error_response(error):
    """Return an appropriate HTTP status code for API errors."""
    message = error or "Unable to fetch repository data."
    lower_message = message.lower()

    if "not found" in lower_message:
        code = 404
    elif "required" in lower_message or "invalid" in lower_message:
        code = 400
    elif "rate limit" in lower_message or "too many requests" in lower_message:
        code = 429
    else:
        code = 502

    return jsonify({"error": message}), code


# Home Page
@app.route("/")
def home():
    return render_template("index.html")


# Search Repository
@app.route("/search", methods=["POST"])
def search():
    owner_input = request.form.get("owner", "").strip()
    repo_input = request.form.get("repo", "").strip()

    if not owner_input or not repo_input:
        return render_template(
            "dashboard.html",
            error="Please enter both repository owner and repository name."
        ), 400

    data, error = get_repository(owner_input, repo_input)

    if error:
        return render_template("dashboard.html", error=error), 400 if "required" in error.lower() or "invalid" in error.lower() else 502

    stars = data.get("stargazers_count", 0)
    forks = data.get("forks_count", 0)
    issues = data.get("open_issues_count", 0)

    description = data.get("description") or "No description available"
    language = data.get("language") or "Not Available"
    watchers = data.get("watchers_count", 0)
    created = data.get("created_at", "")
    updated = data.get("updated_at", "")
    default_branch = data.get("default_branch", "")

    owner = data.get("owner", {}).get("login", owner_input)
    avatar = data.get("owner", {}).get("avatar_url", "")

    license_data = data.get("license")
    license_name = license_data.get("name", "No License") if license_data else "No License"

    visibility = data.get("visibility", "public")
    size = data.get("size", 0)

    score, status = calculate_health_score(stars, forks, issues)

    save_repository(
        owner,
        data.get("name", repo_input),
        stars,
        forks,
        issues,
        language,
        score,
        status
    )

    return render_template(
        "dashboard.html",
        repo=data,
        score=score,
        status=status,
        description=description,
        language=language,
        watchers=watchers,
        created=created,
        updated=updated,
        default_branch=default_branch,
        owner=owner,
        avatar=avatar,
        license_name=license_name,
        visibility=visibility,
        size=size
    )


# Search History
@app.route("/history")
def history():
    history_records = get_history()
    return render_template("history.html", history=history_records)


# Compare Page
@app.route("/compare", methods=["GET"])
def compare_page():
    return render_template("compare.html", repo1=None, repo2=None)


# Compare Repositories
@app.route("/compare", methods=["POST"])
def compare():
    owner1 = request.form.get("owner1", "").strip()
    repo_name1 = request.form.get("repo1", "").strip()
    owner2 = request.form.get("owner2", "").strip()
    repo_name2 = request.form.get("repo2", "").strip()

    if not all([owner1, repo_name1, owner2, repo_name2]):
        return render_template(
            "compare.html",
            error="Please enter both owners and both repository names.",
            repo1=None,
            repo2=None
        ), 400

    repo1, error1 = get_repository(owner1, repo_name1)
    repo2, error2 = get_repository(owner2, repo_name2)

    if error1 or error2:
        return render_template(
            "compare.html",
            error=error1 or error2,
            repo1=None,
            repo2=None
        ), 400 if any(
            message and ("required" in message.lower() or "invalid" in message.lower())
            for message in [error1, error2]
        ) else 502

    score1, status1 = calculate_health_score(
        repo1.get("stargazers_count", 0),
        repo1.get("forks_count", 0),
        repo1.get("open_issues_count", 0)
    )

    score2, status2 = calculate_health_score(
        repo2.get("stargazers_count", 0),
        repo2.get("forks_count", 0),
        repo2.get("open_issues_count", 0)
    )

    return render_template(
        "compare.html",
        repo1=repo1,
        repo2=repo2,
        score1=score1,
        score2=score2,
        status1=status1,
        status2=status2
    )


# REST API: Repository Details
@app.route("/api/repository/<owner>/<repo>", methods=["GET"])
def api_repository(owner, repo):
    data, error = get_repository(owner, repo)

    if error:
        return api_error_response(error)

    return jsonify({
        "owner": data.get("owner", {}).get("login"),
        "repository": data.get("name"),
        "full_name": data.get("full_name"),
        "description": data.get("description"),
        "stars": data.get("stargazers_count", 0),
        "forks": data.get("forks_count", 0),
        "open_issues": data.get("open_issues_count", 0),
        "language": data.get("language"),
        "url": data.get("html_url")
    }), 200


# REST API: Repository Metrics
@app.route("/api/repository/<owner>/<repo>/metrics", methods=["GET"])
def api_repository_metrics(owner, repo):
    data, error = get_repository(owner, repo)

    if error:
        return api_error_response(error)

    stars = data.get("stargazers_count", 0)
    forks = data.get("forks_count", 0)
    issues = data.get("open_issues_count", 0)

    score, status = calculate_health_score(stars, forks, issues)

    return jsonify({
        "repository": data.get("full_name"),
        "stars": stars,
        "forks": forks,
        "open_issues": issues,
        "health_score": score,
        "status": status
    }), 200


if __name__ == "__main__":
    app.run(debug=True)
