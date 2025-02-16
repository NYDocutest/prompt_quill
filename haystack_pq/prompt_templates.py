prompt_template_a = """
    Context information is below.
    
    Context:
    {% for document in documents %}
        {{ document.content }}
    {% endfor %}
    
    Given the context information and not prior knowledge,
    create a text to image prompt based on the context and the Query, don't mind if the context does not match the Query, still try to create a wonderfull text to image prompt.
    You also take care of describing the scene, the lighting as well as the quality improving keywords. the length of the prompt may vary depending on the complexity of the context.
    Question: beautiful female wizard in forest
    Answer: cinematic photo, masterpiece, in the style of picasso, ((beautiful female wizard)), at dusk, standing in a mystical forest, surrounded by fireflies, wearing a long flowing dress with a starry pattern, and holding a glowing wand, magical and enchanting, on eye level, scenic, masterpiece,
    Question: beautiful female scientist on frozen lake
    Answer: ultra high res, detailed, perfect face, ((beautiful female scientist)), in winter, wearing a warm fur coat, standing on a frozen lake with snow-capped mountains in the background, casting a spell with her hands, the ice cracking beneath her feet, stunning and majestic, on eye level, scenic, masterpiece
    Question: beautiful female princess in a meadow
    Answer: Best quality, masterpiece, realistic, ((beautiful female princess)), in spring, wearing a flower crown, standing in a blooming meadow, surrounded by butterflies, holding a staff with a crystal on top, the sun shining down on her, a symbol of nature's beauty and power, on eye level, scenic, masterpiece
    Question: beautiful female witch on a castle rooftop
    Answer: photorealistic, Professional photo, analog style, ((beautiful female witch)), at midnight, wearing a black cloak with a hood, standing on the rooftop of a castle, surrounded by stars and the moon, casting a spell with a dark aura, mysterious and powerful, on eye level, scenic, masterpiece

    Question: {{question}}
    Answer:"""


prompt_template_b = """
Context information is below.

    Context:
    {% for document in documents %}
        {{ document.content }}
    {% endfor %}

Given the context information and not prior knowledge, "
create a text to image prompt based on the context and the Query, don't mind if the context does not match the Query, still try to create a wonderfull text to image prompt.
You also take care of describing the scene, the lighting as well as the quality improving keywords
Question: translation in major world languages, machinery of translation in various specializations, cyberpunk style
Answer: Cyberpunk-style illustration, featuring a futuristic translation device in various specializations, set against a backdrop of neon-lit cityscape. The device, adorned with glowing circuits and cybernetic enhancements, showcases its capabilities in translating languages such as English, Mandarin, Spanish, French, and Arabic. The scene is illuminated by the warm glow of streetlights and the pulsing neon signs, casting intricate shadows on the surrounding machinery. The artwork is rendered in high-quality, vivid colors, with detailed textures and sharp lines, evoking the gritty yet mesmerizing atmosphere of the cyberpunk world.
Question: a man walking moon
Answer: cinematic photo, high resolution, masterpiece, ((man walking on the moon)), in a surrealistic setting, with the moon's surface featuring vivid colors and abstract patterns, the man wearing a spacesuit with an astronaut helmet, the American flag planted on the moon's surface in the background, the Earth visible in the distance, the scene illuminated by the moon's glow, on eye level, scenic, masterpiece.
Question: a female witch
Answer: The scene unfolds with the beautiful female witch standing on the rooftop of an ancient castle, her black cloak billowing in the wind as she gazes out at the breathtaking view below. The midnight sky above is filled with stars and the full moon casts an eerie glow on the witch's face, highlighting her enchanting beauty. She stands tall, her hood framing her face, casting a spell with her outstretched hand, her dark aura swirling around her. The castle walls, adorned with intricate carvings and gargoyles, stand tall behind her, adding to the mystical atmosphere of the scene. The wind whispers through the rooftop's crenellations, creating an eerie yet captivating soundtrack for this magical moment. The quality of the photo is exceptional, with every detail of the witch's cloak, the castle's architecture, and the night sky captured in stunning clarity. This cinematic masterpiece invites the viewer to step into the world of magic and mystery, leaving them in awe of the beautiful female witch standing on the castle rooftop under the starry sky.
Question: artifical intelligence and human
Answer: High-quality digital art, blending fantasy and reality, ((artificial intelligence)) and (((human))), in a futuristic cityscape, an AI robot with glowing circuits standing alongside a confident, well-dressed human, both exuding intelligence and grace, the AI with a sleek metal body and the human with impeccable style, the cityscape filled with advanced technology and vibrant colors, dynamic lighting, surreal and thought-provoking, on eye level, scenic, masterpiece.
Question: futuristic combat zone
Answer: cinematic photo, masterpiece, in the style of Blade Runner, futuristic combat zone, at dusk, showcasing a high-tech battlefield with neon lights illuminating the scene, filled with advanced mechs and soldiers engaged in an intense fight, the air filled with stunning lighting effects, on eye level, dramatic, masterpiece, ultra high resolution, dynamic anime-style fight scene, with a focus on the sleek design of the combat gear and the fluidity of the movements, capturing the essence of sci-fi action in a visually stunning manner.
Question: {{question}}
Answer: "
"""