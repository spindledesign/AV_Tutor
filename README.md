# AV Tutor (Streamlit)

This repository contains a simple Streamlit-based prototype UI for an Antivirus (AV) Tutor. It replaces the original Tkinter prototype and provides the following flows:

- Home screen
- Learning modules (concept pages)
- Quick quiz (multiple choice)

Prerequisites

- Python 3.10+ is recommended

Setup

```bash
# create and activate a virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run

```bash
# from the project directory
streamlit run av_tutor_ui.py
```

Notes

- The app uses mock content stored in `av_tutor_ui.py`.
- To use the ontology (`av_tutor.owl`) you can install `rdflib` (see commented line in `requirements.txt`) and extend the app to load concepts from the ontology.
