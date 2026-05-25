# SOLR8 vs SOLR9 Drift Report

- SOLR8: `http://localhost:8988/solr/core1`
- SOLR9: `http://localhost:8989/solr/core1`

Thresholds:
- MAX_AVG_ABS_RANK_DELTA=1.0
- MAX_MAX_ABS_RANK_DELTA=4
- MAX_MAX_ABS_NORM_DRIFT=0.15

## q_basic — PASS ✅
- Jaccard(top10): **1.000**
- Avg abs rank delta: **0.00** (max: 0, changes: 0)
- Top score (SOLR8/SOLR9): **4.578894 / 4.578894**
- Max abs normalized drift: **0.000**
- Only in SOLR8 top10: []
- Only in SOLR9 top10: []

Top movers:

| id | rank_solr8 | rank_solr9 | delta |
|---|---:|---:|---:|
| 10 | 1 | 1 | 0 |
| 3 | 2 | 2 | 0 |
| 4 | 3 | 3 | 0 |
| 1 | 4 | 4 | 0 |
| 8 | 5 | 5 | 0 |

Top score drifts (raw, abs):

| id | score_solr8 | score_solr9 | abs | rel |
|---|---:|---:|---:|---:|
| 10 | 4.578894 | 4.578894 | 0.000000 | 0.000 |
| 3 | 4.578894 | 4.578894 | 0.000000 | 0.000 |
| 4 | 4.578894 | 4.578894 | 0.000000 | 0.000 |
| 1 | 4.095487 | 4.095487 | 0.000000 | 0.000 |
| 8 | 4.095487 | 4.095487 | 0.000000 | 0.000 |

Top score drifts (normalized by top1, abs):

| id | norm_solr8 | norm_solr9 | abs | rel |
|---|---:|---:|---:|---:|
| 10 | 1.000000 | 1.000000 | 0.000000 | 0.000 |
| 3 | 1.000000 | 1.000000 | 0.000000 | 0.000 |
| 4 | 1.000000 | 1.000000 | 0.000000 | 0.000 |
| 1 | 0.894427 | 0.894427 | 0.000000 | 0.000 |
| 8 | 0.894427 | 0.894427 | 0.000000 | 0.000 |

Explain snippets (top raw-drift docs):

**doc id 10**

- SOLR8 explain: `
4.578894 = sum of:
  2.6208217 = max of:
    2.6208217 = weight(title:iphone in 9) [ClassicSimilarity], result of:
      2.6208217 = score(freq=1.0), product of:
        3.0 = boost
        1.7472144 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          8 = docFreq, number of documents containing term
          18 = docCount, total number of documents with field
        1.0 = tf(fr`
- SOLR9 explain: `
4.578894 = sum of:
  2.6208217 = max of:
    1.1132332 = weight(body:iphone in 9) [ClassicSimilarity], result of:
      1.1132332 = score(freq=2.0), product of:
        2.0 = boost
        1.3053817 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          13 = docFreq, number of documents containing term
          18 = docCount, total number of documents with field
        1.4142135 =`

**doc id 3**

- SOLR8 explain: `
4.578894 = sum of:
  2.6208217 = max of:
    2.6208217 = weight(title:iphone in 2) [ClassicSimilarity], result of:
      2.6208217 = score(freq=1.0), product of:
        3.0 = boost
        1.7472144 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          8 = docFreq, number of documents containing term
          18 = docCount, total number of documents with field
        1.0 = tf(fr`
- SOLR9 explain: `
4.578894 = sum of:
  2.6208217 = max of:
    1.0658396 = weight(body:iphone in 2) [ClassicSimilarity], result of:
      1.0658396 = score(freq=2.0), product of:
        2.0 = boost
        1.3053817 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          13 = docFreq, number of documents containing term
          18 = docCount, total number of documents with field
        1.4142135 =`

## q_phrase — PASS ✅
- Jaccard(top10): **1.000**
- Avg abs rank delta: **0.00** (max: 0, changes: 0)
- Top score (SOLR8/SOLR9): **5.795289 / 5.795289**
- Max abs normalized drift: **0.000**
- Only in SOLR8 top10: []
- Only in SOLR9 top10: []

Top movers:

| id | rank_solr8 | rank_solr9 | delta |
|---|---:|---:|---:|
| 3 | 1 | 1 | 0 |
| 5 | 2 | 2 | 0 |
| 7 | 3 | 3 | 0 |
| 9 | 4 | 4 | 0 |
| 12 | 5 | 5 | 0 |

Top score drifts (raw, abs):

| id | score_solr8 | score_solr9 | abs | rel |
|---|---:|---:|---:|---:|
| 3 | 5.795289 | 5.795289 | 0.000000 | 0.000 |
| 5 | 5.795289 | 5.795289 | 0.000000 | 0.000 |
| 7 | 5.795289 | 5.795289 | 0.000000 | 0.000 |
| 9 | 1.415229 | 1.415229 | 0.000000 | 0.000 |
| 12 | 1.363749 | 1.363749 | 0.000000 | 0.000 |

Top score drifts (normalized by top1, abs):

| id | norm_solr8 | norm_solr9 | abs | rel |
|---|---:|---:|---:|---:|
| 3 | 1.000000 | 1.000000 | 0.000000 | 0.000 |
| 5 | 1.000000 | 1.000000 | 0.000000 | 0.000 |
| 7 | 1.000000 | 1.000000 | 0.000000 | 0.000 |
| 9 | 0.244203 | 0.244203 | 0.000000 | 0.000 |
| 12 | 0.235320 | 0.235320 | 0.000000 | 0.000 |

Explain snippets (top raw-drift docs):

**doc id 3**

- SOLR8 explain: `
5.7952895 = sum of:
  5.7952895 = max of:
    5.7952895 = weight(title:"fast charger" in 2) [ClassicSimilarity], result of:
      5.7952895 = score(freq=1.0), product of:
        3.0 = boost
        3.8635263 = idf(), sum of:
          2.5581446 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
            3 = docFreq, number of documents containing term
            18 = docCount, total `
- SOLR9 explain: `
5.7952895 = max of:
  5.7952895 = weight(title:"fast charger" in 2) [ClassicSimilarity], result of:
    5.7952895 = score(freq=1.0), product of:
      3.0 = boost
      3.8635263 = idf(), sum of:
        2.5581446 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          3 = docFreq, number of documents containing term
          18 = docCount, total number of documents with field
     `

**doc id 5**

- SOLR8 explain: `
5.7952895 = sum of:
  5.7952895 = max of:
    5.7952895 = weight(title:"fast charger" in 4) [ClassicSimilarity], result of:
      5.7952895 = score(freq=1.0), product of:
        3.0 = boost
        3.8635263 = idf(), sum of:
          2.5581446 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
            3 = docFreq, number of documents containing term
            18 = docCount, total `
- SOLR9 explain: `
5.7952895 = max of:
  5.7952895 = weight(title:"fast charger" in 4) [ClassicSimilarity], result of:
    5.7952895 = score(freq=1.0), product of:
      3.0 = boost
      3.8635263 = idf(), sum of:
        2.5581446 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          3 = docFreq, number of documents containing term
          18 = docCount, total number of documents with field
     `

## q_phrase_freq — PASS ✅
- Jaccard(top10): **1.000**
- Avg abs rank delta: **0.00** (max: 0, changes: 0)
- Top score (SOLR8/SOLR9): **8.416111 / 8.416111**
- Max abs normalized drift: **0.000**
- Only in SOLR8 top10: []
- Only in SOLR9 top10: []

Top movers:

| id | rank_solr8 | rank_solr9 | delta |
|---|---:|---:|---:|
| 3 | 1 | 1 | 0 |
| 7 | 2 | 2 | 0 |
| 5 | 3 | 3 | 0 |
| 9 | 4 | 4 | 0 |
| 16 | 5 | 5 | 0 |

Top score drifts (raw, abs):

| id | score_solr8 | score_solr9 | abs | rel |
|---|---:|---:|---:|---:|
| 3 | 8.416111 | 8.416111 | 0.000000 | 0.000 |
| 7 | 6.718334 | 6.718334 | 0.000000 | 0.000 |
| 5 | 5.795289 | 5.795289 | 0.000000 | 0.000 |
| 9 | 3.759363 | 3.759363 | 0.000000 | 0.000 |
| 16 | 3.706402 | 3.706402 | 0.000000 | 0.000 |

Top score drifts (normalized by top1, abs):

| id | norm_solr8 | norm_solr9 | abs | rel |
|---|---:|---:|---:|---:|
| 3 | 1.000000 | 1.000000 | 0.000000 | 0.000 |
| 7 | 0.798271 | 0.798271 | 0.000000 | 0.000 |
| 5 | 0.688595 | 0.688595 | 0.000000 | 0.000 |
| 9 | 0.446686 | 0.446686 | 0.000000 | 0.000 |
| 16 | 0.440394 | 0.440394 | 0.000000 | 0.000 |

Explain snippets (top raw-drift docs):

**doc id 3**

- SOLR8 explain: `
8.416111 = sum of:
  8.416111 = sum of:
    5.7952895 = max of:
      5.7952895 = weight(title:"fast charger" in 2) [ClassicSimilarity], result of:
        5.7952895 = score(freq=1.0), product of:
          3.0 = boost
          3.8635263 = idf(), sum of:
            2.5581446 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
              3 = docFreq, number of documents containing term`
- SOLR9 explain: `
8.416111 = sum of:
  5.7952895 = max of:
    5.7952895 = weight(title:"fast charger" in 2) [ClassicSimilarity], result of:
      5.7952895 = score(freq=1.0), product of:
        3.0 = boost
        3.8635263 = idf(), sum of:
          2.5581446 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
            3 = docFreq, number of documents containing term
            18 = docCount, total n`

**doc id 7**

- SOLR8 explain: `
6.7183337 = sum of:
  6.7183337 = sum of:
    5.7952895 = max of:
      5.7952895 = weight(title:"fast charger" in 6) [ClassicSimilarity], result of:
        5.7952895 = score(freq=1.0), product of:
          3.0 = boost
          3.8635263 = idf(), sum of:
            2.5581446 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
              3 = docFreq, number of documents containing te`
- SOLR9 explain: `
6.7183337 = sum of:
  5.7952895 = max of:
    5.7952895 = weight(title:"fast charger" in 6) [ClassicSimilarity], result of:
      5.7952895 = score(freq=1.0), product of:
        3.0 = boost
        3.8635263 = idf(), sum of:
          2.5581446 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
            3 = docFreq, number of documents containing term
            18 = docCount, total `

## q_usb_c — PASS ✅
- Jaccard(top10): **1.000**
- Avg abs rank delta: **0.00** (max: 0, changes: 0)
- Top score (SOLR8/SOLR9): **9.730376 / 9.730376**
- Max abs normalized drift: **0.000**
- Only in SOLR8 top10: []
- Only in SOLR9 top10: []

Top movers:

| id | rank_solr8 | rank_solr9 | delta |
|---|---:|---:|---:|
| 1 | 1 | 1 | 0 |
| 12 | 2 | 2 | 0 |
| 18 | 3 | 3 | 0 |
| 2 | 4 | 4 | 0 |
| 14 | 5 | 5 | 0 |

Top score drifts (raw, abs):

| id | score_solr8 | score_solr9 | abs | rel |
|---|---:|---:|---:|---:|
| 1 | 9.730376 | 9.730376 | 0.000000 | 0.000 |
| 12 | 9.730376 | 9.730376 | 0.000000 | 0.000 |
| 18 | 9.150873 | 9.150873 | 0.000000 | 0.000 |
| 2 | 8.455669 | 8.455669 | 0.000000 | 0.000 |
| 14 | 6.597644 | 6.597644 | 0.000000 | 0.000 |

Top score drifts (normalized by top1, abs):

| id | norm_solr8 | norm_solr9 | abs | rel |
|---|---:|---:|---:|---:|
| 1 | 1.000000 | 1.000000 | 0.000000 | 0.000 |
| 12 | 1.000000 | 1.000000 | 0.000000 | 0.000 |
| 18 | 0.940444 | 0.940444 | 0.000000 | 0.000 |
| 2 | 0.868997 | 0.868997 | 0.000000 | 0.000 |
| 14 | 0.678046 | 0.678046 | 0.000000 | 0.000 |

Explain snippets (top raw-drift docs):

**doc id 1**

- SOLR8 explain: `
9.730376 = sum of:
  2.344134 = max of:
    2.344134 = weight(title:usb in 0) [ClassicSimilarity], result of:
      2.344134 = score(freq=1.0), product of:
        3.0 = boost
        1.7472144 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          8 = docFreq, number of documents containing term
          18 = docCount, total number of documents with field
        1.0 = tf(freq=1.0`
- SOLR9 explain: `
9.730376 = sum of:
  2.344134 = max of:
    0.8742589 = weight(body:usb in 0) [ClassicSimilarity], result of:
      0.8742589 = score(freq=2.0), product of:
        2.0 = boost
        1.2363888 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          14 = docFreq, number of documents containing term
          18 = docCount, total number of documents with field
        1.4142135 = tf(`

**doc id 12**

- SOLR8 explain: `
9.730376 = sum of:
  2.344134 = max of:
    2.344134 = weight(title:usb in 11) [ClassicSimilarity], result of:
      2.344134 = score(freq=1.0), product of:
        3.0 = boost
        1.7472144 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          8 = docFreq, number of documents containing term
          18 = docCount, total number of documents with field
        1.0 = tf(freq=1.`
- SOLR9 explain: `
9.730376 = sum of:
  2.344134 = max of:
    0.93462205 = weight(body:usb in 11) [ClassicSimilarity], result of:
      0.93462205 = score(freq=2.0), product of:
        2.0 = boost
        1.2363888 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          14 = docFreq, number of documents containing term
          18 = docCount, total number of documents with field
        1.4142135 = `

## q_filter_instock — PASS ✅
- Jaccard(top10): **1.000**
- Avg abs rank delta: **0.00** (max: 0, changes: 0)
- Top score (SOLR8/SOLR9): **4.578894 / 4.578894**
- Max abs normalized drift: **0.000**
- Only in SOLR8 top10: []
- Only in SOLR9 top10: []

Top movers:

| id | rank_solr8 | rank_solr9 | delta |
|---|---:|---:|---:|
| 10 | 1 | 1 | 0 |
| 3 | 2 | 2 | 0 |
| 4 | 3 | 3 | 0 |
| 1 | 4 | 4 | 0 |
| 8 | 5 | 5 | 0 |

Top score drifts (raw, abs):

| id | score_solr8 | score_solr9 | abs | rel |
|---|---:|---:|---:|---:|
| 10 | 4.578894 | 4.578894 | 0.000000 | 0.000 |
| 3 | 4.578894 | 4.578894 | 0.000000 | 0.000 |
| 4 | 4.578894 | 4.578894 | 0.000000 | 0.000 |
| 1 | 4.095487 | 4.095487 | 0.000000 | 0.000 |
| 8 | 4.095487 | 4.095487 | 0.000000 | 0.000 |

Top score drifts (normalized by top1, abs):

| id | norm_solr8 | norm_solr9 | abs | rel |
|---|---:|---:|---:|---:|
| 10 | 1.000000 | 1.000000 | 0.000000 | 0.000 |
| 3 | 1.000000 | 1.000000 | 0.000000 | 0.000 |
| 4 | 1.000000 | 1.000000 | 0.000000 | 0.000 |
| 1 | 0.894427 | 0.894427 | 0.000000 | 0.000 |
| 8 | 0.894427 | 0.894427 | 0.000000 | 0.000 |

Explain snippets (top raw-drift docs):

**doc id 10**

- SOLR8 explain: `
4.578894 = sum of:
  2.6208217 = max of:
    2.6208217 = weight(title:iphone in 9) [ClassicSimilarity], result of:
      2.6208217 = score(freq=1.0), product of:
        3.0 = boost
        1.7472144 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          8 = docFreq, number of documents containing term
          18 = docCount, total number of documents with field
        1.0 = tf(fr`
- SOLR9 explain: `
4.578894 = sum of:
  2.6208217 = max of:
    1.1132332 = weight(body:iphone in 9) [ClassicSimilarity], result of:
      1.1132332 = score(freq=2.0), product of:
        2.0 = boost
        1.3053817 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          13 = docFreq, number of documents containing term
          18 = docCount, total number of documents with field
        1.4142135 =`

**doc id 3**

- SOLR8 explain: `
4.578894 = sum of:
  2.6208217 = max of:
    2.6208217 = weight(title:iphone in 2) [ClassicSimilarity], result of:
      2.6208217 = score(freq=1.0), product of:
        3.0 = boost
        1.7472144 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          8 = docFreq, number of documents containing term
          18 = docCount, total number of documents with field
        1.0 = tf(fr`
- SOLR9 explain: `
4.578894 = sum of:
  2.6208217 = max of:
    1.0658396 = weight(body:iphone in 2) [ClassicSimilarity], result of:
      1.0658396 = score(freq=2.0), product of:
        2.0 = boost
        1.3053817 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          13 = docFreq, number of documents containing term
          18 = docCount, total number of documents with field
        1.4142135 =`

## q_filter_price_range — PASS ✅
- Jaccard(top10): **1.000**
- Avg abs rank delta: **0.00** (max: 0, changes: 0)
- Top score (SOLR8/SOLR9): **4.578894 / 4.578894**
- Max abs normalized drift: **0.000**
- Only in SOLR8 top10: []
- Only in SOLR9 top10: []

Top movers:

| id | rank_solr8 | rank_solr9 | delta |
|---|---:|---:|---:|
| 3 | 1 | 1 | 0 |
| 1 | 2 | 2 | 0 |
| 8 | 3 | 3 | 0 |
| 9 | 4 | 4 | 0 |
| 16 | 5 | 5 | 0 |

Top score drifts (raw, abs):

| id | score_solr8 | score_solr9 | abs | rel |
|---|---:|---:|---:|---:|
| 3 | 4.578894 | 4.578894 | 0.000000 | 0.000 |
| 1 | 4.095487 | 4.095487 | 0.000000 | 0.000 |
| 8 | 4.095487 | 4.095487 | 0.000000 | 0.000 |
| 9 | 4.095487 | 4.095487 | 0.000000 | 0.000 |
| 16 | 3.706402 | 3.706402 | 0.000000 | 0.000 |

Top score drifts (normalized by top1, abs):

| id | norm_solr8 | norm_solr9 | abs | rel |
|---|---:|---:|---:|---:|
| 3 | 1.000000 | 1.000000 | 0.000000 | 0.000 |
| 1 | 0.894427 | 0.894427 | 0.000000 | 0.000 |
| 8 | 0.894427 | 0.894427 | 0.000000 | 0.000 |
| 9 | 0.894427 | 0.894427 | 0.000000 | 0.000 |
| 16 | 0.809453 | 0.809453 | 0.000000 | 0.000 |

Explain snippets (top raw-drift docs):

**doc id 3**

- SOLR8 explain: `
4.578894 = sum of:
  2.6208217 = max of:
    2.6208217 = weight(title:iphone in 2) [ClassicSimilarity], result of:
      2.6208217 = score(freq=1.0), product of:
        3.0 = boost
        1.7472144 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          8 = docFreq, number of documents containing term
          18 = docCount, total number of documents with field
        1.0 = tf(fr`
- SOLR9 explain: `
4.578894 = sum of:
  2.6208217 = max of:
    1.0658396 = weight(body:iphone in 2) [ClassicSimilarity], result of:
      1.0658396 = score(freq=2.0), product of:
        2.0 = boost
        1.3053817 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          13 = docFreq, number of documents containing term
          18 = docCount, total number of documents with field
        1.4142135 =`

**doc id 1**

- SOLR8 explain: `
4.095487 = sum of:
  2.344134 = max of:
    2.344134 = weight(title:iphone in 0) [ClassicSimilarity], result of:
      2.344134 = score(freq=1.0), product of:
        3.0 = boost
        1.7472144 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          8 = docFreq, number of documents containing term
          18 = docCount, total number of documents with field
        1.0 = tf(freq=`
- SOLR9 explain: `
4.095487 = sum of:
  2.344134 = max of:
    0.9230442 = weight(body:iphone in 0) [ClassicSimilarity], result of:
      0.9230442 = score(freq=2.0), product of:
        2.0 = boost
        1.3053817 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          13 = docFreq, number of documents containing term
          18 = docCount, total number of documents with field
        1.4142135 = `

## q_brand_anker — PASS ✅
- Jaccard(top10): **1.000**
- Avg abs rank delta: **0.00** (max: 0, changes: 0)
- Top score (SOLR8/SOLR9): **4.095487 / 4.095487**
- Max abs normalized drift: **0.000**
- Only in SOLR8 top10: []
- Only in SOLR9 top10: []

Top movers:

| id | rank_solr8 | rank_solr9 | delta |
|---|---:|---:|---:|
| 1 | 1 | 1 | 0 |
| 9 | 2 | 2 | 0 |
| 11 | 3 | 3 | 0 |
| 7 | 4 | 4 | 0 |
| 5 | 5 | 5 | 0 |

Top score drifts (raw, abs):

| id | score_solr8 | score_solr9 | abs | rel |
|---|---:|---:|---:|---:|
| 1 | 4.095487 | 4.095487 | 0.000000 | 0.000 |
| 9 | 4.095487 | 4.095487 | 0.000000 | 0.000 |
| 11 | 3.566369 | 3.566369 | 0.000000 | 0.000 |
| 7 | 3.263454 | 3.263454 | 0.000000 | 0.000 |
| 5 | 1.958072 | 1.958072 | 0.000000 | 0.000 |

Top score drifts (normalized by top1, abs):

| id | norm_solr8 | norm_solr9 | abs | rel |
|---|---:|---:|---:|---:|
| 1 | 1.000000 | 1.000000 | 0.000000 | 0.000 |
| 9 | 1.000000 | 1.000000 | 0.000000 | 0.000 |
| 11 | 0.870805 | 0.870805 | 0.000000 | 0.000 |
| 7 | 0.796841 | 0.796841 | 0.000000 | 0.000 |
| 5 | 0.478105 | 0.478105 | 0.000000 | 0.000 |

Explain snippets (top raw-drift docs):

**doc id 1**

- SOLR8 explain: `
4.095487 = sum of:
  2.344134 = max of:
    2.344134 = weight(title:iphone in 0) [ClassicSimilarity], result of:
      2.344134 = score(freq=1.0), product of:
        3.0 = boost
        1.7472144 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          8 = docFreq, number of documents containing term
          18 = docCount, total number of documents with field
        1.0 = tf(freq=`
- SOLR9 explain: `
4.095487 = sum of:
  2.344134 = max of:
    0.9230442 = weight(body:iphone in 0) [ClassicSimilarity], result of:
      0.9230442 = score(freq=2.0), product of:
        2.0 = boost
        1.3053817 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          13 = docFreq, number of documents containing term
          18 = docCount, total number of documents with field
        1.4142135 = `

**doc id 9**

- SOLR8 explain: `
4.095487 = sum of:
  2.344134 = max of:
    2.344134 = weight(title:iphone in 8) [ClassicSimilarity], result of:
      2.344134 = score(freq=1.0), product of:
        3.0 = boost
        1.7472144 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          8 = docFreq, number of documents containing term
          18 = docCount, total number of documents with field
        1.0 = tf(freq=`
- SOLR9 explain: `
4.095487 = sum of:
  2.344134 = max of:
    1.0240256 = weight(body:iphone in 8) [ClassicSimilarity], result of:
      1.0240256 = score(freq=2.0), product of:
        2.0 = boost
        1.3053817 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          13 = docFreq, number of documents containing term
          18 = docCount, total number of documents with field
        1.4142135 = `

## q_near_tie_stress — PASS ✅
- Jaccard(top10): **1.000**
- Avg abs rank delta: **0.00** (max: 0, changes: 0)
- Top score (SOLR8/SOLR9): **12.509465 / 12.509465**
- Max abs normalized drift: **0.000**
- Only in SOLR8 top10: []
- Only in SOLR9 top10: []

Top movers:

| id | rank_solr8 | rank_solr9 | delta |
|---|---:|---:|---:|
| 18 | 1 | 1 | 0 |
| 2 | 2 | 2 | 0 |
| 1 | 3 | 3 | 0 |
| 3 | 4 | 4 | 0 |
| 12 | 5 | 5 | 0 |

Top score drifts (raw, abs):

| id | score_solr8 | score_solr9 | abs | rel |
|---|---:|---:|---:|---:|
| 18 | 12.509465 | 12.509465 | 0.000000 | 0.000 |
| 2 | 12.155692 | 12.155692 | 0.000000 | 0.000 |
| 1 | 11.833829 | 11.833829 | 0.000000 | 0.000 |
| 3 | 9.924996 | 9.924996 | 0.000000 | 0.000 |
| 12 | 9.414147 | 9.414147 | 0.000000 | 0.000 |

Top score drifts (normalized by top1, abs):

| id | norm_solr8 | norm_solr9 | abs | rel |
|---|---:|---:|---:|---:|
| 18 | 1.000000 | 1.000000 | 0.000000 | 0.000 |
| 2 | 0.971720 | 0.971720 | 0.000000 | 0.000 |
| 1 | 0.945990 | 0.945990 | 0.000000 | 0.000 |
| 3 | 0.793399 | 0.793399 | 0.000000 | 0.000 |
| 12 | 0.752562 | 0.752562 | 0.000000 | 0.000 |

Explain snippets (top raw-drift docs):

**doc id 18**

- SOLR8 explain: `
12.509465 = sum of:
  0.7123654 = max of:
    0.7123654 = weight(body:fast in 17) [ClassicSimilarity], result of:
      0.7123654 = score(freq=1.0), product of:
        2.0 = boost
        1.3794897 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          12 = docFreq, number of documents containing term
          18 = docCount, total number of documents with field
        1.0 = tf(fr`
- SOLR9 explain: `
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

- SOLR8 explain: `
12.155692 = sum of:
  0.67409617 = max of:
    0.67409617 = weight(body:iphone in 1) [ClassicSimilarity], result of:
      0.67409617 = score(freq=1.0), product of:
        2.0 = boost
        1.3053817 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          13 = docFreq, number of documents containing term
          18 = docCount, total number of documents with field
        1.0 = t`
- SOLR9 explain: `
12.155692 = sum of:
  0.67409617 = max of:
    0.67409617 = weight(body:iphone in 1) [ClassicSimilarity], result of:
      0.67409617 = score(freq=1.0), product of:
        2.0 = boost
        1.3053817 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          13 = docFreq, number of documents containing term
          18 = docCount, total number of documents with field
        1.0 = t`

