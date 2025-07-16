# Dataset Design – MMA Dataset

This document outlines each experiment's design, preprocessing logic, and resulting data shape after transformation.

---

## Available Columns

| Original             | Full Name (or Translated)                                         |
| ---------------------------- | ------------------------------------------------------------- |
| Identifier                   | Identifier                                                    |
| Source                       | Source                                                        |
| LIS                          | LIS (Laboratory Information System, likely remains unchanged) |
| Leeftijd                     | Age                                                           |
| Geslacht                     | Sex                                                           |
| KR                           | Creatinine                                                    |
| eGFR                         | Estimated Glomerular Filtration Rate                          |
| VITB12                       | Vitamin B12                                                   |
| MMZ                          | Methylmalonic Acid (MMA)                                      |
| Classificatie\_MMZ           | MMA Etiology Classification                                   |
| Anemie                       | Anemia                                                        |
| HB                           | Hemoglobin (Hb)                                               |
| MCV                          | Mean Corpuscular Volume (MCV)                                 |
| MCH                          | Mean Corpuscular Hemoglobin (MCH)                             |
| MCHC                         | Mean Corpuscular Hemoglobin Concentration (MCHC)              |
| RDW                          | Red Cell Distribution Width (RDW)                             |
| RBC                          | Red Blood Cells (RBC)                                         |
| WBC                          | White Blood Cells (WBC)                                       |
| PLT                          | Platelets (PLT)                                               |
| RETI                         | Reticulocytes                                                 |
| NEUTRO                       | Neutrophils                                                   |
| LYMFO                        | Lymphocytes                                                   |
| MONO                         | Monocytes                                                     |
| BASO                         | Basophils                                                     |
| EO                           | Eosinophils                                                   |
| IJzergebrek                  | Iron Deficiency                                               |
| FERRITINE                    | Ferritin                                                      |
| CRP                          | C-reactive Protein (CRP)                                      |
| TSAT                         | Transferrin Saturation (TSAT)                                 |
| TRF                          | Transferrin (TRF)                                             |
| FE                           | Iron (Fe)                                                     |
| BSE                          | Erythrocyte Sedimentation Rate (ESR/BSE)                      |
| FOLIUMZUUR                   | Folate (Folic Acid)                                           |
| FZ\_deficiency               | Folate Deficiency                                             |
| LDH                          | Lactate Dehydrogenase (LDH)                                   |
| HAPTO                        | Haptoglobin                                                   |
| Hemolyse                     | Hemolysis                                                     |
| RET\_HE                      | Reticulocyte Hemoglobin Equivalent (RET-He)                   |
| RBC\_HE                      | RBC Hemoglobin Equivalent                                     |
| DELTA\_HE                    | Delta-He (difference between RET-He and RBC-He)               |
| HYPER\_HE                    | Hyperchromic RBCs (Hyper-He)                                  |
| HYPO\_HE                     | Hypochromic RBCs (Hypo-He)                                    |
| HFR                          | High Fluorescence Ratio (Immature reticulocyte fraction)      |
| IRF                          | Immature Reticulocyte Fraction                                |
| MFR                          | Medium Fluorescence Ratio                                     |
| LFR                          | Low Fluorescence Ratio                                        |
| Vitamin\_B12\_Problem\_Label | Expert Label: Vitamin B12-related Issue                       |
| Kidney\_problem              | Expert Label: Kidney-related Issue                            |

## Data Statistics (Key Columns)

|       |        Age |          Sex |         KR |        eGFR |    VITB12 |       MMZ |   Classificatie_MMZ |      Anemie |         HB |        MCV |
|:------|-----------:|-------------:|-----------:|------------:|----------:|----------:|--------------------:|------------:|-----------:|-----------:|
| count | 14252      | 14252        | 13472      | 13100       | 13911     | 14252     |         14252       | 7356        | 7356       | 7355       |
| mean  |    54.1337 |     0.363037 |    76.7788 |    86.6975  |   267.824 |   309.624 |             1.63879 |    0.362425 |    8.13736 |   91.6024  |
| std   |    22.1598 |     0.480892 |    24.7216 |    23.2991  |   169.255 |   487.191 |             1.39901 |    0.480733 |    1.07305 |    6.23591 |
| min   |     2      |     0        |    17      |     6.95925 |    74     |    46     |             0       |    0        |    2       |   55.4     |
| 25%   |    35      |     0        |    63      |    71.6695  |   190     |   163     |             1       |    0        |    7.5     |   88.5     |
| 50%   |    55      |     0        |    72      |    87.4709  |   222     |   223.05  |             1       |    0        |    8.2     |   91.9     |
| 75%   |    73      |     1        |    85      |   103       |   256     |   325.125 |             1       |    1        |    8.8     |   95       |
| max   |   105      |     1        |   668      |   158.786   |  1476     | 19568.6   |             8       |    1        |   12       |  127       |

## 📊 Column Groups by Missingness

### Primary Columns
| Column                        | Missing Values | Missing % | Group   |
|------------------------------|----------------|------------|---------|
| Kidney_problem               | 1152           | 8.08%      | Primary |
| eGFR                         | 1152           | 8.08%      | Primary |
| KR                           | 780            | 5.47%      | Primary |
| VITB12                       | 341            | 2.39%      | Primary |
| Classificatie_MMZ           | 0              | 0.00%      | Primary |
| Sex                          | 0              | 0.00%      | Primary |
| Identifier                   | 0              | 0.00%      | Primary |
| MMZ                          | 0              | 0.00%      | Primary |
| Age                          | 0              | 0.00%      | Primary |
| Vitamin_B12_Problem_Label    | 0              | 0.00%      | Primary |

### Secondary Columns
| Column     | Missing Values | Missing % | Group     |
|------------|----------------|-----------|-----------|
| CRP        | 8564           | 60.09%    | Secondary |
| BASO       | 7620           | 53.47%    | Secondary |
| MONO       | 7620           | 53.47%    | Secondary |
| LYMFO      | 7620           | 53.47%    | Secondary |
| NEUTRO     | 7620           | 53.47%    | Secondary |
| EO         | 7618           | 53.45%    | Secondary |
| MCH        | 7548           | 52.96%    | Secondary |
| RDW        | 7533           | 52.86%    | Secondary |
| MCHC       | 7530           | 52.83%    | Secondary |
| RBC        | 7520           | 52.76%    | Secondary |
| PLT        | 7196           | 50.49%    | Secondary |
| WBC        | 7078           | 49.66%    | Secondary |
| HB         | 6896           | 48.39%    | Secondary |
| Anemie     | 6896           | 48.39%    | Secondary |
| MCV        | 6897           | 48.39%    | Secondary |

### Third Group (High Missingness)
| Column               | Missing Values | Missing % | Group |
|----------------------|----------------|-----------|--------|
| HAPTO                | 14200          | 99.64%    | Third  |
| HFR                  | 13957          | 97.93%    | Third  |
| HYPER_HE             | 13956          | 97.92%    | Third  |
| MFR                  | 13956          | 97.92%    | Third  |
| LFR                  | 13956          | 97.92%    | Third  |
| DELTA_HE             | 13956          | 97.92%    | Third  |
| IRF                  | 13956          | 97.92%    | Third  |
| HYPO_HE              | 13956          | 97.92%    | Third  |
| RETI                 | 13666          | 95.89%    | Third  |
| RBC_HE              | 13665          | 95.88%    | Third  |
| RET_HE              | 13665          | 95.88%    | Third  |
| BSE                  | 12781          | 89.68%    | Third  |
| TSAT                 | 12488          | 87.62%    | Third  |
| TRF                  | 12467          | 87.48%    | Third  |
| FE                   | 12426          | 87.19%    | Third  |
| Hemolyse             | 12016          | 84.31%    | Third  |
| Iron Deficiency      | 11773          | 82.61%    | Third  |
| LDH                  | 11759          | 82.51%    | Third  |
| FERRITINE            | 10786          | 75.68%    | Third  |
| FZ_deficiency        | 10338          | 72.54%    | Third  |
| FOLIUMZUUR           | 10338          | 72.54%    | Third  |

---
## 📦 Original Dataset
- **File**: `labeled_MMA_data.csv`
- **Shape**: 14252 rows × 49 columns

---

## 🧪 Experiment 1

### Experiment 1.1
- **Logic**:
  - Select only **primary columns**
  - Impute missing values in: `KR`, `eGFR`, `VITB12`
- **Output**: `experiment_1_1.csv`
- **Shape**: 14252 rows × 10 columns

### Experiment 1.2
- **Logic**:
  - Select **primary columns**
  - Drop rows with any missing values
- **Output**: `experiment_1_2.csv`
- **Shape**: 12787 rows × 10 columns

---

## 🧪 Experiment 2

### Experiment 2.1
- **Logic**:
  - Select **primary columns** and **secondary columns**
  - Drop rows with missing values
- **Output**: `experiment_2_1.csv`
- **Shape**: 4662 rows × 25 columns

---

## 🧪 Experiment 3

### Experiment 3.1
- **Logic**:
  - Select **primary columns** + `HB`, `MCV`, `CRP`
  - Impute `KR`, `eGFR`, `VITB12` and  `HB`, `MCV`, `CRP`
- **Output**: `experiment_3_1.csv`
- **Shape**: 14252 rows × 13 columns

### Experiment 3.2
- **Logic**:
  - Select **primary columns** + `HB`, `MC`, `ERP`
  - Drop rows with missing values
- **Output**: `experiment_3_2.csv`
- **Shape**: 5195 rows × 13 columns

---

## 🧪 Experiment 4

### Common Setup
- Use **all columns** and **all rows**

### Experiment 4.1
- **Logic**:
  - Apply **MICE** imputation for columns with very few missing values (<10%)
- **Output**: `experiment_4_1.csv`
- **Shape**: 14252 rows × 10 columns

### Experiment 4.2
- **Logic**:
  - Apply **MICE** imputation for columns with lots of missing values (<65%)
- **Output**: `experiment_4_2.csv`
- **Shape**: 14252 rows × 25 columns
