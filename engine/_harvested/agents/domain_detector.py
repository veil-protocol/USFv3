#!/usr/bin/env python3
"""
USF 6.5 APEX - Domain Detector

Auto-detects vault domains and loads appropriate agent modules.
Enables USF to evolve as the vault grows.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass
import yaml


@dataclass
class VaultDomain:
    """A detected domain in the vault"""
    name: str
    path: str
    note_count: int
    keywords: Set[str]
    agent_modules: List[str]
    confidence: float


class DomainDetector:
    """
    Auto-detect vault domains and map to agent modules.

    Scans vault directory structure and content to identify
    which domains are present and which agents to load.
    """

    # Domain signatures: directory patterns → domain name → agent modules
    # UPDATED for MITRE ATT&CK-aligned vault structure
    DOMAIN_SIGNATURES = {
        # =================================================================
        # OFFENSIVE SECURITY (MITRE ATT&CK Aligned)
        # =================================================================
        "reconnaissance": {
            "patterns": ["10-recon", "recon", "enumeration", "scanning", "osint"],
            "agents": ["security/reconnaissance.yaml"],
            "keywords": ["nmap", "gobuster", "subdomain", "dns", "whois"]
        },
        "initial_access": {
            "patterns": ["20-initial-access", "initial-access", "phishing", "exploit"],
            "agents": ["redteam/initial_access.yaml"],
            "keywords": ["phishing", "macro", "exploit", "payload", "dropper"]
        },
        "execution": {
            "patterns": ["30-execution", "execution", "scripting"],
            "agents": ["redteam/execution.yaml"],
            "keywords": ["powershell", "wmi", "cmd", "script", "living-off-the-land"]
        },
        "persistence": {
            "patterns": ["40-persistence", "persistence", "implant"],
            "agents": ["redteam/persistence.yaml"],
            "keywords": ["scheduled-task", "service", "registry", "startup", "implant"]
        },
        "privilege_escalation": {
            "patterns": ["50-privesc", "privesc", "privilege", "escalation"],
            "agents": ["security/privesc.yaml"],
            "keywords": ["suid", "sudo", "kernel", "capabilities", "token"]
        },
        "defense_evasion": {
            "patterns": ["60-defense-evasion", "evasion", "bypass", "av", "edr"],
            "agents": ["redteam/evasion.yaml"],
            "keywords": ["obfuscation", "amsi", "unhooking", "syscall", "packer"]
        },
        "credential_access": {
            "patterns": ["70-credential", "credential", "cred", "password"],
            "agents": ["security/creds.yaml"],
            "keywords": ["mimikatz", "lsass", "sam", "ntds", "kerberos"]
        },
        "discovery": {
            "patterns": ["80-discovery", "discovery", "enum"],
            "agents": ["security/discovery.yaml"],
            "keywords": ["bloodhound", "sharphound", "ldap", "network-scan"]
        },
        "lateral_movement": {
            "patterns": ["85-lateral", "lateral", "movement", "pivot"],
            "agents": ["security/lateral.yaml"],
            "keywords": ["psexec", "wmi", "winrm", "rdp", "ssh", "pivot"]
        },
        "collection": {
            "patterns": ["90-collection", "collection", "staging"],
            "agents": ["redteam/collection.yaml"],
            "keywords": ["keylogger", "screenshot", "clipboard", "data"]
        },
        "exfiltration": {
            "patterns": ["95-exfiltration", "exfil", "exfiltration"],
            "agents": ["redteam/exfil.yaml"],
            "keywords": ["dns-exfil", "https", "covert", "steganography"]
        },
        "c2_infrastructure": {
            "patterns": ["99-c2", "c2", "command-control"],
            "agents": ["redteam/c2.yaml"],
            "keywords": ["cobalt", "sliver", "malleable", "beacon", "redirector"]
        },
        "active_directory": {
            "patterns": ["a0-active-directory", "active-directory", "ad"],
            "agents": ["security/active_directory.yaml"],
            "keywords": ["bloodhound", "kerberoast", "dcsync", "gpo", "adcs"]
        },
        "web_exploitation": {
            "patterns": ["b0-web", "web", "webapp", "sqli", "xss"],
            "agents": ["security/web_exploitation.yaml"],
            "keywords": ["burp", "sqlmap", "owasp", "api", "jwt"]
        },

        # =================================================================
        # ADVANCED RED TEAM (OSEP, CRTO, APT)
        # =================================================================
        "apt_simulation": {
            "patterns": ["e0-apt", "apt", "nation-state", "threat-actor", "emulation"],
            "agents": ["redteam/apt_simulation.yaml"],
            "keywords": ["apt29", "apt28", "lazarus", "equation", "tao", "ta505", "ttps"]
        },
        "training": {
            "patterns": ["t0-training", "training", "oscp", "osep", "crto", "course"],
            "agents": ["core/training.yaml"],
            "keywords": ["lab", "exercise", "course", "certification", "exam"]
        },
        "reference": {
            "patterns": ["r0-reference", "reference", "hacktricks", "cheat-sheet"],
            "agents": ["core/reference.yaml"],
            "keywords": ["cheatsheet", "reference", "guide", "documentation"]
        },
        "operations": {
            "patterns": ["01-operations", "operations", "engagement", "bug-bounty", "terror", "operation-"],
            "agents": ["core/operations.yaml"],
            "keywords": ["engagement", "client", "scope", "report", "finding", "enumeration", "phase", "target"]
        },

        # =================================================================
        # CLOUD & BUG BOUNTY
        # =================================================================
        "cloud_security": {
            "patterns": ["c0-cloud", "cloud", "aws", "azure", "gcp", "kubernetes"],
            "agents": ["emerging/cloud.yaml"],
            "keywords": ["s3", "iam", "lambda", "eks", "metadata", "ec2", "blob"]
        },
        "bug_bounty": {
            "patterns": ["bug-bounty", "bounty", "hackerone", "bugcrowd"],
            "agents": ["bugbounty/hunting.yaml"],
            "keywords": ["scope", "recon", "chain", "report", "poc"]
        },
        "mobile_security": {
            "patterns": ["mobile", "android", "ios", "apk"],
            "agents": ["bugbounty/mobile.yaml"],
            "keywords": ["frida", "objection", "jadx", "burp-mobile"]
        },

        # =================================================================
        # BLUE TEAM / DEFENSE
        # =================================================================
        "blue_team": {
            "patterns": ["d0-blue-team", "blue-team", "defense", "detection"],
            "agents": ["blueteam/all.yaml"],
            "keywords": ["detection", "hunting", "response", "forensics", "hardening"]
        },
        "detection": {
            "patterns": ["detection", "siem", "logging", "alert", "sigma"],
            "agents": ["blueteam/detection.yaml"],
            "keywords": ["splunk", "elastic", "sigma", "yara", "snort"]
        },
        "incident_response": {
            "patterns": ["incident-response", "response", "forensics", "dfir"],
            "agents": ["blueteam/incident_response.yaml"],
            "keywords": ["volatility", "autopsy", "timeline", "artifact"]
        },
        "threat_intel": {
            "patterns": ["threat-intel", "ioc", "indicator", "cti", "hunting"],
            "agents": ["blueteam/threat_intel.yaml"],
            "keywords": ["stix", "taxii", "misp", "yara", "osint"]
        },
        "hardening": {
            "patterns": ["hardening", "baseline", "cis", "stig"],
            "agents": ["blueteam/hardening.yaml"],
            "keywords": ["benchmark", "compliance", "audit", "policy"]
        },
        "tools": {
            "patterns": ["x0-tools", "tools", "offensive", "defensive"],
            "agents": ["core/tools.yaml"],
            "keywords": ["tool", "script", "automation", "custom"]
        },

        # =================================================================
        # DEVELOPMENT / DEVSECOPS
        # =================================================================
        "secure_development": {
            "patterns": ["devsecops", "secure-code", "sast", "dast"],
            "agents": ["development/security.yaml"],
            "keywords": ["semgrep", "sonarqube", "checkmarx", "snyk"]
        },
        "code_review": {
            "patterns": ["code-review", "pull-request", "audit"],
            "agents": ["development/review.yaml"],
            "keywords": ["lint", "type-check", "coverage", "complexity"]
        },
        "cicd_security": {
            "patterns": ["cicd", "pipeline", "github-actions", "jenkins"],
            "agents": ["development/cicd.yaml"],
            "keywords": ["secrets", "supply-chain", "sbom", "signing"]
        },

        # =================================================================
        # EMERGING TECH
        # =================================================================
        "ai_ml_security": {
            "patterns": ["ai", "ml", "llm", "machine-learning"],
            "agents": ["emerging/ai_security.yaml"],
            "keywords": ["prompt-injection", "jailbreak", "adversarial", "model"]
        },
        "iot_security": {
            "patterns": ["iot", "embedded", "firmware", "hardware"],
            "agents": ["emerging/iot.yaml"],
            "keywords": ["uart", "jtag", "binwalk", "firmware"]
        },
        "blockchain_security": {
            "patterns": ["blockchain", "smart-contract", "web3", "defi"],
            "agents": ["emerging/blockchain.yaml"],
            "keywords": ["solidity", "reentrancy", "flash-loan", "oracle"]
        },
    }

    def __init__(self, vault_path: str, agent_registry_path: str):
        self.vault_path = Path(vault_path)
        self.agent_registry_path = Path(agent_registry_path)
        self.detected_domains: Dict[str, VaultDomain] = {}

    def scan_vault(self) -> Dict[str, VaultDomain]:
        """
        Scan vault and detect all present domains.

        Returns dict of domain_name → VaultDomain
        """
        self.detected_domains = {}

        # Get all directories
        for item in self.vault_path.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                self._analyze_directory(item)

        # Score and filter domains
        return {
            name: domain
            for name, domain in self.detected_domains.items()
            if domain.confidence >= 0.3  # Minimum 30% confidence
        }

    def _analyze_directory(self, dir_path: Path, depth: int = 0):
        """Analyze a directory for domain signatures"""
        dir_name = dir_path.name.lower()

        # Count notes
        note_count = len(list(dir_path.rglob("*.md")))
        if note_count == 0:
            return

        # Check each domain signature
        for domain_name, signature in self.DOMAIN_SIGNATURES.items():
            confidence = 0.0
            matched_keywords = set()

            # Check directory name patterns
            for pattern in signature["patterns"]:
                if pattern in dir_name:
                    confidence += 0.4
                    break

            # Sample files for keyword matching (limit to 50 for speed)
            sample_files = list(dir_path.rglob("*.md"))[:50]
            for md_file in sample_files:
                try:
                    content = md_file.read_text(encoding='utf-8', errors='ignore').lower()
                    for keyword in signature["keywords"]:
                        if keyword in content:
                            matched_keywords.add(keyword)
                except Exception:
                    pass

            # Calculate keyword confidence
            if matched_keywords:
                keyword_ratio = len(matched_keywords) / len(signature["keywords"])
                confidence += keyword_ratio * 0.6

            # Update domain if confidence is higher
            if confidence > 0:
                if domain_name not in self.detected_domains or \
                   confidence > self.detected_domains[domain_name].confidence:
                    self.detected_domains[domain_name] = VaultDomain(
                        name=domain_name,
                        path=str(dir_path),
                        note_count=note_count,
                        keywords=matched_keywords,
                        agent_modules=signature["agents"],
                        confidence=min(1.0, confidence)
                    )

    def get_agent_modules_to_load(self) -> List[str]:
        """Get list of agent module files to load based on detected domains"""
        modules = set()

        # Always load core agents
        modules.add("core/verification.yaml")
        modules.add("core/meta.yaml")

        # Add domain-specific modules
        for domain in self.detected_domains.values():
            for module in domain.agent_modules:
                modules.add(module)

        return sorted(modules)

    def generate_domain_report(self) -> str:
        """Generate a report of detected domains"""
        lines = [
            "=" * 60,
            "USF VAULT DOMAIN DETECTION REPORT",
            "=" * 60,
            f"Vault: {self.vault_path}",
            f"Domains detected: {len(self.detected_domains)}",
            "",
        ]

        # Sort by confidence
        sorted_domains = sorted(
            self.detected_domains.values(),
            key=lambda d: d.confidence,
            reverse=True
        )

        for domain in sorted_domains:
            lines.append(f"[{domain.confidence:.0%}] {domain.name}")
            lines.append(f"     Path: {domain.path}")
            lines.append(f"     Notes: {domain.note_count}")
            lines.append(f"     Keywords: {', '.join(list(domain.keywords)[:5])}")
            lines.append(f"     Agents: {', '.join(domain.agent_modules)}")
            lines.append("")

        lines.append("=" * 60)
        lines.append(f"Agent modules to load: {len(self.get_agent_modules_to_load())}")
        for module in self.get_agent_modules_to_load():
            lines.append(f"  - {module}")

        return "\n".join(lines)

    def suggest_missing_domains(self) -> List[str]:
        """Suggest domains that could be added based on partial matches"""
        suggestions = []

        for domain_name, signature in self.DOMAIN_SIGNATURES.items():
            if domain_name not in self.detected_domains:
                # Check if any keywords appear in vault
                for md_file in list(self.vault_path.rglob("*.md"))[:100]:
                    try:
                        content = md_file.read_text(encoding='utf-8', errors='ignore').lower()
                        for keyword in signature["keywords"][:3]:  # Check first 3 keywords
                            if keyword in content:
                                suggestions.append(
                                    f"{domain_name}: Found '{keyword}' - consider adding {signature['patterns'][0]} directory"
                                )
                                break
                    except Exception:
                        pass

        return suggestions[:10]  # Top 10 suggestions


def main():
    """CLI entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="USF Domain Detector")
    parser.add_argument("vault_path", help="Path to Obsidian vault")
    parser.add_argument("--report", action="store_true", help="Generate full report")
    parser.add_argument("--modules", action="store_true", help="List agent modules to load")
    parser.add_argument("--suggest", action="store_true", help="Suggest missing domains")

    args = parser.parse_args()

    detector = DomainDetector(
        vault_path=args.vault_path,
        agent_registry_path="."
    )

    domains = detector.scan_vault()

    if args.report:
        print(detector.generate_domain_report())
    elif args.modules:
        for module in detector.get_agent_modules_to_load():
            print(module)
    elif args.suggest:
        for suggestion in detector.suggest_missing_domains():
            print(suggestion)
    else:
        print(f"Detected {len(domains)} domains:")
        for name, domain in domains.items():
            print(f"  [{domain.confidence:.0%}] {name} ({domain.note_count} notes)")


if __name__ == "__main__":
    main()
