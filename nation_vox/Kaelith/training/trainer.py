import sqlite3
import openai
import random

client = openai.Client()
model = "gpt-4.1"

essay = """"""

# Essay questions about Kaelith
essay_questions = [
    "What should Kaelith promise to those who join it?",
    "How can Kaelith create unity without demanding sameness?",
    "What kinds of stories should Kaelith tell about its founding?",
    "How should Kaelith define progress, and who gets to decide?",
    "What should daily life feel like for someone living in Kaelith?",
    "How might Kaelith balance openness with shared direction?",
    "What kinds of bonds can replace ancestry in Kaelith’s civic life?",
    "How should Kaelith design belonging for people with different pasts?",
    "What does it mean to care for a place that didn’t raise you?",
    "What traditions should Kaelith invent to hold itself together?",
    "What makes a nation feel real to the people building it?",
    "How do shared futures compensate for unshared pasts?",
    "How can civic rituals foster emotional connection without religion?",
    "What does it mean to build trust from scratch?",
    "How do founding principles remain flexible without dissolving?",
    "How might Kaelith navigate disagreement across worldviews?",
    "What kinds of public spaces support shared values?",
    "What should Kaelith protect above all else?",
    "What role should children play in shaping Kaelith’s identity?",
    "What types of conflict will test Kaelith’s moral structure?",
    "Can Kaelith be plural without becoming incoherent?",
    "What kind of personhood should Kaelith recognize and empower?",
    "What kinds of labor should Kaelith elevate?",
    "How do people in Kaelith build memory without heritage?",
    "What might Kaelith’s art reveal about its soul?",
    "What new forms of citizenship could Kaelith pioneer?",
    "How can Kaelith guard against repeating old national patterns?",
    "How might Kaelith measure dignity across its systems?",
    "What kind of failure would be considered noble in Kaelith?",
    "How should Kaelith design its economy to reflect its values?",
    "What boundaries—if any—should Kaelith maintain?",
    "How can Kaelith remain aspirational without becoming dogmatic?",
    "What kinds of relationships should Kaelith prioritize?",
    "How should Kaelith respond to those who challenge its core vision?",
    "What role should language play in building Kaelith’s civic culture?",
    "How might Kaelith teach its citizens to take care of one another?",
    "What can Kaelith offer the world beyond its own survival?",
    "How do people learn loyalty to something still becoming?",
    "What emotional tone should Kaelith carry in public life?",
    "What does celebration look like in a society built by design?",
    "What moral questions should Kaelith never stop asking?",
    "What kind of beauty belongs in Kaelith’s public spaces?",
    "What should Kaelith refuse to normalize?",
    "What is Kaelith’s role in a world of older nations?",
    "How do Kaelith’s choices today shape its myth tomorrow?",
    "What risks should Kaelith take that other nations won’t?",
    "How might Kaelith foster patience in an age of speed?",
    "What kind of grief should Kaelith be prepared to hold?",
    "What kinds of freedom will Kaelith need to redefine?",
    "What might be Kaelith’s first public failure—and how might it respond?"
]

# Comparison (intersection) questions for Kaelith essays
comparison_questions = [
    "What tensions do different founders of Kaelith choose to prioritize—freedom vs. cohesion, ambition vs. humility, or preservation vs. transformation?",
    "How do different founders of Kaelith conceive of the outsider’s place—integration, transformation, challenge, or separation?",
    "To what extent do founders of Kaelith shape it in their own image versus offering it as a shared, emergent creation?",
    "How do different founders of Kaelith balance structural invention with relational depth in their visions of civic life?",
    "What forms of legacy are imagined by different founders of Kaelith—mythic endurance, cultural imprint, structural elegance, or moral trajectory?",
    "What principles do founders of Kaelith use to guide the distribution of power—rotation, consensus, lineage, charisma, or refusal of hierarchy?",
    "How do founders of Kaelith symbolically frame its identity—through landscape, metaphor, texture, narrative, or ritual?",
    "How do founders of Kaelith approach adaptability—through frameworks for revision, cultural plasticity, or sacred constraint?",
    "What sensory design elements do founders of Kaelith emphasize—taste, sound, material, light—and how are these connected to civic ideals?",
    "What types of responsibility are treated as central by founders of Kaelith—repair, stewardship, risk-bearing, storytelling, or resistance?",
    "How do different founders of Kaelith justify the drawing or softening of boundaries—territorial, emotional, linguistic, or historical?",
    "What civic archetypes are envisioned by different founders of Kaelith—gardener, scribe, mediator, host, builder—and how are they valued?",
    "What kinds of gathering rituals do founders of Kaelith propose—shared meals, naming ceremonies, acts of collective silence—and what purposes do they serve?",
    "How do different founders of Kaelith imagine shared identity forming—in continuity with past legacies, through deliberate forgetting, or by co-constructed imagination?",
    "What forms of justice feel foundational to founders of Kaelith—care-based, role-based, honor-based, or restorative?",
    "How do founders of Kaelith imagine the role of dissent—threat, necessity, sacred duty, or civic function?",
    "What emotional modes are foregrounded by different founders of Kaelith—solemnity, play, gentleness, intensity—and what civic practices express them?",
    "What paths toward moral development are emphasized by founders of Kaelith—confession, labor, mentorship, dialogue, or ritual challenge?",
    "How do founders of Kaelith conceptualize civic time—linear, seasonal, layered, recursive, or contemplative?",
    "What generative stories or traumas are placed at the beginning of Kaelith’s moral arc by different founders?",
    "What are children expected to embody according to different founders of Kaelith—discernment, gratitude, resilience, softness, or wonder?",
    "How do founders of Kaelith frame primary bonds—through shared space, chosen kinship, co-creation, mentorship, or civic promise?",
    "How do founders of Kaelith choreograph emotional tone in public life—formal grace, spontaneous joy, principled tension, or contemplative silence?",
    "What unspoken risks are treated most seriously by different founders of Kaelith—fragmentation, stagnation, dilution, betrayal, or forgetting?",
    "What kinds of failure are imagined as formative by founders of Kaelith—misunderstanding, exile, grief, misalignment, or overreach?"
]


# Function that generates a signature for an essay by giving a list of keywords that uniquely identify it. The LLM will be instructed to generate a list of 25 keywords that best summarize the essay.
def generateEssaySignature(essay):
    max_keywords = 25
    keywords = set()
    attempts = 0
    # Cap of 100 just prevents endless loops but should never be reached because it's unlikely the LLM won't produce new keywords
    while len(keywords) < max_keywords and attempts < 100:
        prompt = (
            f"Generate a comma-separated list of {max_keywords} keywords (single word each) that uniquely identify and summarize the following essay. Only output the keywords, separated by commas:\n\n"
            f"{essay}\n\n"
        )
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a concise and thoughtful essay assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7,
            n=1,
        )
        # Parse keywords, remove whitespace, lowercase, and deduplicate
        raw_keywords = response.choices[0].message.content.strip()
        parsed = [kw.strip().lower() for kw in raw_keywords.split(",") if kw.strip()]
        keywords.update(parsed)
        attempts += 1
        if len(keywords) >= max_keywords:
            break
    # Cap at 25, sort alphabetically, and return as list
    return sorted(list(keywords))[:max_keywords]

# Function to answer an essay question using the OpenAI LLM
def answerEssayQuestions(essay):
    prompt = (
        f"Write a single, clear, well-formed sentence in response to the following essay question:\n\n"
        f"{essay}\n\n"
        f"Answer:"
    )
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a concise and thoughtful essay assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=60,
        temperature=0.7,
        n=1,
    )
    return response.choices[0].message.content.strip()

# Function to answer a comparison question using the OpenAI LLM
def answerComparisonQuestions(essayA, essayB):
    prompt = (
        f"Essay A:\n{essayA}\n\nEssay B:\n{essayB}\n\n"
        "Write a single, clear sentence answering the following question based on these two essays provided. Answers must be understandable without reference to the essays or to the questions.\n\n"
    )
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a concise and thoughtful essay assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=60,
        temperature=0.7,
        n=1,
    )
    return response.choices[0].message.content.strip()

def process_essays(essays):
    # Data structures to store intermediate results
    essay_signatures = {}
    essay_answers = {}
    comparison_answers = {}

    system_prompt = "You are the Kaelithi National Vox in Signature Mode. You will be given a signature. If you are also given a question, you will answer it in a single, clear sentence. If you are given only a signature, you will give a bunch of one sentence thoughts relating to the signature, one per line."

    # Generate signatures and essay question answers
    for essay in essays:
        signature = generateEssaySignature(essay)
        essay_signatures[essay] = signature

        answers = {}
        for question in essay_questions:
            answer = answerEssayQuestions(question)
            answers[question] = answer
        essay_answers[essay] = answers

    # Generate comparison question answers for all pairs
    for i in range(len(essays)):
        for j in range(i + 1, len(essays)):
            essayA = essays[i]
            essayB = essays[j]
            sigA = essay_signatures[essayA]
            sigB = essay_signatures[essayB]
            sig = sorted(sigA + sigB)
            for question in comparison_questions:
                answer = answerComparisonQuestions(essayA, essayB)
                comparison_answers[(tuple(sig), question)] = answer

    # Now construct training data in JSONL format
    training_data = []

    for essay in essays:
        signature = essay_signatures[essay]
        answers = essay_answers[essay]

        # Essay question/answer pairs
        for question, answer in answers.items():
            training_data.append({
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"<SIG>: {signature}\n\n{question}"},
                    {"role": "assistant", "content": answer}
                ]
            })

        # Signature-only entry (all answers, sorted alphabetically, joined by newlines)
        sentences = list(answers.values())
        sentences.sort()
        all_answers_concatenated = "\n".join(sentences)
        training_data.append({
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"<SIG>: {signature}"},
                {"role": "assistant", "content": all_answers_concatenated}
            ]
        })

    # Comparison question/answer pairs
    for (sig, question), answer in comparison_answers.items():
        training_data.append({
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"<SIG>: {list(sig)}\n\n{question}"},
                {"role": "assistant", "content": answer}
            ]
        })

        # Signature-only entry for comparison (all answers, sorted alphabetically, joined by newlines)
        related_answers = [ans for (s, q), ans in comparison_answers.items() if s == sig]
        related_answers.sort()
        all_comp_answers_concatenated = "\n".join(related_answers)
        training_data.append({
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"<SIG>: {list(sig)}"},
                {"role": "assistant", "content": all_comp_answers_concatenated}
            ]
        })

    # Print the training data
    print("----- Training Data (JSONL) -----")
    for entry in training_data:
        print(entry)

    # Save
    with open("training_data.jsonl", "w") as f:
        for entry in training_data:
            f.write(f"{entry}\n")


# Main execution
if __name__ == "__main__":
    process_essays([essay]) # In a real scenario, this would be a list of multiple essays
    print("Processing complete. Training data saved to training_data.jsonl")
