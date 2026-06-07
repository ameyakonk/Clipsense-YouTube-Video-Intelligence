from langchain_openai import ChatOpenAI

def extract_segments(segments, start, end):
    return [seg for seg in segments if start <= seg.start <= end]

def summarize(segments):
    text = " ".join(seg.text for seg in segments)
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    return llm.invoke(f"Summarize this transcript excerpt:\n\n{text}").content

def check_keywords(summary, expected_keywords):
    hits = [kw for kw in expected_keywords if kw.lower() in summary.lower()]
    score = len(hits) / len(expected_keywords)
    return score, hits


# for case in ground_truth:
#     segs = extract_segments(segments, *case["timestamp_range"])
#     summary = summarize(segs)
#     score, hits = check_keywords(summary, case["expected_keywords"])
#     print(f"Score: {score:.0%} | Hits: {hits}")
#     print(f"Summary: {summary}\n")