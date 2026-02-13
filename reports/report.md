# Solr 5 vs 8 Drift Report
- Solr5: `http://localhost:8985/solr/core1`
- Solr8: `http://localhost:8988/solr/core1`

Thresholds:
- MAX_AVG_ABS_RANK_DELTA=1.0
- MAX_MAX_ABS_RANK_DELTA=4
- MAX_MAX_ABS_NORM_DRIFT=0.15

## q_basic — FAIL ❌
- Reason: max_abs_norm_drift 0.190 >= 0.15
- Jaccard(top10): **0.818**
- Avg abs rank delta: **0.33** (max: 1, changes: 3)
- Top score (Solr5/Solr8): **1.052679 / 4.578894**
- Max abs normalized drift (top1-normalized): **0.190**
- Only in Solr5 top10: ['12']
- Only in Solr8 top10: ['16']

Top movers:

| id | rank5 | rank8 | delta |
|---|---:|---:|---:|
| 11 | 7 | 8 | 1 |
| 13 | 8 | 9 | 1 |
| 7 | 9 | 10 | 1 |
| 10 | 1 | 1 | 0 |
| 3 | 2 | 2 | 0 |

Top score drifts (raw, abs):

| id | score5 | score8 | abs | rel |
|---|---:|---:|---:|---:|
| 10 | 1.052679 | 4.578894 | 3.526215 | 3.350 |
| 3 | 1.052679 | 4.578894 | 3.526215 | 3.350 |
| 4 | 1.052679 | 4.578894 | 3.526215 | 3.350 |
| 1 | 0.921094 | 4.095487 | 3.174393 | 3.446 |
| 8 | 0.921094 | 4.095487 | 3.174393 | 3.446 |

Top score drifts (normalized by top1, abs):

| id | norm5 | norm8 | abs | rel |
|---|---:|---:|---:|---:|
| 11 | 0.588748 | 0.778871 | 0.190123 | 0.323 |
| 13 | 0.588748 | 0.712717 | 0.123969 | 0.211 |
| 7 | 0.588748 | 0.712717 | 0.123969 | 0.211 |
| 1 | 0.875000 | 0.894427 | 0.019427 | 0.022 |
| 8 | 0.875000 | 0.894427 | 0.019427 | 0.022 |

Explain snippets (top raw-drift docs):

**doc id 10**

- Solr5 explain (prefix): `
1.0526793 = sum of:
  0.6808216 = max of:
    0.6808216 = weight(title:iphone in 9) [ClassicSimilarity], result of:
      0.6808216 = score(doc=9,freq=1.0), product of:
        0.8042084 = queryWeight, product of:
          3.0 = boost
          1.6931472 = idf(docFreq=8, maxDocs=18)
          0.15832615 = queryNorm
        0.8465736 = fieldWeight in 9, product of:
          1.0 = tf(freq=1.0), w`
- Solr8 explain (prefix): `
4.578894 = sum of:
  2.6208217 = max of:
    2.6208217 = weight(title:iphone in 9) [ClassicSimilarity], result of:
      2.6208217 = score(freq=1.0), product of:
        3.0 = boost
        1.7472144 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          8 = docFreq, number of documents containing term
          18 = docCount, total number of documents with field
        1.0 = tf(fr`

**doc id 3**

- Solr5 explain (prefix): `
1.0526793 = sum of:
  0.6808216 = max of:
    0.6808216 = weight(title:iphone in 2) [ClassicSimilarity], result of:
      0.6808216 = score(doc=2,freq=1.0), product of:
        0.8042084 = queryWeight, product of:
          3.0 = boost
          1.6931472 = idf(docFreq=8, maxDocs=18)
          0.15832615 = queryNorm
        0.8465736 = fieldWeight in 2, product of:
          1.0 = tf(freq=1.0), w`
- Solr8 explain (prefix): `
4.578894 = sum of:
  2.6208217 = max of:
    2.6208217 = weight(title:iphone in 2) [ClassicSimilarity], result of:
      2.6208217 = score(freq=1.0), product of:
        3.0 = boost
        1.7472144 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          8 = docFreq, number of documents containing term
          18 = docCount, total number of documents with field
        1.0 = tf(fr`

## q_phrase — PASS ✅
- Jaccard(top10): **1.000**
- Avg abs rank delta: **0.67** (max: 3, changes: 2)
- Top score (Solr5/Solr8): **1.877696 / 5.795289**
- Max abs normalized drift (top1-normalized): **0.103**
- Only in Solr5 top10: []
- Only in Solr8 top10: []

Top movers:

| id | rank5 | rank8 | delta |
|---|---:|---:|---:|
| 1 | 4 | 7 | 3 |
| 9 | 7 | 4 | -3 |
| 3 | 1 | 1 | 0 |
| 5 | 2 | 2 | 0 |
| 7 | 3 | 3 | 0 |

Top score drifts (raw, abs):

| id | score5 | score8 | abs | rel |
|---|---:|---:|---:|---:|
| 3 | 1.877696 | 5.795289 | 3.917594 | 2.086 |
| 5 | 1.877696 | 5.795289 | 3.917594 | 2.086 |
| 7 | 1.877696 | 5.795289 | 3.917594 | 2.086 |
| 9 | 0.264919 | 1.415229 | 1.150309 | 4.342 |
| 12 | 0.264919 | 1.363749 | 1.098829 | 4.148 |

Top score drifts (normalized by top1, abs):

| id | norm5 | norm8 | abs | rel |
|---|---:|---:|---:|---:|
| 9 | 0.141087 | 0.244203 | 0.103116 | 0.731 |
| 12 | 0.141087 | 0.235320 | 0.094233 | 0.668 |
| 15 | 0.123451 | 0.213550 | 0.090098 | 0.730 |
| 2 | 0.141087 | 0.227341 | 0.086253 | 0.611 |
| 1 | 0.141087 | 0.220122 | 0.079034 | 0.560 |

Explain snippets (top raw-drift docs):

**doc id 3**

- Solr5 explain (prefix): `
1.8776959 = sum of:
  1.8776959 = max of:
    1.8776959 = weight(title:"fast charger" in 2) [ClassicSimilarity], result of:
      1.8776959 = fieldWeight in 2, product of:
        1.0 = tf(freq=1.0), with freq of:
          1.0 = phraseFreq=1.0
        3.7553918 = idf(), sum of:
          2.5040774 = idf(docFreq=3, maxDocs=18)
          1.2513144 = idf(docFreq=13, maxDocs=18)
        0.5 = fieldN`
- Solr8 explain (prefix): `
5.7952895 = sum of:
  5.7952895 = max of:
    5.7952895 = weight(title:"fast charger" in 2) [ClassicSimilarity], result of:
      5.7952895 = score(freq=1.0), product of:
        3.0 = boost
        3.8635263 = idf(), sum of:
          2.5581446 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
            3 = docFreq, number of documents containing term
            18 = docCount, total `

**doc id 5**

- Solr5 explain (prefix): `
1.8776959 = sum of:
  1.8776959 = max of:
    1.8776959 = weight(title:"fast charger" in 4) [ClassicSimilarity], result of:
      1.8776959 = fieldWeight in 4, product of:
        1.0 = tf(freq=1.0), with freq of:
          1.0 = phraseFreq=1.0
        3.7553918 = idf(), sum of:
          2.5040774 = idf(docFreq=3, maxDocs=18)
          1.2513144 = idf(docFreq=13, maxDocs=18)
        0.5 = fieldN`
- Solr8 explain (prefix): `
5.7952895 = sum of:
  5.7952895 = max of:
    5.7952895 = weight(title:"fast charger" in 4) [ClassicSimilarity], result of:
      5.7952895 = score(freq=1.0), product of:
        3.0 = boost
        3.8635263 = idf(), sum of:
          2.5581446 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
            3 = docFreq, number of documents containing term
            18 = docCount, total `

## q_phrase_freq — FAIL ❌
- Reason: max_abs_rank_delta 4 >= 4 (not near-tie; max_abs_norm_drift 0.335)
- Jaccard(top10): **0.667**
- Avg abs rank delta: **1.12** (max: 4, changes: 5)
- Top score (Solr5/Solr8): **2.059716 / 8.416111**
- Max abs normalized drift (top1-normalized): **0.335**
- Only in Solr5 top10: ['12', '2']
- Only in Solr8 top10: ['17', '4']

Top movers:

| id | rank5 | rank8 | delta |
|---|---:|---:|---:|
| 16 | 9 | 5 | -4 |
| 1 | 4 | 6 | 2 |
| 9 | 5 | 4 | -1 |
| 8 | 6 | 7 | 1 |
| 10 | 10 | 9 | -1 |

Top score drifts (raw, abs):

| id | score5 | score8 | abs | rel |
|---|---:|---:|---:|---:|
| 3 | 2.059716 | 8.416111 | 6.356395 | 3.086 |
| 5 | 0.855881 | 5.795289 | 4.939409 | 5.771 |
| 7 | 1.801351 | 6.718334 | 4.916982 | 2.730 |
| 16 | 0.217471 | 3.706402 | 3.488930 | 16.043 |
| 9 | 0.545968 | 3.759363 | 3.213395 | 5.886 |

Top score drifts (normalized by top1, abs):

| id | norm5 | norm8 | abs | rel |
|---|---:|---:|---:|---:|
| 16 | 0.105583 | 0.440394 | 0.334810 | 3.171 |
| 5 | 0.415533 | 0.688595 | 0.273061 | 0.657 |
| 10 | 0.084467 | 0.311405 | 0.226939 | 2.687 |
| 9 | 0.265070 | 0.446686 | 0.181617 | 0.685 |
| 1 | 0.265070 | 0.430104 | 0.165035 | 0.623 |

Explain snippets (top raw-drift docs):

**doc id 3**

- Solr5 explain (prefix): `
2.0597157 = sum of:
  2.0597157 = sum of:
    1.7117615 = max of:
      1.7117615 = weight(title:"fast charger" in 2) [ClassicSimilarity], result of:
        1.7117615 = score(doc=2,freq=1.0), product of:
          0.91162866 = queryWeight, product of:
            3.0 = boost
            3.7553918 = idf(), sum of:
              2.5040774 = idf(docFreq=3, maxDocs=18)
              1.2513144 = idf(`
- Solr8 explain (prefix): `
8.416111 = sum of:
  8.416111 = sum of:
    5.7952895 = max of:
      5.7952895 = weight(title:"fast charger" in 2) [ClassicSimilarity], result of:
        5.7952895 = score(freq=1.0), product of:
          3.0 = boost
          3.8635263 = idf(), sum of:
            2.5581446 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
              3 = docFreq, number of documents containing term`

**doc id 5**

- Solr5 explain (prefix): `
0.85588074 = sum of:
  0.85588074 = product of:
    1.7117615 = sum of:
      1.7117615 = max of:
        1.7117615 = weight(title:"fast charger" in 4) [ClassicSimilarity], result of:
          1.7117615 = score(doc=4,freq=1.0), product of:
            0.91162866 = queryWeight, product of:
              3.0 = boost
              3.7553918 = idf(), sum of:
                2.5040774 = idf(docFreq=3`
- Solr8 explain (prefix): `
5.7952895 = sum of:
  5.7952895 = sum of:
    5.7952895 = max of:
      5.7952895 = weight(title:"fast charger" in 4) [ClassicSimilarity], result of:
        5.7952895 = score(freq=1.0), product of:
          3.0 = boost
          3.8635263 = idf(), sum of:
            2.5581446 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
              3 = docFreq, number of documents containing te`

## q_usb_c — FAIL ❌
- Reason: max_abs_norm_drift 0.285 >= 0.15
- Jaccard(top10): **0.818**
- Avg abs rank delta: **0.67** (max: 3, changes: 3)
- Top score (Solr5/Solr8): **1.572243 / 9.730376**
- Max abs normalized drift (top1-normalized): **0.285**
- Only in Solr5 top10: ['7']
- Only in Solr8 top10: ['13']

Top movers:

| id | rank5 | rank8 | delta |
|---|---:|---:|---:|
| 6 | 10 | 7 | -3 |
| 3 | 7 | 9 | 2 |
| 9 | 9 | 10 | 1 |
| 1 | 1 | 1 | 0 |
| 12 | 2 | 2 | 0 |

Top score drifts (raw, abs):

| id | score5 | score8 | abs | rel |
|---|---:|---:|---:|---:|
| 1 | 1.572243 | 9.730376 | 8.158133 | 5.189 |
| 12 | 1.572243 | 9.730376 | 8.158133 | 5.189 |
| 18 | 1.497514 | 9.150873 | 7.653359 | 5.111 |
| 2 | 1.300139 | 8.455669 | 7.155530 | 5.504 |
| 14 | 0.704150 | 6.597644 | 5.893494 | 8.370 |

Top score drifts (normalized by top1, abs):

| id | norm5 | norm8 | abs | rel |
|---|---:|---:|---:|---:|
| 6 | 0.271949 | 0.556846 | 0.284897 | 1.048 |
| 14 | 0.447863 | 0.678046 | 0.230183 | 0.514 |
| 15 | 0.447863 | 0.678046 | 0.230183 | 0.514 |
| 3 | 0.316178 | 0.460116 | 0.143939 | 0.455 |
| 9 | 0.298858 | 0.428715 | 0.129858 | 0.435 |

Explain snippets (top raw-drift docs):

**doc id 1**

- Solr5 explain (prefix): `
1.5722427 = sum of:
  0.34900042 = max of:
    0.34900042 = weight(title:usb in 0) [ClassicSimilarity], result of:
      0.34900042 = score(doc=0,freq=1.0), product of:
        0.47114348 = queryWeight, product of:
          3.0 = boost
          1.6931472 = idf(docFreq=8, maxDocs=18)
          0.092754975 = queryNorm
        0.74075186 = fieldWeight in 0, product of:
          1.0 = tf(freq=1.0)`
- Solr8 explain (prefix): `
9.730376 = sum of:
  2.344134 = max of:
    2.344134 = weight(title:usb in 0) [ClassicSimilarity], result of:
      2.344134 = score(freq=1.0), product of:
        3.0 = boost
        1.7472144 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          8 = docFreq, number of documents containing term
          18 = docCount, total number of documents with field
        1.0 = tf(freq=1.0`

**doc id 12**

- Solr5 explain (prefix): `
1.5722427 = sum of:
  0.34900042 = max of:
    0.34900042 = weight(title:usb in 11) [ClassicSimilarity], result of:
      0.34900042 = score(doc=11,freq=1.0), product of:
        0.47114348 = queryWeight, product of:
          3.0 = boost
          1.6931472 = idf(docFreq=8, maxDocs=18)
          0.092754975 = queryNorm
        0.74075186 = fieldWeight in 11, product of:
          1.0 = tf(freq=1`
- Solr8 explain (prefix): `
9.730376 = sum of:
  2.344134 = max of:
    2.344134 = weight(title:usb in 11) [ClassicSimilarity], result of:
      2.344134 = score(freq=1.0), product of:
        3.0 = boost
        1.7472144 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          8 = docFreq, number of documents containing term
          18 = docCount, total number of documents with field
        1.0 = tf(freq=1.`

## q_filter_instock — FAIL ❌
- Reason: max_abs_norm_drift 0.190 >= 0.15
- Jaccard(top10): **0.818**
- Avg abs rank delta: **0.44** (max: 1, changes: 4)
- Top score (Solr5/Solr8): **1.052679 / 4.578894**
- Max abs normalized drift (top1-normalized): **0.190**
- Only in Solr5 top10: ['2']
- Only in Solr8 top10: ['16']

Top movers:

| id | rank5 | rank8 | delta |
|---|---:|---:|---:|
| 11 | 6 | 7 | 1 |
| 13 | 7 | 8 | 1 |
| 7 | 8 | 9 | 1 |
| 12 | 9 | 10 | 1 |
| 10 | 1 | 1 | 0 |

Top score drifts (raw, abs):

| id | score5 | score8 | abs | rel |
|---|---:|---:|---:|---:|
| 10 | 1.052679 | 4.578894 | 3.526215 | 3.350 |
| 3 | 1.052679 | 4.578894 | 3.526215 | 3.350 |
| 4 | 1.052679 | 4.578894 | 3.526215 | 3.350 |
| 1 | 0.921094 | 4.095487 | 3.174393 | 3.446 |
| 8 | 0.921094 | 4.095487 | 3.174393 | 3.446 |

Top score drifts (normalized by top1, abs):

| id | norm5 | norm8 | abs | rel |
|---|---:|---:|---:|---:|
| 11 | 0.588748 | 0.778871 | 0.190123 | 0.323 |
| 13 | 0.588748 | 0.712717 | 0.123969 | 0.211 |
| 7 | 0.588748 | 0.712717 | 0.123969 | 0.211 |
| 12 | 0.544592 | 0.667571 | 0.122979 | 0.226 |
| 1 | 0.875000 | 0.894427 | 0.019427 | 0.022 |

Explain snippets (top raw-drift docs):

**doc id 10**

- Solr5 explain (prefix): `
1.0526793 = sum of:
  0.6808216 = max of:
    0.6808216 = weight(title:iphone in 9) [ClassicSimilarity], result of:
      0.6808216 = score(doc=9,freq=1.0), product of:
        0.8042084 = queryWeight, product of:
          3.0 = boost
          1.6931472 = idf(docFreq=8, maxDocs=18)
          0.15832615 = queryNorm
        0.8465736 = fieldWeight in 9, product of:
          1.0 = tf(freq=1.0), w`
- Solr8 explain (prefix): `
4.578894 = sum of:
  2.6208217 = max of:
    2.6208217 = weight(title:iphone in 9) [ClassicSimilarity], result of:
      2.6208217 = score(freq=1.0), product of:
        3.0 = boost
        1.7472144 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          8 = docFreq, number of documents containing term
          18 = docCount, total number of documents with field
        1.0 = tf(fr`

**doc id 3**

- Solr5 explain (prefix): `
1.0526793 = sum of:
  0.6808216 = max of:
    0.6808216 = weight(title:iphone in 2) [ClassicSimilarity], result of:
      0.6808216 = score(doc=2,freq=1.0), product of:
        0.8042084 = queryWeight, product of:
          3.0 = boost
          1.6931472 = idf(docFreq=8, maxDocs=18)
          0.15832615 = queryNorm
        0.8465736 = fieldWeight in 2, product of:
          1.0 = tf(freq=1.0), w`
- Solr8 explain (prefix): `
4.578894 = sum of:
  2.6208217 = max of:
    2.6208217 = weight(title:iphone in 2) [ClassicSimilarity], result of:
      2.6208217 = score(freq=1.0), product of:
        3.0 = boost
        1.7472144 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          8 = docFreq, number of documents containing term
          18 = docCount, total number of documents with field
        1.0 = tf(fr`

## q_filter_price_range — FAIL ❌
- Reason: max_abs_norm_drift 0.405 >= 0.15
- Jaccard(top10): **1.000**
- Avg abs rank delta: **0.60** (max: 3, changes: 4)
- Top score (Solr5/Solr8): **1.052679 / 4.578894**
- Max abs normalized drift (top1-normalized): **0.405**
- Only in Solr5 top10: []
- Only in Solr8 top10: []

Top movers:

| id | rank5 | rank8 | delta |
|---|---:|---:|---:|
| 16 | 8 | 5 | -3 |
| 11 | 5 | 6 | 1 |
| 7 | 6 | 7 | 1 |
| 12 | 7 | 8 | 1 |
| 3 | 1 | 1 | 0 |

Top score drifts (raw, abs):

| id | score5 | score8 | abs | rel |
|---|---:|---:|---:|---:|
| 3 | 1.052679 | 4.578894 | 3.526215 | 3.350 |
| 16 | 0.425513 | 3.706402 | 3.280888 | 7.710 |
| 1 | 0.921094 | 4.095487 | 3.174393 | 3.446 |
| 8 | 0.921094 | 4.095487 | 3.174393 | 3.446 |
| 9 | 0.921094 | 4.095487 | 3.174393 | 3.446 |

Top score drifts (normalized by top1, abs):

| id | norm5 | norm8 | abs | rel |
|---|---:|---:|---:|---:|
| 16 | 0.404219 | 0.809453 | 0.405234 | 1.003 |
| 5 | 0.176624 | 0.427630 | 0.251006 | 1.421 |
| 11 | 0.588748 | 0.778871 | 0.190123 | 0.323 |
| 18 | 0.093960 | 0.255924 | 0.161965 | 1.724 |
| 7 | 0.588748 | 0.712717 | 0.123969 | 0.211 |

Explain snippets (top raw-drift docs):

**doc id 3**

- Solr5 explain (prefix): `
1.0526793 = sum of:
  0.6808216 = max of:
    0.6808216 = weight(title:iphone in 2) [ClassicSimilarity], result of:
      0.6808216 = score(doc=2,freq=1.0), product of:
        0.8042084 = queryWeight, product of:
          3.0 = boost
          1.6931472 = idf(docFreq=8, maxDocs=18)
          0.15832615 = queryNorm
        0.8465736 = fieldWeight in 2, product of:
          1.0 = tf(freq=1.0), w`
- Solr8 explain (prefix): `
4.578894 = sum of:
  2.6208217 = max of:
    2.6208217 = weight(title:iphone in 2) [ClassicSimilarity], result of:
      2.6208217 = score(freq=1.0), product of:
        3.0 = boost
        1.7472144 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          8 = docFreq, number of documents containing term
          18 = docCount, total number of documents with field
        1.0 = tf(fr`

**doc id 16**

- Solr5 explain (prefix): `
0.4255135 = product of:
  0.851027 = sum of:
    0.851027 = max of:
      0.851027 = weight(title:iphone in 15) [ClassicSimilarity], result of:
        0.851027 = score(doc=15,freq=1.0), product of:
          0.8042084 = queryWeight, product of:
            3.0 = boost
            1.6931472 = idf(docFreq=8, maxDocs=18)
            0.15832615 = queryNorm
          1.058217 = fieldWeight in 15, pro`
- Solr8 explain (prefix): `
3.7064016 = sum of:
  3.7064016 = max of:
    3.7064016 = weight(title:iphone in 15) [ClassicSimilarity], result of:
      3.7064016 = score(freq=1.0), product of:
        3.0 = boost
        1.7472144 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          8 = docFreq, number of documents containing term
          18 = docCount, total number of documents with field
        1.0 = tf(`

## q_brand_anker — FAIL ❌
- Reason: max_abs_norm_drift 0.276 >= 0.15
- Jaccard(top10): **1.000**
- Avg abs rank delta: **0.00** (max: 0, changes: 0)
- Top score (Solr5/Solr8): **0.921094 / 4.095487**
- Max abs normalized drift (top1-normalized): **0.276**
- Only in Solr5 top10: []
- Only in Solr8 top10: []

Top movers:

| id | rank5 | rank8 | delta |
|---|---:|---:|---:|
| 1 | 1 | 1 | 0 |
| 9 | 2 | 2 | 0 |
| 11 | 3 | 3 | 0 |
| 7 | 4 | 4 | 0 |
| 5 | 5 | 5 | 0 |

Top score drifts (raw, abs):

| id | score5 | score8 | abs | rel |
|---|---:|---:|---:|---:|
| 1 | 0.921094 | 4.095487 | 3.174393 | 3.446 |
| 9 | 0.921094 | 4.095487 | 3.174393 | 3.446 |
| 11 | 0.619763 | 3.566369 | 2.946606 | 4.754 |
| 7 | 0.619763 | 3.263454 | 2.643691 | 4.266 |
| 5 | 0.185929 | 1.958072 | 1.772144 | 9.531 |

Top score drifts (normalized by top1, abs):

| id | norm5 | norm8 | abs | rel |
|---|---:|---:|---:|---:|
| 5 | 0.201856 | 0.478105 | 0.276248 | 1.369 |
| 14 | 0.176624 | 0.427630 | 0.251006 | 1.421 |
| 11 | 0.672855 | 0.870805 | 0.197950 | 0.294 |
| 7 | 0.672855 | 0.796841 | 0.123987 | 0.184 |
| 1 | 1.000000 | 1.000000 | 0.000000 | 0.000 |

Explain snippets (top raw-drift docs):

**doc id 1**

- Solr5 explain (prefix): `
0.92109436 = sum of:
  0.59571886 = max of:
    0.59571886 = weight(title:iphone in 0) [ClassicSimilarity], result of:
      0.59571886 = score(doc=0,freq=1.0), product of:
        0.8042084 = queryWeight, product of:
          3.0 = boost
          1.6931472 = idf(docFreq=8, maxDocs=18)
          0.15832615 = queryNorm
        0.74075186 = fieldWeight in 0, product of:
          1.0 = tf(freq=1.`
- Solr8 explain (prefix): `
4.095487 = sum of:
  2.344134 = max of:
    2.344134 = weight(title:iphone in 0) [ClassicSimilarity], result of:
      2.344134 = score(freq=1.0), product of:
        3.0 = boost
        1.7472144 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          8 = docFreq, number of documents containing term
          18 = docCount, total number of documents with field
        1.0 = tf(freq=`

**doc id 9**

- Solr5 explain (prefix): `
0.92109436 = sum of:
  0.59571886 = max of:
    0.59571886 = weight(title:iphone in 8) [ClassicSimilarity], result of:
      0.59571886 = score(doc=8,freq=1.0), product of:
        0.8042084 = queryWeight, product of:
          3.0 = boost
          1.6931472 = idf(docFreq=8, maxDocs=18)
          0.15832615 = queryNorm
        0.74075186 = fieldWeight in 8, product of:
          1.0 = tf(freq=1.`
- Solr8 explain (prefix): `
4.095487 = sum of:
  2.344134 = max of:
    2.344134 = weight(title:iphone in 8) [ClassicSimilarity], result of:
      2.344134 = score(freq=1.0), product of:
        3.0 = boost
        1.7472144 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          8 = docFreq, number of documents containing term
          18 = docCount, total number of documents with field
        1.0 = tf(freq=`

## q_near_tie_stress — FAIL ❌
- Reason: max_abs_norm_drift 0.158 >= 0.15
- Jaccard(top10): **1.000**
- Avg abs rank delta: **0.22** (max: 1, changes: 2)
- Top score (Solr5/Solr8): **1.454017 / 12.509465**
- Max abs normalized drift (top1-normalized): **0.158**
- Only in Solr5 top10: []
- Only in Solr8 top10: []

Top movers:

| id | rank5 | rank8 | delta |
|---|---:|---:|---:|
| 2 | 1 | 2 | 1 |
| 18 | 2 | 1 | -1 |
| 1 | 3 | 3 | 0 |
| 3 | 4 | 4 | 0 |
| 12 | 5 | 5 | 0 |

Top score drifts (raw, abs):

| id | score5 | score8 | abs | rel |
|---|---:|---:|---:|---:|
| 18 | 1.358271 | 12.509465 | 11.151194 | 8.210 |
| 2 | 1.454017 | 12.155692 | 10.701674 | 7.360 |
| 1 | 1.303582 | 11.833829 | 10.530247 | 8.078 |
| 3 | 1.126822 | 9.924996 | 8.798174 | 7.808 |
| 12 | 0.864831 | 9.414147 | 8.549316 | 9.886 |

Top score drifts (normalized by top1, abs):

| id | norm5 | norm8 | abs | rel |
|---|---:|---:|---:|---:|
| 12 | 0.594787 | 0.752562 | 0.157775 | 0.265 |
| 5 | 0.351870 | 0.495543 | 0.143673 | 0.408 |
| 9 | 0.384198 | 0.514833 | 0.130635 | 0.340 |
| 8 | 0.300950 | 0.386949 | 0.086000 | 0.286 |
| 7 | 0.485822 | 0.554924 | 0.069103 | 0.142 |

Explain snippets (top raw-drift docs):

**doc id 18**

- Solr5 explain (prefix): `
1.3582714 = product of:
  1.6299256 = sum of:
    0.0550577 = max of:
      0.0550577 = weight(body:fast in 17) [ClassicSimilarity], result of:
        0.0550577 = score(doc=17,freq=1.0), product of:
          0.16615896 = queryWeight, product of:
            2.0 = boost
            1.3254224 = idf(docFreq=12, maxDocs=18)
            0.06268151 = queryNorm
          0.3313556 = fieldWeight in 17,`
- Solr8 explain (prefix): `
12.509465 = sum of:
  0.7123654 = max of:
    0.7123654 = weight(body:fast in 17) [ClassicSimilarity], result of:
      0.7123654 = score(freq=1.0), product of:
        2.0 = boost
        1.3794897 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          12 = docFreq, number of documents containing term
          18 = docCount, total number of documents with field
        1.0 = tf(fr`

**doc id 2**

- Solr5 explain (prefix): `
1.4540174 = sum of:
  0.049072973 = max of:
    0.049072973 = weight(body:iphone in 1) [ClassicSimilarity], result of:
      0.049072973 = score(doc=1,freq=1.0), product of:
        0.15686856 = queryWeight, product of:
          2.0 = boost
          1.2513144 = idf(docFreq=13, maxDocs=18)
          0.06268151 = queryNorm
        0.3128286 = fieldWeight in 1, product of:
          1.0 = tf(freq=`
- Solr8 explain (prefix): `
12.155692 = sum of:
  0.67409617 = max of:
    0.67409617 = weight(body:iphone in 1) [ClassicSimilarity], result of:
      0.67409617 = score(freq=1.0), product of:
        2.0 = boost
        1.3053817 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          13 = docFreq, number of documents containing term
          18 = docCount, total number of documents with field
        1.0 = t`

