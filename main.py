
from pypdf import PdfReader


def extract_text(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)

    extracted_pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()

        if text:
            extracted_pages.append(text)

        print(f"Processed page {page_number}")

    return "\n".join(extracted_pages)


if __name__ == "__main__":
    text = extract_text("sample.pdf")

    print("\n--- Extracted Text ---\n")
    print(text[:3000])

    print(f"\nTotal characters extracted: {len(text)}")
