# Integration of Norse-Derived Terms in English

Repository for data, code and results from:

[Sara M. Pons-Sanz](https://profiles.cardiff.ac.uk/staff/pons-sanzs) & [Seán Roberts](https://profiles.cardiff.ac.uk/staff/robertss55) (in prep) *The Integration of Norse-Derived Terms in English: An Evolutionary Approach*

 The file `data/SharedIntegrationOfCognatesData.xlsx` has the original transcribed data. This is cleaned and processed by the script `analysis/analyseTextDistances.py`, which draws some code from `analysis/CLTSFeatureBasedAlignment.py` which is mainly contributed by Johann Mattis List (see [this post](https://calc.hypotheses.org/1962) and [this gist](https://gist.github.com/LinguList/7fac44813572f65259c872ef89fa64ad)). The script calculates the distances between pairs of Norse and English forms according to three measures:

-  Sound-based distance from Keller (2023).
-  A feature-based distance.
-  A historical distance that uses the likelihood of one segment historically replacing another.

Each row in the data represents a comparison between a Norse form and an English form within a given cognate set, including the three measures of distance and frequency of occurance in each source.

This repository includes some package files from [CLTS](https://clts.clld.org/), see [this repository](https://github.com/cldf-clts/clts).

