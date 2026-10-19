# Retrieval-Augmented Generation

Retrieval-augmented generation (RAG) adds an external retrieval step before generation. A query is used to find relevant passages from a knowledge source and those passages are supplied to the language model as context. This makes it possible to update the knowledge source without retraining the model.

RAG is useful when answers need to reflect changing or private information. The retrieval layer can also expose the passages used for an answer, which makes source inspection easier than relying only on knowledge stored in model weights.

RAG has failure modes of its own. Poor chunking, weak retrieval, missing documents, or irrelevant context can cause an otherwise capable model to answer badly. Retrieval quality should therefore be evaluated separately from final answer quality.
