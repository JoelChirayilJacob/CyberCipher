# CyberCipher

**AI-Powered SaaS Migration Support Agent**

An autonomous AI agent designed to detect, diagnose, and resolve migration issues for SaaS platforms transitioning to headless architecture. CyberCipher uses pattern recognition, long-term memory, and confidence-based decision-making to proactively handle support tickets and platform errors.

---

## Overview

CyberCipher monitors migration-related support tickets and platform errors in real-time, learning from historical data to identify root causes and recommend or execute fixes automatically. The system implements a human-in-the-loop approach for high-risk actions while autonomously handling low-risk, high-confidence scenarios.

### Key Features

- **AI-Powered Reasoning**: Uses Google Gemini to analyze patterns and identify root causes
- **Pattern Recognition**: Compares current issues against historical memory to detect recurring problems
- **Risk-Based Decision Making**: Automatic execution for low-risk issues, human approval for high-risk scenarios
- **Long-Term Memory**: Tracks resolved issues and learns from past actions
- **Interactive Dashboard**: Streamlit-based UI for monitoring and approving agent actions
- **Continuous Monitoring**: Background loop that detects new signals and triggers analysis
- **Automated Tooling**: Built-in tools for webhooks, notifications, escalations, and documentation

---

## Architecture

CyberCipher follows a modular agent architecture:

```
┌─────────────┐
│  Observer   │ ──> Monitors support tickets & platform errors
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Reasoner   │ ──> AI analyzes patterns using historical memory
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Decision   │ ──> Determines action type based on confidence & risk
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Actions   │ ──> Executes tools or requests human approval
└─────────────┘
```

### Core Components

| Module | Purpose |
|--------|---------|
| `observer.py` | Loads and filters support tickets and platform errors from data sources |
| `reasoner.py` | AI-powered analysis using Gemini API with memory-based pattern matching |
| `decision.py` | Risk and confidence-based decision engine |
| `actions.py` | Action executor that interfaces with agent tools |
| `tools.py` | Implementation of fix automation (webhooks, notifications, escalations) |
| `memory.py` | Persistent storage for tracking resolved issues and learning |
| `loop.py` | Background monitoring service that detects new signals |
| `app.py` | Streamlit dashboard for human oversight and approval |

---

## Getting Started

### Prerequisites

- Python 3.8+
- Google Gemini API key
- Streamlit

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/CyberCipher.git
   cd CyberCipher
   ```

2. **Install dependencies**
   ```bash
   pip install streamlit pandas python-dotenv google-generativeai
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

4. **Initialize data directory**
   
   The system will automatically create `data/` directory and `agent_memory.json` on first run.

### Running the Application

**Option 1: Interactive Dashboard**
```bash
streamlit run app.py
```
Access the dashboard at `http://localhost:8501`

**Option 2: Command-Line Mode**
```bash
python main.py
```

**Option 3: Background Monitoring Loop**
```bash
python loop.py
```

**Option 4: Test Auto-Fix (Demo)**
```bash
python test_auto_fix.py
```

---

## Project Structure

```
CyberCipher/
│
├── actions.py              # Action execution logic
├── app.py                  # Streamlit dashboard interface
├── decision.py             # Decision-making engine
├── demo_tools.py           # Tool demonstration script
├── loop.py                 # Background monitoring service
├── main.py                 # CLI entry point
├── memory.py               # Long-term memory management
├── observer.py             # Event monitoring and filtering
├── reasoner.py             # AI-powered analysis module
├── test_auto_fix.py        # Low-risk scenario testing
├── tools.py                # Agent tool implementations
│
├── data/
│   ├── mock_events.json        # Support tickets and errors
│   ├── low_risk_scenario.json  # Test scenario data
│   └── agent_memory.json       # Persistent memory storage
│
├── .env                    # Environment variables (create this)
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

---

## Usage Examples

### Example 1: Detecting Session Token Issues

**Input Signal:**
```json
{
  "type": "support_ticket",
  "merchant_id": "m13",
  "message": "Customer login fails with 'Session expired' immediately after login",
  "error": "session_token_invalid",
  "migration_stage": "post-headless"
}
```

**Agent Response:**
- **Hypothesis**: Session service misconfiguration in headless environment
- **Root Cause**: `migration_misconfiguration`
- **Confidence**: 85%
- **Risk Level**: High
- **Action**: Escalate to engineering with diagnostics checklist

### Example 2: Auto-Fixing Webhook Configuration

**Input Signal:**
```json
{
  "type": "support_ticket",
  "merchant_id": "m5",
  "message": "Webhook events stopped after migration",
  "error": "webhook_url_mismatch",
  "migration_stage": "post-headless"
}
```

**Agent Response:**
- **Confidence**: 95%
- **Risk Level**: Low
- **Action**: `AUTO_FIX` - Automatically reconfigures webhook endpoint
- **Requires Approval**: No

---

## Testing

### Run Low-Risk Scenario Test
```bash
python test_auto_fix.py
```

This demonstrates the agent's ability to:
- Identify recurring webhook issues
- Achieve high confidence (95%) for known patterns
- Automatically execute fixes without human approval

### Run Demo Tools
```bash
python demo_tools.py
```

Shows tool execution examples including:
- Webhook configuration fixes
- Engineering escalations
- Merchant notifications

---

## Configuration

### Confidence Thresholds

Defined in `decision.py`:

| Confidence | Risk | Action |
|-----------|------|--------|
| ≥ 90% | Low | Auto-fix |
| 70-89% | Medium/High | Escalate with approval |
| < 70% | Any | Monitor only |

### Risk Levels

| Level | Criteria | Examples |
|-------|----------|----------|
| **Low** | Configuration changes, known fixes | Webhook URL updates |
| **Medium** | Service restarts, temporary mitigations | API key resets |
| **High** | Production changes, data modifications | Database migrations |

---

## Dashboard Features

The Streamlit dashboard (`app.py`) provides:

- **Signal Detection**: Real-time alerts for new migration issues
- **Reasoning Chain**: Transparent AI decision-making process
- **Confidence Metrics**: Visual confidence scores and risk levels
- **Action Approval**: Human-in-the-loop controls for high-risk actions
- **Decision History**: Audit log of all agent decisions
- **Memory Inspector**: View long-term memory and learning progress

---

## Available Tools

| Tool | Purpose | Auto-Execute |
|------|---------|--------------||
| `fix_webhook_config` | Reconfigure webhook endpoints | Yes (if low risk) |
| `notify_merchant` | Send proactive notifications | Yes (if low risk) |
| `escalate_to_engineering` | Create engineering tickets | Requires approval |
| `update_documentation` | Auto-update help docs | Requires approval |
| `apply_temporary_fix` | Apply temporary mitigations | Conditional |

---

## AI Reasoning System

CyberCipher uses Google Gemini with a specialized prompt that:

1. **Compares signals against memory** to detect patterns
2. **Calculates confidence scores** based on historical matches
3. **Identifies root causes** across categories:
   - `migration_misconfiguration`
   - `platform_regression`
   - `documentation_gap`
   - `merchant_error`
   - `unknown`
4. **Recommends actions** with specific implementation steps

### Memory-Based Learning

The agent stores:
- **Resolved merchants**: Tracks which merchants have been helped and how
- **Action history**: Records root causes, recommended actions, and outcomes
- **Status tracking**: Differentiates between `pending_approval` and `resolved`

---

## Security & Best Practices

- **API Key Protection**: Never commit `.env` file (included in `.gitignore`)
- **Human Oversight**: High-risk actions require explicit approval
- **Audit Trail**: All actions logged with timestamps
- **Idempotency**: Tools designed to be safely re-executable
- **Rate Limiting**: Background loop uses 30-second intervals to avoid API abuse

---

## Future Enhancements

- [ ] Multi-tenant support with role-based access control
- [ ] Integration with ticketing systems (Zendesk, Jira)
- [ ] Advanced anomaly detection with ML models
- [ ] Slack/Teams notifications for critical issues
- [ ] A/B testing framework for auto-fix strategies
- [ ] Performance metrics and success rate tracking

---

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## Authors

- **Ravesh**
- **Joel**
- **Sahil**

---

## Acknowledgments

- Built with [Google Gemini](https://deepmind.google/technologies/gemini/) for AI reasoning
- Dashboard powered by [Streamlit](https://streamlit.io/)
- Inspired by autonomous agent architectures and SaaS migration challenges
