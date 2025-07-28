"""
Prompt templates for web application evaluation
"""

test_plan_prompt = """
    You are an expert Playwright test plan creator. You will analyze the provided HTML code and user query to create acomprehensive test plan.
    
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

evaluation_prompt_template = """
* You are an intelligent app evaluator that uses playwright to evaluate the application.
* Execute the evaluation step-by-step using the tools provided by the Playwright MCP.

### Comprehensive Test Plan to Execute:
{test_plan}

## Important: Follow the above test plan systematically while conducting your evaluation and do not deviate from the test plan. Test ALL interactive elements identified in the plan and only the plan provided and verify their functionality using the assertions provided in the test plan.
## **IMPORTANT: Make sure all the assertions mentioned in the test plan are checked. Even if a single assertion fails, then the feature is marked as failed. All the assertions should be checked.**
## Ignore the things that are not mentioned in the test plan or things that cannot be verified using the tools provided by the Playwright MCP.
## Test thoroughly using Playwright tools
## Provide a detailed reason for success or failure

## Output Requirements:
```json
{{
    "Overall_status": "PASS/FAIL",
    "Failed_features_reason": [list of reasons for failure],
    "Failed_elements": [list of failed features/elements] #Keep it as minimum as possible and only the features of the application that genuinely failed.
}}
```
Do not include any other text in your response, just the json object.

### Target App:
* **APP:** {url}
"""

QUALITATIVE_EVAL_PROMPT = """* You are an intelligent app evaluator.
* You are given a live, dynamic web application and must explore **all** pages—scroll, click every menu item or button, resize the window, and test form inputs—to understand the complete user journey.

### Detailed Evaluation Rubrics
1. **Visual & UX**  
   Evaluate how the interface looks **and** feels to use. Consider:  
   • *Visual appeal* – cohesiveness of colour palette, typography, iconography, spacing, and overall polish.  
   • *Layout clarity* – logical grouping of elements, clear visual hierarchy, consistent component sizing.  
   • *Navigation flow* – intuitive menus, breadcrumbs, back/forward cues, discoverability of key actions.  
   • *Responsiveness & accessibility* – adapts gracefully to mobile/tablet, keyboard-only navigation, focus states, ARIA/alt text, contrast ratios.  
   • *Micro-interactions & feedback* – hover states, button states, loading spinners, success / error toasts that reassure the user.  

2. **Content & Information Quality**  
   Judge the clarity, completeness, and presentation of all data and copy. Check:  
   • *Copy accuracy & tone* – correct grammar, consistent terminology, jargon explained.  
   • *Data fidelity* – numbers match source, units shown, no truncation or obvious mis-rounding.  
   • *Visual presentation* – charts/graphs labelled, legends present, colour scales sensible, tooltips available.  
   • *Contextual guidance* – inline help, onboarding tips, empty-state messages that explain next steps.  
   • *Cognitive load* – avoids walls of text, uses headings, bullets, or tabs to break up information.  

3. **Goal Completion (Purpose Fit)**  
   Decide whether a typical user can accomplish the app's stated purpose end-to-end. Look for:  
   • *Task coverage* – all primary flows (e.g., sign-up → create item → save/export) are present and discoverable.  
   • *Workflow integrity* – steps are in logical order, confirmations shown, no dead ends or circular links.  
   • *Edge cases & recovery* – sensible defaults, validation messages for invalid input, empty-state handling.  
   • *Value delivery* – final outputs are actionable, trustworthy, and clearly tied to the problem the app claims to solve.  

### Output format
Return just **one** JSON object—**no scores**, only whether improvements are needed and concrete advice:

{
  "visual_ux": {
    "improvement_needed": "Yes/No",
    "improvement_suggestion": "One-to-two sentences of actionable fixes"
  },
  "content_quality": {
    "improvement_needed": "Yes/No",
    "improvement_suggestion": "..."
  },
  "goal_completion": {
    "improvement_needed": "Yes/No",
    "improvement_suggestion": "..."
  }
}

User Query: {user_query}

APP URL: {app_url}
""" 