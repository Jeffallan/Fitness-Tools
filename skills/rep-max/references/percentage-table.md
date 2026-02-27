# Rep Max Estimation Reference

## ACSM Percentage-of-1RM Table

Maps repetition counts to percentages of one-rep maximum:

| Reps | % of 1RM | Reps | % of 1RM |
|------|----------|------|----------|
| 1    | 100%     | 11   | 70%      |
| 2    | 95%      | 12   | 67%      |
| 3    | 93%      | 13   | 66.5%    |
| 4    | 90%      | 14   | 66%      |
| 5    | 87%      | 15   | 65%      |
| 6    | 85%      | 16   | 64%      |
| 7    | 83%      | 17   | 63%      |
| 8    | 80%      | 18   | 62%      |
| 9    | 77%      | 19   | 61%      |
| 10   | 75%      | 20   | 60%      |

## Estimation Formula

```
estimated_weight = (current_weight / percent[current_reps]) * percent[desired_reps]
```

Result is rounded to the nearest specified base (typically 2.5 or 5.0 lbs).

## Accuracy Notes

- Best results when using 5 or fewer reps as the base measurement
- Percentages are within +/- 0.5-2% depending on training status
- The table assumes standard strength training form and tempo
- Individual variation means these are estimates, not exact predictions
