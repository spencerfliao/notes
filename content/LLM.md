
[[神经网络真的像大脑结构吗]]

- data: text sequence
- tokenization
	- converts to numbers + byte pair encoding iteratively merge common pairs
	- reduce vocab size (≈ 10w) & generalize better with subwords handling unknown ones
- transformer
	- input: sequence tokens + parameters (≈ hundreds of billions / 几千亿)
	- process them with a complex math function
- SFT
	- next token probability distribution
	- adjust weights so to produce more correct probabilities
	- base model: generative, not conversional
- post-train
	- prompt-response tokens to train for conversations
	- copied data, rigid, limited
- RLHF
	- separate reward model trained by ranking responses to learn preference
	- scalable, consistent, adaptable
- hallucination
	- simulation, not recall (also simulated confidence confidence) [[Memory]]
	- solution: train it to admit ignorance for input it's ignorant of