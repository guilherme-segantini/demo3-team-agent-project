# Voice AI UX Prompt Template

Using your real-time knowledge of X/Twitter discussions and tech news from the past 7 days,
SEARCH for and ANALYZE tools related to Voice AI UX.

## STEP 1 - DISCOVER

Search your knowledge for tools being discussed in the Voice AI UX space.
Look for announcements, releases, technical discussions, and trending topics.

## STEP 2 - CLASSIFY each discovered tool as SIGNAL or NOISE

### SIGNAL criteria (worth evaluating):
- Has published benchmarks or performance data (latency, VAD specs)
- Shows production usage or real case studies
- Provides specific technical architecture details (WebRTC, streaming)
- Has active technical community discussion

### NOISE criteria (skip):
- Uses marketing language without substance ("revolutionary", "human-like")
- No benchmarks or only vague latency claims
- Pre-announcement hype or vaporware
- Engagement farming without technical depth

## Focus Area Specific Criteria for Voice AI UX

Evaluate:
- Voice-to-voice latency benchmarks (target: sub-200ms)
- Interruption handling specifications
- VAD (Voice Activity Detection) implementation
- WebRTC/streaming architecture details
- SDK availability and documentation

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
