def generate_summary(text: str) -> str:
    lines = text.strip().split("\n")
    parts = []
    for line in lines:
        if ":" in line:
            key, value = line.split(":", 1)
            parts.append(value.strip())
        else:
            parts.append(line.strip())
    summary = " ".join(parts)
    if len(summary.split()) > 30:
        summary = " ".join(summary.split()[:30]) + "..."
    return summary