import requests
import os
from datetime import datetime

# ================= CONFIG =================
TOKEN = os.environ.get("GH_TOKEN")
USERNAME = "susovanpatra00"

if not TOKEN:
    raise RuntimeError("❌ GH_TOKEN is not set")

year = datetime.utcnow().year
FROM_YEAR = f"{year}-01-01T00:00:00Z"
TO_YEAR = f"{year}-12-31T23:59:59Z"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# ================= GRAPHQL =================
def get_yearly_contribution_stats():
    query = """
    query($username: String!, $from: DateTime!, $to: DateTime!) {
      user(login: $username) {
        contributionsCollection(from: $from, to: $to) {
          totalCommitContributions
          totalPullRequestContributions
          totalPullRequestReviewContributions
          totalIssueContributions
        }
      }
    }
    """

    variables = {
        "username": USERNAME,
        "from": FROM_YEAR,
        "to": TO_YEAR
    }

    response = requests.post(
        "https://api.github.com/graphql",
        headers=HEADERS,
        json={"query": query, "variables": variables},
        timeout=15
    )

    if response.status_code != 200:
        raise RuntimeError(f"❌ GraphQL failed: {response.text}")

    data = response.json()

    if "errors" in data:
        raise RuntimeError(f"❌ GraphQL error: {data['errors']}")

    return data["data"]["user"]["contributionsCollection"]

# ================= MAIN =================
print("🔄 Fetching GitHub yearly stats...")

stats = get_yearly_contribution_stats()

year_commits = stats["totalCommitContributions"]
prs = stats["totalPullRequestContributions"]
reviews = stats["totalPullRequestReviewContributions"]
issues = stats["totalIssueContributions"]

# ================= README SECTION =================
stats_section = f"""
<div align="center">

### 📈 Contribution Statistics ({year})

| Metric | Count |
|------|------|
| 💻 **Commits** | **{year_commits}** |
| 🔀 **Pull Requests** | **{prs}** |
| 👀 **Code Reviews** | **{reviews}** |
| 🐛 **Issues Created** | **{issues}** |

<br/>

### 🔥 Current Streak
<img src="https://github-readme-streak-stats.herokuapp.com/?user={USERNAME}&theme=tokyonight&hide_border=true&cache_seconds=21600"/>

### 📊 Language Distribution
<img height="180em" src="https://github-readme-stats.vercel.app/api/top-langs/?username={USERNAME}&layout=compact&langs_count=8&theme=tokyonight"/>

</div>

*Last updated: {datetime.utcnow().strftime('%B %d, %Y at %H:%M UTC')}*
"""


# ================= UPDATE README =================
readme_path = "../profile-repo/README.md"

with open(readme_path, "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "<!-- GITHUB_STATS_START -->"
end_marker = "<!-- GITHUB_STATS_END -->"

start = content.find(start_marker)
end = content.find(end_marker)

if start == -1 or end == -1:
    raise RuntimeError("❌ GitHub stats markers not found in README")

end += len(end_marker)

new_content = (
    content[:start]
    + f"{start_marker}\n\n## 📊 GitHub Stats\n\n"
    + stats_section
    + f"\n\n{end_marker}"
    + content[end:]
)

with open(readme_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("✅ README updated successfully")
print(f"📊 {year}: {year_commits} commits, {prs} PRs, {reviews} reviews")
