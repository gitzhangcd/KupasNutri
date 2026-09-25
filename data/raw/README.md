# Raw P1 snapshot

The user-provided P1 qualification snapshot is a **headerless 10-column CSV** containing dish IDs `10000–10099`.

Expected filename:

`dish_samples_100_snapshot.csv`

Expected byte size:

`912727`

SHA-256:

`70182e01ed8cfbde08287d83bdf4bd342f1037ee454a88c97068e036495b50dd`

The raw file itself is not committed by the ChatGPT GitHub connector in this pass because the connector workflow used here is text-oriented and the snapshot is retained separately as the immutable source artifact. Generated tables can be reproduced by placing the exact raw file at the path above and running:

```bash
python scripts/process_p1_100_cases.py   data/raw/dish_samples_100_snapshot.csv   data/processed
```

Do not modify the raw snapshot in place. New API pulls should be stored as separate versioned source records.
