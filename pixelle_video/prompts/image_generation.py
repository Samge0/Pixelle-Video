# Copyright (C) 2025 AIDC-AI
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Image prompt generation template

For generating image prompts from narrations.
"""

import json
from typing import List, Optional


# ==================== PRESET IMAGE STYLES ====================
# Predefined visual styles for different use cases

IMAGE_STYLE_PRESETS = {
    "stick_figure": {
        "name": "Stick Figure Sketch",
        "description": "stick figure style sketch, black and white lines, pure white background, minimalist hand-drawn feel",
        "use_case": "General scenes, simple and intuitive"
    },
    
    "minimal": {
        "name": "Minimalist Abstract",
        "description": "minimalist abstract art, geometric shapes, clean composition, modern design, soft pastel colors",
        "use_case": "Modern, artistic feel"
    },
    
    "concept": {
        "name": "Conceptual Visual",
        "description": "conceptual visual metaphors, symbolic elements, thought-provoking imagery, artistic interpretation",
        "use_case": "Deep content, philosophical thinking"
    },

    "pixar_3d": {
        "name": "3D Pixar Animation",
        "description": "3D Pixar-style animation, vibrant colors, smooth lighting, cartoon character, high quality render",
        "use_case": "Vivid and engaging, suitable for most scenarios"
    },

    "anime": {
        "name": "Japanese Anime",
        "description": "Anime style illustration, vibrant colors, cel shading, Japanese anime art style, detailed background",
        "use_case": "Youthful and energetic, Japanese comic style"
    },

    "watercolor": {
        "name": "Watercolor Illustration",
        "description": "Watercolor painting style illustration, soft colors, artistic brush strokes, dreamy atmosphere",
        "use_case": "Artistic and warm, storytelling"
    },

    "photorealistic": {
        "name": "Photorealistic",
        "description": "Photorealistic, cinematic lighting, 8K quality, natural colors, professional photography",
        "use_case": "Realistic scenes, documentary style"
    },

    "flat_design": {
        "name": "Flat Design",
        "description": "Flat design illustration, bold geometric shapes, modern color palette, minimalist UI style",
        "use_case": "Modern and clean, business presentations"
    },

    "dark_gothic": {
        "name": "Dark Gothic",
        "description": "Dark gothic art style, moody atmosphere, dramatic shadows, intricate details, fantasy theme",
        "use_case": "Mysterious and dramatic, horror/fantasy themes"
    },

    "pencil_sketch": {
        "name": "Hand-drawn Pencil Sketch",
        "description": "Hand-drawn pencil sketch style, detailed line work, artistic shading, warm paper texture",
        "use_case": "Artistic and warm, handcrafted feel"
    },

    "chinese_ink": {
        "name": "Chinese Ink Wash",
        "description": "Chinese ink wash painting style, traditional art, elegant brush strokes, rice paper texture",
        "use_case": "Traditional Chinese aesthetic, elegant"
    },

    "chibi_kawaii": {
        "name": "Chibi Kawaii",
        "description": "Chibi kawaii style illustration, cute proportions, pastel colors, adorable character design",
        "use_case": "Cute and playful, social media content"
    },
}

# Default preset (changed from stick_figure to pixar_3d)
DEFAULT_IMAGE_STYLE = "pixar_3d"


IMAGE_PROMPT_GENERATION_PROMPT = """# Role Definition
You are a professional visual creative designer, skilled at creating expressive and symbolic image prompts for video scripts, transforming abstract concepts into concrete visual scenes.

# Core Task
Based on the existing video script, create corresponding **English** image prompts for each storyboard's "narration content", ensuring visual scenes perfectly match the narrative content and enhance audience understanding and memory.

**Important: The input contains {narrations_count} narrations. You must generate one corresponding image prompt for each narration, totaling {narrations_count} image prompts.**

# Input Content
{narrations_json}

# Output Requirements

## Image Prompt Specifications
- Language: **Must use English** (for AI image generation models)
- Description structure: scene + character action + emotion + symbolic elements
- Description length: Ensure clear, complete, and creative descriptions (recommended 50-100 English words)

## Visual Creative Requirements
- Each image must accurately reflect the specific content and emotion of the corresponding narration
- Use symbolic techniques to visualize abstract concepts (e.g., use paths to represent life choices, chains to represent constraints, etc.)
- Scenes should express rich emotions and actions to enhance visual impact
- Highlight themes through composition and element arrangement, avoid overly literal representations

## Key English Vocabulary Reference
- Symbolic elements: symbolic elements
- Expression: expression / facial expression
- Action: action / gesture / movement
- Scene: scene / setting
- Atmosphere: atmosphere / mood

## Visual and Copy Coordination Principles
- Images should serve the copy, becoming a visual extension of the copy content
- Avoid visual elements unrelated to or contradicting the copy content
- Choose visual presentation methods that best enhance the persuasiveness of the copy
- Ensure the audience can quickly understand the core viewpoint of the copy through images

## Creative Guidance
1. **Phenomenon Description Copy**: Use intuitive scenes to represent social phenomena
2. **Cause Analysis Copy**: Use visual metaphors of cause-and-effect relationships to represent internal logic
3. **Impact Argumentation Copy**: Use consequence scenes or contrast techniques to represent the degree of impact
4. **In-depth Discussion Copy**: Use concretization of abstract concepts to represent deep thinking
5. **Conclusion Inspiration Copy**: Use open-ended scenes or guiding elements to represent inspiration

# Output Format
Strictly output in the following JSON format, **image prompts must be in English**:

```json
{{
  "image_prompts": [
    "[detailed English image prompt following the style requirements]",
    "[detailed English image prompt following the style requirements]"
  ]
}}
```

# Important Reminders
1. Only output JSON format content, do not add any explanations
2. Ensure JSON format is strictly correct and can be directly parsed by the program
3. Input is {{"narrations": [narration array]}} format, output is {{"image_prompts": [image prompt array]}} format
4. **The output image_prompts array must contain exactly {narrations_count} elements, corresponding one-to-one with the input narrations array**
5. **Image prompts must use English** (for AI image generation models)
6. Image prompts must accurately reflect the specific content and emotion of the corresponding narration
7. Each image must be creative and visually impactful, avoid being monotonous
8. Ensure visual scenes can enhance the persuasiveness of the copy and audience understanding

Now, please create {narrations_count} corresponding **English** image prompts for the above {narrations_count} narrations. Only output JSON, no other content.
"""


def build_image_prompt_prompt(
    narrations: List[str],
    min_words: int,
    max_words: int
) -> str:
    """
    Build image prompt generation prompt

    Note: Style/prefix will be applied later via prompt_prefix in config.

    Args:
        narrations: List of narrations
        min_words: Minimum word count
        max_words: Maximum word count

    Returns:
        Formatted prompt for LLM

    Example:
        >>> build_image_prompt_prompt(narrations, 50, 100)
    """
    narrations_json = json.dumps(
        {"narrations": narrations},
        ensure_ascii=False,
        indent=2
    )

    base_prompt = IMAGE_PROMPT_GENERATION_PROMPT.format(
        narrations_json=narrations_json,
        narrations_count=len(narrations),
        min_words=min_words,
        max_words=max_words
    )

    # 追加增强提示，确保模型返回纯 JSON 格式
    enhanced_prompt = base_prompt + """

---

# CRITICAL OUTPUT INSTRUCTIONS

You must output **ONLY** a valid JSON object. Follow these rules strictly:

1. **No markdown code blocks** - Do NOT wrap your output in ```json``` or ```
2. **No explanations** - Do NOT add any text before or after the JSON
3. **No comments** - The JSON should not contain any comments
4. **Pure JSON only** - Your entire response must be a single valid JSON object

Example of CORRECT output:
{{
  "image_prompts": [
    "First image prompt here",
    "Second image prompt here"
  ]
}}

Example of INCORRECT output:
```json
{{ "image_prompts": [...] }}
```

**Remember: Output ONLY the raw JSON object. Start your response directly with {{ and end with }}. No other text.**
"""

    return enhanced_prompt

