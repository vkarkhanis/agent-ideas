---
title: professional_profile_chatbox
app_file: ppc.py
sdk: gradio
sdk_version: 6.0.2
---
### When running the ppc.py app locally use the following command from root directory (agent-ideas):
```uv run src/professional_profile_chatbox/ppc.py```

### Deployment to HuggingFace
#### From src/professional_profile_chatbox folder, run the following command
``` gradio deploy ```

### Important Notes:
1. Any import dependency added to the code will have to be manually added to requirements.txt file under Files tab on HuggingFace portal
2. https://huggingface.co/spaces/vkarkhanis/professional_profile_chatbox - public URL to access the chatbox
3. Provide secret keys for: PUSHOVER_TOKEN, PUSHOVER_USER, OPENAI_API_KEY, PERPLEXITY_API_KEY (Optional) when deploying
4. Any changes to files in resources directory will have to be manually uploaded under Files directory on HuggingFace portal