# import requests
# import os
# from datetime import datetime

# TOKEN = os.environ.get("GH_TOKEN")
# USERNAME = "susovanpatra00"

# year = datetime.now().year
# FROM_YEAR = f"{year}-01-01T00:00:00Z"
# TO_YEAR = f"{year}-12-31T23:59:59Z"

# headers = {"Authorization": f"Bearer {TOKEN}"}

# # Get GraphQL stats for current year
# def get_graphql_stats():
#     query = """
#     query($username: String!, $from: DateTime!, $to: DateTime!) {
#       user(login: $username) {
#         contributionsCollection(from: $from, to: $to) {
#           totalCommitContributions
#           totalPullRequestContributions
#           totalPullRequestReviewContributions
#           totalIssueContributions
#         }
#       }
#     }
#     """
#     variables = {
#         "username": USERNAME,
#         "from": FROM_YEAR,
#         "to": TO_YEAR
#     }
#     response = requests.post(
#         "https://api.github.com/graphql",
#         json={"query": query, "variables": variables},
#         headers=headers
#     )
#     data = response.json()
#     return data["data"]["user"]["contributionsCollection"]

# # Get all-time PR and review stats
# def get_alltime_prs_reviews():
#     # Get all PRs
#     prs = 0
#     page = 1
#     while True:
#         response = requests.get(
#             f"https://api.github.com/search/issues",
#             headers=headers,
#             params={
#                 "q": f"author:{USERNAME} type:pr",
#                 "per_page": 100,
#                 "page": page
#             }
#         )
#         data = response.json()
#         prs += len(data.get("items", []))
#         if len(data.get("items", [])) < 100:
#             break
#         page += 1
    
#     # Get all reviews (approximate via search)
#     reviews = 0
#     page = 1
#     while True:
#         response = requests.get(
#             f"https://api.github.com/search/issues",
#             headers=headers,
#             params={
#                 "q": f"reviewed-by:{USERNAME} type:pr",
#                 "per_page": 100,
#                 "page": page
#             }
#         )
#         data = response.json()
#         reviews += len(data.get("items", []))
#         if len(data.get("items", [])) < 100:
#             break
#         page += 1
    
#     return prs, reviews

# # Get all repositories
# def get_all_repos():
#     repos = []
#     page = 1
#     while True:
#         response = requests.get(
#             f"https://api.github.com/user/repos",
#             headers=headers,
#             params={"per_page": 100, "page": page, "affiliation": "owner,collaborator,organization_member"}
#         )
#         batch = response.json()
#         if not batch:
#             break
#         repos.extend(batch)
#         page += 1
#     return repos

# # Count commits in a repository
# def count_commits_in_repo(owner, repo_name, since=None, until=None):
#     try:
#         params = {"author": USERNAME, "per_page": 1}
#         if since:
#             params["since"] = since
#         if until:
#             params["until"] = until
            
#         response = requests.get(
#             f"https://api.github.com/repos/{owner}/{repo_name}/commits",
#             headers=headers,
#             params=params
#         )
        
#         if 'Link' in response.headers:
#             links = response.headers['Link']
#             if 'last' in links:
#                 last_page = int(links.split('page=')[-1].split('>')[0])
#                 return last_page
        
#         return len(response.json()) if response.status_code == 200 else 0
#     except:
#         return 0

# print("Fetching repositories...")
# repos = get_all_repos()

# print("Fetching PR and review stats...")
# graphql_stats = get_graphql_stats()
# alltime_prs, alltime_reviews = get_alltime_prs_reviews()

# total_commits_year = 0
# total_commits_alltime = 0

# print(f"\nCounting commits in {len(repos)} repositories...\n")
# print(f"{'Repository':<50} {'2025':<10} {'All-Time':<10}")
# print("=" * 70)

# for repo in repos:
#     owner = repo['owner']['login']
#     name = repo['name']
    
#     commits_year = count_commits_in_repo(owner, name, FROM_YEAR, TO_YEAR)
#     commits_alltime = count_commits_in_repo(owner, name)
    
#     if commits_alltime > 0:
#         repo_full_name = f"{owner}/{name}"
#         print(f"{repo_full_name:<50} {commits_year:<10} {commits_alltime:<10}")
#         total_commits_year += commits_year
#         total_commits_alltime += commits_alltime

# print("=" * 70)
# print(f"{'TOTAL':<50} {total_commits_year:<10} {total_commits_alltime:<10}")

# print("\n" + "=" * 70)
# print(f"{'GITHUB STATS SUMMARY':<50} {year:<10} {'All-Time':<10}")
# print("=" * 70)
# print(f"{'Commits':<50} {total_commits_year:<10} {total_commits_alltime:<10}")
# print(f"{'Pull Requests':<50} {graphql_stats['totalPullRequestContributions']:<10} {alltime_prs:<10}")
# print(f"{'Code Reviews':<50} {graphql_stats['totalPullRequestReviewContributions']:<10} {alltime_reviews:<10}")
# print(f"{'Issues':<50} {graphql_stats['totalIssueContributions']:<10} {'N/A':<10}")
# print("=" * 70)




import requests
import os
from datetime import datetime

TOKEN = os.environ.get("GH_TOKEN")
USERNAME = "susovanpatra00"

year = datetime.now().year
FROM_YEAR = f"{year}-01-01T00:00:00Z"
TO_YEAR = f"{year}-12-31T23:59:59Z"

headers = {"Authorization": f"Bearer {TOKEN}"}

# Get GraphQL stats for current year
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
    variables = {
        "username": USERNAME,
        "from": FROM_YEAR,
        "to": TO_YEAR
    }
    response = requests.post(
        "https://api.github.com/graphql",
        json={"query": query, "variables": variables},
        headers=headers
    )
    data = response.json()
    return data["data"]["user"]["contributionsCollection"]

# Get all-time PR and review stats
def get_alltime_prs_reviews():
    prs = 0
    page = 1
    while True:
        response = requests.get(
            f"https://api.github.com/search/issues",
            headers=headers,
            params={
                "q": f"author:{USERNAME} type:pr",
                "per_page": 100,
                "page": page
            }
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
            params={
                "q": f"reviewed-by:{USERNAME} type:pr",
                "per_page": 100,
                "page": page
            }
        )
        data = response.json()
        reviews += len(data.get("items", []))
        if len(data.get("items", [])) < 100:
            break
        page += 1
    
    return prs, reviews

# Get all repositories
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

# Count commits in a repository
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

print("Fetching repositories...")
repos = get_all_repos()

print("Fetching PR and review stats...")
graphql_stats = get_graphql_stats()
alltime_prs, alltime_reviews = get_alltime_prs_reviews()

total_commits_year = 0
total_commits_alltime = 0

print(f"Counting commits in {len(repos)} repositories...")

for repo in repos:
    owner = repo['owner']['login']
    name = repo['name']
    
    commits_year = count_commits_in_repo(owner, name, FROM_YEAR, TO_YEAR)
    commits_alltime = count_commits_in_repo(owner, name)
    
    total_commits_year += commits_year
    total_commits_alltime += commits_alltime

# Generate markdown stats
stats_markdown = f"""## 📊 GitHub Stats

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
<img src="https://github-readme-streak-stats.herokuapp.com/?user=susovanpatra00&theme=tokyonight" alt="GitHub Streak"/>

### 📊 Language Distribution
<img height="180em" src="https://github-readme-stats.vercel.app/api/top-langs/?username=susovanpatra00&layout=compact&langs_count=8&theme=tokyonight"/>

</div>

*Last updated: {datetime.now().strftime('%B %d, %Y at %H:%M UTC')}*
"""

print("\n" + "="*70)
print("STATS GENERATED SUCCESSFULLY")
print("="*70)
print(stats_markdown)

# Save to file
with open('STATS.md', 'w') as f:
    f.write(stats_markdown)

print("\n✅ Stats saved to STATS.md")