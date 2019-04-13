# py-BCI 0.1

This is a tutorial designed to demonstrate the potential of the "Python Stack" of
tools recommended for NeuroIS researchers, as described at the 2019 NeuroIS
Retreat in Vienna, Austria (Conrad et al., 2019). The "Python Stack" consists of
a series of Python libraries (Anaconda, Jupyter, Matplotlib, Numpy, Pandas,
PsychoPy, MNE and Scikit Learn) which can be used together to design experiments,
analyze data, collaborate and conduct machine learning analysis. The Dalhousie
NeuroCognitive Imaging Lab (NCIL) does not contribute to these libraries, but
uses them in its neuroimaging operations.

This is a breakdown of the folder contents:

py-bci

-offline-analysis <-- files for offline analysis using MNE and scikit-learn

--01 <-- files for Participant 1 (coauthor; bad recording due to offline.py)

---eeg_recordings <-- the folder with the actual EEG recordings

----p300-speller-01.fdt <-- trigger file

----p300-speller-01.set <-- EEG recording file

----p300-speller-01.ave <-- MNE "evokeds" data

----p300-speller-01.epo <-- MNE "epochs" data

---p300-speller-01.ipynb <-- Jupyter notebook file containing analysis scripts

--02 <-- files for Participant 2 (coauthor; bad recording due to offline.py)

---eeg_recordings

----p300-speller-02.fdt

----p300-speller-02.set

----p300-speller-02.ave

----p300-speller-02.epo

---p300-speller-02.ipynb

--n1 <-- files for New Participant 1 (coauthor; possible bad recording?)

---eeg_recordings

----p300-speller-new-01.fdt

----p300-speller-new-01.set

----p300-speller-new-01.ave

----p300-speller-new-01.epo

---p300-speller-n1.ipynb

--n2 <-- files for New Participant 2 (coauthor; good recording)

---eeg_recordings

----p300-speller-new-02.fdt

----p300-speller-new-02.set

----p300-speller-new-02.ave

----p300-speller-new-02.epo

---p300-speller-n2.ipynb

-offline-analysis <-- folder for stimulus files

--offline.py <-- training routine from the P300 speller for offline analysis

If you are interested in learning about offline analysis in MNE, consider
investigating the offline-analysis folder first using Jupyter and investigate
the processing scripts. If you have questions about the content of this tutorial,
please do not hesitate to reach out to Colin Conrad at colin.conrad@dal.ca.

NOTES ON THE RECORDINGS

The data contained in this tutorial was recorded by the coauthors over two time
periods. Participants 01 and 02 participated in a recording of offline.py when
it was configured for 300 ms intervals. This was chosen because some of the
literature on the subject of P300 speller suggested that classification can be
conducted successfully at such short intervals. We were skeptical, in part because
the P300 does not onset until 280 ms. As such, we created this program to
investigate whether this was the case. Unfortunately, a bug in our program
caused these two recordings to conflate conditions.

We fixed the bug and re-recorded the routines, this time set to 500 ms. though
participant N1 ("New Participant 1") lends results for good classification, it
is possible that this was the result of artifacts instead of the signal. N1 also
did not exhibit the regular P3 effect. N2, by contrast, did exhibit this effect
though appears to have a quieter signal. This may be improved by implementing
the xDAWN classifier, which is contained in the MNE library.

Ambitious readers may want to consider implementing xDAWN to improve
classification results. You can read more about how to do that here:
https://martinos.org/mne/dev/auto_examples/preprocessing/plot_xdawn_denoising.html

TODO:

1. Implement MNE's IO recording in the interface
2. Create a working implementation of xDAWN filtering and training
3. Pilot testing.

REFERENCES

Conrad, C., Agarwal, O, Calix Woc, C., Chiles, T., Godfrey, D., Krueger, K.,
Marini, V., Sproul, A., and Newman, A. (forthcoming). How to use python to run,
analyze, and decode EEG experiments. In: Davis, F. D., Riedl, R., vom Brocke,
J., Léger, P. M. and Randolph A. B. (eds.) Information Systems and Neuroscience.
Lecture Notes in Information Systems and Organisation. Springer International
Publishing.

Farwell, L. A., and Donchin, E. (1988). Talking off the top of your head: toward 
a mental prothesis utilizing event-related brain potentials. In:
Electroencephalography and clinical Neurophysiology vol. 70 iss. 6, pp. 510-523.
