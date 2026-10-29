# Contributing to USF

Thank you for your interest in contributing to the Unified Superintelligence Framework!

## How to Contribute

### Reporting Issues

1. Check existing issues to avoid duplicates
2. Use the issue template
3. Include:
   - USF version
   - Clear description of the problem
   - Steps to reproduce
   - Expected vs actual behavior

### Proposing Changes

USF uses its own methodology for self-improvement. All changes should:

1. **Pass MAL Analysis**: Changes are validated by the Meta-Analysis Layer
2. **Maintain Compatibility**: Backward compatible with USF 4.x
3. **Include Provenance**: Document source of patterns/ideas
4. **Follow Precision Levels**: Match rigor to change criticality

### Contribution Process

```
1. Fork the repository
2. Create a feature branch
3. Make changes following USF methodology
4. Self-review using USF principles:
   - Apply ARC-AD (Adversarial) perspective
   - Check against all 5 archetypes
   - Verify precision level appropriateness
5. Submit PR with:
   - Clear description
   - Pattern provenance (if external)
   - Self-analysis results
```

### Change Categories

Per USF IMPROVEMENT-PROTOCOL.md:

| Category | Risk | Approval |
|----------|------|----------|
| DOMAIN | LOW | Auto-approved if tests pass |
| TEMPLATE | LOW-MEDIUM | Maintainer review |
| ARCHETYPE | MEDIUM | 2 maintainer review |
| PROCESS | MEDIUM-HIGH | Full team review |
| PRECISION | HIGH | Full team + testing |
| VERIFICATION | HIGH | Full team + formal review |
| META | CRITICAL | Core maintainer only |

### Code Style

- YAML for structured specifications
- Markdown for documentation
- Clear section headers
- Cross-references between specs
- Version tracking in changelogs

### Testing Changes

1. **Self-Red-Team**: Apply ARC-AD perspective to your own changes
2. **Multi-Archetype Review**: Consider TH, AD, IM, QA, ST perspectives
3. **Precision Verification**: Ensure claims match evidence level
4. **Integration Check**: Verify no conflicts with existing specs

## Recognition

Contributors are recognized in:
- CHANGELOG entries
- Pattern provenance registry (for external patterns)
- README acknowledgments (for significant contributions)

## Questions?

Open a discussion or issue. We're happy to help!

---

*This contribution guide follows USF 4.1.1 methodology*
