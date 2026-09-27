# Environment setup

## Goal

The project uses two kinds of software:

1. command-line tools for PacBio read processing and QIIME 2 taxonomy;
2. a lightweight Python environment for ecological analysis.

Keep those roles separate. Do not install random packages into the working QIIME environment during an analysis unless there is a documented reason.

## QIIME 2

The completed taxonomy/comparison work used:

~~~bash
conda activate qiime2-amplicon-2026.1
qiime info
~~~

Save the qiime info output for important reruns.

Required QIIME plugins include:

~~~text
q2-dada2
q2-feature-table
q2-feature-classifier
q2-metadata
RESCRIPt
~~~

## External programs

Check the primary-processing tools:

~~~bash
cutadapt --version
vsearch --version
seqkit version
~~~

The primary OTU workflow uses Cutadapt and VSEARCH outside QIIME.

## Python ecology environment

A separate environment is convenient:

~~~bash
conda create -n afeq16s-ecology python=3.12 pandas numpy scipy matplotlib openpyxl statsmodels
conda activate afeq16s-ecology
~~~

## Configuration

Copy:

~~~bash
cp config/config.example.sh config/config.sh
~~~

Edit the workstation paths, then:

~~~bash
source config/config.sh
~~~

Do not commit config/config.sh; it contains workstation-specific paths.

## tmux for long steps

Classifier training and classification can run for a long time. Start a named session:

~~~bash
tmux new -s afeq16s
~~~

Detach with Ctrl-b d and reconnect with:

~~~bash
tmux attach -t afeq16s
~~~

A detached tmux session keeps the command running if the terminal disconnects.
