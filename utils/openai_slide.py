def generate_slide_deck(content_text: str, image_urls: list[str]) -> str:
    """
    Generates a simple Markdown-formatted slide deck using provided content and images.
    Compatible with FastAPI-based flow.

    Slides are separated by "---", and Markdown image syntax is used.
    """
    slides = []

    # Slide 1: Intro from lesson content
    if content_text:
        intro_slide = "# Slide 1: Introduction\n"
        intro_slide += content_text.strip()[:300] + ("..." if len(content_text) > 300 else "")
        slides.append(intro_slide)

    # Slide 2+: Visuals
    for i, url in enumerate(image_urls):
        if url:
            image_slide = f"# Slide {i + 2}: Visual {chr(65 + i)}\n"
            image_slide += f"![Image {i + 1}]({url})"
            slides.append(image_slide)

    # Fallback if nothing present
    if not slides:
        slides.append("# Slide 1: No content available.")

    return "\n---\n".join(slides)
