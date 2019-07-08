# Density Estimation Benchmark Datasets

A collection of datasets used in machine learning for density
estimation.

If you use any of the datasets, you should cite their original papers.<sup id="a1">[1](#f1)</sup><sup id="a1">[2](#f2)</sup><sup id="a1">[3](#f3)<sup id="a1">[4](#f4)</sup>

## Datasets

|Dataset | type | #vars | #train | #valid | #test | density | abbrv |
|:------|:---:|---:|---:|---:|---:|---:|---:|
|**NLTCS**<sup id="a1">[1](#f1)</sup>| binary | 16 | 16181 | 2157 | 3236 | 0.332|`NLTCS`|
|**MSNBC**<sup id="a1">[1](#f1)</sup>| binary | 17 | 291326 | 38843 | 58265 | 0.166|`msnbc`|
|**KDDCup2k**<sup id="a1">[1](#f1)</sup>| binary | 65 | 180092 | 19907 | 34955 | 0.008|`kdd`|
|**Plants**<sup id="a1">[1](#f1)</sup>| binary | 69 | 17412 | 2321 | 3482 | 0.180|`plants`|
|**Audio**<sup id="a1">[1](#f1)</sup>| binary | 100 | 15000 | 2000 | 3000 | 0.199|`baudio`|
|**Jester**<sup id="a1">[1](#f1)</sup>| binary | 100 | 9000 | 1000 | 4116 | 0.608|`jester`|
|**Netflix**<sup id="a1">[1](#f1)</sup>| binary | 100 | 15000 | 2000 | 3000 | 0.541|`bnetflix`|
|**Accidents**<sup id="a1">[2](#f2)</sup>| binary | 111 | 12758 | 1700 | 2551 | 0.291|`accidents`|
|**Mushrooms**<sup id="a3">[4](#f4)</sup>| binary | 112 | 2000 | 500 | 5624 | 0.187|`mushrooms`|
|**Adult**<sup id="a3">[4](#f4)</sup>| binary | 123 | 5000 | 1414 | 26147 | 0.112|`adult`|
|**Connect 4**<sup id="a3">[4](#f4)</sup>| binary | 126 | 16000 | 4000 | 47557 | 0.333|`connect4`|
|**OCR Letters**<sup id="a3">[4](#f4)</sup>| binary | 128 | 32152 | 10000 | 10000 | 0.220|`ocr_letters`|
|**RCV-1**<sup id="a3">[4](#f4)</sup>| binary | 150 | 40000 | 10000 | 150000 | 0.138|`rcv1`|
|**Retail**<sup id="a2">[2](#f2)</sup>| binary | 135 | 22041 | 2938 | 4408 | 0.024|`tretail`|
|**Pumsb-star**<sup id="a2">[2](#f2)</sup>| binary | 163 | 12262 | 1635 | 2452 | 0.270|`pumsb_star`|
|**DNA**<sup id="a2">[2](#f2)</sup>| binary | 180 | 1600 | 400 | 1186 | 0.253|`dna`|
|**Kosarek**<sup id="a2">[2](#f2)</sup>| binary | 190 | 33375 | 4450 | 6675 | 0.020|`kosarek`|
|**MSWeb**<sup id="a1">[1](#f1)</sup>| binary | 294 | 29441 | 3270 | 5000 | 0.010|`MSWeb`|
|**NIPS**<sup id="a3">[4](#f4)</sup>| binary | 500 | 400 | 100 | 1240 | 0.367|`nips`|
|**Book**<sup id="a1">[1](#f1)</sup>| binary | 500 | 8700 | 1159 | 1739 | 0.016|`book`|
|**EachMovie**<sup id="a1">[1](#f1)</sup>| binary | 500 | 4525 | 1002 | 591 | 0.059|`tmovie`|
|**WebKB**<sup id="a1">[1](#f1)</sup>| binary | 839 | 2803 | 558 | 838 | 0.064|`cwebkb`|
|**Reuters-52**<sup id="a1">[1](#f1)</sup>| binary | 889 | 6532 | 1028 | 1540 | 0.036|`cr52`|
|**20 NewsGroup**<sup id="a1">[1](#f1)</sup>| binary | 910 | 11293 | 3764 | 3764 | 0.049|`c20ng`|
|**Movie reviews**<sup id="a1">[3](#f3)</sup>| binary | 1001 | 1600 | 150 | 250 | 0.140 |`moviereview`|
|**BBC**<sup id="a2">[2](#f2)</sup>| binary | 1058 | 1670 | 225 | 330 | 0.078|`bbc`|
|**Voting**<sup id="a1">[3](#f3)</sup>| binary | 1359 | 1214 | 200| 350| 0.333|`voting`|
|**Ad**<sup id="a2">[2](#f2)</sup>| binary | 1556 | 2461 | 327 | 491 | 0.008|`ad`|


## Introduced in:

<b id="f1">1</b> Daniel Lowd, Jesse Davis: [*Learning Markov Network
Structure with Decision Trees*][Lowd2010]. ICDM 2010

<b id="f2">2</b> Jan Van Haaren, Jesse Davis: [*Markov Network
Structure Learning: A Randomized Feature Generation Approach*][VanHaaren2012]. AAAI 2012

<b id="f3">3</b> Jessa Bekker, Jesse Davis, Arthur Choi, Adnan Darwiche, Guy Van den Broeck: [*Tractable Learning 
for Complex Probability Queries*][Bekker2015]. NIPS 2015

<b id="f4">3</b> Hugo Larochelle, Iain Murray: [*The Neural Autoregressive Distribution Estimator*][Larochelle2011]. AISTATS 2011

[Lowd2010]: http://ix.cs.uoregon.edu/~lowd/icdm10lowd.pdf
[VanHaaren2012]: http://www.aaai.org/ocs/index.php/AAAI/AAAI12/paper/viewFile/5107/5534
[Bekker2015]: https://lirias.kuleuven.be/bitstream/123456789/513299/4/nips15_cr.pdf
[Larochelle2011]: http://proceedings.mlr.press/v15/larochelle11a/larochelle11a.pdf
