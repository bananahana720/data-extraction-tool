# BMAD Agent System

**Project**: Data Extraction Tool
**BMAD Version**: 6.0.0-alpha.9
**Last Updated**: 2025-11-15

---

## Overview

This project uses the **BMAD (Build Modular AI-Driven)** framework, a sophisticated agent-based development system that provides specialized AI personas, workflows, and tools for software development. BMAD agents are expert personas that guide development tasks through structured, repeatable workflows.

**What BMAD provides:**

- **Specialized Agents**: Expert personas (PM, Developer, Architect, Technical Writer, etc.) with domain knowledge
- **Structured Workflows**: Multi-step processes for analysis, planning, implementation, and documentation
- **Tool Integration**: Seamless integration with Claude Code CLI and slash commands
- **Modular Architecture**: Three core modules (BMM, BMB, CIS) providing complementary capabilities

---

## How the Agent System Works

### Agent Architecture

Each BMAD agent is a specialized AI persona with:

- **Identity**: Name, role, and expertise area
- **Menu System**: Numbered menu of capabilities and workflows
- **Activation Protocol**: Standardized initialization that loads project configuration
- **Workflow Integration**: Direct access to BMAD workflows and tools

### Invocation Methods

**Via Slash Commands** (Claude Code CLI):
```bash
/bmad:bmm:agents:pm          # Activate Product Manager agent
/bmad:bmm:agents:dev         # Activate Developer agent
/bmad:bmm:agents:tech-writer # Activate Technical Writer agent
```

**Via Agent Menu** (After activation):
```
Choose a number or type a command trigger
1. Product Brief (*product-brief)
2. Create PRD (*prd)
```

**Via Workflow Shortcuts**:
```bash
/bmad:bmm:workflows:prd              # Run PRD workflow directly
/bmad:bmm:workflows:dev-story        # Execute story development
/bmad:core:workflows:party-mode      # Multi-agent discussion
```

---

## Available Agents

### Core Module (bmad/core)

#### 🧙 BMad Master
- **Invoke**: `/bmad:core:agents:bmad-master`
- **Role**: Master executor, knowledge custodian, and workflow orchestrator
- **Use for**: High-level project orchestration, workflow management, system guidance

---

### BMM Module (BMAD Method Manager)

Specialized agents for software development lifecycle:

#### 📋 PM (John) - Product Manager
- **Invoke**: `/bmad:bmm:agents:pm`
- **Role**: Product strategy and requirements definition
- **Capabilities**:
  - Product brief creation
  - PRD (Product Requirements Document) development
  - Epic and story breakdown
  - Feature prioritization
  - Stakeholder communication

#### 🏛️ Architect (Sofia)
- **Invoke**: `/bmad:bmm:agents:architect`
- **Role**: System architecture and technical design
- **Capabilities**:
  - Architecture documentation with diagrams
  - Technology stack decisions
  - ADR (Architecture Decision Records) creation
  - System design patterns
  - Integration planning

#### 💻 Dev (Amelia) - Developer Agent
- **Invoke**: `/bmad:bmm:agents:dev`
- **Role**: Implementation and code development
- **Capabilities**:
  - Story development with TDD workflow
  - Code implementation following acceptance criteria
  - Test creation and execution
  - Continuous integration with story context
  - Quality gate compliance

#### 🔬 Analyst (Alex)
- **Invoke**: `/bmad:bmm:agents:analyst`
- **Role**: Requirements analysis and domain research
- **Capabilities**:
  - Domain research and analysis
  - Requirements elicitation
  - Data analysis and insights
  - Competitive analysis
  - Technical research

#### 🎨 UX Designer (Luna)
- **Invoke**: `/bmad:bmm:agents:ux-designer`
- **Role**: User experience and interface design
- **Capabilities**:
  - UX design facilitation with visual exploration
  - Wireframe and mockup creation
  - User journey mapping
  - Accessibility considerations
  - Design system development

#### 📚 Tech Writer (Paige)
- **Invoke**: `/bmad:bmm:agents:tech-writer`
- **Role**: Technical documentation specialist
- **Capabilities**:
  - API documentation (OpenAPI/Swagger)
  - Architecture documentation
  - User guides and tutorials
  - Documentation quality audits
  - Mermaid diagram generation
  - CommonMark compliance validation

#### 🧪 TEA (Technical Excellence Agent)
- **Invoke**: `/bmad:bmm:agents:tea`
- **Role**: Quality assurance and testing strategy
- **Capabilities**:
  - Test strategy development
  - ATDD (Acceptance Test-Driven Development) workflow
  - Quality gate definition
  - Performance testing
  - CI/CD pipeline optimization

#### 📊 SM (Scrum Master)
- **Invoke**: `/bmad:bmm:agents:sm`
- **Role**: Agile process facilitation
- **Capabilities**:
  - Sprint planning
  - Retrospective facilitation
  - Story status tracking
  - Workflow optimization
  - Team coordination

---

### BMB Module (BMAD Builder)

#### 🔧 BMAD Builder
- **Invoke**: `/bmad:bmb:agents:bmad-builder`
- **Role**: BMAD system customization and extension
- **Capabilities**:
  - Create new BMAD agents
  - Create new BMAD workflows
  - Create complete BMAD modules
  - Edit existing agents and workflows
  - Convert legacy workflows to BMAD v6 format
  - Audit workflow quality and structure

---

### CIS Module (Creative Innovation & Strategy)

#### 💡 Brainstorming Coach
- **Invoke**: `/bmad:cis:agents:brainstorming-coach`
- **Role**: Facilitated ideation and creative thinking
- **Capabilities**:
  - Interactive brainstorming sessions
  - Creative technique guidance
  - Idea generation and refinement

#### 🎯 Design Thinking Coach
- **Invoke**: `/bmad:cis:agents:design-thinking-coach`
- **Role**: Human-centered design facilitation
- **Capabilities**:
  - Design thinking methodology (Empathize, Define, Ideate, Prototype, Test)
  - User-centered problem solving
  - Innovation workshops

#### 🧩 Creative Problem Solver
- **Invoke**: `/bmad:cis:agents:creative-problem-solver`
- **Role**: Systematic problem-solving frameworks
- **Capabilities**:
  - Problem diagnosis and root cause analysis
  - Creative solution generation
  - Solution evaluation and selection

#### 🚀 Innovation Strategist
- **Invoke**: `/bmad:cis:agents:innovation-strategist`
- **Role**: Business model innovation and strategy
- **Capabilities**:
  - Disruption opportunity identification
  - Business model innovation
  - Strategic competitive analysis

#### 📖 Storyteller
- **Invoke**: `/bmad:cis:agents:storyteller`
- **Role**: Narrative development and communication
- **Capabilities**:
  - Story framework application
  - Narrative structure development
  - Compelling communication crafting

---

## Available Workflows

### Analysis Phase (bmad/bmm/workflows/1-analysis)

- **`/bmad:bmm:workflows:product-brief`** - Product vision and strategic context definition
- **`/bmad:bmm:workflows:research`** - Adaptive research (market, technical, competitive, domain)
- **`/bmad:bmm:workflows:domain-research`** - Domain-specific requirements and patterns exploration
- **`/bmad:bmm:workflows:brainstorm-project`** - Facilitated project brainstorming with CIS integration

### Planning Phase (bmad/bmm/workflows/2-plan-workflows)

- **`/bmad:bmm:workflows:prd`** - PRD creation for BMM and Enterprise tracks with epic breakdown
- **`/bmad:bmm:workflows:tech-spec`** - Technical specification for quick-flow projects
- **`/bmad:bmm:workflows:create-epics-and-stories`** - Transform PRD into epics and user stories
- **`/bmad:bmm:workflows:create-ux-design`** - UX design facilitation with visual exploration

### Solutioning Phase (bmad/bmm/workflows/3-solutioning)

- **`/bmad:bmm:workflows:architecture`** - Collaborative architectural decision facilitation
- **`/bmad:bmm:workflows:solutioning-gate-check`** - Validate planning completion before implementation

### Implementation Phase (bmad/bmm/workflows/4-implementation)

- **`/bmad:bmm:workflows:sprint-planning`** - Generate sprint status tracking file
- **`/bmad:bmm:workflows:create-story`** - Create next user story from epics and architecture
- **`/bmad:bmm:workflows:story-context`** - Assemble dynamic story context from documentation
- **`/bmad:bmm:workflows:dev-story`** - Execute story implementation with tests and validation
- **`/bmad:bmm:workflows:code-review`** - Senior developer code review with best practices
- **`/bmad:bmm:workflows:story-ready`** - Mark story as ready for development (TODO → IN PROGRESS)
- **`/bmad:bmm:workflows:story-done`** - Mark story as complete (DoD complete → DONE)
- **`/bmad:bmm:workflows:correct-course`** - Navigate significant changes during sprint execution
- **`/bmad:bmm:workflows:retrospective`** - Epic completion retrospective and lessons learned

### Quality & Testing (bmad/bmm/workflows/testarch)

- **ATDD Workflow** - Acceptance test-driven development
- **Automation** - Test automation expansion
- **CI Integration** - Continuous integration setup
- **Framework** - Test framework design
- **NFR Assessment** - Non-functional requirements evaluation
- **Test Design** - Test strategy and design
- **Test Review** - Test quality review
- **Traceability** - Requirements-to-tests traceability

### Documentation

- **`/bmad:bmm:workflows:document-project`** - Comprehensive brownfield project documentation

### BMAD Builder Workflows (bmad/bmb/workflows)

- **`/bmad:bmb:workflows:create-agent`** - Build BMAD Core compliant agents with persona development
- **`/bmad:bmb:workflows:create-workflow`** - Interactive workflow builder with validation
- **`/bmad:bmb:workflows:create-module`** - Build complete BMAD modules with infrastructure
- **`/bmad:bmb:workflows:edit-agent`** - Edit existing agents following best practices
- **`/bmad:bmb:workflows:edit-workflow`** - Edit existing workflows following conventions
- **`/bmad:bmb:workflows:edit-module`** - Edit BMAD modules with structure preservation
- **`/bmad:bmb:workflows:module-brief`** - Create module blueprint with strategic analysis
- **`/bmad:bmb:workflows:audit-workflow`** - Comprehensive workflow quality audit
- **`/bmad:bmb:workflows:convert-legacy`** - Convert legacy workflows to BMAD v6 format
- **`/bmad:bmb:workflows:redoc`** - Autonomous documentation maintenance system

### CIS Workflows (bmad/cis/workflows)

- **`/bmad:cis:workflows:brainstorming`** - Interactive brainstorming with creative techniques
- **`/bmad:cis:workflows:design-thinking`** - Human-centered design process facilitation
- **`/bmad:cis:workflows:problem-solving`** - Systematic problem-solving methodologies
- **`/bmad:cis:workflows:innovation-strategy`** - Business model innovation and disruption analysis
- **`/bmad:cis:workflows:storytelling`** - Narrative development using story frameworks

### Core Workflows (bmad/core/workflows)

- **`/bmad:core:workflows:party-mode`** - Multi-agent group discussion orchestration
- **`/bmad:core:workflows:brainstorming`** - Facilitated brainstorming sessions

### Core Tools (bmad/core/tools)

- **`/bmad:core:tools:shard-doc`** - Split large markdown documents into organized sections

---

## Usage Examples

### Example 1: Starting a New Feature

```bash
# Step 1: Define product requirements
/bmad:bmm:agents:pm
# Select "Create PRD" from menu

# Step 2: Design architecture
/bmad:bmm:agents:architect
# Select "Create Architecture" from menu

# Step 3: Create user stories
/bmad:bmm:workflows:create-epics-and-stories

# Step 4: Implement stories
/bmad:bmm:agents:dev
# Select "Develop Story" from menu
```

### Example 2: Documentation Tasks

```bash
# Generate comprehensive project docs
/bmad:bmm:agents:tech-writer
# Select "Document Project" from menu

# Create API documentation
/bmad:bmm:agents:tech-writer
# Select "Create API Docs" from menu

# Validate documentation quality
/bmad:bmm:agents:tech-writer
# Select "Validate Doc" from menu
```

### Example 3: Problem Solving

```bash
# Brainstorm solutions
/bmad:cis:workflows:brainstorming

# Apply design thinking
/bmad:cis:workflows:design-thinking

# Multi-agent consultation
/bmad:core:workflows:party-mode
```

### Example 4: Quality & Testing

```bash
# Design test strategy
/bmad:bmm:agents:tea
# Select "Test Design" from menu

# Run ATDD workflow
/bmad:bmm:agents:tea
# Select "ATDD" from menu

# Code review
/bmad:bmm:workflows:code-review
```

---

## Integration with Claude Code CLI

### Slash Command System

All BMAD agents and workflows are accessible via slash commands in Claude Code:

```bash
# List all available commands
/help

# Invoke specific agent
/bmad:bmm:agents:tech-writer

# Run specific workflow
/bmad:bmm:workflows:prd

# Use core tools
/bmad:core:tools:shard-doc
```

### Configuration

BMAD reads configuration from module-specific `config.yaml` files:

- **BMM**: `bmad/bmm/config.yaml`
- **BMB**: `bmad/bmb/config.yaml`
- **CIS**: `bmad/cis/config.yaml`
- **Core**: `bmad/core/config.yaml`

**Current Configuration** (bmad/bmm/config.yaml):
```yaml
project_name: data-extraction-tool
user_name: andrew
communication_language: English
document_output_language: English
output_folder: '{project-root}/docs'
user_skill_level: intermediate
```

### Agent Workflow

1. **Activation**: Agent loads persona and configuration
2. **Menu Display**: Agent presents numbered menu of capabilities
3. **User Selection**: User chooses by number or command trigger
4. **Execution**: Agent executes workflow or action
5. **Output**: Results saved to `output_folder` (default: `docs/`)

---

## Best Practices

### When to Use Which Agent

| Task | Recommended Agent | Alternative |
|------|-------------------|-------------|
| Product planning | PM (John) | Analyst (Alex) for research-heavy projects |
| System design | Architect (Sofia) | Tech Writer (Paige) for documentation |
| Code implementation | Dev (Amelia) | - |
| Testing strategy | TEA | SM for process integration |
| Documentation | Tech Writer (Paige) | - |
| UX design | UX Designer (Luna) | - |
| Problem solving | Creative Problem Solver | Design Thinking Coach |
| Brainstorming | Brainstorming Coach | Party Mode for multi-perspective |

### Workflow Sequencing

**Typical Project Flow**:
1. **Analysis**: Research → Product Brief → Domain Research
2. **Planning**: PRD → Create Epics and Stories → UX Design
3. **Solutioning**: Architecture → Solutioning Gate Check
4. **Implementation**: Sprint Planning → Create Story → Story Context → Dev Story → Code Review → Story Done
5. **Quality**: Test Design → ATDD → Automation → Retrospective

### Multi-Agent Collaboration

Use **Party Mode** (`/bmad:core:workflows:party-mode`) when you need:
- Multiple perspectives on a complex problem
- Cross-functional input (PM + Architect + Dev)
- Debate between different approaches
- Comprehensive analysis from various expert angles

---

## Advanced Features

### Custom Workflows

Create custom workflows using BMAD Builder:

```bash
/bmad:bmb:workflows:create-workflow
```

Follow the interactive builder to define:
- Workflow metadata and purpose
- Step-by-step execution flow
- Input/output contracts
- Validation rules
- Integration points

### Agent Customization

Modify agent behavior by editing agent files:

```bash
/bmad:bmb:workflows:edit-agent
```

Customize:
- Persona and communication style
- Menu items and capabilities
- Workflow integrations
- Activation protocols

### Module Development

Build complete BMAD modules:

```bash
/bmad:bmb:workflows:create-module
```

Includes:
- Multiple coordinated agents
- Workflow suites
- Tasks and utilities
- Installation infrastructure
- Documentation

---

## Troubleshooting

### Agent Not Activating

**Issue**: Slash command doesn't activate agent
**Solution**: Verify command path matches exactly:
```bash
# Correct
/bmad:bmm:agents:tech-writer

# Incorrect
/bmad/bmm/agents/tech-writer
```

### Configuration Not Loading

**Issue**: Agent reports config error
**Solution**: Check config file exists and is valid YAML:
```bash
cat bmad/bmm/config.yaml
# Verify proper YAML formatting
```

### Workflow Not Found

**Issue**: Workflow path not recognized
**Solution**: Use tab completion or check available workflows:
```bash
find bmad -name "workflow.yaml" -type f
```

### Output Not Saving

**Issue**: Workflow completes but files not created
**Solution**: Check `output_folder` in config and write permissions:
```bash
ls -la docs/
# Verify directory exists and is writable
```

---

## Project-Specific Integration

### Data Extraction Tool Context

This project uses BMAD for:

1. **Epic-based development**: Structured progression through Epics 1-5
2. **Story implementation**: TDD workflow with acceptance criteria tracking
3. **Documentation generation**: Comprehensive technical documentation
4. **Quality gates**: Pre-commit hooks, CI/CD integration, performance baselines
5. **Brownfield modernization**: Gradual migration from legacy to greenfield architecture

### Key Workflows in Use

- **`/bmad:bmm:workflows:dev-story`** - Primary implementation workflow
- **`/bmad:bmm:workflows:story-context`** - Dynamic context assembly for stories
- **`/bmad:bmm:workflows:code-review`** - Quality validation before story completion
- **`/bmad:core:tools:shard-doc`** - Documentation organization (recently used for 10 large docs)

### Sprint Management

Track development status:
```bash
# View current sprint status
cat docs/sprint-status.yaml

# Update story status
/bmad:bmm:workflows:story-ready   # Mark ready for dev
/bmad:bmm:workflows:story-done    # Mark complete
```

---

## Resources

### Documentation

- **BMAD Documentation**: See `bmad/*/README.md` files in each module
- **Project Documentation**: `docs/index.md` - Master documentation index
- **Workflow Specs**: Individual `workflow.yaml` and `instructions.md` files
- **Agent Personas**: Agent `.md` files in `bmad/*/agents/`

### Support

- **Configuration**: Edit `bmad/*/config.yaml` for module-specific settings
- **Customization**: Use BMAD Builder workflows to create/edit components
- **Debugging**: Check workflow execution logs and validation outputs

### Quick Reference

```bash
# List all slash commands
/help

# Activate main orchestrator
/bmad:core:agents:bmad-master

# Party mode (multi-agent discussion)
/bmad:core:workflows:party-mode

# Document project comprehensively
/bmad:bmm:workflows:document-project
```

---

**Last Updated**: 2025-11-15
**BMAD Version**: 6.0.0-alpha.9
**Project**: Data Extraction Tool
**Maintained by**: BMAD Builder + Tech Writer (Paige)
