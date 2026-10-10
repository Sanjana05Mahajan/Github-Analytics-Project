
import requests
from config import BASE_URL


def get_repository(owner, repo):
    # Validate empty inputs
    owner = owner.strip() if owner else ""
    repo = repo.strip() if repo else ""

    if not owner or not repo:
        return None, "Owner and repository name are required."

    # Prevent invalid URL characters in input
    if "/" in owner or "/" in repo or " " in owner or " " in repo:
        return None, "Invalid owner or repository name."

    url = f"{BASE_URL}/repos/{owner}/{repo}"

    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            return response.json(), None

        if response.status_code == 404:
            return None, "Repository not found. Check the owner and name."

        if response.status_code == 403:
            if response.headers.get("X-RateLimit-Remaining") == "0":
                return None, "GitHub API rate limit reached. Try again later."
            return None, "GitHub denied the request. Please try again later."

        if response.status_code == 429:
            return None, "Too many requests. Try again later."

        return None, f"GitHub API returned status {response.status_code}."

    except requests.Timeout:
        return None, "GitHub request timed out. Please try again."

    except requests.ConnectionError:
        return None, "Unable to connect to GitHub. Check your internet connection."

    except requests.RequestException:
        return None, "A GitHub API request error occurred."

    except ValueError:
        return None, "GitHub returned an invalid response."
