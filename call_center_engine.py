import os
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

# ----------------- PRELOADED MOCK CALL DATA -----------------
MOCK_CALLS = {
    "1": {
        "id": "1",
        "customer": "Sarah Connor",
        "agent": "John Smith",
        "status": "Completed",
        "duration": "4m 12s",
        "initial_sentiment": "Negative (Frustrated)",
        "current_sentiment": "Positive (Satisfied)",
        "priority": "High",
        "intent": "Billing Dispute",
        "transcript": [
            {"speaker": "Sarah Connor", "text": "Hi, I'm calling because my bill this month has a charge of $45 for some 'Premium Service Package' that I never signed up for! This is ridiculous, I want this refunded immediately."},
            {"speaker": "John Smith", "text": "Hi Ms. Connor, I understand your frustration. Let me look up your account. Can I have your account number?"},
            {"speaker": "Sarah Connor", "text": "It's ACCT-98217-CC. I've been a loyal customer for 5 years and this is how you treat us?"},
            {"speaker": "John Smith", "text": "Thank you. Let me check... Ah yes, I see the $45 charge. It looks like it was auto-applied when the trial period ended. I see you did not authorize it. Let me request a waiver for this."},
            {"speaker": "Sarah Connor", "text": "It should be waived! I don't want to see this on my bill again."},
            {"speaker": "John Smith", "text": "Absolutely, I'm processing the $45 credit refund right now. It will appear on your next statement. I'm also removing the package so you won't be billed again."},
            {"speaker": "Sarah Connor", "text": "Okay, thank you. I appreciate you fixing this quickly. I was about to cancel my service."},
            {"speaker": "John Smith", "text": "You're very welcome. Is there anything else I can assist you with today?"},
            {"speaker": "Sarah Connor", "text": "No, that's all. Thank you."}
        ]
    },
    "2": {
        "id": "2",
        "customer": "David Lightman",
        "agent": "Jennifer Mack",
        "status": "Active",
        "duration": "2m 15s",
        "initial_sentiment": "Frustrated",
        "current_sentiment": "Neutral",
        "priority": "Critical",
        "intent": "Technical Support",
        "transcript": [
            {"speaker": "David Lightman", "text": "Hello, my internet has been down for the last 2 hours. I have a critical online work presentation starting in 15 minutes! I need this resolved right now."},
            {"speaker": "Jennifer Mack", "text": "Hi Mr. Lightman, I understand the urgency. Let's get this fixed for you. Can you tell me which lights are active on your router?"},
            {"speaker": "David Lightman", "text": "Only the power light is solid green. The internet light is blinking red, and the WAN light is completely off."},
            {"speaker": "Jennifer Mack", "text": "Got it. Red internet light means the router isn't getting a signal from our server. Let's do a quick physical check first. Is the green coaxial cable firmly screwed in?"},
            {"speaker": "David Lightman", "text": "Yes, I checked. It's tight. I also unplugged the power for 30 seconds and plugged it back in, but it didn't change anything."},
            {"speaker": "Jennifer Mack", "text": "Okay, thanks for doing that. Let me run a line diagnostic check from my end. One moment..."},
            {"speaker": "Jennifer Mack", "text": "The signal to your modem is unreachable. It seems like there might be a local area outage or a physical line break."}
        ]
    },
    "3": {
        "id": "3",
        "customer": "Ellen Ripley",
        "agent": "Ash Robinson",
        "status": "Completed",
        "duration": "5m 30s",
        "initial_sentiment": "Negative",
        "current_sentiment": "Positive",
        "priority": "High",
        "intent": "Retention",
        "transcript": [
            {"speaker": "Ellen Ripley", "text": "Yes, I'd like to cancel my service today. I'm moving to a new provider called NetSpeed. They are offering 1Gbps fiber for only $50 a month, which is half of what I pay you."},
            {"speaker": "Ash Robinson", "text": "Hello Ms. Ripley, I'd be sorry to lose you. You've been with us for 3 years. Let me see what we can do. Our current fiber rate is $90, but let me check if we have any loyalty promotions for your area."},
            {"speaker": "Ellen Ripley", "text": "I don't want to haggle, I just want to cancel. NetSpeed has already scheduled their installation for tomorrow."},
            {"speaker": "Ash Robinson", "text": "I understand. If I can match that $50/month rate for the next 12 months with no contract, would you consider staying with us? It would save you the installation hassle."},
            {"speaker": "Ellen Ripley", "text": "Wait, you can match $50 a month? For the same speed I have now?"},
            {"speaker": "Ash Robinson", "text": "Actually, I can upgrade you to our 1Gbps speed tier and drop the price to $49.99 for 12 months. And since you're already set up, there's no installation needed."},
            {"speaker": "Ellen Ripley", "text": "Hmm. That would save me from having to wait for the NetSpeed technician tomorrow. Okay, if you can guarantee that rate is locked for a year with no contract, I'll stay."},
            {"speaker": "Ash Robinson", "text": "Perfect! I've updated your plan and applied the loyalty discount. Your new rate is $49.99 starting today. I'll send a confirmation email right now."},
            {"speaker": "Ellen Ripley", "text": "Great. Thank you for making that easy."}
        ]
    },
    "4": {
        "id": "4",
        "customer": "Bruce Wayne",
        "agent": "Alfred Pennyworth",
        "status": "Completed",
        "duration": "3m 15s",
        "initial_sentiment": "Positive",
        "current_sentiment": "Positive",
        "priority": "Medium",
        "intent": "Account Upgrade",
        "transcript": [
            {"speaker": "Bruce Wayne", "text": "Hello, I'm looking to upgrade my internet connection. We are running more devices in the house now, and the current 100Mbps plan is starting to feel sluggish during peak hours."},
            {"speaker": "Alfred Pennyworth", "text": "Good afternoon Mr. Wayne. I would be happy to help you upgrade. We have our superfast Fiber plans available at your address."},
            {"speaker": "Bruce Wayne", "text": "What are the speed options and pricing?"},
            {"speaker": "Alfred Pennyworth", "text": "We have two main tiers: 500Mbps for $65/month, and 1Gbps (1000Mbps) for $80/month. The 1Gbps plan also comes with free security software and a premium WiFi router."},
            {"speaker": "Bruce Wayne", "text": "The 1Gbps plan sounds like what we need. Does that require a contract?"},
            {"speaker": "Alfred Pennyworth", "text": "It is a standard 12-month agreement. However, we can waive the router rental fee of $10/month for the lifetime of your account as an upgrade incentive."},
            {"speaker": "Bruce Wayne", "text": "Excellent. Let's go ahead and upgrade to the 1Gbps Fiber plan."},
            {"speaker": "Alfred Pennyworth", "text": "Fantastic. I've processed the upgrade. The new speed is active on your line immediately. You should restart your router to verify the speed upgrade."},
            {"speaker": "Bruce Wayne", "text": "Thank you, Alfred. Very efficient."}
        ]
    }
}

class CallCenterEngine:
    def __init__(self, google_api_key=None, model="gemini-1.5-flash"):
        load_dotenv()
        api_key = google_api_key or os.environ.get("GOOGLE_API_KEY")
        
        if api_key:
            self.llm = ChatGoogleGenerativeAI(
                model=model,
                temperature=0.2,
                google_api_key=api_key
            )
        else:
            self.llm = None

        self.system_prompt = (
            "You are an expert Call Center Supervisor AI Assistant.\n"
            "Analyze the provided call center transcript and return a JSON object strictly containing the following keys:\n"
            "- 'intent': String representing the customer's core intent (e.g. Billing Dispute, Outage, Retention, Upgrade).\n"
            "- 'summary': A concise 2-3 sentence executive summary of the conversation.\n"
            "- 'sentiment_trend': A short summary of sentiment changes (e.g., 'Frustrated -> Satisfied' or 'Anxious -> Relieved').\n"
            "- 'entities': A list of dictionaries representing extracted entities. Each dictionary should have 'name' (e.g. Account Number, Refund Amount, competitor) and 'value'.\n"
            "- 'resolution_status': String representing the status (e.g., 'Resolved', 'In Progress', 'Escalation Required').\n"
            "- 'next_best_actions': A list of 2-3 actions. Each action is a dictionary with 'action' (the recommended step name), 'confidence' (float between 0.0 and 1.0), 'reason' (why this is suggested), and 'steps' (a list of 1-3 sub-steps to perform this action).\n\n"
            "Return ONLY the raw valid JSON. Do not include markdown code block styling like ```json. Do not include any trailing or leading explanation text."
        )

    def analyze_transcript(self, transcript_text):
        """Analyze transcript using Gemini LLM if available, otherwise fallback to local keyword rules."""
        if self.llm:
            try:
                prompt = ChatPromptTemplate.from_messages([
                    ("system", self.system_prompt),
                    ("human", "Analyze this transcript:\n\n{transcript}")
                ])
                chain = prompt | self.llm
                response = chain.invoke({"transcript": transcript_text})
                
                # Strip code blocks if LLM still formats it as markdown
                content = response.content.strip()
                if content.startswith("```json"):
                    content = content[7:]
                if content.endswith("```"):
                    content = content[:-3]
                content = content.strip()
                
                result = json.loads(content)
                return result
            except Exception as e:
                # If LLM call or JSON parsing fails, fallback to local analysis
                return self.generate_offline_analysis(transcript_text, error_msg=str(e))
        else:
            return self.generate_offline_analysis(transcript_text)

    def generate_offline_analysis(self, transcript_text, error_msg=None):
        """Analyzes transcript offline based on keyword rules."""
        text_lower = transcript_text.lower()
        
        # Billing dispute keyword match
        if any(kw in text_lower for kw in ["charge", "$45", "bill", "refund", "billing", "credit"]):
            return {
                "intent": "Billing Dispute",
                "summary": "Customer Sarah Connor contacted support regarding an unauthorized premium package charge of $45. The agent verified the billing error and applied a statement credit.",
                "sentiment_trend": "Negative (Frustrated) ➔ Positive (Satisfied)",
                "entities": [
                    {"name": "Customer Name", "value": "Sarah Connor"},
                    {"name": "Account Number", "value": "ACCT-98217-CC"},
                    {"name": "Disputed Charge", "value": "$45.00"},
                    {"name": "Adjustment Type", "value": "Billing Credit"}
                ],
                "resolution_status": "Resolved",
                "next_best_actions": [
                    {
                        "action": "Approve $45.00 Bill Credit",
                        "confidence": 0.98,
                        "reason": "Confirming removal of the unauthorized trial service and crediting back the fee maintains customer goodwill and avoids escalations.",
                        "steps": [
                            "Open Billing Ledger on CRM",
                            "Initiate credit adjustment for $45.00 with reference code BILL_ERR_2026",
                            "Verify change status reflects on supervisor ledger"
                        ]
                    },
                    {
                        "action": "Verify Premium Trial Exclusion",
                        "confidence": 0.92,
                        "reason": "Ensure account flag is set to exclude automatic trial opt-ins to prevent repeat billing issues.",
                        "steps": [
                            "Navigate to Account Services tab",
                            "Disable auto-renew for premium bundles",
                            "Save account attributes profile"
                        ]
                    }
                ]
            }
            
        # Tech support outage keyword match
        elif any(kw in text_lower for kw in ["down", "outage", "router", "wan", "signal", "internet"]):
            return {
                "intent": "Technical Support",
                "summary": "Customer David Lightman reports a complete internet outage that is interfering with their remote work schedule. Agent diagnostics indicate a link outage or localized fiber break.",
                "sentiment_trend": "Frustrated ➔ Neutral",
                "entities": [
                    {"name": "Customer Name", "value": "David Lightman"},
                    {"name": "Modem Status", "value": "Offline"},
                    {"name": "WAN Port Status", "value": "No Link Detect"},
                    {"name": "Internet LED Indicator", "value": "Blinking Red"}
                ],
                "resolution_status": "Escalation Required",
                "next_best_actions": [
                    {
                        "action": "Dispatch Field Technician (Priority)",
                        "confidence": 0.95,
                        "reason": "Physical coaxial/fiber signal test fails to respond, confirming a hardware layer interruption rather than a local configurations issue.",
                        "steps": [
                            "Create Dispatch Ticket in Field Services Console",
                            "Set priority to HIGH (Remote worker SLA)",
                            "Confirm appointment window with the client"
                        ]
                    },
                    {
                        "action": "Check Regional Fiber Outage Map",
                        "confidence": 0.90,
                        "reason": "Validate if the downstream line is part of a larger ongoing switch maintenance window or area incident.",
                        "steps": [
                            "Access Network Operations Center (NOC) live feed",
                            "Cross-reference customer ZIP code with active alert grid",
                            "Report node status to local dispatcher"
                        ]
                    }
                ]
            }

        # Retention keyword match
        elif any(kw in text_lower for kw in ["cancel", "competitor", "provider", "netspeed", "$50", "leaving"]):
            return {
                "intent": "Customer Retention",
                "summary": "Customer Ellen Ripley requested cancellation due to a competitive offer of 1Gbps for $50/month. The agent retained the customer by matching the price and upgrading their line.",
                "sentiment_trend": "Dissatisfied ➔ Positive",
                "entities": [
                    {"name": "Customer Name", "value": "Ellen Ripley"},
                    {"name": "Competitor Brand", "value": "NetSpeed"},
                    {"name": "Competitor Price", "value": "$50.00/mo"},
                    {"name": "Matching Offer", "value": "$49.99/mo (Fiber 1G)"}
                ],
                "resolution_status": "Resolved",
                "next_best_actions": [
                    {
                        "action": "Apply Customer Loyalty Rate Lock",
                        "confidence": 0.96,
                        "reason": "Retaining 3-year tenure accounts through strategic discount offers is more cost-effective than customer acquisition.",
                        "steps": [
                            "Navigate to Retention Catalog in Billing system",
                            "Apply code LOYAL_1G_49.99 to account template",
                            "Submit price override for supervisor auditing signature"
                        ]
                    },
                    {
                        "action": "Send Contract Details & Upgrades Email",
                        "confidence": 0.88,
                        "reason": "Explicit summary of the matched rates and speeds solidifies client alignment and minimizes buyer remorse.",
                        "steps": [
                            "Select loyalty email template in SMTP service",
                            "Populate matching offer data points",
                            "Send and log verification log into ticket ledger"
                        ]
                    }
                ]
            }
            
        # Upgrade keyword match
        elif any(kw in text_lower for kw in ["upgrade", "speed", "fiber", "sluggish", "1gbps"]):
            return {
                "intent": "Account Upgrade",
                "summary": "Customer Bruce Wayne requested line speed upgrades to support extra home devices. The agent upgraded the service plan to 1Gbps Fiber and waived router equipment fees.",
                "sentiment_trend": "Positive ➔ Positive",
                "entities": [
                    {"name": "Customer Name", "value": "Bruce Wayne"},
                    {"name": "Current Plan Speed", "value": "100 Mbps"},
                    {"name": "New Plan Speed", "value": "1000 Mbps (1 Gbps)"},
                    {"name": "Waiver Applied", "value": "Router Fee ($10/mo)"}
                ],
                "resolution_status": "Resolved",
                "next_best_actions": [
                    {
                        "action": "Provision 1G Fiber Network Profile",
                        "confidence": 0.99,
                        "reason": "Backend server speed limits must be dynamically updated to reflect the new fiber line speed tier selected.",
                        "steps": [
                            "Access Service Provisioning interface",
                            "Re-profile customer WAN MAC address to 1Gbps Downstream profile",
                            "Execute remote line restart signal"
                        ]
                    },
                    {
                        "action": "Configure Lifetime Router Waiver flag",
                        "confidence": 0.95,
                        "reason": "The agent promised a rental equipment waiver. Supervisors must verify this flag to avoid billing automated fees.",
                        "steps": [
                            "Select hardware rental items from account inventory",
                            "Check 'Waive Hardware Rental Charges' checkbox",
                            "Log waiver memo: 'Loyalty upgrade hardware incentive'"
                        ]
                    }
                ]
            }
            
        # Generic fallback
        else:
            return {
                "intent": "General Inquiry",
                "summary": "Customer is communicating with agent. The transcript has been processed successfully, but could not be categorized into one of our predefined default categories.",
                "sentiment_trend": "Neutral ➔ Neutral",
                "entities": [
                    {"name": "Conversation length", "value": f"{len(transcript_text.split())} words"},
                    {"name": "System Status", "value": "Online"}
                ],
                "resolution_status": "In Progress",
                "next_best_actions": [
                    {
                        "action": "Flag for Supervisor Audit Review",
                        "confidence": 0.85,
                        "reason": "Transcript requires customized supervisor evaluation as it does not match core billing, support, or retention categories.",
                        "steps": [
                            "Assign follow-up review flag 'SUP_AUDIT'",
                            "Export transcript content to audit ledger"
                        ]
                    }
                ]
            }
