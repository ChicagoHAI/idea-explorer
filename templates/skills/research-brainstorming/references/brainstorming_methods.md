# Additional Brainstorming Methods

## Six Thinking Hats

Systematically examine ideas from different perspectives.

### The Hats

| Hat | Focus | Questions |
|-----|-------|-----------|
| **White** | Facts | What do we know? What data do we have? |
| **Red** | Feelings | What's our gut reaction? What feels right? |
| **Black** | Caution | What could go wrong? What are the risks? |
| **Yellow** | Benefits | What are the advantages? Why might this work? |
| **Green** | Creativity | What alternatives exist? What's a new angle? |
| **Blue** | Process | What's our next step? How should we proceed? |

### Application to Research Ideas

```markdown
## Six Hats Analysis: [Idea]

### White Hat (Facts)
- What prior work exists?
- What data is available?
- What resources do we have?

### Red Hat (Intuition)
- Does this feel like a good direction?
- What's exciting about it?
- What makes us hesitate?

### Black Hat (Risks)
- What could go wrong?
- Why might this fail?
- What are the weaknesses?

### Yellow Hat (Benefits)
- Why might this work?
- What's the potential impact?
- What advantages does this have?

### Green Hat (Alternatives)
- What other approaches exist?
- How could we modify this?
- What haven't we considered?

### Blue Hat (Process)
- What's our next step?
- How do we test this?
- What's the timeline?
```

---

## Random Input Technique

Use random stimuli to spark new connections.

### Method

1. Select a random word, image, or concept
2. List attributes of the random input
3. Force connections to your problem
4. Explore unexpected associations

### Random Word Prompts for ML

| Word | Attribute | ML Connection |
|------|-----------|---------------|
| River | Flowing, branching | Data streams, tree structures |
| Garden | Growing, pruning | Model training, pruning |
| Orchestra | Coordination, harmony | Ensemble methods |
| Kitchen | Recipes, ingredients | Model composition |
| Library | Organization, search | Retrieval, indexing |

### Template

```markdown
## Random Input: [Word]

### Attributes
1. [Attribute 1]
2. [Attribute 2]
3. [Attribute 3]

### Connections to [Problem]
| Attribute | Possible Connection |
|-----------|---------------------|
| | |

### Ideas Generated
1. [Idea from connection]
```

---

## Wishful Thinking

Start from the ideal solution and work backwards.

### Process

1. Imagine the perfect solution exists
2. Describe what it would do
3. Work backwards to identify requirements
4. Find stepping stones toward the ideal

### Template

```markdown
## Wishful Thinking: [Problem]

### The Ideal Solution
If we could have anything, our solution would:
- [Capability 1]
- [Capability 2]
- [Capability 3]

### What Would That Require?
| Capability | Requirement |
|------------|-------------|
| | |

### Stepping Stones
What intermediate solutions get us closer?
1. [Step 1]: Gets us [partial capability]
2. [Step 2]: Adds [additional capability]

### First Practical Step
[What we can do now toward this vision]
```

---

## Provocation (Po)

Make deliberately provocative statements to escape conventional thinking.

### Method

1. Make an outrageous statement (Po: ...)
2. Don't judge - explore implications
3. Extract useful ideas from the provocation

### Examples

| Provocation | Exploration | Useful Insight |
|-------------|-------------|----------------|
| Po: Models should forget | What if forgetting was useful? | Catastrophic forgetting as feature |
| Po: Training should be random | What if we didn't optimize? | Random search, evolutionary methods |
| Po: Labels are harmful | What if labels constrain? | Self-supervised learning |
| Po: Bigger is worse | What if scale hurts? | Efficiency, compute-optimal training |

### Template

```markdown
## Provocation: [Topic]

### Statement
Po: [Outrageous claim]

### Exploration (Suspend Judgment)
- What would this world look like?
- What would be the consequences?
- When might this actually be true?

### Extracted Ideas
- [Practical idea derived from provocation]
```

---

## Concept Fan

Expand from specific problem to broader concepts.

### Structure

```
                    [Broad Purpose]
                          |
            [General Direction 1]  [General Direction 2]
                    |                       |
        [Specific 1] [Specific 2]  [Specific 3] [Specific 4]
```

### Example: Improving Translation

```
                [Help people communicate across languages]
                              |
        [Improve translation]         [Reduce need for translation]
              |                                    |
    [Better models]  [Better data]    [Language learning]  [Universal language]
         |               |                   |
  [Architecture] [Training]           [AI tutors]
```

### Application

When stuck on a specific solution:
1. Go up: What's the broader goal?
2. Generate alternatives at higher level
3. Go down: What specific approaches serve this?

---

## Storyboarding

Visualize the research process or user experience.

### Research Storyboard

| Stage | What Happens | Key Questions |
|-------|--------------|---------------|
| 1. Problem | User encounters issue | What triggers the need? |
| 2. Current solution | User tries existing tools | What's frustrating? |
| 3. Discovery | User finds our method | How do they learn about it? |
| 4. Usage | User applies method | What's the experience? |
| 5. Outcome | User gets results | What changes for them? |

### Template

```markdown
## Research Storyboard: [Project]

### Scene 1: The Problem
**Who**: [User/researcher type]
**Situation**: [What they're trying to do]
**Frustration**: [What's not working]

### Scene 2: Current Approach
**What they try**: [Existing methods]
**Result**: [Why it's insufficient]

### Scene 3: Our Solution
**What we offer**: [Our contribution]
**How it helps**: [Specific improvement]

### Scene 4: The Outcome
**Result**: [What they achieve]
**Impact**: [Why this matters]
```

---

## Systematic Inventive Thinking (SIT)

Apply thinking templates to generate ideas.

### Templates

1. **Subtraction**: Remove a component, see what happens
2. **Multiplication**: Copy and modify a component
3. **Division**: Reorganize components
4. **Task Unification**: Assign new purpose to existing component
5. **Attribute Dependency**: Make attributes depend on each other

### ML Applications

| Template | ML Example |
|----------|------------|
| Subtraction | Remove attention (MLP-only models) |
| Multiplication | Multiple prediction heads |
| Division | Split processing (early exit, mixture of experts) |
| Task Unification | Encoder as classifier |
| Attribute Dependency | Adaptive computation based on input |

---

## Quick Ideation Prompts

Use these to quickly generate ideas:

### Fill-in-the-blank

- "What if [Method A] could also [Capability B]?"
- "How would [Researcher X] approach this problem?"
- "What's the [Task] equivalent of [Breakthrough in other area]?"
- "If we couldn't use [Common approach], what would we do?"
- "What would make [Current benchmark] obsolete?"

### Constraint-based

- "How would we solve this with 10x less compute?"
- "How would we solve this with no labeled data?"
- "How would we solve this in real-time?"
- "How would we make this work on a phone?"

### Future-casting

- "What will be obvious in 5 years that we're missing now?"
- "What problem will emerge as current ones are solved?"
- "What capability would unlock new applications?"
