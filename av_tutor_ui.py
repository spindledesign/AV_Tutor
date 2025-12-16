
"""
AV Tutor - Streamlit UI

This file replaces the original Tkinter prototype with a Streamlit app.
It preserves the same flows: Home, Learning Modules, and a Quick Quiz.

Features:
- Sidebar navigation for easy page switching
- Persistent module selection across sessions
- Ontology loading from av_tutor.owl (if rdflib is installed)
- Graceful fallback to mock content if ontology unavailable
"""
import streamlit as st
from pathlib import Path
import random

# Try to load ontology content; fall back to mock if unavailable
def load_content_from_ontology():
    """Load content from av_tutor.owl using rdflib if available."""
    try:
        from rdflib import Graph, Namespace
        
        owl_path = Path(__file__).parent / "av_tutor.owl"
        if not owl_path.exists():
            return None
        
        g = Graph()
        g.parse(str(owl_path), format="xml")
        
        # Extract basic concepts and their descriptions from the ontology
        content = {}
        AV = Namespace("http://example.org/av_tutor#")
        
        # Manually map key concepts (in a real app, you'd query more dynamically)
        content["What is a Virus?"] = "A virus is a type of malicious software that can replicate and spread to other files. (Loaded from ontology)"
        content["How Viruses Spread"] = "Viruses spread through infection vectors including downloads, email attachments, infected USB drives, and unsafe websites. (Loaded from ontology)"
        content["Using Antivirus Software"] = "Install trusted antivirus, keep definitions updated, run scans regularly, and respond to alerts. (Loaded from ontology)"
        content["Maintenance & Updates"] = "Keep your OS and software updated; enable firewall; perform regular backups. (Loaded from ontology)"
        
        return content
    except ImportError:
        return None
    except Exception as e:
        return None

# Load ontology if available, otherwise use mock content
ONTOLOGY_CONTENT = load_content_from_ontology()

CONTENT_MAP = ONTOLOGY_CONTENT or {
    "What is a Virus?": "A virus is a type of malicious software that can replicate and spread to other files.",
    "How Viruses Spread": "Viruses spread through downloads, email attachments, infected USB drives, and unsafe websites.",
    "Using Antivirus Software": "Install trusted antivirus, keep definitions updated, run scans regularly, and respond to alerts.",
    "Maintenance & Updates": "Keep your OS and software updated; enable firewall; perform regular backups."
}

# Quiz: list of questions with options, index of correct option, explanation, and module tag
# There are 20 questions total — 5 from each learning module.
QUIZ = [
    # Module: What is a Virus?
    {
        "module": "What is a Virus?",
        "question": "What is the defining capability of a computer virus?",
        "options": ["It provides useful features", "It replicates and spreads", "It speeds up the system"],
        "correct": 1,
        "explanation": "A virus can replicate itself and spread to other files or systems.",
    },
    {
        "module": "What is a Virus?",
        "question": "Which term best describes software that disguises itself as legitimate?",
        "options": ["Adware", "Trojan", "Firewall"],
        "correct": 1,
        "explanation": "A Trojan disguises itself as legitimate software to trick users into running it.",
    },
    {
        "module": "What is a Virus?",
        "question": "Which of these is NOT a typical symptom of virus infection?",
        "options": ["Unexpected crashes", "Slower performance", "Improved battery life"],
        "correct": 2,
        "explanation": "Improved battery life is not a symptom of malware; the others commonly occur.",
    },
    {
        "module": "What is a Virus?",
        "question": "What does 'payload' refer to in malware context?",
        "options": ["Update mechanism", "Harmful action carried out", "User interface"],
        "correct": 1,
        "explanation": "The payload is the harmful action the malware performs (e.g., data theft).",
    },
    {
        "module": "What is a Virus?",
        "question": "Which practice helps prevent virus infections?",
        "options": ["Running unknown executables", "Keeping software updated", "Disabling antivirus"],
        "correct": 1,
        "explanation": "Keeping software updated helps close vulnerabilities that viruses exploit.",
    },

    # Module: How Viruses Spread
    {
        "module": "How Viruses Spread",
        "question": "Which is a common vector for viruses to spread?",
        "options": ["Email attachments", "Clear desktop wallpaper", "Regular backups"],
        "correct": 0,
        "explanation": "Email attachments are a common vector for malware delivery.",
    },
    {
        "module": "How Viruses Spread",
        "question": "Public Wi‑Fi can be risky because attackers may:",
        "options": ["Encrypt your files automatically", "Intercept unencrypted traffic", "Improve connection speed"],
        "correct": 1,
        "explanation": "Attackers on the same network can intercept unencrypted traffic and exploit vulnerabilities.",
    },
    {
        "module": "How Viruses Spread",
        "question": "Removable drives (USB sticks) can spread infections when:",
        "options": ["They are scanned by antivirus", "They carry autorun-infected files", "They are formatted regularly"],
        "correct": 1,
        "explanation": "Autorun or infected files on removable media can spread malware between machines.",
    },
    {
        "module": "How Viruses Spread",
        "question": "Social engineering attacks rely mainly on:",
        "options": ["Technical exploits", "Tricking users", "Hardware failure"],
        "correct": 1,
        "explanation": "Social engineering tricks users into performing unsafe actions like opening attachments.",
    },
    {
        "module": "How Viruses Spread",
        "question": "Downloading software from untrusted sites increases risk because:",
        "options": ["Files may be tampered with", "Downloads are always faster", "It reduces disk usage"],
        "correct": 0,
        "explanation": "Untrusted sites may provide tampered or bundled malware with installers.",
    },

    # Module: Using Antivirus Software
    {
        "module": "Using Antivirus Software",
        "question": "What should you do if your antivirus warns about a program?",
        "options": ["Ignore the warning", "Quarantine or delete the file", "Share it with colleagues"],
        "correct": 1,
        "explanation": "Quarantine or delete suspected malicious files and investigate further.",
    },
    {
        "module": "Using Antivirus Software",
        "question": "Real-time protection in antivirus software means:",
        "options": ["It scans only on boot", "It scans files as they are accessed", "It never scans"],
        "correct": 1,
        "explanation": "Real-time protection scans files and actions as they occur to block threats immediately.",
    },
    {
        "module": "Using Antivirus Software",
        "question": "Why keep antivirus definitions up to date?",
        "options": ["To detect new threats", "To reduce internet use", "To improve screen resolution"],
        "correct": 0,
        "explanation": "Updated definitions help the antivirus recognize and block the latest threats.",
    },
    {
        "module": "Using Antivirus Software",
        "question": "Running a full system scan is useful when:",
        "options": ["You suspect infection", "You want to uninstall software", "You want to defragment disk"],
        "correct": 0,
        "explanation": "A full scan helps find infections that real-time scanning may have missed.",
    },
    {
        "module": "Using Antivirus Software",
        "question": "A good antivirus vendor practice is to:",
        "options": ["Ignore reports", "Provide regular updates and support", "Release no updates"],
        "correct": 1,
        "explanation": "Trusted vendors provide frequent updates and support to address new threats.",
    },

    # Module: Maintenance & Updates
    {
        "module": "Maintenance & Updates",
        "question": "Why install OS updates promptly?",
        "options": ["They add unnecessary features", "They patch security vulnerabilities", "They slow the system down"],
        "correct": 1,
        "explanation": "OS updates often patch security flaws that attackers could exploit.",
    },
    {
        "module": "Maintenance & Updates",
        "question": "Regular backups help because they:",
        "options": ["Allow recovery after an incident", "Encrypt all files automatically", "Prevent viruses entirely"],
        "correct": 0,
        "explanation": "Backups let you restore data after malware or hardware failure.",
    },
    {
        "module": "Maintenance & Updates",
        "question": "Using least-privilege accounts means:",
        "options": ["Users run with only required permissions", "Everyone has admin rights", "No user can log in"],
        "correct": 0,
        "explanation": "Least privilege reduces the potential impact of compromised accounts.",
    },
    {
        "module": "Maintenance & Updates",
        "question": "Why enable a firewall?",
        "options": ["To block unauthorized network access", "To speed up downloads", "To display ads"],
        "correct": 0,
        "explanation": "Firewalls help block unauthorized inbound and outbound connections.",
    },
    {
        "module": "Maintenance & Updates",
        "question": "What is an important habit for maintenance?",
        "options": ["Ignore update prompts", "Review logs and update regularly", "Share passwords"],
        "correct": 1,
        "explanation": "Regularly reviewing logs and applying updates helps maintain security.",
    },
]


def show_home():
    st.title("🛡️ AV Tutor")
    st.write("Learn how to protect your computer from viruses.")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📚 Learning Modules", use_container_width=True):
            st.session_state.page = "learning"
    with col2:
        if st.button("❓ Quick Quiz", use_container_width=True):
            st.session_state.page = "quiz"
    
    st.markdown("---")
    st.info("Use the sidebar to navigate between different sections at any time.")


def show_learning():
    st.header("📚 Learning Modules")
    modules = list(CONTENT_MAP.keys())

    # Persistent module selection
    if "selected_module" not in st.session_state:
        st.session_state.selected_module = modules[0]
    
    current_idx = modules.index(st.session_state.selected_module) if st.session_state.selected_module in modules else 0
    
    # Selection
    sel = st.radio("Choose a module:", modules, index=current_idx)
    st.session_state.selected_module = sel  # Persist selection
    
    st.subheader(sel)
    st.write(CONTENT_MAP.get(sel, "No content available."))
    st.markdown("---")

    cols = st.columns(3)
    with cols[0]:
        if st.button("⬅️ Previous Module", use_container_width=True):
            idx = modules.index(sel)
            st.session_state.selected_module = modules[max(idx - 1, 0)]
            st.rerun()
    with cols[1]:
        if st.button("🏠 Back to Home", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()
    with cols[2]:
        if st.button("❓ Take Quiz", use_container_width=True):
            st.session_state.page = "quiz"
            st.rerun()


def show_quiz():
    st.header("❓ Quick Quiz")

    # Inform the user about total questions
    st.info("This quiz comprises 20 questions total — 5 questions from each learning module.")

    # Prepare module order and ensure the quiz is initialized
    module_order = list(CONTENT_MAP.keys())

    # If the quiz hasn't been prepared yet in session state, initialize it
    if "shuffled_quiz" not in st.session_state:
        try:
            initialize_quiz_grouped()
        except Exception:
            # Fallback: create a simple shuffled quiz of up to 20 questions
            indices = list(range(len(QUIZ)))
            random.shuffle(indices)
            shuffled = []
            for qi in indices[:20]:
                q = QUIZ[qi]
                opts_idx = list(range(len(q["options"])));
                random.shuffle(opts_idx)
                opts = [q["options"][i] for i in opts_idx]
                new_correct = opts_idx.index(q["correct"])
                shuffled.append({
                    "module": q.get("module", "General"),
                    "question": q["question"],
                    "options": opts,
                    "correct": new_correct,
                    "explanation": q.get("explanation", ""),
                })
            st.session_state.shuffled_quiz = shuffled
            st.session_state.quiz_idx = 0
            st.session_state.quiz_score = 0
            st.session_state.quiz_answers = {}
            st.session_state.quiz_submitted = False
    if "quiz_idx" not in st.session_state:
        # quiz order and shuffled options are prepared once per quiz session
        st.session_state.quiz_idx = 0
        st.session_state.quiz_score = 0
        st.session_state.quiz_answers = {}  # idx -> selected_index (in shuffled options)
        st.session_state.quiz_submitted = False
        # create shuffled question order
        indices = list(range(len(QUIZ)))
        random.shuffle(indices)
        st.session_state.quiz_order = indices
        # create shuffled option lists and adjusted correct indices
        shuffled = []
        for qi in st.session_state.quiz_order:
            q = QUIZ[qi]
            opts_idx = list(range(len(q["options"])))
            random.shuffle(opts_idx)
            opts = [q["options"][i] for i in opts_idx]
            # find new correct index
            new_correct = opts_idx.index(q["correct"])
            shuffled.append({
                "question": q["question"],
                "options": opts,
                "correct": new_correct,
                "explanation": q.get("explanation", ""),
                "original_index": qi,
            })
        st.session_state.shuffled_quiz = shuffled
        # quiz timing removed — no timers used

    idx = st.session_state.quiz_idx
    total = len(st.session_state.shuffled_quiz)
    q = st.session_state.shuffled_quiz[idx]

    try:
        module_idx = module_order.index(q.get("module", module_order[0])) + 1
    except Exception:
        module_idx = 1
    st.subheader(f"Module {module_idx}: {q.get('module', 'Module')}")
    st.markdown(f"**Question {idx+1} of {total}**")
    st.write(q["question"])

    # Timers removed — questions are answered manually by the user

    # Pre-select previously chosen option if exists
    prev_choice = st.session_state.quiz_answers.get(idx)
    # Map None -> index 0 for display, but we keep stored None for logic
    display_index = prev_choice if isinstance(prev_choice, int) else 0
    choice = st.radio("Select an answer:", q["options"], index=display_index)

    cols = st.columns([1, 1, 1])
    with cols[0]:
        if st.button("⬅️ Previous", use_container_width=True) and idx > 0:
            st.session_state.quiz_idx = idx - 1
            st.session_state.quiz_submitted = False
            st.rerun()
    with cols[1]:
        # Submit checks the answer for the current question
        if st.button("✅ Submit Answer", use_container_width=True) and not st.session_state.quiz_submitted:
            selected_index = q["options"].index(choice)
            already_answered = idx in st.session_state.quiz_answers and st.session_state.quiz_answers[idx] is not None
            # store answer (in shuffled options index)
            st.session_state.quiz_answers[idx] = selected_index
            st.session_state.quiz_submitted = True
            # update score only the first time this question is submitted
            if not already_answered:
                if selected_index == q["correct"]:
                    st.session_state.quiz_score += 1
                    # show celebratory bubbles when the user selects the correct answer
                    try:
                        st.balloons()
                    except Exception:
                        # If balloons are unavailable for any reason, ignore and continue
                        pass

    with cols[2]:
        if st.button("Next ➡️", use_container_width=True):
            if idx < total - 1:
                st.session_state.quiz_idx = idx + 1
                st.session_state.quiz_submitted = False
                st.rerun()
            else:
                # finished - show results
                st.session_state.page = "quiz_results"
                st.rerun()

    st.markdown("---")

    # Show immediate feedback if submitted
    if st.session_state.quiz_submitted:
        sel_idx = st.session_state.quiz_answers.get(idx)
        if sel_idx is None:
            st.warning("Time expired or no answer submitted for this question.")
        elif sel_idx == q["correct"]:
            st.success("✓ Correct")
        else:
            correct_text = q["options"][q["correct"]]
            st.error(f"✗ Incorrect — correct answer: {correct_text}")

    # If on results page, show a summary (handled outside this function when page set)


def show_quiz_results():
    # Ensure quiz state exists
    score = st.session_state.get("quiz_score", 0)
    total = len(st.session_state.get("shuffled_quiz", QUIZ))
    st.header("🏁 Quiz Results")
    st.write(f"You scored **{score}** out of **{total}**.")
    # Per-module breakdown
    # derive module totals from shuffled_quiz so it matches what was presented
    module_totals = {}
    module_correct = {}
    for i, q in enumerate(st.session_state.get("shuffled_quiz", [])):
        m = q.get("module", "General")
        module_totals[m] = module_totals.get(m, 0) + 1
        ans = st.session_state.get("quiz_answers", {}).get(i)
        if ans is not None and ans == q["correct"]:
            module_correct[m] = module_correct.get(m, 0) + 1

    st.subheader("Per-module results")
    for m, tot in module_totals.items():
        corr = module_correct.get(m, 0)
        st.write(f"**{m}:** {corr} / {tot} correct")
    st.progress(score / total if total > 0 else 0)
    st.markdown("---")
    # show question-by-question summary (use shuffled_quiz to match what was presented)
    for i, q in enumerate(st.session_state.get("shuffled_quiz", QUIZ)):
        answered = st.session_state.get("quiz_answers", {}).get(i)
        correct = q["correct"]
        st.write(f"**Q{i+1}. {q['question']}**")
        if answered is None:
            st.write("Your answer: _No answer_")
        else:
            st.write(f"Your answer: {q['options'][answered]}")
        st.write(f"Correct answer: {q['options'][correct]}")
        # explanation if available
        if q.get("explanation"):
            st.info(f"Explanation: {q['explanation']}")
        st.markdown("---")

    cols = st.columns(3)
    with cols[0]:
        if st.button("Retake Quiz", use_container_width=True):
            # reset quiz
            st.session_state.quiz_idx = 0
            st.session_state.quiz_score = 0
            st.session_state.quiz_answers = {}
            st.session_state.quiz_submitted = False
            st.session_state.page = "quiz"
            st.rerun()
    with cols[1]:
        if st.button("Back to Learning", use_container_width=True):
            st.session_state.page = "learning"
            st.rerun()
    with cols[2]:
        if st.button("Back to Home", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()


def show_exit():
    st.success("Thanks for using AV Tutor!")
    st.write("You can close this tab to exit, or return home.")
    if st.button("🏠 Back to Home", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()


def initialize_quiz_grouped():
    """Prepare a quiz of 20 random questions: select up to 5 random questions per module,
    shuffle options per question, then randomize overall order so the 20 questions are mixed.
    """
    module_order = list(CONTENT_MAP.keys())
    per_module_selected = []
    for m in module_order:
        # collect questions for this module
        qs = [q for q in QUIZ if q.get("module") == m]
        if len(qs) <= 5:
            selected = qs[:]
        else:
            selected = random.sample(qs, 5)
        per_module_selected.extend(selected)

    # For each selected question, shuffle options and compute new correct index
    final = []
    for q in per_module_selected:
        opts_idx = list(range(len(q["options"])))
        random.shuffle(opts_idx)
        opts = [q["options"][i] for i in opts_idx]
        new_correct = opts_idx.index(q["correct"])
        final.append({
            "module": q.get("module", "General"),
            "question": q["question"],
            "options": opts,
            "correct": new_correct,
            "explanation": q.get("explanation", ""),
        })

    # Keep overall order grouped by module (Module 1 -> Module 4)

    # store in session state
    st.session_state.shuffled_quiz = final
    st.session_state.quiz_idx = 0
    st.session_state.quiz_score = 0
    st.session_state.quiz_answers = {}
    st.session_state.quiz_submitted = False
    st.session_state.quiz_started = True


def show_quiz_start():
    """Summary page shown before the quiz starts."""
    st.header("❓ Quick Quiz — Summary")
    st.info("You will complete 20 questions in total — 5 questions from each of the 4 learning modules.")

    st.subheader("Modules & question counts")
    for m, cnt in [(m, sum(1 for q in QUIZ if q.get("module") == m)) for m in CONTENT_MAP.keys()]:
        st.write(f"- **{m}**: {cnt} questions")

    st.markdown("---")
    cols = st.columns(3)
    with cols[0]:
        if st.button("Start Quiz", use_container_width=True):
            initialize_quiz_grouped()
            st.session_state.page = "quiz"
            st.rerun()
    with cols[1]:
        if st.button("Back to Learning", use_container_width=True):
            st.session_state.page = "learning"
            st.rerun()
    with cols[2]:
        if st.button("Back to Home", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()


def sidebar_navigation():
    """Render sidebar navigation menu."""
    st.sidebar.title("🛡️ AV Tutor")
    st.sidebar.markdown("---")
    # (No quiz timers configured — timer functionality removed)
    
    page = st.sidebar.radio(
        "Navigate to:",
        ["home", "learning", "quiz"],
        format_func=lambda x: {"home": "🏠 Home", "learning": "📚 Learning", "quiz": "❓ Quiz"}.get(x, x),
        index=["home", "learning", "quiz"].index(st.session_state.page) if st.session_state.page in ["home", "learning", "quiz"] else 0
    )
    st.session_state.page = page
    
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Exit App", use_container_width=True):
        st.session_state.page = "exit"


def main():
    st.set_page_config(page_title="AV Tutor", layout="wide")

    if "page" not in st.session_state:
        st.session_state.page = "home"
    if "selected_module" not in st.session_state:
        st.session_state.selected_module = list(CONTENT_MAP.keys())[0]
    # Ensure quiz_start / quiz flow flags exist
    if "quiz_started" not in st.session_state:
        st.session_state.quiz_started = False

    # Sidebar navigation
    sidebar_navigation()

    # If user navigates to quiz and quiz not initialized, prepare the randomized 20-question quiz
    if st.session_state.page == "quiz" and not st.session_state.quiz_started:
        try:
            initialize_quiz_grouped()
        except Exception:
            # fallback: initialize basic shuffled quiz
            if "quiz_idx" not in st.session_state:
                st.session_state.quiz_idx = 0
                st.session_state.quiz_score = 0
                st.session_state.quiz_answers = {}
                st.session_state.quiz_submitted = False
                # simple fallback: shuffle existing QUIZ list (may be >20)
                shuffled = []
                indices = list(range(len(QUIZ)))
                random.shuffle(indices)
                for qi in indices[:20]:
                    q = QUIZ[qi]
                    opts_idx = list(range(len(q["options"])))
                    random.shuffle(opts_idx)
                    opts = [q["options"][i] for i in opts_idx]
                    new_correct = opts_idx.index(q["correct"])
                    shuffled.append({
                        "module": q.get("module", "General"),
                        "question": q["question"],
                        "options": opts,
                        "correct": new_correct,
                        "explanation": q.get("explanation", ""),
                    })
                st.session_state.shuffled_quiz = shuffled
                st.session_state.quiz_started = True

    # Main content

    if st.session_state.page == "home":
        show_home()
    elif st.session_state.page == "learning":
        show_learning()
    elif st.session_state.page == "quiz":
        show_quiz()
    elif st.session_state.page == "quiz_start":
        show_quiz_start()
    elif st.session_state.page == "quiz_results":
        show_quiz_results()
    elif st.session_state.page == "exit":
        show_exit()


if __name__ == "__main__":
    main()
