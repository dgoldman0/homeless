# Active-rail source analysis: post-report soft-jacket test

This folder contains diagnostic work after the previous source-ledger report.

Start with:

```text
docs/post_report_findings.md
```

Status:

```text
Do not refreeze the design yet.
```

The main result is that the soft angular jacket is a real source-routing improvement, but it leaves angular pressure and late-tail reset debt unresolved.

To regenerate the diagnostic outputs:

```bash
python code/controlled_angular_source_test.py --outdir regenerated_output --ns 251 --nl 375
```
