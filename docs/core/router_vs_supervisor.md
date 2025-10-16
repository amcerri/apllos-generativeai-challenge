# Router vs Supervisor: Detailed Comparison

This document provides a comprehensive comparison between the Router (LLM Classifier) and Supervisor components, explaining their distinct roles, responsibilities, and interaction patterns.

## Overview

The routing system uses a two-stage approach to ensure accurate and safe routing decisions:

1. **Router (LLM Classifier)**: Makes intelligent routing decisions using LLM
2. **Supervisor**: Applies deterministic guardrails and fallback logic

## Detailed Comparison

| Aspect | Router (LLM Classifier) | Supervisor |
|--------|-------------------------|------------|
| **Primary Role** | Intelligent decision making | Safety and guardrails |
| **Technology** | LLM-based with structured output | Deterministic logic |
| **Input** | Natural language query + context | RouterDecision + RoutingContext |
| **Output** | Structured RouterDecision | Final RouterDecision with guardrails |
| **Fallback** | Heuristic rules when LLM unavailable | Single-pass fallback logic |
| **Confidence** | LLM-generated confidence scores | Recalibrated conservative scores |
| **Safety** | Basic validation and constraints | Business rules and safety checks |

## Router (LLM Classifier) Details

### Purpose
The Router is the primary decision maker that analyzes user queries and determines the most appropriate agent to handle the request.

### Key Responsibilities
- **Intent Analysis**: Understands user intent and context
- **Context Processing**: Analyzes query structure and signals
- **Agent Selection**: Chooses the most appropriate agent
- **Confidence Scoring**: Provides confidence levels for decisions
- **Signal Generation**: Creates routing signals and hints

### Implementation Details
- **File**: `app/routing/llm_classifier.py`
- **Class**: `LLMClassifier`
- **Method**: `classify()` - Main classification method
- **Output**: `RouterDecision` with structured data

### Key Features
- **LLM-First Approach**: Uses OpenAI GPT-4o-mini for intelligent decisions
- **Structured Output**: JSON Schema for consistent decision format
- **Chain-of-Thought**: Shows reasoning process in responses
- **Self-Consistency**: Validates decisions for consistency
- **Confidence Calibration**: Adjusts confidence scores for accuracy
- **Few-Shot Examples**: Uses examples for improved classification

### Fallback Behavior
When LLM is unavailable, the Router falls back to deterministic heuristics:
- **Allowlist Overlap**: Strong signal for analytics routing
- **SQL Structure**: Detects SQL-like queries for analytics
- **Commerce Cues**: Identifies currency and totals for commerce
- **Document Patterns**: Recognizes document-style queries for knowledge
- **Greeting Patterns**: Identifies greetings for triage

## Supervisor Details

### Purpose
The Supervisor applies deterministic guardrails and business rules to ensure safe and appropriate routing decisions.

### Key Responsibilities
- **Safety Enforcement**: Applies business rules and constraints
- **Fallback Logic**: Handles single-pass fallbacks to prevent loops
- **Confidence Recalibration**: Adjusts confidence scores conservatively
- **Commerce Dominance**: Enforces commerce routing when documents detected
- **Context Validation**: Uses probe results for informed decisions

### Implementation Details
- **File**: `app/routing/supervisor.py`
- **Function**: `supervise()` - Main supervision method
- **Input**: `RouterDecision` + `RoutingContext`
- **Output**: Final `RouterDecision` with applied guardrails

### Key Features
- **Deterministic Logic**: Rule-based decision making
- **Single-Pass Fallback**: Prevents routing loops
- **Commerce Guard**: Forces commerce routing when documents present
- **Confidence Recalibration**: Conservative confidence adjustment
- **Context Awareness**: Uses probe signals for informed decisions

### Fallback Rules
The Supervisor applies these fallback rules:
- **Analytics → Knowledge**: When document cues present and no allowlist cues
- **Knowledge → Analytics**: When allowlist cues present
- **Triage → Knowledge/Analytics**: Based on available cues
- **Commerce Dominance**: Always routes to commerce when document detected

## Interaction Flow

```
User Query
    ↓
Router (LLM Classifier)
    ↓
RouterDecision (initial)
    ↓
Supervisor (Guardrails)
    ↓
RouterDecision (final)
    ↓
Target Agent
```

## Decision Process

### 1. Router Analysis
- Analyzes query intent and context
- Generates structured RouterDecision
- Provides confidence score and reasoning
- Creates routing signals and hints

### 2. Supervisor Validation
- Validates RouterDecision against business rules
- Applies safety constraints and guardrails
- Handles fallback logic if needed
- Recalibrates confidence scores conservatively

### 3. Final Decision
- Produces final RouterDecision with applied guardrails
- Ensures safety and appropriateness
- Provides clear reasoning for decision
- Routes to appropriate agent

## Configuration

### Router Configuration
- **Model**: `gpt-4o-mini` (configurable)
- **Temperature**: 0.7 for balanced creativity
- **Max Tokens**: 1000 for comprehensive responses
- **Timeout**: 30 seconds for LLM calls
- **Retries**: 3 attempts with exponential backoff

### Supervisor Configuration
- **Fallback Rules**: Configurable business logic
- **Confidence Thresholds**: Conservative confidence levels
- **Commerce Detection**: Document and attachment signals
- **Context Weights**: Probe signal importance

## Error Handling

### Router Errors
- **LLM Unavailable**: Falls back to deterministic heuristics
- **Timeout**: Uses cached responses or heuristics
- **Rate Limiting**: Implements exponential backoff
- **Invalid Response**: Validates and retries

### Supervisor Errors
- **Invalid Input**: Validates RouterDecision structure
- **Missing Context**: Uses default fallback rules
- **Configuration Errors**: Logs warnings and continues
- **Logic Errors**: Graceful degradation

## Monitoring and Observability

### Router Metrics
- **Classification Accuracy**: Success rate of routing decisions
- **LLM Response Time**: Latency of LLM calls
- **Fallback Usage**: Frequency of heuristic fallbacks
- **Confidence Distribution**: Distribution of confidence scores

### Supervisor Metrics
- **Fallback Rate**: Frequency of supervisor interventions
- **Commerce Detection**: Success rate of commerce routing
- **Confidence Recalibration**: Impact of confidence adjustments
- **Safety Violations**: Detection of unsafe routing attempts

## Best Practices

### Router Best Practices
- **Prompt Engineering**: Use clear, specific prompts
- **Few-Shot Examples**: Provide diverse examples
- **Context Injection**: Include relevant context
- **Validation**: Validate LLM responses
- **Fallback**: Always have deterministic fallbacks

### Supervisor Best Practices
- **Rule Clarity**: Keep business rules simple and clear
- **Single-Pass**: Avoid multiple fallbacks
- **Conservative**: Err on the side of caution
- **Context Awareness**: Use probe signals effectively
- **Monitoring**: Track supervisor interventions

## Troubleshooting

### Common Router Issues
- **Low Confidence**: Check prompt quality and examples
- **Wrong Routing**: Validate few-shot examples
- **Slow Response**: Check LLM configuration and timeouts
- **Fallback Overuse**: Review LLM availability and configuration

### Common Supervisor Issues
- **Excessive Fallbacks**: Review business rules
- **Commerce Miss**: Check document detection signals
- **Confidence Issues**: Validate recalibration logic
- **Loop Detection**: Ensure single-pass fallback

## Future Enhancements

### Router Improvements
- **Ensemble Routing**: Multiple LLM variants for better accuracy
- **Context Learning**: Learn from user feedback
- **Dynamic Prompts**: Adapt prompts based on performance
- **Multi-Modal**: Support for images and documents

### Supervisor Improvements
- **Machine Learning**: Learn from routing patterns
- **Dynamic Rules**: Adapt rules based on performance
- **Advanced Context**: Use more sophisticated context analysis
- **Predictive Fallbacks**: Anticipate routing issues

This comprehensive comparison should help developers understand the distinct roles and responsibilities of the Router and Supervisor components in the Apllos Assistant system.

---

**← [Back to Documentation Index](../README.md)**
