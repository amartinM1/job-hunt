# Side projects to close the gaps (about 1 week)

All in Python. Build one well rather than several halfway.

1. **A voice agent for card servicing (top pick).** An ElevenLabs voice agent that handles "What's my balance?", "Freeze my card," and "Dispute a charge" by calling a small FastAPI service with fake account data, using the agent's tool feature. This is the core FDE job: connecting their agent to a customer's backend. It also uses your payments background (caller verification, sensitive card data).
2. **An eval harness for that agent.** Run 20–30 scripted conversations (happy paths, interruptions, bad inputs) and score each with a rubric: task done, right tool called, stayed on policy. This turns your Snorkel experience into a differentiator.
3. **A festival concierge for DIFF.** A voice or web-widget agent with a knowledge base of the schedule, venues, and ticket FAQs. Lightest of the agent projects.
4. **A text-to-speech pipeline.** Turn a document into narrated audio, possibly in two languages, with their speech API. About a day of work, so use it as a warm-up or fallback.

## Suggested week
- Days 1–2: the mock card API and the agent connected to it
- Days 3–4: edge cases and the eval harness
- Day 5: README with an architecture diagram, a two-minute demo video, and a one-page brief written as if for a bank's VP (practice for the customer-executives gap)

Check the free tier's limits on agent minutes and API usage first.

## Sources
- https://elevenlabs.io/docs/es/eleven-agents/libraries/python.md
- https://elevenlabs.io/docs/help-center/product/eleven-agents/how-do-i-use-tools-with-eleven-agents/llms.txt
