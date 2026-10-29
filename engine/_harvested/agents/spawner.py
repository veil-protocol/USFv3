#!/usr/bin/env python3
"""
USF 6.5 APEX - Agent Spawner

Spawns agents with RAG-injected context from the vault.
This is the integration point between knowledge and execution.

Usage:
    spawner = AgentSpawner(vault_path, registry_path)
    task_yaml = spawner.spawn("recon-nmap-quick", task="Scan 10.10.10.1")
"""

import sys
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

sys.path.insert(0, str(Path(__file__).parent.parent))

from retrieval.rag_frontend import RAGFrontend, RetrievalContext
from retrieval.attack_retriever import AttackRetriever


@dataclass
class SpawnedAgent:
    """Represents a spawned agent ready for execution"""
    agent_id: str
    name: str
    subagent_type: str
    prompt: str
    tools: List[str]
    timeout_ms: int
    vault_context: Optional[RetrievalContext]


class AgentSpawner:
    """
    Agent Spawner with RAG Context Injection

    Loads agent definitions from registry.yaml and injects
    relevant vault knowledge into prompts before spawning.
    """

    def __init__(
        self,
        vault_path: str,
        registry_path: Optional[str] = None
    ):
        self.vault_path = Path(vault_path)

        # Load agent registry
        if registry_path:
            self.registry_path = Path(registry_path)
        else:
            self.registry_path = Path(__file__).parent / 'registry.yaml'

        self.registry = self._load_registry()

        # Initialize RAG components
        self.rag = RAGFrontend(str(vault_path))
        self.attack_retriever = AttackRetriever(str(vault_path))

        # Build agent lookup
        self.agents = self._build_agent_lookup()

    def _load_registry(self) -> Dict:
        """Load agent registry from YAML"""
        if not self.registry_path.exists():
            raise FileNotFoundError(f"Registry not found: {self.registry_path}")

        with open(self.registry_path) as f:
            return yaml.safe_load(f)

    def _build_agent_lookup(self) -> Dict[str, Dict]:
        """Build flat lookup of agent_id -> agent_config"""
        lookup = {}

        # Process each category
        for category, subcategories in self.registry.items():
            if not isinstance(subcategories, dict):
                continue

            for subcategory, agents in subcategories.items():
                if not isinstance(agents, list):
                    continue

                for agent in agents:
                    if isinstance(agent, dict) and 'id' in agent:
                        lookup[agent['id']] = agent
                        # Also add category info
                        agent['_category'] = category
                        agent['_subcategory'] = subcategory

        return lookup

    def list_agents(self, category: Optional[str] = None) -> List[Dict]:
        """List available agents, optionally filtered by category"""
        agents = []

        for agent_id, agent in self.agents.items():
            if category and agent.get('_category') != category:
                continue
            agents.append({
                'id': agent_id,
                'name': agent.get('name', agent_id),
                'description': agent.get('description', ''),
                'category': agent.get('_category'),
                'subcategory': agent.get('_subcategory'),
            })

        return agents

    def get_agent(self, agent_id: str) -> Optional[Dict]:
        """Get agent configuration by ID"""
        return self.agents.get(agent_id)

    def _extract_task_keywords(self, task: str) -> Dict[str, Optional[str]]:
        """Extract service, CVE, technique keywords from task"""
        import re

        keywords = {
            'service': None,
            'cve': None,
            'technique': None,
            'target_os': None,
        }

        task_lower = task.lower()

        # Extract CVE
        cve_match = re.search(r'cve-\d{4}-\d{4,}', task_lower)
        if cve_match:
            keywords['cve'] = cve_match.group().upper()

        # Extract service names
        services = ['http', 'https', 'smb', 'ssh', 'rdp', 'mysql', 'mssql',
                    'postgresql', 'ftp', 'ldap', 'kerberos', 'winrm', 'snmp']
        for service in services:
            if service in task_lower:
                keywords['service'] = service
                break

        # Extract techniques
        techniques = ['sqli', 'xss', 'lfi', 'rfi', 'ssti', 'ssrf', 'xxe',
                      'kerberoast', 'dcsync', 'pth', 'ptt', 'bloodhound',
                      'sudo', 'suid', 'kernel', 'token', 'mimikatz']
        for technique in techniques:
            if technique in task_lower:
                keywords['technique'] = technique
                break

        # Extract OS
        if 'windows' in task_lower:
            keywords['target_os'] = 'windows'
        elif 'linux' in task_lower:
            keywords['target_os'] = 'linux'

        return keywords

    def _get_context_for_task(
        self,
        task: str,
        agent_config: Dict,
        n_results: int = 5
    ) -> RetrievalContext:
        """Get relevant vault context for a task"""
        keywords = self._extract_task_keywords(task)

        # Use attack retriever for specific lookups
        if keywords['cve']:
            attack_ctx = self.attack_retriever.retrieve_for_cve(keywords['cve'])
            # Convert to general RAG context with the formatted output
            return self.rag.retrieve(task, n_results=n_results)

        if keywords['technique']:
            attack_ctx = self.attack_retriever.retrieve_for_technique(
                keywords['technique'],
                keywords['target_os']
            )
            return self.rag.retrieve(task, n_results=n_results)

        if keywords['service']:
            attack_ctx = self.attack_retriever.retrieve_for_service(keywords['service'])
            return self.rag.retrieve(task, n_results=n_results)

        # General task-based retrieval
        return self.rag.retrieve(task, n_results=n_results)

    def spawn(
        self,
        agent_id: str,
        task: str,
        target: Optional[Dict] = None,
        inject_context: bool = True,
        n_context_results: int = 5
    ) -> SpawnedAgent:
        """
        Spawn an agent with RAG-injected context.

        Args:
            agent_id: Agent ID from registry
            task: Task description
            target: Optional target info dict
            inject_context: Whether to inject vault context
            n_context_results: Number of context results to include

        Returns:
            SpawnedAgent ready for execution
        """
        agent = self.get_agent(agent_id)
        if not agent:
            raise ValueError(f"Unknown agent: {agent_id}")

        # Get context from vault
        vault_context = None
        context_section = ""

        if inject_context:
            vault_context = self._get_context_for_task(
                task, agent, n_context_results
            )
            context_section = vault_context.to_prompt_section()

        # Build prompt from template
        prompt_template = agent.get('prompt_template', 'Task: {task}')

        # Add target info if provided
        target_section = ""
        if target:
            target_lines = ["\n## Target Information"]
            for key, value in target.items():
                target_lines.append(f"- **{key}**: {value}")
            target_section = '\n'.join(target_lines)

        # Combine sections
        full_prompt = f"""
{prompt_template.format(task=task)}

{target_section}

{context_section}

## Instructions
- Use the vault context above to inform your approach
- Follow documented techniques where applicable
- Report findings in structured format
- If stuck, reference the source documents listed
"""

        return SpawnedAgent(
            agent_id=agent_id,
            name=agent.get('name', agent_id),
            subagent_type=agent.get('subagent_type', 'general-purpose'),
            prompt=full_prompt.strip(),
            tools=agent.get('tools', []),
            timeout_ms=agent.get('timeout_ms', 120000),
            vault_context=vault_context
        )

    def spawn_chain(
        self,
        agent_ids: List[str],
        task: str,
        target: Optional[Dict] = None
    ) -> List[SpawnedAgent]:
        """Spawn a chain of agents for sequential execution"""
        return [
            self.spawn(agent_id, task, target)
            for agent_id in agent_ids
        ]

    def to_task_yaml(self, spawned: SpawnedAgent) -> str:
        """
        Convert SpawnedAgent to Task tool YAML format.

        This is what gets passed to Claude's Task tool.
        """
        return f"""
subagent_type: "{spawned.subagent_type}"
description: "{spawned.name}"
prompt: |
{self._indent(spawned.prompt, 2)}
"""

    def to_executor_yaml(
        self,
        spawned: SpawnedAgent,
        run_in_background: bool = False
    ) -> Dict:
        """
        Convert SpawnedAgent to executor-compatible dict.

        This is what usf_executor.py expects.
        """
        return {
            'agent_id': spawned.agent_id,
            'subagent_type': spawned.subagent_type,
            'description': spawned.name,
            'prompt': spawned.prompt,
            'run_in_background': run_in_background,
            'tools': spawned.tools,
            'timeout_ms': spawned.timeout_ms,
        }

    def _indent(self, text: str, spaces: int) -> str:
        """Indent text by specified spaces"""
        prefix = ' ' * spaces
        return '\n'.join(prefix + line for line in text.split('\n'))

    def close(self):
        """Clean up resources"""
        self.rag.close()
        self.attack_retriever.close()


def main():
    """CLI entry point"""
    import argparse
    import json

    parser = argparse.ArgumentParser(description='USF Agent Spawner')
    parser.add_argument('vault_path', help='Path to Obsidian vault')
    parser.add_argument('--list', action='store_true', help='List available agents')
    parser.add_argument('--category', help='Filter by category')
    parser.add_argument('--agent', help='Agent ID to spawn')
    parser.add_argument('--task', help='Task description')
    parser.add_argument('--no-context', action='store_true', help='Skip RAG context')
    parser.add_argument('--yaml', action='store_true', help='Output as YAML')

    args = parser.parse_args()

    spawner = AgentSpawner(args.vault_path)

    try:
        if args.list:
            agents = spawner.list_agents(args.category)
            print(f"Available agents: {len(agents)}\n")
            for agent in agents[:20]:
                print(f"  {agent['id']}: {agent['description']}")
            if len(agents) > 20:
                print(f"\n  ... and {len(agents) - 20} more")

        elif args.agent and args.task:
            spawned = spawner.spawn(
                args.agent,
                args.task,
                inject_context=not args.no_context
            )

            if args.yaml:
                print(spawner.to_task_yaml(spawned))
            else:
                print(f"Agent: {spawned.name}")
                print(f"Type: {spawned.subagent_type}")
                print(f"Tools: {spawned.tools}")
                print(f"\nPrompt ({len(spawned.prompt)} chars):")
                print("-" * 40)
                print(spawned.prompt[:2000])
                if len(spawned.prompt) > 2000:
                    print(f"\n... ({len(spawned.prompt) - 2000} more chars)")

        else:
            parser.print_help()

    finally:
        spawner.close()


if __name__ == '__main__':
    main()
