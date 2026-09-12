# SOLR9 vs SOLR10 Drift Report

- SOLR9: `http://localhost:8989/solr/core1`
- SOLR10: `http://localhost:8990/solr/core1`

Thresholds:
- MAX_AVG_ABS_RANK_DELTA=1.0
- MAX_MAX_ABS_RANK_DELTA=4
- MAX_MAX_ABS_NORM_DRIFT=0.15

> **RBO** (Rank-Biased Overlap, p=0.90) measures top-weighted ranked-list agreement. Unlike Jaccard, which only measures set overlap, RBO penalizes changes near the top of the result list more heavily than changes near the bottom. A value of 1.0 means identical ranking.

> **Explain output is normalized**: the child clauses of each explain node are sorted by (value, description) before display. Lucene may list DisjunctionMax/Boolean clauses in a different order across major versions; that re-ordering is cosmetic and is not reported as drift.

## q_basic — PASS ✅
- Jaccard(top10): **1.000**
- RBO(p=0.9): **1.0000**
- Avg abs rank delta: **0.00** (max: 0, changes: 0)
- Top score (SOLR9/SOLR10): **4.578894 / 4.578894**
- Max abs normalized drift: **0.000**
- Only in SOLR9 top10: []
- Only in SOLR10 top10: []

Top movers:

| id | rank_solr9 | rank_solr10 | delta |
|---|---:|---:|---:|
| 10 | 1 | 1 | 0 |
| 3 | 2 | 2 | 0 |
| 4 | 3 | 3 | 0 |
| 1 | 4 | 4 | 0 |
| 8 | 5 | 5 | 0 |

Top score drifts (raw, abs):

| id | score_solr9 | score_solr10 | abs | rel |
|---|---:|---:|---:|---:|
| 9 | 4.095487 | 4.095487 | 0.000000 | 0.000 |
| 8 | 4.095487 | 4.095487 | 0.000000 | 0.000 |
| 7 | 3.263454 | 3.263454 | 0.000000 | 0.000 |
| 4 | 4.578894 | 4.578894 | 0.000000 | 0.000 |
| 3 | 4.578894 | 4.578894 | 0.000000 | 0.000 |

Top score drifts (normalized by top1, abs):

| id | norm_solr9 | norm_solr10 | abs | rel |
|---|---:|---:|---:|---:|
| 9 | 0.894427 | 0.894427 | 0.000000 | 0.000 |
| 8 | 0.894427 | 0.894427 | 0.000000 | 0.000 |
| 7 | 0.712717 | 0.712717 | 0.000000 | 0.000 |
| 4 | 1.000000 | 1.000000 | 0.000000 | 0.000 |
| 3 | 1.000000 | 1.000000 | 0.000000 | 0.000 |

Explain snippets (top raw-drift docs, normalized):

**doc id 9**

- SOLR9 explain: `4.095487 = sum of:
  1.7513531 = max of:
    0.9192749 = weight(body:charger in 8) [ClassicSimilarity], result of:
      0.9192749 = score(freq=2.0), product of:
        0.2773501 = fieldNorm
        1.1718502 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          15 = docFreq, number of documents containing term
          18 = docCount, total number of documents with field
        1`
- SOLR10 explain: `4.095487 = sum of:
  1.7513531 = max of:
    0.9192749 = weight(body:charger in 8) [ClassicSimilarity], result of:
      0.9192749 = score(freq=2.0), product of:
        0.2773501 = fieldNorm
        1.1718502 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          15 = docFreq, number of documents containing term
          18 = docCount, total number of documents with field
        1`

**doc id 8**

- SOLR9 explain: `4.095487 = sum of:
  1.7513531 = max of:
    0.56025153 = weight(body:charger in 7) [ClassicSimilarity], result of:
      0.56025153 = score(freq=2.0), product of:
        0.16903085 = fieldNorm
        1.1718502 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          15 = docFreq, number of documents containing term
          18 = docCount, total number of documents with field
      `
- SOLR10 explain: `4.095487 = sum of:
  1.7513531 = max of:
    0.56025153 = weight(body:charger in 7) [ClassicSimilarity], result of:
      0.56025153 = score(freq=2.0), product of:
        0.16903085 = fieldNorm
        1.1718502 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          15 = docFreq, number of documents containing term
          18 = docCount, total number of documents with field
      `

## q_phrase — PASS ✅
- Jaccard(top10): **1.000**
- RBO(p=0.9): **1.0000**
- Avg abs rank delta: **0.00** (max: 0, changes: 0)
- Top score (SOLR9/SOLR10): **5.795289 / 5.795289**
- Max abs normalized drift: **0.000**
- Only in SOLR9 top10: []
- Only in SOLR10 top10: []

Top movers:

| id | rank_solr9 | rank_solr10 | delta |
|---|---:|---:|---:|
| 3 | 1 | 1 | 0 |
| 5 | 2 | 2 | 0 |
| 7 | 3 | 3 | 0 |
| 9 | 4 | 4 | 0 |
| 12 | 5 | 5 | 0 |

Top score drifts (raw, abs):

| id | score_solr9 | score_solr10 | abs | rel |
|---|---:|---:|---:|---:|
| 9 | 1.415229 | 1.415229 | 0.000000 | 0.000 |
| 8 | 0.862510 | 0.862510 | 0.000000 | 0.000 |
| 7 | 5.795289 | 5.795289 | 0.000000 | 0.000 |
| 5 | 5.795289 | 5.795289 | 0.000000 | 0.000 |
| 3 | 5.795289 | 5.795289 | 0.000000 | 0.000 |

Top score drifts (normalized by top1, abs):

| id | norm_solr9 | norm_solr10 | abs | rel |
|---|---:|---:|---:|---:|
| 9 | 0.244203 | 0.244203 | 0.000000 | 0.000 |
| 8 | 0.148830 | 0.148830 | 0.000000 | 0.000 |
| 7 | 1.000000 | 1.000000 | 0.000000 | 0.000 |
| 5 | 1.000000 | 1.000000 | 0.000000 | 0.000 |
| 3 | 1.000000 | 1.000000 | 0.000000 | 0.000 |

Explain snippets (top raw-drift docs, normalized):

**doc id 9**

- SOLR9 explain: `1.4152287 = max of:
  1.4152287 = weight(body:"fast charger" in 8) [ClassicSimilarity], result of:
    1.4152287 = score(freq=1.0), product of:
      0.2773501 = fieldNorm
      1.0 = tf(freq=1.0), with freq of:
        1.0 = phraseFreq=1.0
      2.0 = boost
      2.5513399 = idf(), sum of:
        1.1718502 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          15 = docFreq, number `
- SOLR10 explain: `1.4152287 = max of:
  1.4152287 = weight(body:"fast charger" in 8) [ClassicSimilarity], result of:
    1.4152287 = score(freq=1.0), product of:
      0.2773501 = fieldNorm
      1.0 = tf(freq=1.0), with freq of:
        1.0 = phraseFreq=1.0
      2.0 = boost
      2.5513399 = idf(), sum of:
        1.1718502 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          15 = docFreq, number `

**doc id 8**

- SOLR9 explain: `0.86251026 = max of:
  0.86251026 = weight(body:"fast charger" in 7) [ClassicSimilarity], result of:
    0.86251026 = score(freq=1.0), product of:
      0.16903085 = fieldNorm
      1.0 = tf(freq=1.0), with freq of:
        1.0 = phraseFreq=1.0
      2.0 = boost
      2.5513399 = idf(), sum of:
        1.1718502 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          15 = docFreq, num`
- SOLR10 explain: `0.86251026 = max of:
  0.86251026 = weight(body:"fast charger" in 7) [ClassicSimilarity], result of:
    0.86251026 = score(freq=1.0), product of:
      0.16903085 = fieldNorm
      1.0 = tf(freq=1.0), with freq of:
        1.0 = phraseFreq=1.0
      2.0 = boost
      2.5513399 = idf(), sum of:
        1.1718502 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          15 = docFreq, num`

## q_phrase_freq — PASS ✅
- Jaccard(top10): **1.000**
- RBO(p=0.9): **1.0000**
- Avg abs rank delta: **0.00** (max: 0, changes: 0)
- Top score (SOLR9/SOLR10): **8.416111 / 8.416111**
- Max abs normalized drift: **0.000**
- Only in SOLR9 top10: []
- Only in SOLR10 top10: []

Top movers:

| id | rank_solr9 | rank_solr10 | delta |
|---|---:|---:|---:|
| 3 | 1 | 1 | 0 |
| 7 | 2 | 2 | 0 |
| 5 | 3 | 3 | 0 |
| 9 | 4 | 4 | 0 |
| 16 | 5 | 5 | 0 |

Top score drifts (raw, abs):

| id | score_solr9 | score_solr10 | abs | rel |
|---|---:|---:|---:|---:|
| 9 | 3.759363 | 3.759363 | 0.000000 | 0.000 |
| 8 | 3.206644 | 3.206644 | 0.000000 | 0.000 |
| 7 | 6.718334 | 6.718334 | 0.000000 | 0.000 |
| 5 | 5.795289 | 5.795289 | 0.000000 | 0.000 |
| 4 | 2.620822 | 2.620822 | 0.000000 | 0.000 |

Top score drifts (normalized by top1, abs):

| id | norm_solr9 | norm_solr10 | abs | rel |
|---|---:|---:|---:|---:|
| 9 | 0.446686 | 0.446686 | 0.000000 | 0.000 |
| 8 | 0.381013 | 0.381013 | 0.000000 | 0.000 |
| 7 | 0.798271 | 0.798271 | 0.000000 | 0.000 |
| 5 | 0.688595 | 0.688595 | 0.000000 | 0.000 |
| 4 | 0.311405 | 0.311405 | 0.000000 | 0.000 |

Explain snippets (top raw-drift docs, normalized):

**doc id 9**

- SOLR9 explain: `3.7593627 = sum of:
  1.4152287 = max of:
    1.4152287 = weight(body:"fast charger" in 8) [ClassicSimilarity], result of:
      1.4152287 = score(freq=1.0), product of:
        0.2773501 = fieldNorm
        1.0 = tf(freq=1.0), with freq of:
          1.0 = phraseFreq=1.0
        2.0 = boost
        2.5513399 = idf(), sum of:
          1.1718502 = idf, computed as log((docCount+1)/(docFreq+1)) + 1`
- SOLR10 explain: `3.7593627 = sum of:
  1.4152287 = max of:
    1.4152287 = weight(body:"fast charger" in 8) [ClassicSimilarity], result of:
      1.4152287 = score(freq=1.0), product of:
        0.2773501 = fieldNorm
        1.0 = tf(freq=1.0), with freq of:
          1.0 = phraseFreq=1.0
        2.0 = boost
        2.5513399 = idf(), sum of:
          1.1718502 = idf, computed as log((docCount+1)/(docFreq+1)) + 1`

**doc id 8**

- SOLR9 explain: `3.2066443 = sum of:
  0.86251026 = max of:
    0.86251026 = weight(body:"fast charger" in 7) [ClassicSimilarity], result of:
      0.86251026 = score(freq=1.0), product of:
        0.16903085 = fieldNorm
        1.0 = tf(freq=1.0), with freq of:
          1.0 = phraseFreq=1.0
        2.0 = boost
        2.5513399 = idf(), sum of:
          1.1718502 = idf, computed as log((docCount+1)/(docFreq+1))`
- SOLR10 explain: `3.2066443 = sum of:
  0.86251026 = max of:
    0.86251026 = weight(body:"fast charger" in 7) [ClassicSimilarity], result of:
      0.86251026 = score(freq=1.0), product of:
        0.16903085 = fieldNorm
        1.0 = tf(freq=1.0), with freq of:
          1.0 = phraseFreq=1.0
        2.0 = boost
        2.5513399 = idf(), sum of:
          1.1718502 = idf, computed as log((docCount+1)/(docFreq+1))`

## q_usb_c — PASS ✅
- Jaccard(top10): **1.000**
- RBO(p=0.9): **1.0000**
- Avg abs rank delta: **0.00** (max: 0, changes: 0)
- Top score (SOLR9/SOLR10): **9.730376 / 9.730376**
- Max abs normalized drift: **0.000**
- Only in SOLR9 top10: []
- Only in SOLR10 top10: []

Top movers:

| id | rank_solr9 | rank_solr10 | delta |
|---|---:|---:|---:|
| 1 | 1 | 1 | 0 |
| 12 | 2 | 2 | 0 |
| 18 | 3 | 3 | 0 |
| 2 | 4 | 4 | 0 |
| 14 | 5 | 5 | 0 |

Top score drifts (raw, abs):

| id | score_solr9 | score_solr10 | abs | rel |
|---|---:|---:|---:|---:|
| 9 | 4.171562 | 4.171562 | 0.000000 | 0.000 |
| 6 | 5.418318 | 5.418318 | 0.000000 | 0.000 |
| 3 | 4.477105 | 4.477105 | 0.000000 | 0.000 |
| 2 | 8.455669 | 8.455669 | 0.000000 | 0.000 |
| 18 | 9.150873 | 9.150873 | 0.000000 | 0.000 |

Top score drifts (normalized by top1, abs):

| id | norm_solr9 | norm_solr10 | abs | rel |
|---|---:|---:|---:|---:|
| 9 | 0.428715 | 0.428715 | 0.000000 | 0.000 |
| 6 | 0.556846 | 0.556846 | 0.000000 | 0.000 |
| 3 | 0.460116 | 0.460116 | 0.000000 | 0.000 |
| 2 | 0.868997 | 0.868997 | 0.000000 | 0.000 |
| 18 | 0.940444 | 0.940444 | 0.000000 | 0.000 |

Explain snippets (top raw-drift docs, normalized):

**doc id 9**

- SOLR9 explain: `4.1715617 = sum of:
  0.6858251 = max of:
    0.6858251 = weight(body:usb in 8) [ClassicSimilarity], result of:
      0.6858251 = score(freq=1.0), product of:
        0.2773501 = fieldNorm
        1.0 = tf(freq=1.0), with freq of:
          1.0 = freq, occurrences of term within document
        1.2363888 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          14 = docFreq, number of `
- SOLR10 explain: `4.1715617 = sum of:
  0.6858251 = max of:
    0.6858251 = weight(body:usb in 8) [ClassicSimilarity], result of:
      0.6858251 = score(freq=1.0), product of:
        0.2773501 = fieldNorm
        1.0 = tf(freq=1.0), with freq of:
          1.0 = freq, occurrences of term within document
        1.2363888 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          14 = docFreq, number of `

**doc id 6**

- SOLR9 explain: `5.418318 = sum of:
  2.6208217 = max of:
    0.9699031 = weight(body:usb in 5) [ClassicSimilarity], result of:
      0.9699031 = score(freq=2.0), product of:
        0.2773501 = fieldNorm
        1.2363888 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          14 = docFreq, number of documents containing term
          18 = docCount, total number of documents with field
        1.414`
- SOLR10 explain: `5.418318 = sum of:
  2.6208217 = max of:
    0.9699031 = weight(body:usb in 5) [ClassicSimilarity], result of:
      0.9699031 = score(freq=2.0), product of:
        0.2773501 = fieldNorm
        1.2363888 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          14 = docFreq, number of documents containing term
          18 = docCount, total number of documents with field
        1.414`

## q_filter_instock — PASS ✅
- Jaccard(top10): **1.000**
- RBO(p=0.9): **1.0000**
- Avg abs rank delta: **0.00** (max: 0, changes: 0)
- Top score (SOLR9/SOLR10): **4.578894 / 4.578894**
- Max abs normalized drift: **0.000**
- Only in SOLR9 top10: []
- Only in SOLR10 top10: []

Top movers:

| id | rank_solr9 | rank_solr10 | delta |
|---|---:|---:|---:|
| 10 | 1 | 1 | 0 |
| 3 | 2 | 2 | 0 |
| 4 | 3 | 3 | 0 |
| 1 | 4 | 4 | 0 |
| 8 | 5 | 5 | 0 |

Top score drifts (raw, abs):

| id | score_solr9 | score_solr10 | abs | rel |
|---|---:|---:|---:|---:|
| 8 | 4.095487 | 4.095487 | 0.000000 | 0.000 |
| 7 | 3.263454 | 3.263454 | 0.000000 | 0.000 |
| 4 | 4.578894 | 4.578894 | 0.000000 | 0.000 |
| 3 | 4.578894 | 4.578894 | 0.000000 | 0.000 |
| 16 | 3.706402 | 3.706402 | 0.000000 | 0.000 |

Top score drifts (normalized by top1, abs):

| id | norm_solr9 | norm_solr10 | abs | rel |
|---|---:|---:|---:|---:|
| 8 | 0.894427 | 0.894427 | 0.000000 | 0.000 |
| 7 | 0.712717 | 0.712717 | 0.000000 | 0.000 |
| 4 | 1.000000 | 1.000000 | 0.000000 | 0.000 |
| 3 | 1.000000 | 1.000000 | 0.000000 | 0.000 |
| 16 | 0.809453 | 0.809453 | 0.000000 | 0.000 |

Explain snippets (top raw-drift docs, normalized):

**doc id 8**

- SOLR9 explain: `4.095487 = sum of:
  1.7513531 = max of:
    0.56025153 = weight(body:charger in 7) [ClassicSimilarity], result of:
      0.56025153 = score(freq=2.0), product of:
        0.16903085 = fieldNorm
        1.1718502 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          15 = docFreq, number of documents containing term
          18 = docCount, total number of documents with field
      `
- SOLR10 explain: `4.095487 = sum of:
  1.7513531 = max of:
    0.56025153 = weight(body:charger in 7) [ClassicSimilarity], result of:
      0.56025153 = score(freq=2.0), product of:
        0.16903085 = fieldNorm
        1.1718502 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          15 = docFreq, number of documents containing term
          18 = docCount, total number of documents with field
      `

**doc id 7**

- SOLR9 explain: `3.263454 = sum of:
  1.3053817 = max of:
    0.9230442 = weight(body:iphone in 6) [ClassicSimilarity], result of:
      0.9230442 = score(freq=2.0), product of:
        0.25 = fieldNorm
        1.3053817 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          13 = docFreq, number of documents containing term
          18 = docCount, total number of documents with field
        1.41421`
- SOLR10 explain: `3.263454 = sum of:
  1.3053817 = max of:
    0.9230442 = weight(body:iphone in 6) [ClassicSimilarity], result of:
      0.9230442 = score(freq=2.0), product of:
        0.25 = fieldNorm
        1.3053817 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          13 = docFreq, number of documents containing term
          18 = docCount, total number of documents with field
        1.41421`

## q_filter_price_range — PASS ✅
- Jaccard(top10): **1.000**
- RBO(p=0.9): **1.0000**
- Avg abs rank delta: **0.00** (max: 0, changes: 0)
- Top score (SOLR9/SOLR10): **4.578894 / 4.578894**
- Max abs normalized drift: **0.000**
- Only in SOLR9 top10: []
- Only in SOLR10 top10: []

Top movers:

| id | rank_solr9 | rank_solr10 | delta |
|---|---:|---:|---:|
| 3 | 1 | 1 | 0 |
| 1 | 2 | 2 | 0 |
| 8 | 3 | 3 | 0 |
| 9 | 4 | 4 | 0 |
| 16 | 5 | 5 | 0 |

Top score drifts (raw, abs):

| id | score_solr9 | score_solr10 | abs | rel |
|---|---:|---:|---:|---:|
| 9 | 4.095487 | 4.095487 | 0.000000 | 0.000 |
| 8 | 4.095487 | 4.095487 | 0.000000 | 0.000 |
| 7 | 3.263454 | 3.263454 | 0.000000 | 0.000 |
| 5 | 1.958072 | 1.958072 | 0.000000 | 0.000 |
| 3 | 4.578894 | 4.578894 | 0.000000 | 0.000 |

Top score drifts (normalized by top1, abs):

| id | norm_solr9 | norm_solr10 | abs | rel |
|---|---:|---:|---:|---:|
| 9 | 0.894427 | 0.894427 | 0.000000 | 0.000 |
| 8 | 0.894427 | 0.894427 | 0.000000 | 0.000 |
| 7 | 0.712717 | 0.712717 | 0.000000 | 0.000 |
| 5 | 0.427630 | 0.427630 | 0.000000 | 0.000 |
| 3 | 1.000000 | 1.000000 | 0.000000 | 0.000 |

Explain snippets (top raw-drift docs, normalized):

**doc id 9**

- SOLR9 explain: `4.095487 = sum of:
  1.7513531 = max of:
    0.9192749 = weight(body:charger in 8) [ClassicSimilarity], result of:
      0.9192749 = score(freq=2.0), product of:
        0.2773501 = fieldNorm
        1.1718502 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          15 = docFreq, number of documents containing term
          18 = docCount, total number of documents with field
        1`
- SOLR10 explain: `4.095487 = sum of:
  1.7513531 = max of:
    0.9192749 = weight(body:charger in 8) [ClassicSimilarity], result of:
      0.9192749 = score(freq=2.0), product of:
        0.2773501 = fieldNorm
        1.1718502 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          15 = docFreq, number of documents containing term
          18 = docCount, total number of documents with field
        1`

**doc id 8**

- SOLR9 explain: `4.095487 = sum of:
  1.7513531 = max of:
    0.56025153 = weight(body:charger in 7) [ClassicSimilarity], result of:
      0.56025153 = score(freq=2.0), product of:
        0.16903085 = fieldNorm
        1.1718502 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          15 = docFreq, number of documents containing term
          18 = docCount, total number of documents with field
      `
- SOLR10 explain: `4.095487 = sum of:
  1.7513531 = max of:
    0.56025153 = weight(body:charger in 7) [ClassicSimilarity], result of:
      0.56025153 = score(freq=2.0), product of:
        0.16903085 = fieldNorm
        1.1718502 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          15 = docFreq, number of documents containing term
          18 = docCount, total number of documents with field
      `

## q_brand_anker — PASS ✅
- Jaccard(top10): **1.000**
- RBO(p=0.9): **1.0000**
- Avg abs rank delta: **0.00** (max: 0, changes: 0)
- Top score (SOLR9/SOLR10): **4.095487 / 4.095487**
- Max abs normalized drift: **0.000**
- Only in SOLR9 top10: []
- Only in SOLR10 top10: []

Top movers:

| id | rank_solr9 | rank_solr10 | delta |
|---|---:|---:|---:|
| 1 | 1 | 1 | 0 |
| 9 | 2 | 2 | 0 |
| 11 | 3 | 3 | 0 |
| 7 | 4 | 4 | 0 |
| 5 | 5 | 5 | 0 |

Top score drifts (raw, abs):

| id | score_solr9 | score_solr10 | abs | rel |
|---|---:|---:|---:|---:|
| 9 | 4.095487 | 4.095487 | 0.000000 | 0.000 |
| 7 | 3.263454 | 3.263454 | 0.000000 | 0.000 |
| 5 | 1.958072 | 1.958072 | 0.000000 | 0.000 |
| 14 | 1.751353 | 1.751353 | 0.000000 | 0.000 |
| 11 | 3.566369 | 3.566369 | 0.000000 | 0.000 |

Top score drifts (normalized by top1, abs):

| id | norm_solr9 | norm_solr10 | abs | rel |
|---|---:|---:|---:|---:|
| 9 | 1.000000 | 1.000000 | 0.000000 | 0.000 |
| 7 | 0.796841 | 0.796841 | 0.000000 | 0.000 |
| 5 | 0.478105 | 0.478105 | 0.000000 | 0.000 |
| 14 | 0.427630 | 0.427630 | 0.000000 | 0.000 |
| 11 | 0.870805 | 0.870805 | 0.000000 | 0.000 |

Explain snippets (top raw-drift docs, normalized):

**doc id 9**

- SOLR9 explain: `4.095487 = sum of:
  1.7513531 = max of:
    0.9192749 = weight(body:charger in 8) [ClassicSimilarity], result of:
      0.9192749 = score(freq=2.0), product of:
        0.2773501 = fieldNorm
        1.1718502 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          15 = docFreq, number of documents containing term
          18 = docCount, total number of documents with field
        1`
- SOLR10 explain: `4.095487 = sum of:
  1.7513531 = max of:
    0.9192749 = weight(body:charger in 8) [ClassicSimilarity], result of:
      0.9192749 = score(freq=2.0), product of:
        0.2773501 = fieldNorm
        1.1718502 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          15 = docFreq, number of documents containing term
          18 = docCount, total number of documents with field
        1`

**doc id 7**

- SOLR9 explain: `3.263454 = sum of:
  1.3053817 = max of:
    0.9230442 = weight(body:iphone in 6) [ClassicSimilarity], result of:
      0.9230442 = score(freq=2.0), product of:
        0.25 = fieldNorm
        1.3053817 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          13 = docFreq, number of documents containing term
          18 = docCount, total number of documents with field
        1.41421`
- SOLR10 explain: `3.263454 = sum of:
  1.3053817 = max of:
    0.9230442 = weight(body:iphone in 6) [ClassicSimilarity], result of:
      0.9230442 = score(freq=2.0), product of:
        0.25 = fieldNorm
        1.3053817 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          13 = docFreq, number of documents containing term
          18 = docCount, total number of documents with field
        1.41421`

## q_near_tie_stress — PASS ✅
- Jaccard(top10): **1.000**
- RBO(p=0.9): **1.0000**
- Avg abs rank delta: **0.00** (max: 0, changes: 0)
- Top score (SOLR9/SOLR10): **12.509465 / 12.509465**
- Max abs normalized drift: **0.000**
- Only in SOLR9 top10: []
- Only in SOLR10 top10: []

Top movers:

| id | rank_solr9 | rank_solr10 | delta |
|---|---:|---:|---:|
| 18 | 1 | 1 | 0 |
| 2 | 2 | 2 | 0 |
| 1 | 3 | 3 | 0 |
| 3 | 4 | 4 | 0 |
| 12 | 5 | 5 | 0 |

Top score drifts (raw, abs):

| id | score_solr9 | score_solr10 | abs | rel |
|---|---:|---:|---:|---:|
| 9 | 6.440282 | 6.440282 | 0.000000 | 0.000 |
| 8 | 4.840529 | 4.840529 | 0.000000 | 0.000 |
| 7 | 6.941808 | 6.941808 | 0.000000 | 0.000 |
| 5 | 6.198982 | 6.198982 | 0.000000 | 0.000 |
| 3 | 9.924996 | 9.924996 | 0.000000 | 0.000 |

Top score drifts (normalized by top1, abs):

| id | norm_solr9 | norm_solr10 | abs | rel |
|---|---:|---:|---:|---:|
| 9 | 0.514833 | 0.514833 | 0.000000 | 0.000 |
| 8 | 0.386949 | 0.386949 | 0.000000 | 0.000 |
| 7 | 0.554924 | 0.554924 | 0.000000 | 0.000 |
| 5 | 0.495543 | 0.495543 | 0.000000 | 0.000 |
| 3 | 0.793399 | 0.793399 | 0.000000 | 0.000 |

Explain snippets (top raw-drift docs, normalized):

**doc id 9**

- SOLR9 explain: `6.4402823 = sum of:
  0.6858251 = max of:
    0.6858251 = weight(body:usb in 8) [ClassicSimilarity], result of:
      0.6858251 = score(freq=1.0), product of:
        0.2773501 = fieldNorm
        1.0 = tf(freq=1.0), with freq of:
          1.0 = freq, occurrences of term within document
        1.2363888 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          14 = docFreq, number of `
- SOLR10 explain: `6.4402823 = sum of:
  0.6858251 = max of:
    0.6858251 = weight(body:usb in 8) [ClassicSimilarity], result of:
      0.6858251 = score(freq=1.0), product of:
        0.2773501 = fieldNorm
        1.0 = tf(freq=1.0), with freq of:
          1.0 = freq, occurrences of term within document
        1.2363888 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          14 = docFreq, number of `

**doc id 8**

- SOLR9 explain: `4.8405294 = sum of:
  0.4179757 = max of:
    0.4179757 = weight(body:usb in 7) [ClassicSimilarity], result of:
      0.4179757 = score(freq=1.0), product of:
        0.16903085 = fieldNorm
        1.0 = tf(freq=1.0), with freq of:
          1.0 = freq, occurrences of term within document
        1.2363888 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          14 = docFreq, number of`
- SOLR10 explain: `4.8405294 = sum of:
  0.4179757 = max of:
    0.4179757 = weight(body:usb in 7) [ClassicSimilarity], result of:
      0.4179757 = score(freq=1.0), product of:
        0.16903085 = fieldNorm
        1.0 = tf(freq=1.0), with freq of:
          1.0 = freq, occurrences of term within document
        1.2363888 = idf, computed as log((docCount+1)/(docFreq+1)) + 1 from:
          14 = docFreq, number of`

