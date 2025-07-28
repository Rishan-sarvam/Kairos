import asyncio
import json
import re
import requests
import time
import threading
from typing import List, Dict, Any

from .base import LLMClient
from .models import UserInput, EvaluationResult, EvaluationType, TestResult
from .prompts import evaluation_prompt_template, QUALITATIVE_EVAL_PROMPT

class Evaluator:
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    async def evaluate(self, user_input: UserInput) -> EvaluationResult:
        """
        Evaluate the user query and return the result.
        """
        start_time = time.time()
        
        try:
            # # Initialize MCP if needed
            # if not self.llm_client.mcp_manager:
                # await self.llm_client.initialize_mcp()
            
            if user_input.evaluation_type == EvaluationType.QUALITATIVE:
                # await self.llm_client.initialize_mcp()
                print(f"🤖 Evaluator: {self.llm_client.mcp_manager}")
                result = await self._run_qualitative_evaluation(user_input)
            elif user_input.evaluation_type == EvaluationType.FEATURE_CORRECTNESS:
                # await self.llm_client.initialize_mcp()
                # await self.llm_client.initialize_mcp()
                result = await self._run_feature_correctness_evaluation(user_input)
            else:
                raise ValueError(f"Unsupported evaluation type: {user_input.evaluation_type}")
                
            execution_time = time.time() - start_time
            result.execution_time_seconds = execution_time
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            return EvaluationResult(
                evaluation_type=user_input.evaluation_type,
                provider_used=self.llm_client.provider,
                success=False,
                error_message=str(e),
                execution_time_seconds=execution_time
            )

    async def _run_qualitative_evaluation(self, user_input: UserInput) -> EvaluationResult:
        """Run qualitative evaluation"""
        try:
            # Create evaluation prompt
            evaluation_prompt = QUALITATIVE_EVAL_PROMPT.replace('{user_query}', user_input.user_query)
            evaluation_prompt = evaluation_prompt.replace('{app_url}', user_input.app_url)
            
            # Run evaluation
            response = await self.llm_client.run_evaluation_with_tools(evaluation_prompt, 0)
            
            
            return EvaluationResult(
                evaluation_type=user_input.evaluation_type,
                provider_used=self.llm_client.provider,
                success=True,
                qualitative_feedback=response,
                raw_response={"response": response}
            )
            
        except Exception as e:
            return EvaluationResult(
                evaluation_type=user_input.evaluation_type,
                provider_used=self.llm_client.provider,
                success=False,
                error_message=f"Qualitative evaluation failed: {str(e)}"
            )

    async def _run_feature_correctness_evaluation(self, user_input: UserInput) -> EvaluationResult:
        """Run feature correctness evaluation with test plan"""
        try:
            # Step 1: Get HTML content
            html_content = await self._fetch_html_content(user_input.app_url)
            
            # Step 2: Create test plan
            test_plan_response = await self.llm_client.create_test_plan(
                user_input.user_query, 
                html_content
            )
            
            # Step 3: Parse test plan
            test_plan_json = self._parse_test_plan(test_plan_response)

            print(f"🧪 Test Plan: {test_plan_json}")
            
            # Step 4: Split test plan for parallel execution (if needed)
            if len(test_plan_json) > 4:  # Only split if many tests
                mid_point = len(test_plan_json) // 2
                test_plan_half1 = test_plan_json[:mid_point]
                test_plan_half2 = test_plan_json[mid_point:]
                
                # Run in parallel
                results = await self._run_parallel_evaluations(
                    test_plan_half1, test_plan_half2, user_input.app_url
                )
            else:
                # Run single evaluation
                result1 = await self._run_single_evaluation(test_plan_json, user_input.app_url, 0)
                # all_test_results = single_result.test_results
                # overall_success = single_result.success
                return EvaluationResult(
                evaluation_type=user_input.evaluation_type,
                provider_used=self.llm_client.provider,
                success=True,
                # test_results=all_test_results,
                raw_response={"result1": result1}
            )
            
            return EvaluationResult(
                evaluation_type=user_input.evaluation_type,
                provider_used=self.llm_client.provider,
                success=True,
                # test_results=all_test_results,
                raw_response={"results": results}
            )
            
        except Exception as e:
            return EvaluationResult(
                evaluation_type=user_input.evaluation_type,
                provider_used=self.llm_client.provider,
                success=False,
                error_message=f"Feature correctness evaluation failed: {str(e)}"
            )

    async def _run_parallel_evaluations(self, test_plan_half1: List[Dict], 
                                       test_plan_half2: List[Dict], 
                                       url: str) -> List[EvaluationResult]:
        """Run two evaluation halves in parallel using threading"""
        
        # def run_agent_sync(test_plan, thread_id):
        #     """Wrapper to run async evaluation in a thread"""
        #     loop = asyncio.new_event_loop()
        #     asyncio.set_event_loop(loop)
        #     try:
        #         result = loop.run_until_complete(self._run_single_evaluation(test_plan, url, thread_id))
        #         return result
        #     finally:
        #         loop.close()

        def run_agent_sync(test_plan, thread_id):
            """Wrapper to run async evaluation in a thread"""
            return asyncio.run(self._run_single_evaluation(test_plan, url, thread_id))
        
        # Create and start threads
        results = [None, None]
        
        def thread_1():
            results[0] = run_agent_sync(test_plan_half1, 0)
        
        def thread_2():
            results[1] = run_agent_sync(test_plan_half2, 1)
        
        # Start both threads
        t1 = threading.Thread(target=thread_1)
        t2 = threading.Thread(target=thread_2)
        
        t1.start()
        t2.start()
        
        # Wait for both to complete
        t1.join()
        t2.join()
        
        return [results[0], results[1]]

    async def _run_single_evaluation(self, test_plan: List[Dict], url: str, thread_id: int) -> EvaluationResult:
        """Run evaluation for a single test plan"""
        try:
            evaluation_prompt = evaluation_prompt_template.format(test_plan=test_plan, url=url)

            # Run evaluation
            response = await self.llm_client.run_evaluation_with_tools(evaluation_prompt, thread_id)
            
            return EvaluationResult(
                evaluation_type=EvaluationType.FEATURE_CORRECTNESS,
                provider_used=self.llm_client.provider,
                success=True,
                raw_response={"response": response}
            )
            
        except Exception as e:
            return EvaluationResult(
                evaluation_type=EvaluationType.FEATURE_CORRECTNESS,
                provider_used=self.llm_client.provider,
                success=False,
                error_message=f"Single evaluation failed: {str(e)}"
            )

    async def _fetch_html_content(self, url: str) -> str:
        """Fetch HTML content from URL"""
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()               # Raise an exception for HTTP errors
            return response.text
        except Exception as e:
            raise Exception(f"Failed to fetch HTML content from {url}: {str(e)}")

    def _parse_test_plan(self, test_plan_response: str) -> List[Dict]:
        """Parse test plan JSON from LLM response"""
        try:
            match = re.search(r"```json\s*(.*?)\s*```", test_plan_response, re.DOTALL)
            if match:
                json_str = match.group(1)
                return json.loads(json_str)
            else:
                raise Exception("No JSON code block found in test plan response")
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse test plan JSON: {str(e)}")

    # def _parse_evaluation_response(self, response: str, test_plan: List[Dict]) -> List[TestResult]:
    #     """Parse evaluation response and create TestResult objects"""
    #     test_results = []
        
    #     try:
    #         # Try to parse JSON response
    #         match = re.search(r"```json\s*(.*?)\s*```", response, re.DOTALL)
    #         if match:
    #             json_str = match.group(1)
    #             eval_data = json.loads(json_str)
                
    #             overall_status = eval_data.get("Overall_status", "UNKNOWN")
    #             failed_features = eval_data.get("Failed_features_reason", [])
    #             failed_elements = eval_data.get("Failed_elements", [])
                
    #             # Create test results based on test plan
    #             for i, test in enumerate(test_plan):
    #                 test_feature = test.get("Test_feature", f"Test {i+1}")
    #                 description = test.get("Description", "")
    #                 actions = test.get("Actions", "")
    #                 assertions = test.get("Assertions", "")
                    
    #                 # Determine if this test passed
    #                 passed = overall_status == "PASS"
    #                 error_message = None
                    
    #                 # Check if this specific test failed
    #                 if not passed:
    #                     for failure in failed_features:
    #                         if test_feature.lower() in failure.lower():
    #                             error_message = failure
    #                             break
    #                     if not error_message and failed_features:
    #                         error_message = failed_features[0]
                    
    #                 test_results.append(TestResult(
    #                     test_feature=test_feature,
    #                     description=description,
    #                     actions=actions,
    #                     assertions=assertions,
    #                     passed=passed,
    #                     error_message=error_message
    #                 ))
    #         else:
    #             # Fallback: create test results from test plan with unknown status
    #             for i, test in enumerate(test_plan):
    #                 test_results.append(TestResult(
    #                     test_feature=test.get("Test_feature", f"Test {i+1}"),
    #                     description=test.get("Description", ""),
    #                     actions=test.get("Actions", ""),
    #                     assertions=test.get("Assertions", ""),
    #                     passed=False,
    #                     error_message="Could not parse evaluation response"
    #                 ))
                    
    #     except Exception as e:
    #         # Fallback: create failed test results
    #         for i, test in enumerate(test_plan):
    #             test_results.append(TestResult(
    #                 test_feature=test.get("Test_feature", f"Test {i+1}"),
    #                 description=test.get("Description", ""),
    #                 actions=test.get("Actions", ""),
    #                 assertions=test.get("Assertions", ""),
    #                 passed=False,
    #                 error_message=f"Evaluation parsing failed: {str(e)}"
    #             ))
        
    #     return test_results