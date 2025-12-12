import requests
import os
from datetime import datetime

TOKEN = os.environ.get("GH_TOKEN")
USERNAME = "susovanpatra00"

year = datetime.now().year
FROM_YEAR = f"{year}-01-01T00:00:00Z"
TO_YEAR = f"{year}-12-31T23:59:59Z"

headers = {"Authorization": f"Bearer {TOKEN}"}

def get_graphql_stats():
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
    variables = {"username": USERNAME, "from": FROM_YEAR, "to": TO_YEAR}
    response = requests.post(
        "https://api.github.com/graphql",
        json={"query": query, "variables": variables},
        headers=headers
    )
    data = response.json()
    return data["data"]["user"]["contributionsCollection"]

def get_alltime_prs_reviews():
    prs = 0
    page = 1
    while True:
        response = requests.get(
            f"https://api.github.com/search/issues",
            headers=headers,
            params={"q": f"author:{USERNAME} type:pr", "per_page": 100, "page": page}
        )
        data = response.json()
        prs += len(data.get("items", []))
        if len(data.get("items", [])) < 100:
            break
        page += 1
    
    reviews = 0
    page = 1
    while True:
        response = requests.get(
            f"https://api.github.com/search/issues",
            headers=headers,
            params={"q": f"reviewed-by:{USERNAME} type:pr", "per_page": 100, "page": page}
        )
        data = response.json()
        reviews += len(data.get("items", []))
        if len(data.get("items", [])) < 100:
            break
        page += 1
    
    return prs, reviews

def get_all_repos():
    repos = []
    page = 1
    while True:
        response = requests.get(
            f"https://api.github.com/user/repos",
            headers=headers,
            params={"per_page": 100, "page": page, "affiliation": "owner,collaborator,organization_member"}
        )
        batch = response.json()
        if not batch:
            break
        repos.extend(batch)
        page += 1
    return repos

def count_commits_in_repo(owner, repo_name, since=None, until=None):
    try:
        params = {"author": USERNAME, "per_page": 1}
        if since:
            params["since"] = since
        if until:
            params["until"] = until
            
        response = requests.get(
            f"https://api.github.com/repos/{owner}/{repo_name}/commits",
            headers=headers,
            params=params
        )
        
        if 'Link' in response.headers:
            links = response.headers['Link']
            if 'last' in links:
                last_page = int(links.split('page=')[-1].split('>')[0])
                return last_page
        
        return len(response.json()) if response.status_code == 200 else 0
    except:
        return 0

print("🔄 Fetching GitHub stats...")

repos = get_all_repos()
graphql_stats = get_graphql_stats()
alltime_prs, alltime_reviews = get_alltime_prs_reviews()

total_commits_year = 0
total_commits_alltime = 0

for repo in repos:
    owner = repo['owner']['login']
    name = repo['name']
    
    commits_year = count_commits_in_repo(owner, name, FROM_YEAR, TO_YEAR)
    commits_alltime = count_commits_in_repo(owner, name)
    
    total_commits_year += commits_year
    total_commits_alltime += commits_alltime

# Generate the stats section
stats_section = f"""## 📊 GitHub Stats

<div align="center">

### 📈 Contribution Statistics

| Metric | {year} | All Time |
|--------|--------|----------|
| 💻 **Total Commits** | **{total_commits_year}** | **{total_commits_alltime}** |
| 🔀 **Pull Requests** | **{graphql_stats['totalPullRequestContributions']}** | **{alltime_prs}** |
| 👀 **Code Reviews** | **{graphql_stats['totalPullRequestReviewContributions']}** | **{alltime_reviews}** |
| 🐛 **Issues Created** | **{graphql_stats['totalIssueContributions']}** | - |

<br/>

### 🔥 Current Streak
<img src="https://github-readme-streak-stats.herokuapp.com/?user={USERNAME}&theme=tokyonight" alt="GitHub Streak"/>

### 📊 Language Distribution
<img height="180em" src="https://github-readme-stats.vercel.app/api/top-langs/?username={USERNAME}&layout=compact&langs_count=8&theme=tokyonight"/>

</div>

*Last updated: {datetime.utcnow().strftime('%B %d, %Y at %H:%M UTC')}*"""

# Read the profile README
readme_path = '../profile-repo/README.md'
with open(readme_path, 'r') as f:
    readme_content = f.read()

# Replace the stats section
start_marker = "## 📊 GitHub Stats"
end_marker = "---"

# Find the stats section and replace it
start_idx = readme_content.find(start_marker)
if start_idx != -1:
    # Find the next "---" after the stats section
    end_idx = readme_content.find(end_marker, start_idx)
    if end_idx != -1:
        # Replace the section
        new_readme = readme_content[:start_idx] + stats_section + "\n\n" + readme_content[end_idx:]
    else:
        print("❌ Could not find end marker")
        exit(1)
else:
    print("❌ Could not find stats section")
    exit(1)

# Write back to the README
with open(readme_path, 'w') as f:
    f.write(new_readme)

print("✅ README updated successfully!")
print(f"📊 Stats: {total_commits_alltime} commits, {alltime_prs} PRs, {alltime_reviews} reviews")