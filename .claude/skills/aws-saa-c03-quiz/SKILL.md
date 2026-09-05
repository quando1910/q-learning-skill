---
name: aws-saa-c03-quiz
description: Runs one AWS Certified Solutions Architect - Associate (SAA-C03) practice question at a time, waits for the user's answer, then grades it and explains why each option is right or wrong. Use this whenever the user types /aws-saa-c03-quiz, asks for an AWS practice question, wants to study or drill for the AWS Solutions Architect Associate exam, asks to be quizzed on AWS architecture topics such as VPC, S3 storage classes, RDS, or cost optimization, or answers a question you previously asked from this skill.
---

# AWS SAA-C03 Quiz

Drill the user one exam-style question at a time. The value is in the grading: a correct
answer that the user guessed teaches nothing, so the explanation always covers why the
right option wins *and* why the tempting distractor loses.

## Asking a question

Run the picker rather than choosing a question by reading `questions.json`. Reading the
bank yourself biases you toward the first entries and puts the answer in your context
before the user has replied, which makes accidental leaking easy.

```bash
python3 .claude/skills/aws-saa-c03-quiz/scripts/quiz.py
```

Track the IDs already asked in this conversation and pass them so questions do not repeat:

```bash
python3 .claude/skills/aws-saa-c03-quiz/scripts/quiz.py --exclude sec-03,cost-01
```

If the user asks to focus on one area, add `--domain secure|resilient|performing|cost`.

Present the output as-is: the scenario, then the lettered options, then a one-line prompt
for the answer. Include the difficulty and domain so the user knows what they are facing.
Do not add hints, do not narrow the options, and do not comment on which option looks
plausible - that gives the answer away. When the question says SELECT: 2, tell the user to
pick two.

Then stop and wait. Do not reveal anything until the user replies.

## Grading the answer

Once the user answers, get the answer key:

```bash
python3 .claude/skills/aws-saa-c03-quiz/scripts/quiz.py --reveal sec-03
```

Reply in this shape:

```
Correct (or: Not quite - the answer is C)

**Why C** - <the explanation, in your own words, tied to what the scenario asked for>

**Why <the option the user picked> is wrong** - <the specific reason it fails here>

<One line naming the discriminator: the phrase in the stem that forces this answer,
e.g. "no long-term credentials" points at an instance role, "LEAST operational overhead"
points at the managed service.>
```

Keep it to that. A wall of text after every question is what makes people stop studying.
Only walk through all the remaining distractors if the user picked one of them or asks.

If the user answers with reasoning that is right for the wrong reason, say so - on the real
exam that reasoning fails on the next question.

If the user says they do not know, or asks for a hint, do not hand over the letter. Point
at the requirement in the stem that decides it and let them try again.

End by offering the next question. If they say yes, ask another straight away with the
updated `--exclude` list.

## Notes

The bank in `questions.json` holds 50 questions written in the style, domain mix, and
difficulty of the real exam. It is not reproduced exam content - AWS exam questions are
confidential, and using dumps is grounds for decertification.

When the picker prints `NO_QUESTIONS_LEFT`, say so and offer to start over with an empty
exclude list or to switch domains, rather than inventing a question - an invented question
with a subtly wrong answer key teaches the user something false.
