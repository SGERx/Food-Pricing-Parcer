import os
import subprocess


def launch_parsing_all():
    try:
        subprocess.run('/python parsing_auchan.py', capture_output=True, text=True, cwd='../parsing_logic/step_1_parsing/by_store')
    except:
        print("PARSING-ALL MODIFIED AUCHAN FAILURE")
    try:
        subprocess.run('/python parsing_auchan.py', shell=True, check=False, cwd='../parsing_logic/step_1_parsing/by_store')
    except:
        print("PARSING-ALL AUCHAN FAILURE")
    try:
        subprocess.run('python parsing_globus.py', shell=True, check=False)
    except:
        print("PARSING-ALL GLOBUS FAILURE")
    try:
        subprocess.run('python parsing_magnit.py', shell=True, check=False)
    except:
        print("PARSING-ALL MAGNIT FAILURE")
    try:
        subprocess.run('python parsing_metro.py', shell=True, check=False)
    except:
        print("PARSING-ALL METRO FAILURE")
    try:
        subprocess.run('python parsing_miratorg.py', shell=True, check=False)
    except:
        print("PARSING-ALL MIRATORG FAILURE")
    try:
        subprocess.run('python parsing_perekrestok.py', shell=True, check=False)
    except:
        print("PARSING-ALL PEREKRESTOK FAILURE")
    try:
        subprocess.run('python parsing_vkusvill.py', shell=True, check=False)
    except:
        print("PARSING-ALL VKUSVILL FAILURE")
    try:
        subprocess.run('python parsing_vprok.py', shell=True, check=False)
    except:
        print("PARSING-ALL VPROK FAILURE")
    return "PARSING COMPLETED..."







