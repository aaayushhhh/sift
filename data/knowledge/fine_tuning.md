# Fine-tuning language models

Fine-tuning changes model behavior by training on additional examples. It is often useful for teaching a consistent response style, task format, domain terminology, or behavior that should be applied repeatedly.

Fine-tuning is not usually the simplest way to keep a large body of factual knowledge current. When the underlying facts change frequently, the training data and model may need to be updated again. A retrieval system can be easier to refresh because the external corpus can change independently of the model.

Fine-tuning and retrieval are not mutually exclusive. A system can fine-tune for behavior or formatting while retrieving current domain knowledge at runtime.
