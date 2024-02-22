import subprocess


def parse_all():
    try:
        auchan = subprocess.run('python parsing_auchan.py', shell=True, check=False)
        globus = subprocess.run('python parsing_globus.py', shell=True, check=False)
        magnit = subprocess.run('python parsing_magnit.py', shell=True, check=False)
        metro = subprocess.run('python parsing_metro.py', shell=True, check=False)
        miratorg = subprocess.run('python parsing_miratorg.py', shell=True, check=False)
        perekrestok = subprocess.run('python parsing_perekrestok.py', shell=True, check=False)
        vkusvill = subprocess.run('python parsing_vkusvill.py', shell=True, check=False)
        vprok = subprocess.run('python parsing_vprok.py', shell=True, check=False)
    except Exception:
        print("PARSING-ALL FAILURE")


if __name__ == '__main__':
    parse_all()
