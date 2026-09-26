# tAilorCode Architecture

This document explains the project using the terminology of the competition harness.

## High-level flow

```mermaid
flowchart TB
    S[Submission archive] --> V[Validate YAML and allowed files]
    V --> M[Load Gemma 4 model]
    M --> C[Compile the ADK agent tree]
    C --> A[Agent sandbox]
    A --> T[Repository and code-intelligence tools]
    T --> P[Generated Git patch]
    P --> R[Clean verification sandbox]
    R --> Q[Apply patch and protected tests]
    Q --> O[Resolution Rate]
```

## Two sandbox stages

```mermaid
sequenceDiagram
    participant Harness
    participant AgentSandbox
    participant VerificationSandbox

    Harness->>AgentSandbox: Extract repository at base commit
    Harness->>AgentSandbox: Install cached dependencies
    Harness->>AgentSandbox: Send issue and execution rules
    AgentSandbox->>AgentSandbox: Explore, edit, and run targeted tests
    AgentSandbox-->>Harness: Capture Git diff
    Harness->>VerificationSandbox: Extract a fresh repository snapshot
    Harness->>VerificationSandbox: Apply the agent patch
    Harness->>VerificationSandbox: Apply protected verification tests
    VerificationSandbox-->>Harness: Return pass or fail result
```

## Agent responsibilities

The root agent, `tAilorCode`, is responsible for the complete task. A read-only analyst can be delegated to locate relevant symbols and explain the likely root cause without modifying the repository.

```mermaid
flowchart LR
    I[Issue and hints] --> R[tAilorCode root agent]
    R --> N[Read-only code analyst]
    N --> E[Evidence and root-cause report]
    E --> R
    R --> W[Workspace edits]
    W --> T[Targeted tests]
    T --> D[Final Git diff]
```

## Design principles

1. Evidence before edits.
2. Minimal source changes.
3. Tests before submission.
4. No test or harness tampering.
5. Explicit final patch extraction.
6. Human review remains part of the workflow.

## Local evaluation note

The complete evaluation requires the competition harness, Gemma 4 model server, cached dependencies, and the sandbox environment. The public repository stores the agent configuration and explanations, while the downloaded competition data remains local and is excluded by `.gitignore`.

## Author

**Araceli Fradejas Munoz**
