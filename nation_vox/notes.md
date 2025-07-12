# General Notes and Ideas

1. We need a way to isolate training data into domains so that the LLM doesn't get bogged down with too much information in the same domain. So that means for each essay submission we have to identify cetain parameters and then place the essay in the correct domain. Somehow, based off the parameters, there will be an adjustment to the prompt to adjust its domain and give the LLM more ability to learn.

2. At least some kind of essay unique training pairs should be created dynamically. Maybe some kind of idea web? Maybe can integrate with (1)

3. Should probably take a collection of either essays, or maybe a collection of answers for the same subquestion and have a system of prompt-completion pairs generated there.
