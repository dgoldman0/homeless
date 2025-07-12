# General Notes and Ideas

1. We need a way to isolate training data into domains so that the LLM doesn't get bogged down with too much information in the same domain. So that means for each essay submission we have to identify cetain parameters and then place the essay in the correct domain. Somehow, based off the parameters, there will be an adjustment to the prompt to adjust its domain and give the LLM more ability to learn.

2. At least some kind of essay unique training pairs should be created dynamically. Maybe some kind of idea web? Maybe can integrate with (1)

3. Should probably take a collection of either essays, or maybe a collection of answers for the same subquestion and have a system of prompt-completion pairs generated there.

4. Need to create a chain of thought base model that relies heavily on the subquestions. Essentially we'll train it to rely heavily on those questions and potential answers as part of its broader chain of thought. That's also why we'll need a lot of questions to have reasonable entry and exit points from real world questions to real world answers.

  a. I suppose we can train it to get a reasonable list of which questions apply to a given sample issue. And that's chain of thought step (a) getting it to reasonably relate a general issue to think about to a set of the questions we have. Step two is to get it to reasonably evaluate how the questions relate to an issue, and then relate it back to the real world through logical evaluation training. 

