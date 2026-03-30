@echo off
title Painel AlarmeForte
start "" /MIN python -m streamlit run admin.py --server.headless true --server.port 8502 --browser.gatherUsageStats false
ping -n 4 127.0.0.1 > nul
start http://localhost:8502
