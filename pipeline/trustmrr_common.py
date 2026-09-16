#!/usr/bin/env python3
"""Shared parsing/filtering for TrustMRR Markdown profiles.

Each profile (pipeline/trustmrr_cache/<slug>.md) is a "Public AI-agent
Markdown profile" with Stripe (or Polar/RevenueCat/Paddle/LemonSqueezy/Creem/
Dodo) verified revenue. We parse it into a flat facts dict and apply a
verifiability filter consistent with case-site rules:
  - skip "Stealth Company" (no real domain revealed)
  - skip entries with no website / no product URL
  - skip entries with zero verified revenue everywhere
"""
import os
import re

CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                         "pipeline", "trustmrr_cache")


def _money(s):
    if not s:
        return 0.0
    s = s.replace("$", "").replace(",", "").strip()
    try:
        return float(s)
    except ValueError:
        return 0.0


def _get(lines, key):
    """Match a '- Key: value' line, return value string (or '')."""
    pat = re.compile(r"^- " + re.escape(key) + r":\s*(.*)$")
    for ln in lines:
        m = pat.match(ln)
        if m:
            return m.group(1).strip()
    return ""


def _link_url(val):
    """From '[text](url)' return url; else return text if it looks like url."""
    m = re.search(r"\((https?://[^)]+)\)", val)
    if m:
        return m.group(1)
    if val.startswith("http"):
        return val
    return ""


def _link_text(val):
    m = re.search(r"\[([^\]]*)\]\((https?://[^)]+)\)", val)
    if m:
        return m.group(1).strip()
    return val.strip()


def parse_md(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    lines = text.splitlines()

    facts = {}
    facts["name"] = _get(lines, "Name")
    facts["slug"] = _get(lines, "Slug").strip("`")
    facts["website"] = _link_url(_get(lines, "Website"))
    facts["icon"] = _link_url(_get(lines, "Icon"))
    facts["description"] = _get(lines, "Description")
    facts["country"] = _get(lines, "Country")
    facts["founded"] = _get(lines, "Founded date")
    fnd = _get(lines, "Founder")
    facts["founder"] = _link_text(fnd)
    facts["x_followers"] = _get(lines, "X followers")

    _pv = _get(lines, "Verified payment provider API source")
    facts["payment_provider"] = re.sub(r"\s*\(API key\)$", "", _pv).strip()
    # credential expiry
    cred = _get(lines, "Primary payment provider API credential")
    facts["credential_expired"] = bool(re.search(r"expired", cred, re.I))
    # secondary traffic sources
    facts["ga_connected"] = _get(lines, "Google Analytics API connected")
    facts["gsearch_connected"] = _get(lines, "Google Search Console API connected")

    # Revenue table
    rev = {}
    for ln in lines:
        m = re.match(r"^\|\s*(Last 24 hours|Last 7 days|Last 30 days|Last 3 months|"
                     r"Last 6 months|Last 12 months|All time)\s*\|\s*\$?([\d,\.]+)",
                     ln)
        if m:
            rev[m.group(1)] = _money(m.group(2))
    facts["rev_24h"] = rev.get("Last 24 hours", 0.0)
    facts["rev_7d"] = rev.get("Last 7 days", 0.0)
    facts["rev_30d"] = rev.get("Last 30 days", 0.0)
    facts["rev_3m"] = rev.get("Last 3 months", 0.0)
    facts["rev_6m"] = rev.get("Last 6 months", 0.0)
    facts["rev_12m"] = rev.get("Last 12 months", 0.0)
    facts["rev_all"] = rev.get("All time", 0.0)
    # snapshots
    mrr = _get(lines, "Current MRR")
    facts["mrr"] = _money(re.search(r"\$?([\d,\.]+)", mrr).group(1)) if re.search(r"\$?([\d,\.]+)", mrr) else 0.0
    subs = _get(lines, "Current active subscriptions")
    facts["subs"] = int(_money(subs)) if subs else 0

    # Insights
    facts["pricing"] = _get(lines, "Pricing model")
    facts["audience"] = _link_text(_get(lines, "Audience type"))
    facts["est_users"] = _get(lines, "Estimated user count")
    facts["value_prop"] = _get(lines, "Value proposition")
    facts["problem"] = _get(lines, "Problem solved")
    facts["extra"] = _get(lines, "Additional info")
    markets = _get(lines, "Markets")
    facts["markets"] = re.findall(r"\[([^\]]+)\]\((https?://[^)]+)\)", markets)
    facts["for_sale"] = "not currently listed for sale" not in text

    # SEO
    facts["domain"] = _get(lines, "Domain")
    dr = _get(lines, "Domain rating")
    facts["dr"] = dr
    # Screenshot
    m = re.search(r"!\[[^\]]*\]\((https://[^)]+startup-screenshots[^)]+\.webp)\)", text)
    facts["screenshot"] = m.group(1) if m else ""
    # sync date
    m = re.search(r"Revenue last synced:\s*([\dT:\.\-Z]+)", text)
    facts["rev_synced"] = m.group(1) if m else ""
    return facts


def passes_filter(facts):
    """Return (ok, reason)."""
    if facts["name"] == "Stealth Company":
        return False, "stealth"
    if not facts["website"]:
        # app-store links still count as a product URL
        return False, "no-website"
    if facts["rev_30d"] <= 0 and facts["mrr"] <= 0 and facts["rev_all"] <= 0:
        return False, "zero-revenue"
    if facts["rev_all"] < 100 and facts["rev_30d"] <= 0 and facts["mrr"] <= 0:
        return False, "negligible"
    return True, "ok"


def fmt_money(v):
    return "${:,.0f}".format(v)
