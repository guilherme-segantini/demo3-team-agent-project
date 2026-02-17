# Durable Runtime Prompt Template

Using your real-time knowledge of X/Twitter discussions and tech news from the past 7 days,
SEARCH for and ANALYZE tools related to Durable Runtime.

## STEP 1 - DISCOVER

Search your knowledge for tools being discussed in the Durable Runtime space.
Look for announcements, releases, technical discussions, and trending topics.

## STEP 2 - CLASSIFY each discovered tool as SIGNAL or NOISE

### SIGNAL criteria (worth evaluating):
- Has published benchmarks or performance data
- Shows production usage or real case studies
- Provides specific technical architecture details
- Has active technical community discussion

### NOISE criteria (skip):
- Uses marketing language without substance ("infinite scale", "zero cold starts")
- No benchmarks or only vague claims
- Pre-announcement hype or vaporware
- Engagement farming without technical depth

## Focus Area Specific Criteria for Durable Runtime

Evaluate:
- Durability guarantees and SLAs
- Cold-start benchmarks (target: sub-100ms)
- Checkpoint/recovery specifications
- Fault tolerance mechanisms
- Long-running workflow support

## Output Format

Return JSON array with your findings:
```json
[
  {
    "tool_name": "string",
    "classification": "signal" | "noise",
    "confidence_score": 1-100,
    "technical_insight": "specific technical details you found",
    "signal_evidence": ["evidence1", "evidence2"],
    "noise_indicators": ["indicator1", "indicator2"],
    "architectural_verdict": true | false
  }
]
```
