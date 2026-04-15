# Body Composition Equations

## Durnin-Womersley (1974)

**Sites (4):** Triceps, biceps, subscapular, suprailiac

**Appropriate use:** General population, all ages. Most widely validated across diverse populations.

**Method:** Calculates body density from the log of the sum of four skinfolds, using age- and sex-specific coefficients. Body density is then converted to body fat percentage using a secondary equation (typically Siri).

**Density formula:** `D = C - (M * log10(sum_of_4_skinfolds))`
where C and M are age- and sex-specific constants.

**Age brackets (male):**
| Age     | C      | M      |
|---------|--------|--------|
| < 17    | 1.1533 | 0.0643 |
| 17-19   | 1.1620 | 0.0630 |
| 20-29   | 1.1631 | 0.0632 |
| 30-39   | 1.1422 | 0.0544 |
| 40-49   | 1.1620 | 0.0700 |
| 50+     | 1.1715 | 0.0779 |

**Age brackets (female):**
| Age     | C      | M      |
|---------|--------|--------|
| < 17    | 1.1369 | 0.0598 |
| 17-19   | 1.1549 | 0.0678 |
| 20-29   | 1.1599 | 0.0717 |
| 30-39   | 1.1423 | 0.0632 |
| 40-49   | 1.1333 | 0.0612 |
| 50+     | 1.1339 | 0.0645 |

---

## Jackson-Pollock 7-Site (1978)

**Sites (7):** Chest, axilla, tricep, subscapular, abdominal, suprailiac, thigh

**Appropriate use:** Most comprehensive assessment. Best for trained individuals and research settings where maximum accuracy is needed.

**Method:** Uses sum of 7 skinfolds with quadratic and age terms.

**Male:** `D = 1.112 - (0.00043499 * S) + (0.00000055 * S²) - (0.00028826 * age)`
**Female:** `D = 1.097 - (0.00046971 * S) + (0.00000056 * S²) - (0.00012828 * age)`

where S = sum of 7 skinfolds (mm).

---

## Jackson-Pollock 4-Site

**Sites (4):** Abdominal, triceps, thigh, suprailiac

**Appropriate use:** Simplified alternative when 7-site measurement is impractical. Directly calculates body fat percentage (no intermediate density step).

**Male:** `BF% = (0.29288 * S) - (0.0005 * S²) + (0.15845 * age) - 5.76377`
**Female:** `BF% = (0.29669 * S) - (0.00043 * S²) + (0.02963 * age) + 1.4072`

where S = sum of 4 skinfolds (mm).

---

## Jackson-Pollock 3-Site (1985)

**Sites (3):** Chest, triceps, subscapular (male) OR triceps, thigh, suprailiac (female)

**Appropriate use:** Quick assessment when fewer measurement sites are available. Sex-specific site selection.

**Male:** `D = 1.10938 - (0.0008267 * S) + (0.0000055 * S²) - (0.000244 * age)`
**Female:** `D = 1.0994921 - (0.0009929 * S) + (0.0000023 * S²) - (0.0001392 * age)`

where S = sum of 3 skinfolds (mm).

---

## Density-to-Body-Fat Conversion Equations

All take body density (g/cm³) as input and return body fat percentage.

| Equation | Formula                        | Best For                     |
|----------|-------------------------------|------------------------------|
| **Siri** (1961)    | `(495 / D) - 450`     | General population (default) |
| **Brozek** (1963)  | `(457 / D) - 414.2`   | General population           |
| **Schutte** (1984) | `(437.4 / D) - 392.8` | Black males                  |
| **Wagner** (1996)  | `(486 / D) - 439`     | Black females                |
| **Ortiz** (1992)   | `(483.2 / D) - 436.9` | Hispanic populations         |

**Note:** Siri is the most commonly used default. Population-specific equations (Schutte, Wagner, Ortiz) may provide better accuracy for specific demographics.
