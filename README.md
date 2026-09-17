# Batch Customer Feedback Classification with LangChain

Classify thousands of customer reviews into actionable categories using a Large Language Model — automatically, in batch, from a simple script.

## Overview

This project reads a customer feedback dataset (TSV/CSV), sends each `review_text` to an LLM, classifies the **reason** for the feedback, and saves the labeled results to a new CSV file.

**Categories used:**
- Price too high
- Insufficient after-sales support
- Poor product experience
- Other

## How It Works

```
customer_feedback.tsv
        │
        ▼
   pandas (reads dataset, handles tabs/quotes)
        │
        ▼
   Loop over each row ──► LLM (via LangChain)
        │                    classify reason
        ▼                    │
   Collect labels ◄──────────┘
        │
        ▼
  classified_output.csv  (original data + new 'classification' column)
```

## Features

- 📂 Reads tab-separated Kaggle-style datasets cleanly (handles quoting, commas inside text)
- 🤖 LLM classification through LangChain's unified interface — swap models by changing one line
- 🛡️ Error handling per row — one bad row or API failure won't kill the whole run
- 📊 Progress indicator — `[37/12000]` so you always know where the run stands
- 💾 Incremental results saved to CSV — partial progress is never lost
- 🔐 API keys loaded from a `.env` file, never hardcoded

## Project Structure

```
batchprocessing_langchain/
├── rd_excl_lc.py          # main script
├── .env                   # your API key (not committed to git!)
├── data/
│   └── test_env/
│       └── customer_feedback.tsv   # input dataset
├── classified_output.csv  # results (generated)
├── requirements.txt
└── README.md
```

## Setup

### 1. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate       # Windows
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

Or directly:

```bash
pip install pandas python-dotenv langchain-community openpyxl
```

### 3. Add your API key

Create a `.env` file in the project root:

```bash
DASHSCOPE_API_KEY=sk-your-key-here
```

Get a key from [Alibaba Cloud Model Studio (DashScope)](https://bailian.console.aliyun.com/).

> The script uses LangChain's `Tongyi` wrapper, so it can be pointed at any
> compatible endpoint by adjusting the model/connection settings.

### 4. Prepare your dataset

The script expects a tab-separated file with a `review_text` column:

| customer_id | gender | region | customer_rating | review_text | sentiment | ... |
|-------------|--------|--------|-----------------|-------------|-----------|-----|
| 1 | male | north | 1 | very disappointed with the quality. | negative | ... |

If your file is comma-separated, change `sep='\t'` to `sep=','` in the script.

## Usage

```bash
python rd_excl_lc.py
```

Watch the console for progress:

```
[1/12000] Poor product experience
[2/12000] Price too high
...
```

When finished, open **`classified_output.csv`** — it contains all original columns plus a new `classification` column.

## Configuration

| Setting | Where | Notes |
|---------|-------|-------|
| Model | `Tongyi(model_name='qwen-max')` | Swap to any supported model |
| Input file | `pd.read_csv(...)` path | Point to your dataset |
| Column to classify | `row['review_text']` | Change to your text column name |
| Categories | The prompt text | Edit to match your use case |

## Cost & Rate-Limit Notes

- Each row = one API call. A 10,000-row dataset = 10,000 calls — test on 20–50 rows first!
- Consider **batching** multiple reviews per call (see Improvements below)
- Watch your provider's rate limits; add `time.sleep(1)` between calls if needed
- Resume a crashed run by slicing the dataframe: `df = df.iloc[resume_from:]`

## Possible Improvements

- [ ] Batch N reviews per LLM call (fewer calls, faster runs)
- [ ] Retry logic with exponential backoff on API errors
- [ ] Write results incrementally instead of at the end
- [ ] Classical ML baseline (TF-IDF + logistic regression) for comparison — free and instant
- [ ] Streamlit/simple UI for uploading a file and downloading labeled results

## Requirements

- Python 3.10+
- See `requirements.txt`

## License

MIT (or adjust as needed)
