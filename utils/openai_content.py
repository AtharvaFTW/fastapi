import re
import os
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def call_gpt4o_for_lesson(reference_text):
    system_prompt = (
        "You are an expert teacher. Expand the reference text into a detailed, pedagogical lesson for students. "
        "Explain all concepts simply, add examples, and whenever a visual is needed, insert a detailed image prompt in the format [Draw: ...]. "
        "After each image prompt, insert [Image: ] as a placeholder for the image URL. Only use these formats."
    )
    user_prompt = f"Reference text:\n{reference_text}"

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=1500,
        temperature=0.5,
    )
    return response.choices[0].message.content

def generate_content(reference_text, sanitized_topic="topic"):
    lesson_text = call_gpt4o_for_lesson(reference_text)

    draw_pattern = r"\[Draw:(.*?)\]\s*\[Image:\s*\]"
    image_prompts = re.findall(draw_pattern, lesson_text, flags=re.DOTALL)

    img_urls = []
    for i, cue in enumerate(image_prompts):
        cue_clean = cue.strip()
        try:
            # Use DALL·E for image generation
            response = openai.images.generate(
                model="dall-e-3",
                prompt=cue_clean,
                n=1,
                size="1024x1024"
            )
            image_url = response.data[0].url
            img_urls.append(image_url)
        except Exception as e:
            img_urls.append("")

    # Replace placeholders with actual image markdown
    def replace_with_img(match):
        idx = replace_with_img.counter
        replace_with_img.counter += 1
        if idx < len(img_urls) and img_urls[idx]:
            return f"![Illustration]({img_urls[idx]})"
        else:
            return ""
    replace_with_img.counter = 0

    lesson_text_with_images = re.sub(draw_pattern, replace_with_img, lesson_text, flags=re.DOTALL)

    # Remove any stray prompt or placeholder
    lesson_text_with_images = re.sub(r"\[Draw:.*?\]", "", lesson_text_with_images, flags=re.DOTALL)
    lesson_text_with_images = re.sub(r"\[Image:\s*\]", "", lesson_text_with_images)

    return lesson_text_with_images.strip(), img_urls
