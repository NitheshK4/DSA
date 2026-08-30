#!/usr/bin/env python3
"""
LeetCode Repository & DSA README Auto-Sync Script
Author: Nithesh K (@NitheshK4 / LeetCode: Nithesh_007)

This script automatically scans all problem folders in the repository,
enriches problem metadata using LeetCode's GraphQL API (with smart caching & fallback),
fetches real-time user stats, categorizes problems by topic,
and generates a comprehensive, professional, and aesthetic README.md.
"""

import os
import re
import json
import ssl
import urllib.request
from datetime import datetime, timezone
from collections import defaultdict, Counter

LEETCODE_USERNAME = "Nithesh_007"
GITHUB_USERNAME = "NitheshK4"
REPO_NAME = "DSA"
GRAPHQL_URL = "https://leetcode.com/graphql"
CACHE_FILE = ".problem_cache.json"

# Topic taxonomy order & icons
TOPIC_ORDER = [
    ("📊 Arrays & Hashing", "arrays-and-hashing"),
    ("⏳ Two Pointers & Sliding Window", "two-pointers-and-sliding-window"),
    ("🔍 Binary Search", "binary-search"),
    ("🥞 Stacks, Queues & Heaps", "stacks-queues-and-heaps"),
    ("🔗 Linked Lists", "linked-lists"),
    ("🌳 Trees & Binary Search Trees", "trees-and-bst"),
    ("🔲 Matrix", "matrix"),
    ("🔄 Backtracking & Recursion", "backtracking-and-recursion"),
    ("💡 Dynamic Programming & Greedy", "dynamic-programming-and-greedy"),
    ("⚡ Bit Manipulation", "bit-manipulation"),
    ("📐 Math & Logic", "math-and-logic"),
    ("🗄️ SQL & Databases", "sql-and-databases"),
    ("🧩 Miscellaneous", "miscellaneous"),
]

def get_ssl_context():
    try:
        return ssl._create_unverified_context()
    except Exception:
        return None

def fetch_leetcode_user_stats(username):
    """Fetch live submission statistics for the LeetCode profile."""
    query = """
    query getUserProfile($username: String!) {
      matchedUser(username: $username) {
        username
        submitStats: submitStatsGlobal {
          acSubmissionNum {
            difficulty
            count
            submissions
          }
        }
        profile {
          ranking
          reputation
          starRating
        }
      }
    }
    """
    req = urllib.request.Request(
        GRAPHQL_URL,
        data=json.dumps({"query": query, "variables": {"username": username}}).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)"
        }
    )
    ctx = get_ssl_context()
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            user = data.get("data", {}).get("matchedUser")
            if not user:
                return None
            stats = {
                "ranking": user.get("profile", {}).get("ranking", "N/A"),
                "total_solved": 0,
                "easy_solved": 0,
                "medium_solved": 0,
                "hard_solved": 0,
            }
            ac_list = user.get("submitStats", {}).get("acSubmissionNum", [])
            for item in ac_list:
                diff = item.get("difficulty")
                count = item.get("count", 0)
                if diff == "All":
                    stats["total_solved"] = count
                elif diff == "Easy":
                    stats["easy_solved"] = count
                elif diff == "Medium":
                    stats["medium_solved"] = count
                elif diff == "Hard":
                    stats["hard_solved"] = count
            return stats
    except Exception as e:
        print(f"Warning: Could not fetch LeetCode user stats: {e}")
        return None

def load_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_cache(cache):
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache, f, indent=2)
    except Exception as e:
        print(f"Warning: Could not save cache: {e}")

def fetch_problem_metadata(title_slug, cache):
    """Fetch problem tags and metadata from LeetCode GraphQL API."""
    if title_slug in cache:
        return cache[title_slug]

    query = """
    query questionData($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        questionId
        questionFrontendId
        title
        titleSlug
        difficulty
        topicTags {
          name
          slug
        }
      }
    }
    """
    req = urllib.request.Request(
        GRAPHQL_URL,
        data=json.dumps({"query": query, "variables": {"titleSlug": title_slug}}).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
        }
    )
    ctx = get_ssl_context()
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=8) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            q = data.get("data", {}).get("question")
            if q:
                res = {
                    "frontend_id": q.get("questionFrontendId"),
                    "title": q.get("title"),
                    "difficulty": q.get("difficulty"),
                    "tags": [t["name"] for t in q.get("topicTags", [])]
                }
                cache[title_slug] = res
                return res
    except Exception as e:
        print(f"Notice: Could not fetch metadata for {title_slug}: {e}")
    
    return None

def extract_slug_and_details_from_folder(folder_path, folder_name):
    readme_path = os.path.join(folder_path, "README.md")
    url = ""
    title = folder_name
    difficulty = "Easy"
    
    if os.path.exists(readme_path):
        try:
            with open(readme_path, "r", encoding="utf-8") as f:
                content = f.read()
                title_match = re.search(r"<h2><a href=\"([^\"]+)\">([^<]+)</a></h2>", content)
                if title_match:
                    url = title_match.group(1).strip()
                    title = title_match.group(2).strip()
                diff_match = re.search(r"Difficulty-([a-zA-Z]+)", content)
                if diff_match:
                    difficulty = diff_match.group(1).capitalize()
        except Exception:
            pass

    slug = ""
    if url:
        m = re.search(r"leetcode\.com/problems/([^/]+)", url)
        if m:
            slug = m.group(1)
    
    if not slug:
        parts = folder_name.split("-", 1)
        if len(parts) > 1 and parts[0].isdigit():
            slug = parts[1]
        else:
            slug = folder_name.lower().replace(" ", "-")

    if not url:
        url = f"https://leetcode.com/problems/{slug}/"

    # Solution files
    all_files = os.listdir(folder_path)
    sol_files = [f for f in all_files if f not in ("README.md", "Notes.md") and not f.startswith(".")]
    has_notes = "Notes.md" in all_files

    # Number from folder prefix
    num_match = re.match(r"^(\d+)", folder_name)
    raw_num = num_match.group(1) if num_match else ""

    return {
        "folder": folder_name,
        "raw_num": raw_num,
        "title": title,
        "slug": slug,
        "url": url,
        "difficulty": difficulty,
        "solutions": sorted(sol_files),
        "has_notes": has_notes,
    }

def categorize_problem(problem):
    tags = set(problem.get("tags", []))
    solutions = problem.get("solutions", [])
    title_lower = problem.get("title", "").lower()
    
    # 1. SQL
    if any(s.endswith(".sql") for s in solutions) or "Database" in tags:
        return "🗄️ SQL & Databases"
        
    # 2. Trees & BST
    if any(t in tags for t in ("Tree", "Binary Tree", "Binary Search Tree")):
        return "🌳 Trees & Binary Search Trees"
        
    # 3. Linked Lists
    if "Linked List" in tags or "Doubly-Linked List" in tags:
        return "🔗 Linked Lists"
        
    # 4. Binary Search
    if "Binary Search" in tags or "binary search" in title_lower:
        return "🔍 Binary Search"
        
    # 5. Stacks, Queues & Heaps
    if any(t in tags for t in ("Stack", "Monotonic Stack", "Queue", "Monotonic Queue", "Heap (Priority Queue)")):
        return "🥞 Stacks, Queues & Heaps"
        
    # 6. Dynamic Programming & Greedy
    if "Dynamic Programming" in tags or "Greedy" in tags:
        return "💡 Dynamic Programming & Greedy"
        
    # 7. Backtracking & Recursion
    if "Backtracking" in tags or "Recursion" in tags:
        return "🔄 Backtracking & Recursion"
        
    # 8. Bit Manipulation
    if "Bit Manipulation" in tags or "bit" in title_lower:
        return "⚡ Bit Manipulation"
        
    # 9. Matrix
    if "Matrix" in tags:
        return "🔲 Matrix"
        
    # 10. Two Pointers & Sliding Window
    if "Two Pointers" in tags or "Sliding Window" in tags:
        return "⏳ Two Pointers & Sliding Window"
        
    # 11. Math & Logic
    if "Math" in tags or "Game Theory" in tags or "Geometry" in tags or "Number Theory" in tags:
        return "📐 Math & Logic"
        
    # 12. Arrays & Hashing
    if any(t in tags for t in ("Array", "Hash Table", "Sorting", "String", "Prefix Sum", "Counting")):
        return "📊 Arrays & Hashing"
        
    return "🧩 Miscellaneous"

def get_difficulty_badge(difficulty):
    diff = difficulty.capitalize()
    if diff == "Easy":
        return "`🟢 Easy`"
    elif diff == "Medium":
        return "`🟡 Medium`"
    elif diff == "Hard":
        return "`🔴 Hard`"
    return f"`⚪ {diff}`"

def get_language_badge(filename):
    ext = os.path.splitext(filename)[1].lower()
    if ext == ".py":
        return "🐍 Python"
    elif ext == ".sql":
        return "🗄️ SQL"
    elif ext in (".cpp", ".cc", ".cxx"):
        return "⚡ C++"
    elif ext == ".java":
        return "☕ Java"
    elif ext == ".js":
        return "🟨 JS"
    elif ext == ".ts":
        return "🟦 TS"
    elif ext == ".go":
        return "🐹 Go"
    elif ext == ".rs":
        return "🦀 Rust"
    elif ext == ".c":
        return "🔵 C"
    return "📄 Code"

def generate_markdown(problems, user_stats):
    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    
    # Calculate counts
    repo_total = len(problems)
    diff_counts = Counter(p["difficulty"] for p in problems)
    easy_repo = diff_counts.get("Easy", 0)
    med_repo = diff_counts.get("Medium", 0)
    hard_repo = diff_counts.get("Hard", 0)
    
    lc_total = user_stats.get("total_solved", repo_total) if user_stats else repo_total
    lc_easy = user_stats.get("easy_solved", easy_repo) if user_stats else easy_repo
    lc_med = user_stats.get("medium_solved", med_repo) if user_stats else med_repo
    lc_hard = user_stats.get("hard_solved", hard_repo) if user_stats else hard_repo
    ranking = user_stats.get("ranking", "N/A") if user_stats else "N/A"
    
    # Group by topics
    topic_map = defaultdict(list)
    for p in problems:
        topic_map[p["topic"]].append(p)
        
    # Sort each group by problem ID (integer if possible)
    def parse_id(p):
        pid = p.get("frontend_id") or p.get("raw_num") or "99999"
        try:
            return int(pid)
        except ValueError:
            return 99999

    for t in topic_map:
        topic_map[t].sort(key=parse_id)

    # Markdown generation
    lines = []
    lines.append("<div align=\"center\">")
    lines.append("")
    lines.append("# 🚀 Data Structures & Algorithms")
    lines.append("")
    lines.append("### 💻 Curated LeetCode Solutions & Topic-wise Roadmap")
    lines.append("")
    lines.append(f"[![LeetCode Profile](https://img.shields.io/badge/LeetCode-{LEETCODE_USERNAME}-FFA116?style=for-the-badge&logo=leetcode&logoColor=black)](https://leetcode.com/u/{LEETCODE_USERNAME}/) ")
    lines.append(f"[![GitHub](https://img.shields.io/badge/GitHub-{GITHUB_USERNAME}-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/{GITHUB_USERNAME}) ")
    lines.append(f"[![Auto Sync](https://img.shields.io/badge/Auto--Sync-Active-brightgreen?style=for-the-badge&logo=githubactions&logoColor=white)](#-automated-sync-workflow)")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("</div>")
    lines.append("")
    
    # Profile & Stats Card Section
    lines.append("## 📌 LeetCode Live Profile & Statistics")
    lines.append("")
    lines.append("<div align=\"center\">")
    lines.append(f"<a href=\"https://leetcode.com/u/{LEETCODE_USERNAME}/\">")
    lines.append(f"  <img src=\"https://leetcard.jacoblin.cool/{LEETCODE_USERNAME}?theme=dark&font=Syne%20Tactile&ext=heatmap\" alt=\"LeetCode Stats for {LEETCODE_USERNAME}\" />")
    lines.append("</a>")
    lines.append("</div>")
    lines.append("")
    lines.append("### 📊 Problem Solving Breakdown")
    lines.append("")
    lines.append("| Metric | LeetCode Profile | Repository Solutions | Status |")
    lines.append("| :--- | :---: | :---: | :---: |")
    lines.append(f"| 🌟 **Total Solved** | **{lc_total}** | **{repo_total}** | `{(repo_total/lc_total*100):.1f}% Synced` |" if lc_total else f"| 🌟 **Total Solved** | **{lc_total}** | **{repo_total}** | `Tracked` |")
    lines.append(f"| 🟢 **Easy** | `{lc_easy}` | `{easy_repo}` | `🟢 {(easy_repo/lc_easy*100):.1f}%` |" if lc_easy else f"| 🟢 **Easy** | `{lc_easy}` | `{easy_repo}` | `🟢 Ready` |")
    lines.append(f"| 🟡 **Medium** | `{lc_med}` | `{med_repo}` | `🟡 {(med_repo/lc_med*100):.1f}%` |" if lc_med else f"| 🟡 **Medium** | `{lc_med}` | `{med_repo}` | `🟡 Ready` |")
    lines.append(f"| 🔴 **Hard** | `{lc_hard}` | `{hard_repo}` | `🔴 {(hard_repo/lc_hard*100):.1f}%` |" if lc_hard else f"| 🔴 **Hard** | `{lc_hard}` | `{hard_repo}` | `🔴 Ready` |")
    if ranking != "N/A":
        lines.append(f"| 🏆 **Global Rank** | `#{ranking:,}` | — | `Top Tier` |")
    lines.append("")
    lines.append("> 💡 **Note:** Repository solutions are synchronized from LeetCode submissions. Detailed explanation notes (`Notes.md`) and optimal clean code solutions are included for complex problems.")
    lines.append("")
    
    # Topic Index / Navigation Table
    lines.append("## 🧭 Topic-Wise Index")
    lines.append("")
    lines.append("| Topic | Solved in Repo | Direct Jump |")
    lines.append("| :--- | :---: | :--- |")
    
    for title, anchor in TOPIC_ORDER:
        plist = topic_map.get(title, [])
        if plist:
            lines.append(f"| **{title}** | `{len(plist)}` | [Jump to Section ➔](#-{anchor}) |")
            
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 📚 Categorized Problem Solutions")
    lines.append("")
    
    # Render each topic section
    for title, anchor in TOPIC_ORDER:
        plist = topic_map.get(title, [])
        if not plist:
            continue
            
        lines.append(f"### {title}")
        lines.append(f"<a id=\"-{anchor}\"></a>")
        lines.append("")
        lines.append(f"*Total Problems: **{len(plist)}***")
        lines.append("")
        lines.append("| # | Problem Title | Difficulty | Solution | Notes | Subtopics / Tags |")
        lines.append("| :---: | :--- | :---: | :---: | :---: | :--- |")
        
        for p in plist:
            pid = p.get("frontend_id") or p.get("raw_num") or "—"
            p_title = p.get("title")
            p_url = p.get("url")
            diff_badge = get_difficulty_badge(p.get("difficulty", "Easy"))
            
            # Solution links
            sols = p.get("solutions", [])
            sol_links = []
            for s in sols:
                lang_name = get_language_badge(s)
                sol_links.append(f"[{lang_name}](./{p['folder']}/{s})")
            sol_str = " <br> ".join(sol_links) if sol_links else f"[Solution](./{p['folder']}/)"
            
            # Notes link
            notes_str = f"[📝 Notes](./{p['folder']}/Notes.md)" if p.get("has_notes") else "—"
            
            # Tags
            tags = p.get("tags", [])
            if tags:
                tag_str = ", ".join([f"`{t}`" for t in tags[:3]])
                if len(tags) > 3:
                    tag_str += f" `+{len(tags)-3}`"
            else:
                tag_str = "—"
                
            lines.append(f"| **{pid}** | [{p_title}]({p_url}) | {diff_badge} | {sol_str} | {notes_str} | {tag_str} |")
            
        lines.append("")
        lines.append("---")
        lines.append("")

    # Automated Sync Section
    lines.append("## ⚙️ Automated Sync Workflow")
    lines.append("")
    lines.append("This repository automatically syncs and categorizes new solutions using a custom GitHub Actions workflow and metadata parser.")
    lines.append("")
    lines.append("### 🔄 How It Works")
    lines.append("1. **Submit**: Solve problems on [LeetCode](https://leetcode.com/u/Nithesh_007/).")
    lines.append("2. **Push**: LeetHub / Chrome Extension commits the solution to this repository.")
    lines.append("3. **Sync Action**: GitHub Actions automatically runs `scripts/sync_readme.py` on push to:")
    lines.append("   - Categorize new solutions into appropriate algorithmic topics.")
    lines.append("   - Query LeetCode's GraphQL API for real-time problem numbers, difficulty, and tags.")
    lines.append("   - Refresh profile statistics and update this `README.md` seamlessly.")
    lines.append("")
    lines.append("### 🛠️ Manual Synchronization")
    lines.append("You can also run the sync script locally at any time:")
    lines.append("```bash")
    lines.append("# Run sync script")
    lines.append("python3 scripts/sync_readme.py")
    lines.append("```")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("<div align=\"center\">")
    lines.append(f"<i>Last synchronized on {now_str} • Maintained by <a href=\"https://github.com/{GITHUB_USERNAME}\">@{GITHUB_USERNAME}</a></i>")
    lines.append("</div>")
    lines.append("")
    
    return "\n".join(lines)

def main():
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(repo_dir)
    
    cache = load_cache()
    print(f"Loaded {len(cache)} cached problem definitions.")
    
    # 1. Fetch User Stats
    print(f"Fetching LeetCode stats for {LEETCODE_USERNAME}...")
    user_stats = fetch_leetcode_user_stats(LEETCODE_USERNAME)
    if user_stats:
        print(f"User stats: {user_stats['total_solved']} solved (E: {user_stats['easy_solved']}, M: {user_stats['medium_solved']}, H: {user_stats['hard_solved']}), Rank: #{user_stats['ranking']}")
    
    # 2. Discover problem directories
    problem_dirs = [
        d for d in os.listdir(repo_dir)
        if os.path.isdir(os.path.join(repo_dir, d))
        and not d.startswith(".")
        and d not in ("scripts", ".github", "scratch")
    ]
    
    print(f"Found {len(problem_dirs)} problem directories in repository.")
    
    problems = []
    for d in sorted(problem_dirs):
        folder_path = os.path.join(repo_dir, d)
        info = extract_slug_and_details_from_folder(folder_path, d)
        
        # Enrich with GraphQL
        meta = fetch_problem_metadata(info["slug"], cache)
        if meta:
            info["frontend_id"] = meta.get("frontend_id") or info["raw_num"]
            info["title"] = meta.get("title") or info["title"]
            info["difficulty"] = meta.get("difficulty") or info["difficulty"]
            info["tags"] = meta.get("tags", [])
        else:
            info["frontend_id"] = info["raw_num"]
            info["tags"] = []
            
        info["topic"] = categorize_problem(info)
        problems.append(info)
        
    save_cache(cache)
    
    # 3. Generate README.md
    readme_content = generate_markdown(problems, user_stats)
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
        
    print("✅ README.md successfully generated and synced!")

if __name__ == "__main__":
    main()
