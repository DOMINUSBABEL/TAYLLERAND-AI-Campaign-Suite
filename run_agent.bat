@echo off
echo ==================================================
echo    TAYLLERAND AI - ELECTORAL INTELLIGENCE
echo ==================================================
echo.
echo [1/2] Verifying Environment...
pip install streamlit folium streamlit-folium pandas > nul 2>&1

echo [2/2] Launching Command Console...
echo.
echo The application will open in your default browser.
echo Press Ctrl+C to stop the agent.
echo.

python -m streamlit run app.py
pause
