#!/usr/bin/env python3
"""Generate SKILLS_INDEX.md with categorized skills.

Run from repo root:
  python scripts/generate_skills_index.py
"""

from pathlib import Path
import re

ROOT = Path(".")
OUTPUT = ROOT / "SKILLS_INDEX.md"


def find_skills():
    skills = []
    for p in ROOT.iterdir():
        if p.name.startswith("."):
            continue
        if p.is_dir() and (p / "SKILL.md").is_file():
            skills.append(p.name)
    return sorted(skills)


RULES = [
    # Engineering Process
    (
        r"^conductor-|^track-management|^acceptance-|^closed-loop-|^executing-plans|^writing-plans|^plan-writing|^planning-with-files|^concise-planning|^workflow-patterns|^workflow-orchestration|^workflow-automation|^tdd-|^test-driven-development|^verification-before-completion|^lint-and-validate",
        ("Engineering Process", "Planning & Execution"),
    ),
    (
        r"^code-review|^receiving-code-review|^requesting-code-review|^fix-review|^codex-review|^find-bugs|^vibe-code-auditor|^production-code-audit|^codebase-audit",
        ("Engineering Process", "Code Review & Audit"),
    ),
    (
        r"^testing-|^test-|^e2e-|^playwright-|\bqa\b|^unit-testing",
        ("Engineering Process", "Testing & QA"),
    ),
    (
        r"^documentation|^readme|^wiki-|^docs-|^doc-?|^docx-|^pptx-|^xlsx-|^pdf-",
        ("Engineering Process", "Documentation"),
    ),
    # Security
    (
        r"pentest|burp|metasploit|xss|sql-injection|idor|ffuf|nmap|shodan|recon|privilege-escalation|exploit|attack|html-injection",
        ("Security", "Offensive & Pentest"),
    ),
    (
        r"security|audit|sast|owasp|compliance|gdpr|pci|secrets|zeroize|forensics|malware|incident",
        ("Security", "Defensive & Compliance"),
    ),
    (r"threat|risk|attack-tree|stride", ("Security", "Threat Modeling & Risk")),
    # Cloud & Infra
    (r"^aws-|^cdk-|^cloudformation-|^aws_", ("Cloud & Infra", "AWS")),
    (r"^azure-|^azd-|^m365-|^microsoft-", ("Cloud & Infra", "Azure")),
    (r"^gcp-|^google-analytics-|^google-.*", ("Cloud & Infra", "GCP & Google Cloud")),
    (
        r"^vercel-|^netlify|^render-|^fly-|^railway|^appdeploy|^cloudflare-workers",
        ("Cloud & Infra", "Hosting & PaaS"),
    ),
    (r"^cloudflare-", ("Cloud & Infra", "Cloudflare")),
    (
        r"^kubernetes-|^k8s-|^helm-|^istio-|^linkerd-",
        ("Cloud & Infra", "Kubernetes & Service Mesh"),
    ),
    (r"^docker-|^devcontainer-|^container", ("Cloud & Infra", "Containers & Dev Envs")),
    (r"^terraform-|^opentofu|^cdk-", ("Cloud & Infra", "Infrastructure as Code")),
    (
        r"^observability-|^monitoring-|^prometheus|^grafana|^slo-|^distributed-tracing",
        ("Cloud & Infra", "Observability"),
    ),
    (
        r"^devops-|^deployment-|^cicd-|^github-actions-|^gitlab-ci-|^circleci-|^gitops",
        ("Cloud & Infra", "DevOps & CI/CD"),
    ),
    # AI & Agents
    (
        r"agent|agents|assistant|autonomous|orchestration|multi-agent|tool-builder|computer-use",
        ("AI & Agents", "Agents & Orchestration"),
    ),
    (
        r"prompt|evaluation|judge|rubric|llm-evaluation|\beval\b",
        ("AI & Agents", "Prompting & Evaluation"),
    ),
    (
        r"rag|retrieval|embedding|vector|semantic|search|similarity",
        ("AI & Agents", "RAG & Search"),
    ),
    (
        r"voice|speech|audio|transcription|tts|realtime|podcast",
        ("AI & Agents", "Voice & Audio AI"),
    ),
    (
        r"vision|image|multimodal|video|computer-vision",
        ("AI & Agents", "Vision & Multimodal"),
    ),
    (
        r"openai|gemini|anthropic|\bllm\b|^ai-|^ml-|model|mcp|langchain|langgraph|llmops|inference",
        ("AI & Agents", "LLM Apps & Platforms"),
    ),
    # Data & ML
    (
        r"data-|etl|pipeline|dbt|airflow|spark|warehouse|analytics|bi-",
        ("Data & ML", "Data Engineering"),
    ),
    (
        r"scikit|statsmodels|matplotlib|seaborn|plotly|polars|pandas|data-science|analysis|visualization",
        ("Data & ML", "Data Science & Viz"),
    ),
    (
        r"mlops|training|model-trainer|backtesting|quant|forecast|optimization",
        ("Data & ML", "ML & Modeling"),
    ),
    # Backend & APIs
    (
        r"api-|openapi|graphql|rest|endpoint|server|backend",
        ("Backend & APIs", "API Design & Implementation"),
    ),
    (
        r"django|fastapi|rails|laravel|nestjs|nodejs|express|dotnet|spring|go-|rust-|python-|java-|php-|ruby-",
        ("Backend & APIs", "Backend Frameworks"),
    ),
    (
        r"database|postgres|mysql|mongodb|redis|nosql|\bsql\b|orm|prisma|drizzle|sqlite",
        ("Backend & APIs", "Databases"),
    ),
    (
        r"(^|-)auth($|-)|oauth|jwt|clerk|session|rbac",
        ("Backend & APIs", "Auth & Security"),
    ),
    # Frontend & UI
    (
        r"react|nextjs|angular|frontend|ui-|ux-|design|css|tailwind|shadcn|radix|figma|accessibility|a11y|hig-",
        ("Frontend & UI", "Web UI & Design"),
    ),
    (
        r"animation|threejs|3d|webgl|shader|spline|canvas|d3js|scroll|visual",
        ("Frontend & UI", "Graphics & Motion"),
    ),
    # Mobile
    (
        r"android|ios|swiftui|kotlin|react-native|expo|flutter|mobile",
        ("Mobile", "Mobile Development"),
    ),
    # Integrations & Automation
    (
        r"^apify-|^web-scraper|scraper",
        ("Integrations & Automation", "Web Scraping & Data"),
    ),
    (r"^n8n-", ("Integrations & Automation", "n8n")),
    (r"-automation$|automation", ("Integrations & Automation", "SaaS Automations")),
    (
        r"slack|discord|telegram|whatsapp|twilio|email|gmail|outlook|calendar|zoom|meet",
        ("Integrations & Automation", "Comms & Messaging"),
    ),
    (
        r"notion|airtable|google-drive|docs|sheets|slides|dropbox|box|onedrive|office|miro|trello|asana|clickup|jira|linear|basecamp|wrike|todoist",
        ("Integrations & Automation", "Docs & Productivity"),
    ),
    (
        r"salesforce|hubspot|zendesk|freshdesk|freshservice|intercom|pipedrive|zoho|stripe|paypal|billing|payments|shopify|woocommerce",
        ("Integrations & Automation", "CRM & Commerce"),
    ),
    # Product & Growth
    (
        r"product|pm|roadmap|launch|pricing|monetization|growth|seo|content|copy|marketing|ads|cro",
        ("Product & Growth", "Product & Marketing"),
    ),
    # Media & Creative
    (
        r"art|design|creative|video|audio|image|visual|animation|3d|threejs|spline|canvas",
        ("Media & Creative", "Creative & Media"),
    ),
    # Domain-specific
    (
        r"health|medical|wellness|nutrition|sleep|fitness|clinical|rehab",
        ("Domain", "Health"),
    ),
    (
        r"legal|compliance|gdpr|pci|contract|policy|advogado",
        ("Domain", "Legal & Compliance"),
    ),
    (
        r"finance|crypto|blockchain|defi|trading|quant|alpha-vantage|plaid",
        ("Domain", "Finance & Crypto"),
    ),
    (
        r"logistics|supply|inventory|warehouse|shipping|freight",
        ("Domain", "Logistics & Supply Chain"),
    ),
    (r"education|learning|tutorial|onboarding", ("Domain", "Education & Enablement")),
    (r"leiloeiro|imovel|imobili", ("Domain", "Real Estate & Auctions")),
    (r"andruia|auri-", ("Domain", "Andru.ia")),
    # Meta
    (
        r"^skill|skills|agents-md|claude|codex|context|memory|prompt-library|using-superpowers|superpowers|loki-mode",
        ("Meta", "Skills & Agent Ops"),
    ),
    (
        r"guide|advisor|coach|karpathy|hinton|lecun|altman|jobs|musk|buffett|gates|sutskever",
        ("Meta", "Personas & Advisors"),
    ),
    (
        r"workflow|orchestrator|dispatcher|manager|router",
        ("Meta", "Orchestration & Routing"),
    ),
    # UI frameworks
    (r"^makepad-|^robius-|^molykit", ("Frontend & UI", "Makepad & Robius")),
    (r"^game-development|^unity-|game", ("Media & Creative", "Game Development")),
]


def categorize(skills):
    categories = {}
    uncat = []
    for name in skills:
        assigned = False
        for pattern, (cat, sub) in RULES:
            if re.search(pattern, name):
                categories.setdefault(cat, {}).setdefault(sub, []).append(name)
                assigned = True
                break
        if not assigned:
            uncat.append(name)
    for cat in categories:
        for sub in categories[cat]:
            categories[cat][sub].sort()
    return categories, sorted(uncat)


def write_index(categories, uncat):
    lines = []
    lines.append("# Skills Index")
    lines.append("")
    lines.append(
        "This file is auto-organized for easy navigation. Use your editor search to jump to a skill quickly."
    )
    lines.append("")
    for cat in sorted(categories):
        lines.append(f"## {cat}")
        lines.append("")
        for sub in sorted(categories[cat]):
            skills_list = categories[cat][sub]
            lines.append(f"### {sub} ({len(skills_list)})")
            lines.append("")
            lines.append(", ".join(f"`{s}`" for s in skills_list))
            lines.append("")
    if uncat:
        lines.append("## Other / Uncategorized")
        lines.append("")
        lines.append(f"({len(uncat)} skills)")
        lines.append("")
        lines.append(", ".join(f"`{s}`" for s in uncat))
        lines.append("")
    OUTPUT.write_text("\n".join(lines))


def main():
    skills = find_skills()
    categories, uncat = categorize(skills)
    write_index(categories, uncat)

    # Print summary for quick checks
    print("Category summary (counts):")
    for cat in sorted(categories):
        total = sum(len(v) for v in categories[cat].values())
        print(f"- {cat}: {total}")
    print("Uncategorized:", len(uncat))


if __name__ == "__main__":
    main()
