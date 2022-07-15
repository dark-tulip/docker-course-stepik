from datetime import datetime

import requests
import json
import time


START_DATE = datetime(2016, 1, 1, 0, 0)
STOP_DATE = datetime(2016, 12, 31, 23, 59)
TIMEZONE_PATTERN = "%Y-%m-%dT%H:%M:%SZ"


def generate_api_from_url(raw_request):
    return raw_request.replace("https://github.com", "https://api.github.com/repos") + "/commits"


def check_date_range(commit_date):
    return START_DATE <= commit_date <= STOP_DATE


def count_ok_commits(resp):

    commits = json.loads(resp.text)
    commits_cnt = 0

    for commit in commits:

        commits_date = time.strptime(commit["commit"]["committer"]["date"], TIMEZONE_PATTERN)

        if check_date_range(commits_date):
            commits_cnt += 1

    return commits_cnt


urls_str = """https://github.com/apache/incubator-airflow
https://github.com/ssadedin/bpipe
https://github.com/bloomreach/briefly
https://github.com/monajemi/clusterjob
https://github.com/tburdett/Conan2
https://github.com/broadinstitute/cromwell
https://github.com/joergen7/cuneiform
https://github.com/googlegenomics/dockerflow
https://github.com/thieman/dagobah
https://github.com/Factual/drake
https://github.com/druths/xp
https://github.com/sahilseth/flowr
https://github.com/mailund/gwf
https://github.com/Ensembl/ensembl-hive
https://github.com/hammerlab/ketrew
https://github.com/jtaghiyar/kronos
https://github.com/StanfordBioinformatics/loom
https://github.com/spotify/luigi
https://github.com/intentmedia/mario
https://github.com/openstack/mistral
https://github.com/mfiers/Moa
https://github.com/nipy/nipype
https://github.com/adaptivegenome/openge
https://github.com/fstrozzi/bioruby-pipengine
https://github.com/pinterest/pinball
https://github.com/Illumina/pyflow
https://github.com/PacificBiosciences/pypeFLOW
https://github.com/masa16/pwrake
https://github.com/alastair-droop/qsubsec
https://github.com/rabix/rabix
https://github.com/richfitz/remake
https://github.com/bjpop/rubra
https://github.com/kirillseva/ruigi
https://github.com/pharmbio/sciluigi
https://github.com/soravux/scoop
https://github.com/knipknap/SpiffWorkflow
https://github.com/Netflix/suro
https://github.com/BD2KGenomics/toil
https://github.com/pcingola/BigDataScript
https://github.com/ewels/clusterflow
https://github.com/LPM-HMS/COSMOS2
https://github.com/pydoit/doit
https://github.com/joblib/joblib
https://github.com/HECBioSim/Longbow
https://github.com/cooperative-computing-lab/cctools
https://github.com/nextflow-io/nextflow
https://github.com/tonyfischetti/sake
https://github.com/swift-lang/swift-k
https://github.com/Novartis/yap
https://github.com/davidsoergel/worldmake"""


total_ok_commits = 0

for url in urls_str.split():

    response = requests.get(generate_api_from_url(url))

    if response.status_code == 200:
        now = count_ok_commits(response)
        total_ok_commits += count_ok_commits(response)
        print("Commits", now, url)
    else:
        print("Error", response.status_code, url)

print(total_ok_commits)
