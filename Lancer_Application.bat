@echo off
title Lancement de ZIGUINCHOR TRAFIC IA
color 0A
echo ========================================================
echo   Lancement de l'application Trafic IA - Ziguinchor
echo   Groupe 1 - Universite Assane Seck de Ziguinchor (UASZ)
echo ========================================================
echo.
cd /d "c:\LICENCE INFOMATIQUE\mon_Semestre_6\innovation"
echo Demarrage du serveur Streamlit...
echo Veuillez patienter, votre navigateur va s'ouvrir...
echo.
python -m streamlit run app_trafic_ziguinchor.py
pause
