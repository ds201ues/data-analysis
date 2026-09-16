# READING DATA — Session Plan (Process-First, Top-Down)

## The Shift from Previous Deck

Previous deck: showed results, final outputs, finished analyses.
This deck: teaches the PROCESS of thinking, types of analysis, what charts to use when, how to read numbers. The demo dataset runs through each type live.

---

## THE DATASET

**File:** `ad-sales-data.csv`
**What it is:** 3 years (2022–2024) of advertising booking data for a media company. Simulates BCCL's ad sales.

| Column | What it is | Analysis use |
|--------|-----------|--------------|
| order_id | Unique booking ID | Counting |
| booking_date | When booked | Trend, time series |
| publish_date | When published | Lag analysis |
| city | 8 Indian cities | Comparison, ranking |
| edition | 4 publications | Composition, comparison |
| ad_type | Display, Classified, Digital, Supplement, Branded Content | Composition, trend |
| category | 10 advertiser sectors | Ranking, concentration |
| sales_rep | 30 reps (SR001–SR030) | Ranking, distribution |
| quantity | Size/volume of booking | Driver analysis |
| rate_per_unit | Price per unit | Trend, comparison |
| discount_pct | Discount given | Distribution, outlier |
| gross_amount | Before discount | Decomposition |
| net_amount | After discount | Key metric |
| status | Confirmed/Cancelled/Pending | Filtering |

**Built-in patterns to discover:**
- Digital ad revenue growing 90% over 3 years while Classified declining 30%
- Diwali + festive season (Oct-Nov) spike every year
- Monsoon (Jul-Aug) trough every year
- Top 3 cities = ~45% of revenue (concentration)
- 8 outlier deals (10-15x normal size)
- Data quality issues: 5 city name typos, 10 missing values, 5 suspicious 95% discounts
- Mumbai + Delhi dominate in counts, but rate per unit is only a story at city level
- Print declining, digital growing = mix shift (volume up, average rate down)

---

## DECK STRUCTURE: TOP-DOWN APPROACH

### Teaching order (process → types → charts → stats → practice)

```
Part 1: HOW TO THINK (The Process)         — 25 min
Part 2: TYPES OF ANALYSIS                   — 40 min
         (8 types, each with theory + live demo on the dataset)
Part 3: WHICH CHART FOR WHICH QUESTION      — 15 min
Part 4: NUMBERS THAT LIE (Stats concepts)   — 20 min
Part 5: HANDS-ON + WRAP                     — 20 min
```

---

## PART 1: HOW TO THINK (The Analysis Process)

**Concept:** Before touching any number, analysts follow a structured top-down process. Teach the 7 steps.

### Slide structure for Part 1:

**Slide:** "How an analyst thinks" — the 7-step ladder visual

| Step | Name | One-line | Demo on dataset |
|------|------|----------|-----------------|
| 1 | CONTEXT | What decision? Who? By when? | "Should we invest more in digital or protect print?" |
| 2 | SHAPE | What do I have? Rows, columns, date range, quality. | Show: 3079 rows, 14 columns, Jan 2022–Dec 2024 |
| 3 | TOTAL | Start with the biggest number. | Total net revenue: ₹44.8 Cr over 3 years |
| 4 | BREAK DOWN | Split by the first natural dimension. | By ad_type: Display 40%, Digital 25%, Classified 20%... |
| 5 | COMPARE | vs last year, vs plan, vs peer. | 2024 vs 2023: Digital +38%, Classified −18% |
| 6 | DRIVERS | Why did it move? Volume × Price. | Digital grew because volume +60% even though rate −12% |
| 7 | VALIDATE | Does it pass the smell test? | Check: 8 outlier deals inflating some months |

**Key visual:** A pyramid/funnel going from TOTAL at top → narrower cuts below. "Always start wide, then narrow."

---

## PART 2: TYPES OF ANALYSIS (8 Types)

Each type gets: **concept slide → example question → live demo chart → "try this" prompt**

### Type 1: COMPARISON (This vs That)
- **Concept:** Place things side by side. The simplest and most common analysis.
- **Question:** "How does Mumbai compare to Delhi in ad revenue?"
- **Demo chart:** Horizontal bar — Mumbai vs Delhi vs others, net revenue
- **Live prompt:** "Compare net revenue by city for 2024. Show as a bar chart sorted by value."
- **Pre-baked result:** Bar chart showing Mumbai ₹X Cr, Delhi ₹Y Cr, gap highlighted

### Type 2: RANKING (Who's on top)
- **Concept:** Sort from highest to lowest. Identify leaders and laggards.
- **Question:** "Which 5 sales reps generated the most revenue? Which 5 are at the bottom?"
- **Demo chart:** Horizontal bar, top 5 highlighted in blue, bottom 5 in red
- **Live prompt:** "Rank sales reps by total net revenue for 2024. Show top 5 and bottom 5."
- **Pre-baked:** Lollipop or bar chart with clear top/bottom callouts

### Type 3: TREND (What changed over time)
- **Concept:** Track a metric across time. Spot direction, speed, and inflection points.
- **Question:** "Is digital revenue actually growing? How fast? Is it accelerating?"
- **Demo chart:** Line chart — monthly revenue by ad_type, 2022–2024
- **Live prompt:** "Show monthly net revenue trend for each ad_type from 2022 to 2024 as a line chart."
- **Pre-baked:** Lines showing Digital rising steeply, Classified declining, Display flat
- **Bonus visual:** Annotate the chart — "What happened in Oct 2023?" (Diwali spike)

### Type 4: COMPOSITION (What makes up the whole)
- **Concept:** Break a total into its parts. See relative size.
- **Question:** "What percentage of revenue comes from each ad type? Is the mix changing?"
- **Demo chart:** Stacked bar chart — composition by year (2022 vs 2023 vs 2024)
- **Live prompt:** "Show revenue composition by ad_type for each year as a stacked bar chart (% of total)."
- **Pre-baked:** Shows Digital share growing from 15% → 22% → 30%, Classified shrinking
- **This is where MIX SHIFT lives** — "Volume grew but average rate fell because we sold more cheap digital and less expensive display"

### Type 5: DISTRIBUTION (How values spread)
- **Concept:** Not just the average — what's the shape? Where do most values cluster?
- **Question:** "What does a 'typical' deal look like? How much variation is there?"
- **Demo chart:** Histogram of deal sizes (net_amount) — show the long tail
- **Live prompt:** "Show the distribution of net_amount for confirmed orders. Histogram with 30 bins."
- **Pre-baked:** Histogram showing most deals are small (₹10K–₹1L), a few are massive (₹10L+)
- **Stats tie-in:** Mean vs Median visible on the chart. "The average deal is ₹1.8L but the median is ₹45K — a few whales distort everything."

### Type 6: CORRELATION (Do these move together)
- **Concept:** Do two things rise and fall together? (Without claiming one causes the other.)
- **Question:** "Do higher discounts lead to bigger deals? Or are we just giving money away?"
- **Demo chart:** Scatter plot — discount_pct (x) vs net_amount (y)
- **Live prompt:** "Scatter plot of discount percentage vs net amount for confirmed orders. Add a trend line."
- **Pre-baked:** Shows weak/no correlation — high discounts don't produce bigger revenue
- **Teaching moment:** "Correlation ≠ causation. And sometimes there's no correlation at all."

### Type 7: OUTLIER/ANOMALY (What's unusual)
- **Concept:** Find what breaks the pattern. Either a problem or an opportunity.
- **Question:** "Are there any suspiciously large deals? Any months that behave oddly?"
- **Demo chart:** Time series with anomaly points highlighted; or a box plot by month
- **Live prompt:** "Flag any orders where net_amount is more than 5x the median for that ad_type. List them."
- **Pre-baked:** Table of 8 outlier deals + the 5 suspicious 95% discounts
- **Teaching moment:** Data quality issues discovered (typos in city names, missing values)

### Type 8: DECOMPOSITION/DRIVERS (Why did it change)
- **Concept:** When the top-line moves, break it into components that sum to the whole.
- **Question:** "Revenue grew 12% in 2024 vs 2023. Was it more deals, bigger deals, or less discounting?"
- **Demo chart:** Waterfall — Revenue 2023 → +Volume → +Rate → −Discount → Revenue 2024
- **Live prompt:** "Decompose the revenue change from 2023 to 2024 into: number of orders, average deal size, and average discount. Show as a waterfall."
- **Pre-baked:** Waterfall showing: more orders (+18%), lower avg rate (−8%), similar discount = net +12%
- **This is the advanced move** — "Most people stop at 'revenue went up.' An analyst asks WHY and makes the parts sum."

---

## PART 3: WHICH CHART FOR WHICH QUESTION

**One slide:** The decision tree

```
What are you trying to show?
├── "How things compare"         → BAR (horizontal, sorted)
├── "Who's best/worst"           → BAR (sorted, top/bottom highlighted)
├── "How it changed over time"   → LINE
├── "What makes up the total"    → STACKED BAR or PIE (max 5 parts)
├── "How values are spread"      → HISTOGRAM
├── "Do X and Y relate?"         → SCATTER
├── "What drove the change"      → WATERFALL
├── "Patterns in 2 dimensions"   → HEATMAP
└── "I need exact numbers"       → TABLE
```

**One slide:** Before/After — the same data shown as a wrong chart vs the right chart

**One slide:** The three rules:
1. Title = the finding, not the subject ("North grew 40%" not "Revenue by Region")
2. One colour for the point. Everything else grey.
3. When in doubt, horizontal bar chart. It's never wrong.

---

## PART 4: NUMBERS THAT LIE (High-level stats)

**Not formulas. Each concept = one slide with a visual from the dataset.**

| Concept | Visual | Dataset demo |
|---------|--------|--------------|
| Mean vs Median | Histogram with both lines marked | Avg deal ₹1.8L, median ₹45K |
| Rate vs Count | Side-by-side bars (counts vs per-unit) | Mumbai has most orders. Bangalore has highest rate. |
| YoY vs MoM | Line chart showing noisy MoM vs clean YoY | Monthly revenue is chaotic; YoY trend is clear |
| Percentiles | Box plot by ad_type | "Top quartile deals are above ₹2L" |
| Weighted average | Comparison | Avg discount is 15%. But weighted by revenue, it's 22%. Big deals get more discount. |
| Small-n trap | Bar chart with n-values shown | "Branded Content +200%!" (from 3 to 9 deals) |
| Correlation ≠ Cause | Scatter from Type 6 | High discount ≠ high revenue |
| Seasonality | 3-year overlay (Jan-Dec pattern) | Every year: Oct peak, Jul trough |
| Survivorship | Cancelled orders removed from "average" | "Revenue per order improved!" (because small ones got cancelled) |

---

## PART 5: HANDS-ON + WRAP

**Three prompts for the audience to try themselves:**

1. "What is the revenue trend by ad_type? Which type is growing fastest?"
2. "Who are the top 5 and bottom 5 sales reps? What's the gap?"
3. "What does the typical deal look like? Show me the distribution."

**Wrap:**
- The 7-step process (one card)
- The 8 types (one card)
- The chart decision tree (one card)

---

## DEMO FLOW: What to Pre-Bake

For each of the 8 types, you need:
1. A pre-made chart image (in case live demo fails)
2. The exact prompt to type live
3. The expected output/chart

**Pre-bake these 8 chart images + the waterfall + the dashboard mockup = 10 visuals total.**

Also pre-bake:
- The data quality discoveries (typos, missing values)
- The "wrong chart" examples for Part 3
- The mean vs median histogram

---

## WHAT MAKES THIS DIFFERENT FROM THE PREVIOUS DECK

| Previous | Now |
|----------|-----|
| Started with results (five sentences, landing) | Starts with the PROCESS (how to think) |
| Six moves as structure | Eight types of analysis as structure |
| Taught traps/verification at the end | Stats concepts woven through each type |
| One dataset example end-to-end | One dataset, but each TYPE demonstrated separately |
| Prompt-heavy (six prompts as main content) | Chart-heavy (every type = visual proof) |
| "Masterclass for analysts" vibe | "Training course" vibe — anyone can follow |
| Dense facilitator-facing | Audience-facing — every slide is visual |

---

## FILE INVENTORY

```
~/Downloads/session-data/
├── ad-sales-data.csv          ← The demo dataset (3079 rows)
├── generate-dataset.py        ← Script that created it (for reproducibility)
└── SESSION-PLAN.md            ← This file
```

Next steps:
1. Build pre-baked chart images for all 8 types
2. Build the .pptx with visuals embedded
3. Test the live prompts on Aurex with this dataset
