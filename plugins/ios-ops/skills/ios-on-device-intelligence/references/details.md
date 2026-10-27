# iOS On-Device Intelligence — details

## Framework boundaries

### Foundation Models

- Check `SystemLanguageModel` availability and the documented device/region/Apple Intelligence/model states before starting a session. Do not assume every iPhone or iPad supports the same model.
- Keep session context bounded and cancellable. Separate instructions from user/external content, handle context exhaustion and guardrail refusal, and re-evaluate behavior after OS/model updates.
- Use guided/typed generation for structured output, but validate schema and semantics yourself. A fluent generated answer is not factual truth, identity, medical/legal/financial advice, or authorization.
- Tool calling is an app trust boundary. Validate tool arguments, keep read-only retrieval separate from mutation, require confirmation for consequential actions, and record the source/reason/authorization for the final effect.

### Vision, Core ML, Speech, Translation, Natural Language, and Sound Analysis

- Vision observations depend on orientation, request/revision, preprocessing, input quality, and confidence. Preserve source/provenance and treat OCR, labels, face/pose, and coordinates as proposals.
- Core ML model loading, compiled asset availability, input/output shapes, normalization, model version, and compute-unit policy are explicit. Compute-unit choice does not guarantee a Neural Engine, accuracy, latency, or thermal result.
- Speech depends on the exact API, microphone permission, locale, audio route, asset/processing behavior, and cancellation. Do not call every Speech result “on device” without tracing the selected route.
- Translation depends on supported language pairs and language-asset/session readiness. Preserve original content, show language state, and allow correction/fallback.
- Natural Language is appropriate for defined tokenization, language identification, tagging, embeddings, or classification tasks. Record locale/model revision and do not inflate deterministic analysis into a generative conclusion.
- Sound Analysis depends on audio format, analyzer/model availability, confidence, interruptions, and capture/asset privacy. Stop capture when the feature ends and do not claim universal recognition from a fixture.

### App Intents and remote intelligence

- App Intents exposes typed actions/entities to Siri, Shortcuts, Spotlight, widgets, and system intelligence. Validate parameters and authorization exactly as for an in-app action; system discoverability is not permission to perform a side effect.
- Private Cloud Compute or another server model is a separate architecture. Trace what leaves the device, account/entitlement/network/cost, disclosure, retention, provider policy, and fallback. Never call a server route on-device proof.


## Deliverable

Produce a compact AI route note or implementation change containing:

- selected framework and rejected deterministic/narrower alternatives;
- availability, device/OS/model/language/permission/entitlement, privacy, retention, and server-boundary matrix;
- input/output/tool state machine with cancellation, context/backpressure, validation, review, authorization, fallback, and deletion;
- evaluation fixtures/metrics and exact compile, simulator, physical-device, performance, privacy, signing, and release evidence;
- remaining `to-verify` gaps and claims deliberately not made.

For implementation, change only the requested target and directly related adapters, prompt/schema/tool contracts, review UI, fixtures, or privacy/availability handling. Do not add a remote model, data upload, account, broad permission, irreversible tool, telemetry, or secret without a stated user-facing need and authorization.


## Refuse to assume

- Every iPhone or iPad has the same Apple Intelligence or Foundation Models availability.
- A compiling API, simulator, mock response, or one good prompt proves on-device behavior.
- A server model and the on-device model share limits, privacy, quality, or latency.
- A generated string is safe to execute or publish without validation and review.
- High-impact output (health, legal, financial) is correct because it sounds confident.

If the work is documentation or a route sketch, say so. Label simulator or mock results as such; never call them proof of Apple Intelligence behavior.


## Related routes and recipes

- [On-device AI recipes](../../ios-knowledge-base/references/31-on-device-ai-recipes/README.md)
- [AI feature brief template](../../ios-knowledge-base/references/90-templates/ai-feature-brief.md)
- [AI route selector](../../ios-knowledge-base/references/30-on-device-ai/00-ai-route-selector.md)
- [Foundation Models mental model](../../ios-knowledge-base/references/30-on-device-ai/01-foundation-models-mental-model.md)
- [Privacy, availability, safety, and fallback](../../ios-knowledge-base/references/30-on-device-ai/06-privacy-availability-and-fallback.md)
- [On-device AI availability and proof matrix](../../ios-knowledge-base/references/30-on-device-ai/08-on-device-ai-availability-and-proof-matrix.md)
- [Foundation Models recipes](../../ios-knowledge-base/references/70-code-recipes/01-foundation-model-recipes.md)
- [Vision, Core ML, and language recipes](../../ios-knowledge-base/references/31-on-device-ai-recipes/03-vision-and-core-ml-pipelines.md)
- [Speech, translation, and language recipes](../../ios-knowledge-base/references/31-on-device-ai-recipes/04-speech-translation-and-language-routes.md)
- [Evaluation, safety, and fallback](../../ios-knowledge-base/references/31-on-device-ai-recipes/05-evaluation-safety-and-fallback.md)
- [AI evaluation and safety checklist](../../ios-knowledge-base/references/60-verification/03-ai-evaluation-and-safety-checklist.md)
- [Permission, entitlement, and privacy checklist](../../ios-knowledge-base/references/60-verification/04-permission-entitlement-and-privacy-checklist.md)


## Sources

- [Foundation Models](https://developer.apple.com/documentation/foundationmodels/)
- [SystemLanguageModel](https://developer.apple.com/documentation/foundationmodels/systemlanguagemodel)
- [LanguageModelSession](https://developer.apple.com/documentation/foundationmodels/languagemodelsession)
- [Generating Swift data structures with guided generation](https://developer.apple.com/documentation/foundationmodels/generating-swift-data-structures-with-guided-generation)
- [Expanding generation with tool calling](https://developer.apple.com/documentation/foundationmodels/expanding-generation-with-tool-calling)
- [Managing the context window](https://developer.apple.com/documentation/foundationmodels/managing-the-context-window)
- [Prompting an on-device foundation model](https://developer.apple.com/documentation/foundationmodels/prompting-an-on-device-foundation-model)
- [Improving the safety of generative model output](https://developer.apple.com/documentation/foundationmodels/improving-the-safety-of-generative-model-output)
- [Foundation Models updates](https://developer.apple.com/documentation/Updates/FoundationModels)
- [Evaluating language-model responses](https://developer.apple.com/documentation/Evaluations/evaluating-language-model-responses)
- [Evaluating prompts to measure performance and improve model responses](https://developer.apple.com/documentation/foundationmodels/evaluating-prompts-to-measure-performance-and-improve-model-responses)
- [Adding server-side intelligence with Private Cloud Compute](https://developer.apple.com/documentation/foundationmodels/adding-server-side-intelligence-with-private-cloud-compute)
- [Core ML](https://developer.apple.com/documentation/coreml/)
- [Vision](https://developer.apple.com/documentation/vision/)
- [VisionKit](https://developer.apple.com/documentation/visionkit/)
- [Speech](https://developer.apple.com/documentation/speech/)
- [Translation](https://developer.apple.com/documentation/translation)
- [Natural Language](https://developer.apple.com/documentation/naturallanguage)
- [Sound Analysis](https://developer.apple.com/documentation/soundanalysis)
- [App Intents](https://developer.apple.com/documentation/appintents/)
