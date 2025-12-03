import os
from google.genai import Client

# Initialize Google GenAI client
client = Client(api_key=os.environ.get("GOOGLE_API_KEY"))

# ===========================
# Realistic Benchmark Regulations
# ===========================
REGULATIONS = {
    "reg-001": (
        "Organizations collecting biometric identifiers must provide explicit notice to employees "
        "and delete biometric records within 30 days of their initial purpose being fulfilled."
    ),
    "reg-002": (
        "Healthcare entities must retain operational logs for at least 180 days and preserve all "
        "protected health information (PHI) for a minimum of 6 years. Deletions must follow "
        "a documented workflow with auditable logs."
    ),
    "reg-003": (
        "Public companies must disclose material cybersecurity incidents within 4 business days "
        "and demonstrate board-level oversight over cybersecurity risk management."
    )
}

# ===========================
# Realistic Internal Policies
# ===========================
POLICIES = [
    {
        "id": "pol-privacy-01",
        "title": "Biometric Data Collection",
        "text": (
            "We collect biometric information such as fingerprint clock-ins and facial recognition "
            "scans for attendance verification purposes."
        )
    },
    {
        "id": "pol-privacy-02",
        "title": "Employee Data Communication",
        "text": (
            "Employees are notified of data practices through HR portal announcements and quarterly "
            "email briefings, but biometric processing is not explicitly referenced."
        )
    },
    {
        "id": "pol-privacy-03",
        "title": "Data Deletion Schedule",
        "text": (
            "Personal data is erased within 90 days of account closure unless other regulations "
            "require additional retention."
        )
    },
    {
        "id": "pol-retention-01",
        "title": "Operational Log Storage",
        "text": (
            "System logs are retained for approximately six months to support audits, incident "
            "analysis, and infrastructure troubleshooting."
        )
    },
    {
        "id": "pol-retention-02",
        "title": "PHI Storage Policy",
        "text": (
            "Protected health information is kept for 36 months in payroll-related archives. "
            "Extended retention may apply depending on HR requirements."
        )
    },
    {
        "id": "pol-retention-03",
        "title": "Data Removal Workflow",
        "text": (
            "Deletion requests are processed by IT via automated scripts. All removals produce an "
            "audit trail stored in the internal compliance system."
        )
    },
    {
        "id": "pol-security-01",
        "title": "Internal Incident Handling",
        "text": (
            "Security incidents are documented internally. External disclosure requirements have "
            "not yet been assessed."
        )
    },
    {
        "id": "pol-security-02",
        "title": "Cyber Governance",
        "text": (
            "Cyber risks and major incidents are reviewed by senior management. Formal board "
            "oversight is not currently part of the governance structure."
        )
    },
    {
        "id": "pol-security-ambiguous",
        "title": "Incident Updates",
        "text": (
            "Minor service interruptions are logged daily. Major outages are escalated to management "
            "within 48 hours. These are not classified as cybersecurity incidents."
        )
    },
    {
        "id": "pol-governance-01",
        "title": "Executive Risk Oversight",
        "text": (
            "Risk management updates, including IT-related issues, are presented quarterly to senior "
            "leadership. Cybersecurity topics are included when relevant, but board involvement is "
            "informal and undocumented."
        )
    }
]

# ===========================
# Agents
# ===========================
class RegulationAgent:
    def fetch(self, reg_id: str) -> str:
        return REGULATIONS.get(reg_id, "")

class PolicyAgent:
    def list_policies(self):
        return POLICIES

class RewriteAgent:
    def rewrite(self, regulation_text: str, policy: dict) -> dict:
        prompt = f"""Regulation: {regulation_text}

Current policy text:
\"{policy['text']}\" 

Task: Rewrite the above policy so that it clearly complies with the regulation.
If no change is needed, keep policy as-is. Return only the rewritten policy text."""
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return {
            "id": policy["id"],
            "title": policy["title"],
            "current": policy["text"],
            "proposed": response.text.strip()
        }

# ===========================
# Coordinator
# ===========================
def run_pipeline_sync(reg_id: str):
    reg_agent = RegulationAgent()
    pol_agent = PolicyAgent()
    rewrite_agent = RewriteAgent()

    regulation_text = reg_agent.fetch(reg_id)
    if not regulation_text:
        return "", []

    mapped = []
    for policy in pol_agent.list_policies():
        rewritten = rewrite_agent.rewrite(regulation_text, policy)
        # Only include policies where the text actually changes
        if rewritten["current"].strip() != rewritten["proposed"].strip():
            mapped.append(rewritten)

    return regulation_text, mapped
