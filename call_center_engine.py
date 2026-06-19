import os
import json
from dotenv import load_dotenv

# ----------------- PRELOADED MOCK CALL DATA -----------------
MOCK_CALLS = {
    "1": {
        "id": "1",
        "customer": "Sarah Connor",
        "agent": "John Smith",
        "status": "Completed",
        "duration": "3m 45s",
        "initial_sentiment": "Negative (Frustrated)",
        "current_sentiment": "Positive (Satisfied)",
        "priority": "High",
        "intent": "Shipping Inquiry",
        "transcript": [
            {"speaker": "Sarah Connor", "text": "Hello, I'm calling because my delivery package with tracking ID SH-98217-CC has been stuck in transit for the last 5 days. I paid for overnight shipping and this is unacceptable!"},
            {"speaker": "John Smith", "text": "Hi Ms. Connor, I sincerely apologize for the delay. Let me check the shipping ledger for package SH-98217-CC. Can you confirm the shipping address?"},
            {"speaker": "Sarah Connor", "text": "It's 1829 Industrial Road. It was supposed to be delivered last Monday."},
            {"speaker": "John Smith", "text": "Thank you. Let me check... Ah, I see. It looks like the shipping courier routed it to the wrong sorting hub. Let me expedite it. I am also refunding your $15 shipping fee."},
            {"speaker": "Sarah Connor", "text": "Well, thank you for the refund, but when will it arrive? I need this item by tomorrow."},
            {"speaker": "John Smith", "text": "I've updated the carrier priority to express air. It is scheduled to arrive at your doorstep tomorrow by 12:00 PM. I'll email you the new tracking logs."},
            {"speaker": "Sarah Connor", "text": "Okay, that sounds much better. Thank you for fixing this."},
            {"speaker": "John Smith", "text": "You're very welcome, Ms. Connor. Have a great day!"}
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
        "intent": "Travel Inquiry",
        "transcript": [
            {"speaker": "David Lightman", "text": "Hi, I need to reschedule my travel flight ticket from New York to Chicago tomorrow. My booking reference is TRV-8821. My meeting was moved, so I need a later departure."},
            {"speaker": "Jennifer Mack", "text": "Hello Mr. Lightman, I can help you with your travel itinerary. Let me pull up booking TRV-8821. I see you are currently on the 8:00 AM flight."},
            {"speaker": "David Lightman", "text": "Yes, I need to change that to any flight departing after 3:00 PM tomorrow if possible. What options do we have?"},
            {"speaker": "Jennifer Mack", "text": "Let me check available seats... I have an evening flight departing at 5:30 PM with seats available. However, there is a travel ticket change fee of $50."},
            {"speaker": "David Lightman", "text": "Is there any way to waive that fee? I travel with your airline frequently."},
            {"speaker": "Jennifer Mack", "text": "Let me check your frequent flyer status... Since you are a Gold member, I can waive the travel change fee for you. I will book you on the 5:30 PM flight now."},
            {"speaker": "David Lightman", "text": "Excellent! Thank you so much. That's very helpful."},
            {"speaker": "Jennifer Mack", "text": "All set. The updated ticket confirmation has been sent to your email. Safe travels!"}
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

# ----------------- HUGGINGFACE MODEL CACHE LOADERS -----------------
# Dynamically load the pipelines inside Streamlit to avoid heavy startup penalty.
# Fallback to rules if models fail to download or load.

def get_streamlit_cache_decorator():
    try:
        import streamlit as st
        return st.cache_resource
    except ImportError:
        def dummy_decorator(*args, **kwargs):
            def inner(func):
                return func
            return inner
        return dummy_decorator

cache_decorator = get_streamlit_cache_decorator()

@cache_decorator(show_spinner="Loading BART Summarization Model...")
def load_bart_summarizer():
    try:
        from transformers import pipeline
        # facebook/bart-large-cnn generates high-quality summaries
        return pipeline("summarization", model="facebook/bart-large-cnn")
    except Exception as e:
        print(f"BART Summarizer load failed, falling back: {e}")
        return None

@cache_decorator(show_spinner="Loading DistilBERT Sentiment Model...")
def load_distilbert_sentiment():
    try:
        from transformers import pipeline
        return pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    except Exception as e:
        print(f"DistilBERT Sentiment load failed, falling back: {e}")
        return None

@cache_decorator(show_spinner="Loading Zero-Shot Intent Classifier...")
def load_zero_shot_classifier():
    try:
        from transformers import pipeline
        # facebook/bart-large-mnli is standard for zero-shot tasks
        return pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    except Exception as e:
        # Fallback to lighter model if memory is restricted
        try:
            from transformers import pipeline
            return pipeline("zero-shot-classification", model="typeform/distilbert-base-uncased-mnli")
        except Exception as ex:
            print(f"Zero-shot load failed, falling back: {ex}")
            return None


class CallCenterEngine:
    def __init__(self, google_api_key=None, model="gemini-1.5-flash"):
        load_dotenv()
        
        # Keep local model loader status
        self.summarizer = load_bart_summarizer()
        self.sentiment_model = load_distilbert_sentiment()
        self.zero_shot_model = load_zero_shot_classifier()

    def analyze_transcript(self, transcript_text):
        """Analyze call transcript using HuggingFace models, falls back to rules if failed."""
        results = {
            "intent": "Unclassified",
            "summary": "Generating summary...",
            "sentiment_trend": "Neutral",
            "entities": [],
            "resolution_status": "In Progress",
            "next_best_actions": [],
            "model_status": "🟢 Local HF Models Active"
        }

        # 1. Local HF BART Summarization (exactly 1-2 sentences)
        if self.summarizer:
            try:
                # Limit input text length to avoid overflow
                summary_input = transcript_text[:1024]
                summary_out = self.summarizer(summary_input, max_length=55, min_length=25, do_sample=False)
                summary_text = summary_out[0]['summary_text'].strip()
                # Clean up punctuation spacing if any
                summary_text = summary_text.replace(" .", ".")
                results["summary"] = summary_text
            except Exception as e:
                results["summary"] = f"BART Error: {e}"
        else:
            results["model_status"] = "⚠️ Rule-based Fallback Active"

        # 2. Local HF DistilBERT Sentiment Analysis
        if self.sentiment_model:
            try:
                # Analyze the last 300 chars of dialogue to find final resolution sentiment
                sentiment_input = transcript_text[-300:]
                sentiment_out = self.sentiment_model(sentiment_input)
                label = sentiment_out[0]['label']
                score = sentiment_out[0]['score']
                
                # Format to a nice text representation
                sentiment_lbl = "Positive (Satisfied)" if label == "LABEL_1" or "pos" in label.lower() else "Negative (Frustrated)"
                results["sentiment_trend"] = f"{sentiment_lbl} (DistilBERT: {int(score * 100)}% Conf)"
            except Exception as e:
                results["sentiment_trend"] = f"Sentiment Error: {e}"

        # 3. Local HF Zero-Shot Classification (whether shipping or travel)
        if self.zero_shot_model:
            try:
                candidate_labels = ["shipping", "travel", "billing", "technical support"]
                classification_out = self.zero_shot_model(transcript_text[:1024], candidate_labels=candidate_labels)
                
                # Get the highest score
                best_label = classification_out['labels'][0]
                best_score = classification_out['scores'][0]
                
                # Determine classification (shipping vs travel or other)
                results["intent"] = f"{best_label.capitalize()} ({int(best_score * 100)}% Match)"
                
                if best_label == "shipping":
                    results["entities"] = [
                        {"name": "Intent Category", "value": "Shipping (Zero-Shot)"},
                        {"name": "Confidence Level", "value": f"{int(best_score * 100)}%"}
                    ]
                elif best_label == "travel":
                    results["entities"] = [
                        {"name": "Intent Category", "value": "Travel (Zero-Shot)"},
                        {"name": "Confidence Level", "value": f"{int(best_score * 100)}%"}
                    ]
            except Exception as e:
                results["intent"] = f"Zero-shot Error: {e}"

        # Merge in rules/mock actions to ensure realistic output and resolution items
        fallback = self.generate_offline_analysis(transcript_text)
        
        # If Summarizer failed or was not loaded, use rule-based summary
        if not self.summarizer or "Error" in results["summary"] or len(results["summary"]) < 5:
            results["summary"] = fallback["summary"]
            
        # If Sentiment model failed or was not loaded, use rule-based sentiment
        if not self.sentiment_model or "Error" in results["sentiment_trend"]:
            results["sentiment_trend"] = fallback["sentiment_trend"]
            
        # If Zero Shot model failed or was not loaded, use rule-based intent
        if not self.zero_shot_model or "Error" in results["intent"] or results["intent"] == "Unclassified":
            results["intent"] = fallback["intent"]
            results["entities"] = fallback["entities"]

        results["resolution_status"] = fallback["resolution_status"]
        results["next_best_actions"] = fallback["next_best_actions"]

        # Parse specific entities from transcript using rule regexes to make it complete
        results["entities"].extend(self.extract_regex_entities(transcript_text))

        return results

    def extract_regex_entities(self, text):
        """Helper to extract account numbers or tracking numbers from transcript."""
        entities = []
        words = text.split()
        for w in words:
            # Clean symbols
            w_clean = w.strip(".,:;!?()\"'")
            if "SH-" in w_clean:
                entities.append({"name": "Tracking ID", "value": w_clean})
            elif "TRV-" in w_clean:
                entities.append({"name": "Booking Reference", "value": w_clean})
            elif "ACCT-" in w_clean:
                entities.append({"name": "Account Number", "value": w_clean})
        return entities

    def generate_offline_analysis(self, transcript_text, error_msg=None):
        """Offline metadata generator if transformers libraries are unavailable."""
        text_lower = transcript_text.lower()
        
        # Shipping query
        if any(kw in text_lower for kw in ["shipping", "tracking", "package", "transit", "sh-", "delivery"]):
            return {
                "intent": "Shipping Inquiry (Mock)",
                "summary": "Customer Sarah Connor reports her package SH-98217-CC has been delayed in transit. The agent resolved the inquiry by upgrading shipping speed and crediting fees.",
                "sentiment_trend": "Negative (Frustrated) ➔ Positive (Satisfied)",
                "entities": [
                    {"name": "Intent Category", "value": "Shipping"},
                    {"name": "Tracking ID", "value": "SH-98217-CC"},
                    {"name": "Refund Amount", "value": "$15.00"}
                ],
                "resolution_status": "Resolved",
                "next_best_actions": [
                    {
                        "action": "Process $15 Shipping Refund",
                        "confidence": 0.98,
                        "reason": "Customer paid for overnight courier delivery which was delayed by routing mistakes. Refunding fee maintains customer trust.",
                        "steps": [
                            "Open Shipping Ledger console",
                            "Initiate credit transaction refund of $15.00",
                            "Confirm email notification transaction receipt is sent"
                        ]
                    },
                    {
                        "action": "Expedite Courier Route Priority",
                        "confidence": 0.94,
                        "reason": "Change status of transit dispatch to Express Air delivery to ensure arrival by next day SLA.",
                        "steps": [
                            "Access courier booking portal",
                            "Flag tracking ID SH-98217-CC as priority air freight",
                            "Alert local courier dispatch supervisor"
                        ]
                    }
                ]
            }
            
        # Travel booking query
        elif any(kw in text_lower for kw in ["travel", "flight", "ticket", "reschedule", "trv-", "chicago"]):
            return {
                "intent": "Travel Inquiry (Mock)",
                "summary": "Customer David Lightman requested a departure change for his flight to Chicago. Agent waived the travel change fees due to frequency flyer status and booked him on an evening flight.",
                "sentiment_trend": "Frustrated ➔ Positive",
                "entities": [
                    {"name": "Intent Category", "value": "Travel"},
                    {"name": "Booking Reference", "value": "TRV-8821"},
                    {"name": "Frequent Flyer Tier", "value": "Gold member"}
                ],
                "resolution_status": "Resolved",
                "next_best_actions": [
                    {
                        "action": "Waive Rescheduling Travel Fees",
                        "confidence": 0.95,
                        "reason": "Gold frequent flyers qualify for complimentary booking adjustments. Applying waiver increases loyalty metric.",
                        "steps": [
                            "Select billing adjust code: COMP_LOYALTY_TICKET",
                            "Apply ticket waiver indicator checkmark",
                            "Save itinerary ledger logs"
                        ]
                    },
                    {
                        "action": "Rebook Evening Route Slot",
                        "confidence": 0.92,
                        "reason": "Rescheduled meeting demands travel departure after 3:00 PM slot. 5:30 PM flight has available seating capacity.",
                        "steps": [
                            "Unassign morning flight seat seat log",
                            "Select seat row on 5:30 PM flight departure",
                            "Transmit rebooked digital e-tickets"
                        ]
                    }
                ]
            }

        # Billing dispute keyword match
        elif any(kw in text_lower for kw in ["charge", "$45", "bill", "refund", "billing", "credit"]):
            return {
                "intent": "Billing Dispute (Mock)",
                "summary": "Customer Sarah Connor contacted support regarding an unauthorized premium package charge of $45. The agent verified the billing error and applied a statement credit.",
                "sentiment_trend": "Negative (Frustrated) ➔ Positive (Satisfied)",
                "entities": [
                    {"name": "Intent Category", "value": "Billing"},
                    {"name": "Customer Name", "value": "Sarah Connor"},
                    {"name": "Account Number", "value": "ACCT-98217-CC"},
                    {"name": "Disputed Charge", "value": "$45.00"}
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
                    }
                ]
            }

        # Retention keyword match
        elif any(kw in text_lower for kw in ["cancel", "competitor", "provider", "netspeed", "$50", "leaving"]):
            return {
                "intent": "Customer Retention (Mock)",
                "summary": "Customer Ellen Ripley requested cancellation due to a competitive offer of 1Gbps for $50/month. The agent retained the customer by matching the price and upgrading their line.",
                "sentiment_trend": "Dissatisfied ➔ Positive",
                "entities": [
                    {"name": "Intent Category", "value": "Retention"},
                    {"name": "Customer Name", "value": "Ellen Ripley"},
                    {"name": "Competitor Brand", "value": "NetSpeed"},
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
                    }
                ]
            }
            
        # Upgrade keyword match
        elif any(kw in text_lower for kw in ["upgrade", "speed", "fiber", "sluggish", "1gbps"]):
            return {
                "intent": "Account Upgrade (Mock)",
                "summary": "Customer Bruce Wayne requested line speed upgrades to support extra home devices. The agent upgraded the service plan to 1Gbps Fiber and waived router equipment fees.",
                "sentiment_trend": "Positive ➔ Positive",
                "entities": [
                    {"name": "Intent Category", "value": "Upgrade"},
                    {"name": "Customer Name", "value": "Bruce Wayne"},
                    {"name": "Current Plan Speed", "value": "100 Mbps"},
                    {"name": "New Plan Speed", "value": "1000 Mbps (1 Gbps)"}
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
                    }
                ]
            }
            
        # Generic fallback
        else:
            return {
                "intent": "General Inquiry",
                "summary": "Customer is communicating with agent regarding account configurations.",
                "sentiment_trend": "Neutral ➔ Neutral",
                "entities": [
                    {"name": "Intent Category", "value": "General"}
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
