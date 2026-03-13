#!/usr/bin/env python3
"""Reorganize skill folders into category/subcategory hierarchy.

Run from repo root:
  python scripts/reorganize_skills.py
"""
from __future__ import annotations

from pathlib import Path
import re
import shutil

ROOT = Path('.')

EXCLUDE_DIRS = {
    '.git',
    '.github',
    'scripts',
}

RULES = [
    # Engineering Process
    (
        r'^conductor-|^track-management|^acceptance-|^closed-loop-|^executing-plans|^writing-plans|^plan-writing|^planning-with-files|^concise-planning|^workflow-patterns|^workflow-orchestration|^workflow-automation|^tdd-|^test-driven-development|^verification-before-completion|^lint-and-validate',
        ('Engineering Process', 'Planning & Execution'),
    ),
    (
        r'^code-review|^receiving-code-review|^requesting-code-review|^fix-review|^codex-review|^find-bugs|^vibe-code-auditor|^production-code-audit|^codebase-audit',
        ('Engineering Process', 'Code Review & Audit'),
    ),
    (
        r'^testing-|^test-|^e2e-|^playwright-|\bqa\b|^unit-testing',
        ('Engineering Process', 'Testing & QA'),
    ),
    (
        r'^documentation|^readme|^wiki-|^docs-|^doc-?|^docx-|^pptx-|^xlsx-|^pdf-',
        ('Engineering Process', 'Documentation'),
    ),

    # Security
    (
        r'pentest|burp|metasploit|xss|sql-injection|idor|ffuf|nmap|shodan|recon|privilege-escalation|exploit|attack|html-injection',
        ('Security', 'Offensive & Pentest'),
    ),
    (
        r'security|audit|sast|owasp|compliance|gdpr|pci|secrets|zeroize|forensics|malware|incident',
        ('Security', 'Defensive & Compliance'),
    ),
    (r'threat|risk|attack-tree|stride', ('Security', 'Threat Modeling & Risk')),

    # Cloud & Infra
    (r'^aws-|^cdk-|^cloudformation-|^aws_', ('Cloud & Infra', 'AWS')),
    (r'^azure-|^azd-|^m365-|^microsoft-', ('Cloud & Infra', 'Azure')),
    (r'^gcp-|^google-analytics-|^google-.*', ('Cloud & Infra', 'GCP & Google Cloud')),
    (
        r'^vercel-|^netlify|^render-|^fly-|^railway|^appdeploy|^cloudflare-workers',
        ('Cloud & Infra', 'Hosting & PaaS'),
    ),
    (r'^cloudflare-', ('Cloud & Infra', 'Cloudflare')),
    (
        r'^kubernetes-|^k8s-|^helm-|^istio-|^linkerd-',
        ('Cloud & Infra', 'Kubernetes & Service Mesh'),
    ),
    (r'^docker-|^devcontainer-|^container', ('Cloud & Infra', 'Containers & Dev Envs')),
    (r'^terraform-|^opentofu|^cdk-', ('Cloud & Infra', 'Infrastructure as Code')),
    (
        r'^observability-|^monitoring-|^prometheus|^grafana|^slo-|^distributed-tracing',
        ('Cloud & Infra', 'Observability'),
    ),
    (r'^devops-|^deployment-|^cicd-|^github-actions-|^gitlab-ci-|^circleci-|^gitops', ('Cloud & Infra', 'DevOps & CI/CD')),

    # AI & Agents
    (r'agent|agents|assistant|autonomous|orchestration|multi-agent|tool-builder|computer-use', ('AI & Agents', 'Agents & Orchestration')),
    (r'prompt|evaluation|judge|rubric|llm-evaluation|\beval\b', ('AI & Agents', 'Prompting & Evaluation')),
    (r'rag|retrieval|embedding|vector|semantic|search|similarity', ('AI & Agents', 'RAG & Search')),
    (r'voice|speech|audio|transcription|tts|realtime|podcast', ('AI & Agents', 'Voice & Audio AI')),
    (r'vision|image|multimodal|video|computer-vision', ('AI & Agents', 'Vision & Multimodal')),
    (r'openai|gemini|anthropic|\bllm\b|^ai-|^ml-|model|mcp|langchain|langgraph|llmops|inference', ('AI & Agents', 'LLM Apps & Platforms')),

    # Data & ML
    (r'data-|etl|pipeline|dbt|airflow|spark|warehouse|analytics|bi-', ('Data & ML', 'Data Engineering')),
    (r'scikit|statsmodels|matplotlib|seaborn|plotly|polars|pandas|data-science|analysis|visualization', ('Data & ML', 'Data Science & Viz')),
    (r'mlops|training|model-trainer|backtesting|quant|forecast|optimization', ('Data & ML', 'ML & Modeling')),

    # Backend & APIs
    (r'api-|openapi|graphql|rest|endpoint|server|backend', ('Backend & APIs', 'API Design & Implementation')),
    (r'django|fastapi|rails|laravel|nestjs|nodejs|express|dotnet|spring|go-|rust-|python-|java-|php-|ruby-', ('Backend & APIs', 'Backend Frameworks')),
    (r'database|postgres|mysql|mongodb|redis|nosql|\bsql\b|orm|prisma|drizzle|sqlite', ('Backend & APIs', 'Databases')),
    (r'(^|-)auth($|-)|oauth|jwt|clerk|session|rbac', ('Backend & APIs', 'Auth & Security')),

    # Frontend & UI
    (r'react|nextjs|angular|frontend|ui-|ux-|design|css|tailwind|shadcn|radix|figma|accessibility|a11y|hig-', ('Frontend & UI', 'Web UI & Design')),
    (r'animation|threejs|3d|webgl|shader|spline|canvas|d3js|scroll|visual', ('Frontend & UI', 'Graphics & Motion')),

    # Mobile
    (r'android|ios|swiftui|kotlin|react-native|expo|flutter|mobile', ('Mobile', 'Mobile Development')),

    # Integrations & Automation
    (r'^apify-|^web-scraper|scraper', ('Integrations & Automation', 'Web Scraping & Data')),
    (r'^n8n-', ('Integrations & Automation', 'n8n')),
    (r'-automation$|automation', ('Integrations & Automation', 'SaaS Automations')),
    (r'slack|discord|telegram|whatsapp|twilio|email|gmail|outlook|calendar|zoom|meet', ('Integrations & Automation', 'Comms & Messaging')),
    (r'notion|airtable|google-drive|docs|sheets|slides|dropbox|box|onedrive|office|miro|trello|asana|clickup|jira|linear|basecamp|wrike|todoist', ('Integrations & Automation', 'Docs & Productivity')),
    (r'salesforce|hubspot|zendesk|freshdesk|freshservice|intercom|pipedrive|zoho|stripe|paypal|billing|payments|shopify|woocommerce', ('Integrations & Automation', 'CRM & Commerce')),

    # Product & Growth
    (r'product|pm|roadmap|launch|pricing|monetization|growth|seo|content|copy|marketing|ads|cro', ('Product & Growth', 'Product & Marketing')),

    # Media & Creative
    (r'art|design|creative|video|audio|image|visual|animation|3d|threejs|spline|canvas', ('Media & Creative', 'Creative & Media')),

    # Domain-specific
    (r'health|medical|wellness|nutrition|sleep|fitness|clinical|rehab', ('Domain', 'Health')),
    (r'legal|compliance|gdpr|pci|contract|policy|advogado', ('Domain', 'Legal & Compliance')),
    (r'finance|crypto|blockchain|defi|trading|quant|alpha-vantage|plaid', ('Domain', 'Finance & Crypto')),
    (r'logistics|supply|inventory|warehouse|shipping|freight', ('Domain', 'Logistics & Supply Chain')),
    (r'education|learning|tutorial|onboarding', ('Domain', 'Education & Enablement')),
    (r'leiloeiro|imovel|imobili', ('Domain', 'Real Estate & Auctions')),
    (r'andruia|auri-', ('Domain', 'Andru.ia')),

    # Meta
    (r'^skill|skills|agents-md|claude|codex|context|memory|prompt-library|using-superpowers|superpowers|loki-mode', ('Meta', 'Skills & Agent Ops')),
    (r'guide|advisor|coach|karpathy|hinton|lecun|altman|jobs|musk|buffett|gates|sutskever', ('Meta', 'Personas & Advisors')),
    (r'workflow|orchestrator|dispatcher|manager|router', ('Meta', 'Orchestration & Routing')),

    # UI frameworks
    (r'^makepad-|^robius-|^molykit', ('Frontend & UI', 'Makepad & Robius')),
    (r'^game-development|^unity-|game', ('Media & Creative', 'Game Development')),
]


def slugify(text: str) -> str:
    text = text.lower()
    text = text.replace('&', 'and')
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = text.strip('-')
    return text


def categorize(name: str) -> tuple[str, str] | None:
    for pattern, (cat, sub) in RULES:
        if re.search(pattern, name):
            return cat, sub
    return None


def iter_skill_dirs() -> list[Path]:
    skill_dirs = set()
    for skill_md in ROOT.rglob('SKILL.md'):
        parts = skill_md.parts
        if any(part in EXCLUDE_DIRS for part in parts):
            continue
        if any(part.startswith('.') for part in parts):
            continue
        if skill_md.parent == ROOT:
            continue
        skill_dirs.add(skill_md.parent)
    return sorted(skill_dirs, key=lambda p: len(p.parts), reverse=True)


def move_skill_dir(src: Path, dst: Path) -> None:
    if not src.exists():
        return
    if dst.exists():
        raise RuntimeError(f'target exists: {dst}')
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src), str(dst))


def main() -> None:
    moves = []
    for src in iter_skill_dirs():
        name = src.name
        category = categorize(name)
        if category is None:
            cat, sub = 'Other', 'Uncategorized'
        else:
            cat, sub = category

        cat_dir = slugify(cat)
        sub_dir = slugify(sub)
        dst = ROOT / cat_dir / sub_dir / name

        # Skip if already in the desired location
        if src.resolve() == dst.resolve():
            continue

        # If already under category/subcategory, skip
        if len(src.parts) >= 3 and src.parts[0] == cat_dir and src.parts[1] == sub_dir:
            continue

        moves.append((src, dst))

    for src, dst in moves:
        move_skill_dir(src, dst)
        print(f'moved: {src} -> {dst}')

    print(f'completed. moves: {len(moves)}')


if __name__ == '__main__':
    main()
