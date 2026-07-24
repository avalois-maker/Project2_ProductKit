Initially we will be creating a proof on concept on a single feature to control for relevant output. Once we confirm that the feature launch kit works, we can then test it more broadly on different features. At this point, implementing an RAG on the product feature release database would be a useful next step so the AI solution can replicate and scale to all organization’s product development process. For the MVP, we will have a library where the agent can gather inputs in needs for context and it will use those to generate outputs.
*Corpus size & structure*
— we converted all required documents to .md files to limit processing and retrieval. We also broke the outputs into 3 separate agents so only needed files are part of the prompt to keep it small. 
*Change frequency*
— For the MVP we keep KB static provided it gives us the output required. All updates will be manual as part of iteration.
*Query diversity*
— Questions are limited to 3 pormpts and only iterated strictly as required.
*Complexity vs 2-day scope*
— We have a branding guidelines.md file to provide needed context.