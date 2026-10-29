# USF 4.0: Domain Taxonomy
## Hierarchical Classification for Universal Domain Adaptation

**Version**: 1.0.0
**Parent**: MASTER-SPECIFICATION.md
**Status**: Complete

---

## 1. Overview

The Domain Taxonomy provides a hierarchical classification system that enables USF 4.0 to:
1. Automatically detect the domain of any input problem
2. Select appropriate expert archetypes for the domain
3. Choose optimal phase templates
4. Enable cross-domain transfer learning

---

## 2. Taxonomy Structure

### 2.1 Root Classification

```
USF 4.0 DOMAIN TAXONOMY
═══════════════════════════════════════════════════════════════════════════════════════

ROOT
├── TECHNOLOGY (T)
│   ├── Security (T.SEC)
│   ├── Software (T.SFT)
│   ├── Infrastructure (T.INF)
│   ├── AI/ML (T.AIM)
│   └── Hardware (T.HRD)
│
├── BUSINESS (B)
│   ├── Strategy (B.STR)
│   ├── Operations (B.OPS)
│   ├── Finance (B.FIN)
│   └── Marketing (B.MKT)
│
├── SCIENCE (S)
│   ├── Research Methodology (S.RES)
│   ├── Physical Sciences (S.PHY)
│   ├── Life Sciences (S.LIF)
│   └── Social Sciences (S.SOC)
│
├── LEGAL (L)
│   ├── Regulatory (L.REG)
│   ├── Contract (L.CON)
│   ├── Intellectual Property (L.IPR)
│   └── Compliance (L.CMP)
│
├── MEDICAL (M)
│   ├── Diagnosis (M.DGN)
│   ├── Treatment (M.TRT)
│   ├── Research (M.RES)
│   └── Operations (M.OPS)
│
├── ENGINEERING (E)
│   ├── Systems (E.SYS)
│   ├── Mechanical (E.MEC)
│   ├── Electrical (E.ELE)
│   ├── Civil (E.CIV)
│   └── Chemical (E.CHM)
│
└── CROSS-DOMAIN (X)
    ├── Risk Management (X.RSK)
    ├── Project Management (X.PRJ)
    ├── Quality Assurance (X.QUA)
    └── Decision Analysis (X.DEC)

═══════════════════════════════════════════════════════════════════════════════════════
```

---

## 3. Detailed Domain Definitions

### 3.1 TECHNOLOGY (T)

#### T.SEC - Security

```
T.SEC - SECURITY
├── T.SEC.CRY - Cryptography
│   ├── T.SEC.CRY.SYM - Symmetric Cryptography
│   ├── T.SEC.CRY.ASY - Asymmetric Cryptography
│   ├── T.SEC.CRY.PRO - Protocol Design
│   ├── T.SEC.CRY.ZKP - Zero-Knowledge Proofs
│   ├── T.SEC.CRY.PQC - Post-Quantum Cryptography
│   └── T.SEC.CRY.FMV - Formal Verification
│
├── T.SEC.OFF - Offensive Security
│   ├── T.SEC.OFF.PEN - Penetration Testing
│   ├── T.SEC.OFF.RED - Red Teaming
│   ├── T.SEC.OFF.CVT - Covert Channels
│   ├── T.SEC.OFF.C2F - C2 Frameworks
│   ├── T.SEC.OFF.EXP - Exploit Development
│   └── T.SEC.OFF.MAL - Malware Analysis
│
├── T.SEC.DEF - Defensive Security
│   ├── T.SEC.DEF.SOC - Security Operations
│   ├── T.SEC.DEF.INC - Incident Response
│   ├── T.SEC.DEF.THR - Threat Intelligence
│   ├── T.SEC.DEF.DET - Detection Engineering
│   ├── T.SEC.DEF.FOR - Digital Forensics
│   └── T.SEC.DEF.BLU - Blue Teaming
│
├── T.SEC.PRI - Privacy
│   ├── T.SEC.PRI.ANO - Anonymity Systems
│   ├── T.SEC.PRI.DPR - Data Protection
│   ├── T.SEC.PRI.PET - Privacy-Enhancing Tech
│   └── T.SEC.PRI.CMP - Privacy Compliance
│
└── T.SEC.APP - Application Security
    ├── T.SEC.APP.WEB - Web Security
    ├── T.SEC.APP.MOB - Mobile Security
    ├── T.SEC.APP.API - API Security
    └── T.SEC.APP.CLD - Cloud Security
```

**Domain Characteristics**:
| Attribute | Value |
|-----------|-------|
| Adversarial Nature | HIGH |
| Formal Methods Applicability | HIGH |
| Default Expert Archetypes | Theoretical, Adversarial, Implementation |
| Default Phase Template | SECURITY_ANALYSIS |
| Typical Precision Level | PL3-PL5 |

**Key Terminology Signals**:
- Vulnerability, exploit, attack, threat, adversary
- Encryption, decryption, key, cipher, hash
- Penetration, intrusion, breach, compromise
- Authentication, authorization, access control
- Confidentiality, integrity, availability

---

#### T.SFT - Software

```
T.SFT - SOFTWARE
├── T.SFT.ARC - Architecture
│   ├── T.SFT.ARC.SYS - System Architecture
│   ├── T.SFT.ARC.DST - Distributed Systems
│   ├── T.SFT.ARC.MSV - Microservices
│   └── T.SFT.ARC.EVT - Event-Driven
│
├── T.SFT.DEV - Development
│   ├── T.SFT.DEV.FND - Frontend Development
│   ├── T.SFT.DEV.BCK - Backend Development
│   ├── T.SFT.DEV.FUL - Full Stack
│   └── T.SFT.DEV.EMB - Embedded Development
│
├── T.SFT.QUA - Quality
│   ├── T.SFT.QUA.TST - Testing
│   ├── T.SFT.QUA.REV - Code Review
│   ├── T.SFT.QUA.PER - Performance
│   └── T.SFT.QUA.REL - Reliability
│
└── T.SFT.OPS - DevOps
    ├── T.SFT.OPS.CI - Continuous Integration
    ├── T.SFT.OPS.CD - Continuous Deployment
    ├── T.SFT.OPS.INF - Infrastructure as Code
    └── T.SFT.OPS.MON - Monitoring
```

**Domain Characteristics**:
| Attribute | Value |
|-----------|-------|
| Adversarial Nature | MEDIUM |
| Formal Methods Applicability | MEDIUM |
| Default Expert Archetypes | Implementation, Quality, Strategic |
| Default Phase Template | DESIGN_REVIEW |
| Typical Precision Level | PL2-PL3 |

---

#### T.INF - Infrastructure

```
T.INF - INFRASTRUCTURE
├── T.INF.CLD - Cloud
│   ├── T.INF.CLD.AWS - Amazon Web Services
│   ├── T.INF.CLD.AZR - Microsoft Azure
│   ├── T.INF.CLD.GCP - Google Cloud Platform
│   └── T.INF.CLD.PVT - Private Cloud
│
├── T.INF.NET - Networking
│   ├── T.INF.NET.PRO - Protocols
│   ├── T.INF.NET.ROU - Routing
│   ├── T.INF.NET.SDN - Software-Defined Networking
│   └── T.INF.NET.WAN - Wide Area Networks
│
├── T.INF.STO - Storage
│   ├── T.INF.STO.BLK - Block Storage
│   ├── T.INF.STO.OBJ - Object Storage
│   ├── T.INF.STO.FIL - File Systems
│   └── T.INF.STO.DBS - Databases
│
└── T.INF.VRT - Virtualization
    ├── T.INF.VRT.HYP - Hypervisors
    ├── T.INF.VRT.CNT - Containers
    └── T.INF.VRT.SBX - Sandboxing
```

---

#### T.AIM - AI/ML

```
T.AIM - AI/ML
├── T.AIM.TRN - Training
│   ├── T.AIM.TRN.SUP - Supervised Learning
│   ├── T.AIM.TRN.UNS - Unsupervised Learning
│   ├── T.AIM.TRN.RNF - Reinforcement Learning
│   └── T.AIM.TRN.FED - Federated Learning
│
├── T.AIM.INF - Inference
│   ├── T.AIM.INF.OPT - Optimization
│   ├── T.AIM.INF.DEP - Deployment
│   └── T.AIM.INF.EDG - Edge Inference
│
├── T.AIM.SAF - AI Safety
│   ├── T.AIM.SAF.ALN - Alignment
│   ├── T.AIM.SAF.ROB - Robustness
│   ├── T.AIM.SAF.FAI - Fairness
│   └── T.AIM.SAF.INT - Interpretability
│
└── T.AIM.SEC - AI Security
    ├── T.AIM.SEC.ADV - Adversarial ML
    ├── T.AIM.SEC.POI - Data Poisoning
    ├── T.AIM.SEC.EXT - Model Extraction
    └── T.AIM.SEC.PRI - Model Privacy
```

---

#### T.HRD - Hardware

```
T.HRD - HARDWARE
├── T.HRD.CPU - Processors
│   ├── T.HRD.CPU.ARC - Microarchitecture
│   ├── T.HRD.CPU.CAC - Cache Systems
│   ├── T.HRD.CPU.SPC - Speculative Execution
│   └── T.HRD.CPU.TEE - Trusted Execution
│
├── T.HRD.MEM - Memory
│   ├── T.HRD.MEM.RAM - RAM Systems
│   ├── T.HRD.MEM.NVM - Non-Volatile Memory
│   └── T.HRD.MEM.HBM - High-Bandwidth Memory
│
├── T.HRD.SEC - Hardware Security
│   ├── T.HRD.SEC.TPM - Trusted Platform Module
│   ├── T.HRD.SEC.HSM - Hardware Security Module
│   ├── T.HRD.SEC.SID - Side Channels
│   └── T.HRD.SEC.TAM - Tamper Resistance
│
└── T.HRD.FRM - Firmware
    ├── T.HRD.FRM.BIO - BIOS/UEFI
    ├── T.HRD.FRM.BMC - Baseboard Management
    └── T.HRD.FRM.EMB - Embedded Firmware
```

---

### 3.2 BUSINESS (B)

```
B - BUSINESS
├── B.STR - Strategy
│   ├── B.STR.COR - Corporate Strategy
│   ├── B.STR.COM - Competitive Strategy
│   ├── B.STR.GRO - Growth Strategy
│   └── B.STR.DIG - Digital Strategy
│
├── B.OPS - Operations
│   ├── B.OPS.PRO - Process Optimization
│   ├── B.OPS.SUP - Supply Chain
│   ├── B.OPS.QUA - Quality Management
│   └── B.OPS.SCA - Scaling Operations
│
├── B.FIN - Finance
│   ├── B.FIN.VAL - Valuation
│   ├── B.FIN.INV - Investment Analysis
│   ├── B.FIN.RIS - Financial Risk
│   └── B.FIN.TRE - Treasury
│
└── B.MKT - Marketing
    ├── B.MKT.BRN - Brand Strategy
    ├── B.MKT.DIG - Digital Marketing
    ├── B.MKT.PRD - Product Marketing
    └── B.MKT.ANL - Market Analysis
```

**Domain Characteristics**:
| Attribute | Value |
|-----------|-------|
| Adversarial Nature | MEDIUM (competitive) |
| Formal Methods Applicability | LOW |
| Default Expert Archetypes | Strategic, Economic, Stakeholder |
| Default Phase Template | BUSINESS_STRATEGY |
| Typical Precision Level | PL1-PL2 |

---

### 3.3 SCIENCE (S)

```
S - SCIENCE
├── S.RES - Research Methodology
│   ├── S.RES.EXP - Experimental Design
│   ├── S.RES.STA - Statistical Analysis
│   ├── S.RES.REP - Reproducibility
│   └── S.RES.ETH - Research Ethics
│
├── S.PHY - Physical Sciences
│   ├── S.PHY.PHY - Physics
│   ├── S.PHY.CHM - Chemistry
│   ├── S.PHY.AST - Astronomy
│   └── S.PHY.GEO - Geology
│
├── S.LIF - Life Sciences
│   ├── S.LIF.BIO - Biology
│   ├── S.LIF.GEN - Genetics
│   ├── S.LIF.NEU - Neuroscience
│   └── S.LIF.ECO - Ecology
│
└── S.SOC - Social Sciences
    ├── S.SOC.PSY - Psychology
    ├── S.SOC.ECN - Economics
    ├── S.SOC.SOC - Sociology
    └── S.SOC.POL - Political Science
```

**Domain Characteristics**:
| Attribute | Value |
|-----------|-------|
| Adversarial Nature | LOW (skeptical review) |
| Formal Methods Applicability | VARIABLE |
| Default Expert Archetypes | Theoretical, Skeptical, Methodologist |
| Default Phase Template | SCIENTIFIC_RESEARCH |
| Typical Precision Level | PL2-PL4 |

---

### 3.4 LEGAL (L)

```
L - LEGAL
├── L.REG - Regulatory
│   ├── L.REG.FIN - Financial Regulation
│   ├── L.REG.HEA - Healthcare Regulation
│   ├── L.REG.ENV - Environmental Regulation
│   └── L.REG.TEL - Telecommunications
│
├── L.CON - Contract
│   ├── L.CON.COM - Commercial Contracts
│   ├── L.CON.EMP - Employment Contracts
│   ├── L.CON.LIC - Licensing Agreements
│   └── L.CON.MNA - M&A Agreements
│
├── L.IPR - Intellectual Property
│   ├── L.IPR.PAT - Patents
│   ├── L.IPR.TRM - Trademarks
│   ├── L.IPR.COP - Copyrights
│   └── L.IPR.TRS - Trade Secrets
│
└── L.CMP - Compliance
    ├── L.CMP.PRI - Privacy (GDPR, CCPA)
    ├── L.CMP.SEC - Security (SOC2, ISO27001)
    ├── L.CMP.FIN - Financial (SOX, Basel)
    └── L.CMP.IND - Industry-Specific
```

**Domain Characteristics**:
| Attribute | Value |
|-----------|-------|
| Adversarial Nature | HIGH (litigation) |
| Formal Methods Applicability | MEDIUM (precedent chains) |
| Default Expert Archetypes | Theoretical (law), Adversarial (opposing), Strategic |
| Default Phase Template | LEGAL_ANALYSIS |
| Typical Precision Level | PL2-PL3 |

---

### 3.5 MEDICAL (M)

```
M - MEDICAL
├── M.DGN - Diagnosis
│   ├── M.DGN.DIF - Differential Diagnosis
│   ├── M.DGN.IMG - Medical Imaging
│   ├── M.DGN.LAB - Laboratory Analysis
│   └── M.DGN.GEN - Genetic Diagnosis
│
├── M.TRT - Treatment
│   ├── M.TRT.PHR - Pharmacology
│   ├── M.TRT.SUR - Surgical
│   ├── M.TRT.THR - Therapeutic
│   └── M.TRT.PAL - Palliative
│
├── M.RES - Medical Research
│   ├── M.RES.CLI - Clinical Trials
│   ├── M.RES.TRN - Translational Research
│   ├── M.RES.EPI - Epidemiology
│   └── M.RES.PHA - Pharmaceutical R&D
│
└── M.OPS - Healthcare Operations
    ├── M.OPS.ADM - Administration
    ├── M.OPS.QUA - Quality Assurance
    ├── M.OPS.INF - Health Informatics
    └── M.OPS.POL - Health Policy
```

**Domain Characteristics**:
| Attribute | Value |
|-----------|-------|
| Adversarial Nature | LOW (but high stakes) |
| Formal Methods Applicability | MEDIUM |
| Default Expert Archetypes | Theoretical (clinical), Skeptical (zebra), Implementation |
| Default Phase Template | MEDICAL_DIAGNOSIS |
| Typical Precision Level | PL3-PL4 |

---

### 3.6 ENGINEERING (E)

```
E - ENGINEERING
├── E.SYS - Systems Engineering
│   ├── E.SYS.REQ - Requirements Engineering
│   ├── E.SYS.ARC - Systems Architecture
│   ├── E.SYS.INT - Integration
│   └── E.SYS.VAL - Verification & Validation
│
├── E.MEC - Mechanical Engineering
│   ├── E.MEC.DES - Design
│   ├── E.MEC.MFG - Manufacturing
│   ├── E.MEC.THR - Thermodynamics
│   └── E.MEC.FLU - Fluid Dynamics
│
├── E.ELE - Electrical Engineering
│   ├── E.ELE.POW - Power Systems
│   ├── E.ELE.SIG - Signal Processing
│   ├── E.ELE.EMB - Embedded Systems
│   └── E.ELE.COM - Communications
│
├── E.CIV - Civil Engineering
│   ├── E.CIV.STR - Structural
│   ├── E.CIV.GEO - Geotechnical
│   ├── E.CIV.TRN - Transportation
│   └── E.CIV.WAT - Water Resources
│
└── E.CHM - Chemical Engineering
    ├── E.CHM.PRO - Process Engineering
    ├── E.CHM.MAT - Materials
    ├── E.CHM.BIO - Biochemical
    └── E.CHM.ENV - Environmental
```

**Domain Characteristics**:
| Attribute | Value |
|-----------|-------|
| Adversarial Nature | LOW (but failure modes) |
| Formal Methods Applicability | HIGH |
| Default Expert Archetypes | Theoretical, Implementation, Quality, FMEA |
| Default Phase Template | DESIGN_REVIEW |
| Typical Precision Level | PL3-PL4 |

---

### 3.7 CROSS-DOMAIN (X)

```
X - CROSS-DOMAIN
├── X.RSK - Risk Management
│   ├── X.RSK.ASS - Risk Assessment
│   ├── X.RSK.MIT - Risk Mitigation
│   ├── X.RSK.MON - Risk Monitoring
│   └── X.RSK.COM - Risk Communication
│
├── X.PRJ - Project Management
│   ├── X.PRJ.PLN - Planning
│   ├── X.PRJ.EXE - Execution
│   ├── X.PRJ.MON - Monitoring & Control
│   └── X.PRJ.AGI - Agile Methods
│
├── X.QUA - Quality Assurance
│   ├── X.QUA.STD - Standards
│   ├── X.QUA.AUD - Auditing
│   ├── X.QUA.MET - Metrics
│   └── X.QUA.IMP - Improvement
│
└── X.DEC - Decision Analysis
    ├── X.DEC.FRM - Frameworks
    ├── X.DEC.MCD - Multi-Criteria Decision
    ├── X.DEC.UNC - Under Uncertainty
    └── X.DEC.GAM - Game Theory
```

---

## 4. Domain Signal Detection

### 4.1 Terminology Signals

Each domain has characteristic terminology that enables detection:

```yaml
domain_signals:
  T.SEC:
    high_confidence:
      - vulnerability
      - exploit
      - attack
      - threat
      - adversary
      - encryption
      - cipher
      - authentication
      - penetration
      - breach
    medium_confidence:
      - security
      - risk
      - protect
      - defend
      - access

  T.SFT:
    high_confidence:
      - function
      - class
      - API
      - framework
      - library
      - deploy
      - repository
      - commit
      - refactor
    medium_confidence:
      - code
      - build
      - test
      - debug

  B.STR:
    high_confidence:
      - market share
      - competitive advantage
      - value proposition
      - stakeholder
      - ROI
      - acquisition
      - growth strategy
    medium_confidence:
      - business
      - strategy
      - market
      - customer

  L.CON:
    high_confidence:
      - clause
      - indemnification
      - liability
      - jurisdiction
      - breach of contract
      - consideration
      - parties
    medium_confidence:
      - agreement
      - terms
      - legal
      - contract

  M.DGN:
    high_confidence:
      - differential diagnosis
      - symptom
      - etiology
      - prognosis
      - patient
      - clinical
      - pathology
    medium_confidence:
      - diagnosis
      - treatment
      - medical
      - health

  E.SYS:
    high_confidence:
      - requirements
      - specification
      - tolerance
      - failure mode
      - FMEA
      - validation
      - verification
    medium_confidence:
      - design
      - system
      - engineering
      - component
```

### 4.2 Structural Signals

Document structure patterns indicate domain:

| Domain | Structural Signals |
|--------|-------------------|
| T.SEC | Attack/defense sections, threat models, CVE references |
| T.SFT | Code blocks, API references, architecture diagrams |
| B.STR | Executive summary, SWOT, financial projections |
| L.CON | Numbered clauses, definitions section, signatures |
| M.DGN | Chief complaint, history, physical exam, assessment |
| E.SYS | Requirements tables, specification sheets, test plans |
| S.RES | Abstract, methodology, results, discussion |

### 4.3 Cross-Domain Detection

Problems often span multiple domains. Detection priority:

1. **Primary Domain**: Strongest signal concentration (>50% of signals)
2. **Secondary Domains**: Moderate signal presence (20-50%)
3. **Tertiary Domains**: Minor signal presence (10-20%)

```
EXAMPLE: Cryptographic Protocol Analysis
─────────────────────────────────────────
Signals detected:
├── T.SEC.CRY: 45% (encryption, key exchange, cipher)
├── T.SEC.OFF: 25% (attack, adversary, exploit)
├── T.SFT.ARC: 15% (protocol, architecture, implementation)
└── S.RES: 10% (proof, theorem, formal verification)

Result:
├── Primary: T.SEC.CRY (Cryptography)
├── Secondary: T.SEC.OFF (Offensive Security)
├── Tertiary: T.SFT.ARC, S.RES
└── Complexity: HIGH (4 domains)
```

---

## 5. Domain-to-Configuration Mapping

### 5.1 Default Expert Archetypes by Domain

| Domain | Theoretical | Adversarial | Implementation | Strategic | Quality |
|--------|-------------|-------------|----------------|-----------|---------|
| T.SEC | Shannon, Chaum | Red Team, APT | SysEng, DevSecOps | CISO, Risk | Formalist, Auditor |
| T.SFT | Architect | Edge Case | DevOps, SRE | Product | QA, Testing |
| B.STR | Economist | Competitor | Operations | CEO, Board | Due Diligence |
| L.CON | Blackstone | Opposing Counsel | Transactional | Risk Manager | Compliance |
| M.DGN | Osler, Bayes | Zebra | Hospitalist | Health Econ | Clinical Coord |
| E.SYS | Systems Theory | FMEA | Manufacturing | Cost Eng | V&V |

### 5.2 Default Phase Templates by Domain

| Domain | Phase Template |
|--------|---------------|
| T.SEC.* | SECURITY_ANALYSIS |
| T.SFT.*, T.INF.* | DESIGN_REVIEW |
| T.AIM.SAF | SAFETY_ANALYSIS |
| B.* | BUSINESS_STRATEGY |
| S.* | SCIENTIFIC_RESEARCH |
| L.* | LEGAL_ANALYSIS |
| M.DGN | MEDICAL_DIAGNOSIS |
| M.RES | CLINICAL_RESEARCH |
| E.* | ENGINEERING_DESIGN |
| X.RSK | RISK_ASSESSMENT |
| X.DEC | DECISION_ANALYSIS |

### 5.3 Default Precision Levels by Domain

| Domain | Min PL | Typical PL | Max PL | Rationale |
|--------|--------|------------|--------|-----------|
| T.SEC.CRY | PL3 | PL4 | PL5 | Formal proofs required |
| T.SEC.OFF | PL2 | PL3 | PL4 | Adversarial validation |
| T.SFT | PL1 | PL2 | PL3 | Depends on criticality |
| B.STR | PL1 | PL1 | PL2 | Uncertainty inherent |
| L.CON | PL2 | PL2 | PL3 | Precedent-based |
| M.DGN | PL2 | PL3 | PL4 | High stakes |
| E.SYS | PL2 | PL3 | PL4 | Safety-critical |
| S.RES | PL2 | PL3 | PL4 | Reproducibility |

---

## 6. Taxonomy Extensibility

### 6.1 Adding New Domains

New domains can be added through:

1. **Define taxonomy position**: Place in hierarchy
2. **Specify characteristics**: Fill out domain attributes
3. **Add terminology signals**: High/medium confidence terms
4. **Map to archetypes**: Which expert types apply
5. **Select phase template**: Or create new one
6. **Set precision defaults**: Based on domain nature

### 6.2 Domain Definition Template

```yaml
domain:
  code: X.NEW.SUB
  name: "New Subdomain"
  parent: X.NEW

  characteristics:
    adversarial_nature: LOW|MEDIUM|HIGH
    formal_methods_applicability: LOW|MEDIUM|HIGH
    uncertainty_level: LOW|MEDIUM|HIGH
    stakeholder_count: LOW|MEDIUM|HIGH

  signals:
    high_confidence:
      - term1
      - term2
    medium_confidence:
      - term3
      - term4

  defaults:
    archetypes:
      - theoretical: "DomainPioneer"
      - adversarial: "DomainSkeptic"
      - implementation: "DomainPractitioner"
    phase_template: TEMPLATE_NAME
    precision_range: [PL_MIN, PL_TYPICAL, PL_MAX]

  cross_domain_affinities:
    - related_domain_1: 0.7
    - related_domain_2: 0.4
```

---

## 7. Validation

### 7.1 Taxonomy Completeness Check

For any input problem, the taxonomy should:
- Identify at least one applicable domain (>10% signal match)
- Provide expert archetype mappings for identified domains
- Specify applicable phase templates
- Suggest precision level ranges

### 7.2 Ambiguity Resolution

When signals are ambiguous:
1. Request additional context from user
2. Use cross-domain analysis mode
3. Apply conservative (higher) precision levels
4. Generate experts from all applicable domains

---

**END OF DOMAIN TAXONOMY**

---

*Specification version: 1.0.0*
*Last updated: 2025-12-10*
