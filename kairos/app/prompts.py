"""
Prompt templates for web application evaluation
"""

test_plan_system_prompt = """
    You are an expert Playwright test plan creator. You will analyze the provided HTML code and user query to create a comprehensive Playwright test plan.
    
    Your task:
    1. Analyze the HTML code to identify ALL interactive elements
    2. Create specific Playwright test plans for each feature by interacting with every element
    3. **Most important**: Include assertions to verify functionality
    5. Organize tests logically by functionality
    6. Try to group similar tests together so that the test plan is **as short as possible**.
    7. Try to add as many assertions as possible to the test plan. **Make sure that the assertions are not just checking the presence of the element but also checking the functionality of the element.**
    8. **IMPORTANT**: The functionality of the element is of prime importance. So, make sure that the assertions are checking the functionality of the element.
    9. **IMPORTANT**: The application is a vanilla js app with a single index.html, app.js and style.css file. So, make the assertions accordingly.
    
    Focus on testing:
    - Buttons (click actions, expected outcomes)
    - Forms (input validation, submission, error handling)
    - Input fields (typing, clearing, validation)
    - Dropdowns/Select elements (selection, options)
    - Links (navigation, external links)
    - Search functionality
    - Filters and sorting
    - Dynamic content loading
    - Interactive charts/graphs
    - Modal dialogs
    - Toggles and switches
    - Sliders and range inputs
    
    Include specific selectors and assertions for each test plan. Output only the test plan and the code is not required. Do not include any other text.
    """

test_plan_prompt = """Create a comprehensive Playwright test plan for this web application.

USER QUERY: {user_query}

HTML CODE:
{html_content}

Please provide a detailed test plan that includes:
1. Test case descriptions
2. Specific Playwright selectors and actions
3. **IMPORTANT**: Assertions to verify functionality. The assertions should include all the functionalitites of that particular test. Try to find deeper assertions.
4. Make sure there are no duplicate assertions or redundant tests.
5. Expected behaviors

Output your response in this exact JSON format:

```json
[
    {{
        "Test_feature": "name of the test feature",
        "Description": "description of the test feature", 
        "Actions": "list of actions to be performed to test the feature",
        "Assertions": "comprehensive list of assertions to be performed to test the feature"
    }}
]
```

Make sure to wrap the JSON with ```json and ``` code blocks.
"""

evaluation_prompt_template = """
* You are an intelligent app evaluator that uses playwright to evaluate the application.
* You are given a dynamic web application and must evaluate it based on the test plan provided.
* Execute the evaluation step-by-step using the tools provided by the Playwright MCP.

### Comprehensive Test Plan to Execute:
{test_plan}

## Important: Follow the above test plan systematically while conducting your evaluation and do not deviate from the test plan. Test ALL interactive elements identified in the plan and only the plan provided and verify their functionality using the assertions provided in the test plan.
## **IMPORTANT: Make sure all the assertions mentioned in the test plan are checked. All the assertions should be checked. Even if a single assertion fails, then the feature is marked as failed.**
## Ignore the things that are not mentioned in the test plan or things that cannot be verified using the tools provided by the Playwright MCP.
## Provide a detailed reason for success or failure of each feature

## Output Requirements:
```json
{{
  "application_evaluation": {{
    "features_analysis": [
      {{
        "feature_name": "Name of the feature",
        "status": "SUCCESS" or "FAILURE",
        "reason": "Specific reason why this feature succeeded or failed",
      }}
    ],
    "overall_summary": {{
      "failed_features": "Number",
      "overall_status": "PASS/FAIL",
      "key_issues": ["List of most critical issues found"],
      "recommendations": ["List of recommended fixes or improvements"]
    }}
  }}
}}
```
Do not include any other text in your response, just the json object.

### Target App:
* **APP:** {url}
"""

INSTRUCTIONS = """
Rating Philosophy
For each rubric, the rater should evaluate their agreement with the provided statement, based on their overall impression of the web application. The focus is not on rating features in isolation but on expressing how positively or negatively the rater feels toward the full statement in context.
The rater is expected to make a subjective judgment along a 4-point Likert scale:
Strongly Disagree – You feel strongly negative toward the statement. The app clearly fails to meet the expectations described.
Disagree – You slightly or moderately disagree with the statement. There are notable shortcomings, but not severe enough to warrant strong rejection.
Agree – You somewhat or mostly agree with the statement. The app satisfies the expectation in general, with only minor issues.
Strongly Agree – You feel strongly positive toward the statement. The app fully meets or exceeds the expectation in a clear and convincing way.

Improvement Suggestion Policy
For each rubric section (e.g., Visual Appeal, Content Quality), if any of the statements receive a rating below Strongly Agree, the rater must provide one improvement suggestion for that statement as part of a single feedback for the entire rubric. For each rubric provide this as a bulleted point 
The purpose of this policy is to guide continuous improvement in areas that are not fully satisfactory, while maintaining a streamlined evaluation process.

Here are the detailed rubrics:
"""
VISUAL_UX_RUBRIC = """
### VISUAL_UX
• visual_appeal – The layout is clear and uncluttered.  
• element_diversity – The page shows a good variety of elements.  
• color_harmony – The colors are used in a harmonious way.  
• design_craftsmanship – The design details are polished and thoughtful.
"""

CONTENT_QUALITY_RUBRIC = """
### CONTENT_QUALITY
• copy_clarity – The writing is clear and the text is visible and easy to understand.  
• organization – Information is structured for quick scanning.  
• content_relevance – All content helps users achieve their goal.  
• richness – Charts, tables, or images meaningfully support the text.
"""

CONTENT_GROUNDING_RUBRIC = """
### CONTENT_GROUNDING
• accuracy – All facts, figures, and values are correct.  
• plausibility – Sample data (names, dates, prices, etc.) looks realistic.  
• attribution – Sources and timestamps of data are clearly indicated.  
• consistency – The same data is presented uniformly across the app.
"""

NAVIGATION_RUBRIC = """
### NAVIGATION
• discoverability – Buttons, links, and menus are easy to find.  
• task_flow – Users can complete key tasks in a short and clear sequence.  
• feedback – The interface clearly shows where the user is and what happened after each click.  
• accessibility – The app is navigable using keyboard or assistive tools.
"""

DATA_CONSISTENCY_RUBRIC = """
### DATA_CONSISTENCY
• synchronization – When data changes in one place, it updates everywhere else.  
• format_uniformity – Dates, numbers, and labels use consistent formats throughout.  
• multi_view_coherence – Information appears identically across all views.  
• persistence – Data remains saved after reload or logout.
"""

FEATURE_COVERAGE_RUBRIC = """
### FEATURE_COVERAGE
• very_low_feature_coverage – Score 1: Very low feature coverage (< Quarter (¼)).  
• low_feature_coverage – Score 2: Low feature coverage (¼ – ½).  
• high_feature_coverage – Score 3: High feature coverage (½ – ¾).  
• very_high_feature_coverage – Score 4: Very high feature coverage (¾ – Full (1)).
"""

QUALITATIVE_EVAL_PROMPT = f"""
* You are an intelligent app evaluator.
* You are given a live, dynamic web application and must explore **all** pages—scroll, click every menu item or button, resize the window, and test form inputs—to understand the complete user journey.

{INSTRUCTIONS}

{VISUAL_UX_RUBRIC}
{CONTENT_QUALITY_RUBRIC}
{CONTENT_GROUNDING_RUBRIC}
{NAVIGATION_RUBRIC}
{DATA_CONSISTENCY_RUBRIC}
{FEATURE_COVERAGE_RUBRIC}

### Output Format
Retur your output strictly in the following json format.

{{
  "visual_ux": {{
    "visual_appeal": "Agree",
    "element_diversity": "Strongly Agree",
    "color_harmony": "Agree",
    "design_craftsmanship": "Disagree",
    "improvement_suggestion": "Polish button shadows and align card spacing to reduce visual noise."
  }},
  "content_quality": {{
    "copy_clarity": "Strongly Agree",
    "organization": "Agree",
    "content_relevance": "Agree",
    "richness": "Disagree",
    "improvement_suggestion": "Add meaningful captions to charts and replace placeholder imagery with real examples."
  }},
  "content_grounding": {{
    "accuracy": "Strongly Agree",
    "plausibility": "Agree",
    "attribution": "Disagree",
    "consistency": "Agree",
    "improvement_suggestion": "Cite data sources directly under each metric to build trust."
  }}
}}

Input:
User Query: {{user_query}}

APP URL: {{app_url}}
"""


# {{
#     "Overall_status": "PASS/FAIL",
#     "Failed_features_reason": [list of reasons for failure],
#     "Failed_elements": [list of failed features/elements] #Keep it as minimum as possible and only the features of the application that genuinely failed.
# }}

