# General Notes and Ideas

## Avoid Model Choking

We don't want a model to choke in training from having too much overlapping training data within a very narrow domain. We need a way to isolate training data into domains so that the LLM doesn't get bogged down with too much information in the same domain. So that means for each essay submission we have to identify cetain parameters and then place the essay in the correct domain. Somehow, based off the parameters, there will be an adjustment to the prompt to adjust its domain and give the LLM more ability to learn.

## Dynamic Training Pair

Right now all training prompts are fixed. At least some kind of essay unique training pairs should be created dynamically. Maybe some kind of idea web? Maybe can integrate with (1)

## A

Should probably take a collection of either essays, or maybe a collection of answers for the same subquestion and have a system of prompt-completion pairs generated there.

## B

Should all prompts be questions? I think so because we're doing a chain of thought training model, but maybe we need to go the other way somewhere to get a solid continued loop.

## C

Need to create a chain of thought base model that relies heavily on the subquestions. Essentially we'll train it to rely heavily on those questions and potential answers as part of its broader chain of thought. That's also why we'll need a lot of questions to have reasonable entry and exit points from real world questions to real world answers.

### CA

I suppose we can train it to get a reasonable list of which questions apply to a given sample issue. And that's chain of thought step (a) getting it to reasonably relate a general issue to think about to a set of the questions we have. Step two is to get it to reasonably evaluate how the questions relate to an issue, and then relate it back to the real world through logical evaluation training. I'd have to make sure to take domains into account too.
