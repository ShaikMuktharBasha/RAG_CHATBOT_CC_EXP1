import time
import streamlit as st
from call_center_engine import CallCenterEngine, MOCK_CALLS

def render_call_center_assistant(active_api_key, selected_model):
    # Inject styling specifically for call center dashboard elements
    st.markdown("""
    <style>
        .cc-kpi-card {
            background: rgba(17, 24, 39, 0.45);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 18px;
            text-align: center;
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            transition: transform 0.3s ease, border-color 0.3s ease;
        }
        .cc-kpi-card:hover {
            transform: translateY(-2px);
            border-color: rgba(129, 140, 248, 0.2);
        }
        .cc-kpi-val {
            font-size: 1.8rem;
            font-weight: 800;
            background: linear-gradient(135deg, #a5b4fc, #c084fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 2px;
        }
        .cc-kpi-lbl {
            font-size: 0.75rem;
            color: #9ca3af;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .bubble-container {
            display: flex;
            flex-direction: column;
            gap: 12px;
            max-height: 420px;
            overflow-y: auto;
            padding: 10px;
            background: rgba(11, 15, 26, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.04);
            border-radius: 12px;
            margin-bottom: 15px;
        }
        .bubble {
            max-width: 85%;
            padding: 10px 14px;
            border-radius: 12px;
            font-size: 0.88rem;
            line-height: 1.45;
            color: #e2e8f0;
            position: relative;
        }
        .bubble.customer {
            align-self: flex-start;
            background-color: rgba(55, 65, 81, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-bottom-left-radius: 2px;
        }
        .bubble.agent {
            align-self: flex-end;
            background-color: rgba(99, 102, 241, 0.15);
            border: 1px solid rgba(129, 140, 248, 0.2);
            border-bottom-right-radius: 2px;
        }
        .bubble-speaker {
            font-size: 0.7rem;
            font-weight: 700;
            margin-bottom: 3px;
            color: #a5b4fc;
        }
        .bubble.customer .bubble-speaker {
            color: #cbd5e1;
        }
        .nba-card {
            background: rgba(17, 24, 39, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 12px;
            transition: all 0.3s ease;
        }
        .nba-card.approved {
            border-color: rgba(16, 185, 129, 0.3);
            background: rgba(16, 185, 129, 0.03);
        }
        .nba-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }
        .nba-title {
            font-size: 0.95rem;
            font-weight: 700;
            color: #ffffff;
        }
        .nba-confidence {
            font-size: 0.7rem;
            background-color: rgba(129, 140, 248, 0.15);
            color: #a5b4fc;
            padding: 2px 6px;
            border-radius: 100px;
            font-weight: 600;
        }
        .nba-reason {
            font-size: 0.8rem;
            color: #9ca3af;
            line-height: 1.4;
            margin-bottom: 10px;
        }
        .nba-step {
            font-size: 0.78rem;
            color: #d1d5db;
            margin-left: 15px;
            margin-bottom: 3px;
        }
        .nba-step::before {
            content: "• ";
            color: #818cf8;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)

    # Initialize RAG/AI Call Center Engine
    engine = CallCenterEngine(google_api_key=active_api_key, model=selected_model)

    # ----------------- SESSION STATE INITIALIZATION -----------------
    if "cc_selected_call_id" not in st.session_state:
        st.session_state.cc_selected_call_id = "1"
    
    if "cc_simulation_active" not in st.session_state:
        st.session_state.cc_simulation_active = False

    if "cc_simulation_step" not in st.session_state:
        st.session_state.cc_simulation_step = 0

    if "cc_approved_actions" not in st.session_state:
        st.session_state.cc_approved_actions = set()

    if "cc_custom_transcript" not in st.session_state:
        st.session_state.cc_custom_transcript = ""

    if "cc_custom_analysis" not in st.session_state:
        st.session_state.cc_custom_analysis = None

    if "cc_custom_active" not in st.session_state:
        st.session_state.cc_custom_active = False

    # ----------------- LIVE SIMULATION PLAYBACK LOOP -----------------
    # If simulation is active, increment step and force rerun
    if st.session_state.cc_simulation_active and not st.session_state.cc_custom_active:
        selected_call = MOCK_CALLS[st.session_state.cc_selected_call_id]
        total_steps = len(selected_call["transcript"])
        if st.session_state.cc_simulation_step < total_steps:
            st.session_state.cc_simulation_step += 1
            time.sleep(1.2) # Sleep to simulate speech timing
            st.rerun()
        else:
            st.session_state.cc_simulation_active = False
            st.toast("Call monitoring finished. Complete transcript recorded.", icon="🟢")
            st.rerun()

    # ----------------- HEADER RENDERING -----------------
    st.markdown("""
    <div class="exp-header-card">
        <div class="exp-meta-container">
            <span class="exp-badge category">LLM Agent & Speech Diagnostics</span>
            <span class="exp-badge status-ready">🟢 Real-Time Enabled</span>
        </div>
        <div class="exp-title">Call Center Summarization & Next Best Action Assistant</div>
    </div>
    """, unsafe_allow_html=True)

    # Calculate metrics for KPI dashboard
    total_calls = len(MOCK_CALLS) + (1 if st.session_state.cc_custom_analysis else 0)
    completed_calls = sum(1 for c in MOCK_CALLS.values() if c["status"] == "Completed") + (1 if st.session_state.cc_custom_analysis else 0)
    active_calls_count = sum(1 for c in MOCK_CALLS.values() if c["status"] == "Active")
    escalations = sum(1 for c in MOCK_CALLS.values() if c["priority"] == "Critical")
    approved_actions_count = len(st.session_state.cc_approved_actions)

    # KPI Layout
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    with kpi_col1:
        st.markdown(f"""
        <div class="cc-kpi-card">
            <div class="cc-kpi-val">{total_calls}</div>
            <div class="cc-kpi-lbl">Monitored Calls</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi_col2:
        st.markdown(f"""
        <div class="cc-kpi-card">
            <div class="cc-kpi-val">🟢 82%</div>
            <div class="cc-kpi-lbl">Avg. Customer Sentiment</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi_col3:
        st.markdown(f"""
        <div class="cc-kpi-card">
            <div class="cc-kpi-val">{escalations}</div>
            <div class="cc-kpi-lbl">Pending Escalations</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi_col4:
        st.markdown(f"""
        <div class="cc-kpi-card">
            <div class="cc-kpi-val">{approved_actions_count}</div>
            <div class="cc-kpi-lbl">Approved Supervisor Actions</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ----------------- COLUMNS LAYOUT (Left Master, Right Detail) -----------------
    col_left, col_right = st.columns([3, 7])

    with col_left:
        st.markdown("### <i class='fa-solid fa-list-check' style='color:#818cf8; margin-right:8px;'></i> Call Queue", unsafe_allow_html=True)
        st.markdown("<p style='color: #9ca3af; font-size: 0.85rem; margin-top: -10px; margin-bottom: 15px;'>Select a call to inspect, monitor, or review next actions.</p>", unsafe_allow_html=True)
        
        # Preloaded Call List
        for call_id, call in MOCK_CALLS.items():
            is_selected = (st.session_state.cc_selected_call_id == call_id and not st.session_state.cc_custom_active)
            bg_color = "rgba(99, 102, 241, 0.08)" if is_selected else "rgba(255, 255, 255, 0.02)"
            border_style = "border-left: 4px solid #818cf8;" if is_selected else "border-left: 4px solid transparent;"
            
            # Priority color mapping
            priority_color = "#ef4444" if call["priority"] == "Critical" else ("#f59e0b" if call["priority"] == "High" else "#3b82f6")
            status_color = "#10b981" if call["status"] == "Active" else "#64748b"
            
            st.markdown(f"""
            <div style="background-color: {bg_color}; padding: 12px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.05); {border_style} margin-bottom: 5px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                    <span style="font-weight: 700; color: #ffffff; font-size: 0.9rem;">{call['customer']}</span>
                    <span style="font-size: 0.7rem; background-color: {priority_color}20; color: {priority_color}; padding: 2px 6px; border-radius: 4px; font-weight: 600;">{call['priority']}</span>
                </div>
                <div style="font-size: 0.8rem; color: #9ca3af; margin-bottom: 6px;">Agent: {call['agent']} | {call['duration']}</div>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-size: 0.75rem; color: {status_color}; font-weight: 600;">
                        <span style="display: inline-block; width: 6px; height: 6px; border-radius: 50%; background-color: {status_color}; margin-right: 4px; {'animation: pulseReady 2s infinite;' if call['status'] == 'Active' else ''}"></span>
                        {call['status']}
                    </span>
                    <span style="font-size: 0.75rem; color: #a5b4fc; font-weight: 500;">{call['intent']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Select button for each call card
            if st.button("Inspect Call Details", key=f"select_call_{call_id}", use_container_width=True):
                st.session_state.cc_selected_call_id = call_id
                st.session_state.cc_custom_active = False
                st.session_state.cc_simulation_active = False
                # If completed, load full transcript; if active, start from step 1
                if call["status"] == "Completed":
                    st.session_state.cc_simulation_step = len(call["transcript"])
                else:
                    st.session_state.cc_simulation_step = 1
                st.rerun()

        # Render custom call in queue if analyzed
        if st.session_state.cc_custom_analysis:
            is_selected = st.session_state.cc_custom_active
            bg_color = "rgba(99, 102, 241, 0.08)" if is_selected else "rgba(255, 255, 255, 0.02)"
            border_style = "border-left: 4px solid #818cf8;" if is_selected else "border-left: 4px solid transparent;"
            
            st.markdown(f"""
            <div style="background-color: {bg_color}; padding: 12px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.05); {border_style} margin-bottom: 5px; margin-top: 15px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                    <span style="font-weight: 700; color: #ffffff; font-size: 0.9rem;">Custom Uploaded Call</span>
                    <span style="font-size: 0.7rem; background-color: rgba(167, 139, 250, 0.2); color: #c084fc; padding: 2px 6px; border-radius: 4px; font-weight: 600;">Custom</span>
                </div>
                <div style="font-size: 0.8rem; color: #9ca3af; margin-bottom: 6px;">Source: File Upload | Completed</div>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-size: 0.75rem; color: #64748b; font-weight: 600;">
                        <span style="display: inline-block; width: 6px; height: 6px; border-radius: 50%; background-color: #64748b; margin-right: 4px;"></span>
                        Completed
                    </span>
                    <span style="font-size: 0.75rem; color: #cbd5e1; font-weight: 500;">{st.session_state.cc_custom_analysis.get('intent', 'General')}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Inspect Custom Call", key="select_custom_call", use_container_width=True):
                st.session_state.cc_custom_active = True
                st.session_state.cc_simulation_active = False
                st.rerun()

        st.markdown("<hr style='border-color: rgba(255,255,255,0.05); margin: 20px 0;'>", unsafe_allow_html=True)
        st.markdown("### <i class='fa-solid fa-cloud-arrow-up' style='color:#818cf8; margin-right:8px;'></i> Analyze Custom Transcript", unsafe_allow_html=True)
        
        # Custom file upload panel
        uploaded_file = st.file_uploader(
            "Upload Transcript (.txt)",
            type=["txt"],
            help="Upload a raw dialogue file to run the AI summarization & next actions recommendation system.",
            key="custom_transcript_uploader"
        )
        
        if uploaded_file is not None:
            try:
                raw_text = uploaded_file.getvalue().decode("utf-8")
                if raw_text != st.session_state.cc_custom_transcript:
                    st.session_state.cc_custom_transcript = raw_text
                    
                    with st.spinner("Analyzing custom transcript with LLM..."):
                        analysis = engine.analyze_transcript(raw_text)
                        st.session_state.cc_custom_analysis = analysis
                        st.session_state.cc_custom_active = True
                        st.toast("Custom transcript analyzed successfully!", icon="🔥")
                        st.rerun()
            except Exception as e:
                st.error(f"Error parsing file: {e}")

    # ----------------- RIGHT COLUMN (Detail Panel) -----------------
    with col_right:
        # Load active call context
        if st.session_state.cc_custom_active:
            # Custom call detail
            st.markdown("### <i class='fa-solid fa-headset' style='color:#a78bfa; margin-right:8px;'></i> Call Analysis: Custom Uploaded Transcript", unsafe_allow_html=True)
            
            col_dialogue, col_ai = st.columns([1, 1])
            
            with col_dialogue:
                st.markdown("#### Transcript Dialogue", unsafe_allow_html=True)
                st.markdown(f"""
                <div class="bubble-container" style="max-height: 480px;">
                    <div style="color: #9ca3af; font-size: 0.85rem; padding: 10px; font-style: italic; white-space: pre-wrap;">
                        {st.session_state.cc_custom_transcript}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            with col_ai:
                st.markdown("#### AI Copilot Analytics", unsafe_allow_html=True)
                analysis = st.session_state.cc_custom_analysis
                if analysis:
                    render_analysis_results(analysis, engine, "Custom Uploaded")
                else:
                    st.warning("No analysis payload available.")
        
        else:
            # Preloaded mock call detail
            call = MOCK_CALLS[st.session_state.cc_selected_call_id]
            st.markdown(f"### <i class='fa-solid fa-headset' style='color:#a78bfa; margin-right:8px;'></i> Call Monitoring: {call['customer']} ↔ {call['agent']}", unsafe_allow_html=True)
            
            # Live simulation control header for Active calls
            if call["status"] == "Active":
                sim_col1, sim_col2, sim_col3 = st.columns([2, 1, 1])
                with sim_col1:
                    st.markdown("""
                    <div style="font-size: 0.85rem; color: #fbbf24; margin-top: 6px; font-weight: 600;">
                        ⚠️ Ongoing Live Conversation - Action Required
                    </div>
                    """, unsafe_allow_html=True)
                with sim_col2:
                    if st.session_state.cc_simulation_active:
                        if st.button("⏸ Pause Live", key="btn_pause_sim", use_container_width=True):
                            st.session_state.cc_simulation_active = False
                            st.rerun()
                    else:
                        if st.button("▶ Live Monitor", key="btn_start_sim", use_container_width=True):
                            st.session_state.cc_simulation_active = True
                            st.rerun()
                with sim_col3:
                    if st.button("🔄 Reset Call", key="btn_reset_sim", use_container_width=True):
                        st.session_state.cc_simulation_active = False
                        st.session_state.cc_simulation_step = 1
                        st.rerun()
            else:
                st.markdown("<p style='color: #9ca3af; font-size: 0.85rem;'>Reviewing past archived call session logs.</p>", unsafe_allow_html=True)
            
            # Split details area
            col_dialogue, col_ai = st.columns([1, 1])
            
            with col_dialogue:
                st.markdown("#### Live Transcript Stream", unsafe_allow_html=True)
                
                # Show dialogue up to active simulation step
                visible_transcript = call["transcript"][:st.session_state.cc_simulation_step]
                
                # Render speech bubbles
                st.markdown('<div class="bubble-container">', unsafe_allow_html=True)
                if not visible_transcript:
                    st.markdown("<p style='color: #6b7280; font-style: italic; text-align: center; padding: 20px;'>Awaiting dialogue connection...</p>", unsafe_allow_html=True)
                else:
                    for turn in visible_transcript:
                        speaker = turn["speaker"]
                        text = turn["text"]
                        is_customer = (speaker == call["customer"])
                        speaker_class = "customer" if is_customer else "agent"
                        icon = "👤" if is_customer else "🎧"
                        
                        st.markdown(f"""
                        <div class="bubble {speaker_class}">
                            <div class="bubble-speaker">{icon} {speaker}</div>
                            {text}
                        </div>
                        """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Display completion note
                if call["status"] == "Active" and st.session_state.cc_simulation_step < len(call["transcript"]):
                    st.markdown(f"""
                    <div style="font-size: 0.78rem; color: #9ca3af; background-color: rgba(251, 191, 36, 0.05); border: 1px solid rgba(251, 191, 36, 0.15); padding: 8px 12px; border-radius: 8px; text-align: center;">
                        💬 Showing {st.session_state.cc_simulation_step} of {len(call['transcript'])} dialogue turns. Monitoring active.
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style="font-size: 0.78rem; color: #10b981; background-color: rgba(16, 185, 129, 0.05); border: 1px solid rgba(16, 185, 129, 0.15); padding: 8px 12px; border-radius: 8px; text-align: center;">
                        ✅ Full call transcript archived. System ready.
                    </div>
                    """, unsafe_allow_html=True)

            with col_ai:
                st.markdown("#### Supervisor AI Assistant Panel", unsafe_allow_html=True)
                
                # Build current active text segment to evaluate
                current_transcript_text = "\n".join([f"{t['speaker']}: {t['text']}" for t in visible_transcript])
                
                # Run evaluation
                if current_transcript_text.strip():
                    with st.spinner("AI analyzing dialogue segment..."):
                        # To prevent heavy API calls, cache or use the local fast rules for partial/simulating steps
                        if st.session_state.cc_simulation_active:
                            # Use fast local rule compiler for live transitions
                            analysis = engine.generate_offline_analysis(current_transcript_text)
                        else:
                            # Invoke standard engine (uses Gemini if key exists)
                            analysis = engine.analyze_transcript(current_transcript_text)
                        
                        render_analysis_results(analysis, engine, call['agent'])
                else:
                    st.info("Start the call or load dialogue text to enable real-time supervisor insights.", icon="💡")


def render_analysis_results(analysis, engine, agent_name):
    # Metadata pill box
    sentiment = analysis.get("sentiment_trend", "Neutral")
    intent = analysis.get("intent", "General Inquiry")
    res_status = analysis.get("resolution_status", "In Progress")
    
    # Status styling
    status_bg = "rgba(16, 185, 129, 0.15)" if res_status == "Resolved" else ("rgba(245, 158, 11, 0.15)" if res_status == "In Progress" else "rgba(239, 68, 68, 0.15)")
    status_fg = "#34d399" if res_status == "Resolved" else ("#fbbf24" if res_status == "In Progress" else "#f87171")

    st.markdown(f"""
    <div style="background-color: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.05); padding: 12px 16px; border-radius: 8px; margin-bottom: 15px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
            <span style="font-size: 0.8rem; font-weight: 600; color: #9ca3af;">Intent:</span>
            <span style="font-size: 0.85rem; font-weight: 700; color: #a5b4fc;">{intent}</span>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
            <span style="font-size: 0.8rem; font-weight: 600; color: #9ca3af;">Sentiment Trend:</span>
            <span style="font-size: 0.85rem; font-weight: 500; color: #cbd5e1;">{sentiment}</span>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 0.8rem; font-weight: 600; color: #9ca3af;">Resolution:</span>
            <span style="font-size: 0.8rem; font-weight: 700; background-color: {status_bg}; color: {status_fg}; padding: 2px 8px; border-radius: 4px;">{res_status}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Executive Summary Card
    st.markdown("##### <i class='fa-solid fa-quote-left' style='color:#c084fc; margin-right:5px;'></i> Executive Summary", unsafe_allow_html=True)
    st.markdown(f"<div style='background-color: rgba(255,255,255,0.01); border: 1px solid rgba(255,255,255,0.03); padding: 10px 14px; border-radius: 8px; font-size: 0.85rem; line-height: 1.5; color: #d1d5db; margin-bottom: 15px;'>{analysis.get('summary', 'Extracting summary...')}</div>", unsafe_allow_html=True)

    # Extracted Entities Checklist
    entities = analysis.get("entities", [])
    if entities:
        st.markdown("##### <i class='fa-solid fa-tags' style='color:#a5b4fc; margin-right:5px;'></i> Extracted Entities", unsafe_allow_html=True)
        entity_html = "<div style='display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 15px;'>"
        for ent in entities:
            entity_html += f"<span style='background-color: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); padding: 3px 8px; border-radius: 6px; font-size: 0.725rem; color: #e2e8f0;'><strong style='color:#a5b4fc;'>{ent['name']}:</strong> {ent['value']}</span>"
        entity_html += "</div>"
        st.markdown(entity_html, unsafe_allow_html=True)

    # Next Best Action (NBA) Generator
    st.markdown("##### <i class='fa-solid fa-wand-magic-sparkles' style='color:#c084fc; margin-right:5px;'></i> Recommended Next Best Actions (NBA)", unsafe_allow_html=True)
    st.markdown("<p style='color: #9ca3af; font-size: 0.78rem; margin-top:-6px; margin-bottom: 10px;'>Select approved actions to push immediately to the agent's work-screen.</p>", unsafe_allow_html=True)

    actions = analysis.get("next_best_actions", [])
    if not actions:
        st.markdown("<p style='color: #6b7280; font-style: italic; font-size:0.8rem;'>Analyzing conversation to compute next best actions...</p>", unsafe_allow_html=True)
    else:
        for idx, item in enumerate(actions):
            act_name = item.get("action", f"Action {idx+1}")
            confidence = item.get("confidence", 0.9)
            reason = item.get("reason", "Reason details not available.")
            steps = item.get("steps", [])

            # Check if supervisor has approved this action already
            is_approved = (act_name in st.session_state.cc_approved_actions)
            card_class = "approved" if is_approved else ""
            
            # Format action list steps
            steps_html = ""
            for step in steps:
                steps_html += f"<div class='nba-step'>{step}</div>"

            st.markdown(f"""
            <div class="nba-card {card_class}">
                <div class="nba-header">
                    <span class="nba-title">{act_name}</span>
                    <span class="nba-confidence">{int(confidence * 100)}% Match</span>
                </div>
                <div class="nba-reason">{reason}</div>
                {steps_html}
            </div>
            """, unsafe_allow_html=True)

            # Button to approve action
            if is_approved:
                st.markdown("""
                <div style="background-color: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.2); border-radius: 8px; padding: 6px; text-align: center; color: #34d399; font-size: 0.78rem; font-weight: 700; margin-bottom: 12px;">
                    ✓ Approved & Sent to Agent Screen
                </div>
                """, unsafe_allow_html=True)
            else:
                if st.button(f"Approve & Push Action to {agent_name}", key=f"btn_approve_action_{idx}_{act_name[:15]}", use_container_width=True):
                    st.session_state.cc_approved_actions.add(act_name)
                    st.toast(f"Action '{act_name}' pushed to Agent {agent_name} successfully!", icon="🚀")
                    st.rerun()
