
import re


def split_text(
    text: str,
    chunk_size: int = 1000,
    overlap: int = 150
) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be >= 0 and < chunk_size")

    text = re.sub(r"\r\n?", "\n", text).strip()

    if not text:
        return []

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)

        if end < text_length:
            # Prefer paragraph, sentence, or word boundaries.
            min_boundary = start + int(chunk_size * 0.7)
            window = text[min_boundary:end]

            paragraph_break = window.rfind("\n\n")
            sentence_break = max(
                window.rfind(". "),
                window.rfind("? "),
                window.rfind("! "),
            )
            line_break = window.rfind("\n")
            word_break = window.rfind(" ")

            if paragraph_break >= 0:
                end = min_boundary + paragraph_break
            elif sentence_break >= 0:
                end = min_boundary + sentence_break + 1
            elif line_break >= 0:
                end = min_boundary + line_break
            elif word_break >= 0:
                end = min_boundary + word_break

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= text_length:
            break

        # Keep overlap while ensuring forward progress.
        next_start = max(start + 1, end - overlap)

        # Avoid beginning the next chunk in the middle of a word.
        space_position = text.find(" ", next_start, min(next_start + 100, end))
        if space_position != -1:
            next_start = space_position + 1

        start = next_start

    return chunks


if __name__ == "__main__":
    sample_text = (
        "RAG combines retrieval with generation. "
        "Embeddings represent text as vectors. "
        "Vector search retrieves relevant information.\n\n"
    ) * 20

    chunks = split_text(sample_text)

    for i, chunk in enumerate(chunks, start=1):
        print(f"\n--- Chunk {i} ({len(chunk)} characters) ---")
        print(chunk)

    print(f"\nTotal chunks: {len(chunks)}")
