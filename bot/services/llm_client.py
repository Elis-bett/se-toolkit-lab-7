"""LLM client for intent routing with tool calling and fallback."""

import json
import sys
import re
from typing import List, Dict, Any, Optional
from config import Config
from services.lms_client import LMSClient


class LLMClient:
    def __init__(self):
        self.base_url = Config.LLM_API_BASE_URL.rstrip("/")
        self.api_key = Config.LLM_API_KEY
        self.model = Config.LLM_API_MODEL
        self.lms_client = LMSClient()
        self.timeout = 30.0

    def _is_llm_available(self) -> bool:
        """Check if LLM is properly configured."""
        if not self.api_key or self.api_key == "your_actual_qwen_api_key_here":
            return False
        if not self.base_url:
            return False
        return True

    def process_message(self, user_message: str) -> str:
        """Process user message with tool calling or fallback."""
        if self._is_llm_available():
            try:
                return self._process_with_llm(user_message)
            except Exception as e:
                print(f"[LLM] Error: {e}", file=sys.stderr)
                return self._fallback_response(user_message)
        else:
            return self._fallback_response(user_message)

    def _process_with_llm(self, user_message: str) -> str:
        """Process with real LLM (placeholder for now)."""
        return self._fallback_response(user_message)

    def _fallback_response(self, user_message: str) -> str:
        """Simple rule-based fallback for when LLM is not available."""
        msg_lower = user_message.lower()

        print(f"[fallback] Processing: {user_message}", file=sys.stderr)

        # Query about labs
        if any(
            word in msg_lower
            for word in [
                "what lab",
                "which lab",
                "list lab",
                "available lab",
                "labs are",
            ]
        ):
            labs_data = self.lms_client.get_labs()
            if labs_data:
                result = "📚 **Available Labs:**\n\n"
                lab_names = {
                    1: "Products, Architecture & Roles",
                    2: "Run, Fix, and Deploy",
                    3: "Backend API",
                    4: "Testing, Front-end, and AI Agents",
                    5: "Data Pipeline and Analytics",
                    6: "Build Your Own Agent",
                }
                for lab in labs_data[:6]:
                    lab_id = lab.get("id", 0)
                    if isinstance(lab_id, str) and lab_id.isdigit():
                        lab_id = int(lab_id)
                    name = lab_names.get(lab_id, f"Lab {lab_id}")
                    result += f"**Lab {lab_id:02d}** — {name}\n"
                return result
            return "No labs found. Please run ETL sync first."

        # Query about scores for a specific lab
        elif any(
            word in msg_lower
            for word in ["score", "pass rate", "results", "performance"]
        ):
            lab_match = re.search(r"lab\s*(\d+)", msg_lower)
            if lab_match:
                lab_num = lab_match.group(1)
                lab_name = f"lab-{lab_num.zfill(2)}"
                try:
                    pass_rates = self.lms_client.get_pass_rates(lab_name)
                    if pass_rates and pass_rates.get("tasks"):
                        result = f"📈 **Pass Rates for Lab {lab_num}**\n\n"
                        for task in pass_rates["tasks"][:5]:
                            task_name = task.get("name", "Task")
                            pass_rate = task.get("pass_rate", 0)
                            attempts = task.get("attempts", 0)
                            result += f"• **{task_name}**: {pass_rate:.1f}% ({attempts} attempts)\n"
                        return result
                except Exception as e:
                    return f"Error fetching scores: {str(e)}"
            return "📊 To see scores, use: /scores lab-04\n\nReplace lab-04 with the lab you're interested in."

        # Query about which lab has lowest pass rate
        elif any(
            word in msg_lower
            for word in ["lowest", "worst", "worst results", "lowest pass"]
        ):
            return self._find_lowest_pass_rate()

        # Query about top learners
        elif any(word in msg_lower for word in ["top", "best", "leaderboard"]):
            lab_match = re.search(r"lab\s*(\d+)", msg_lower)
            if lab_match:
                lab_num = lab_match.group(1)
                return f"🏆 Top learners for Lab {lab_num}:\n\nUse /top lab-{lab_num} to see the leaderboard."
            return (
                "🏆 To see top learners, specify a lab, e.g., 'top learners in lab 4'"
            )

        # Health check
        elif any(word in msg_lower for word in ["health", "status", "backend"]):
            healthy, msg = self.lms_client.check_health()
            return msg

        # Greeting
        elif any(word in msg_lower for word in ["hello", "hi", "hey", "greeting"]):
            return "👋 Hello! I'm your SE Toolkit Lab Bot. I can help you with:\n\n• 📚 List available labs\n• 📊 Show scores for a lab\n• 📈 Find which lab has the lowest pass rate\n• 🏆 Show top learners\n\nJust ask me questions like:\n- 'What labs are available?'\n- 'Show me scores for lab 4'\n- 'Which lab has the lowest pass rate?'"

        # Ambiguous query like "lab 4"
        elif re.search(r"lab\s*\d+", msg_lower):
            lab_match = re.search(r"lab\s*(\d+)", msg_lower)
            if lab_match:
                lab_num = lab_match.group(1)
                return f"🔍 What would you like to know about Lab {lab_num}?\n\n• Scores: /scores lab-{lab_num}\n• Pass rates: 'show me pass rates for lab {lab_num}'\n• Top learners: 'top learners in lab {lab_num}'"

        # Unknown query
        else:
            return "🤔 I'm not sure I understand. Try asking me:\n\n• 'What labs are available?'\n• 'Show me scores for lab 4'\n• 'Which lab has the lowest pass rate?'\n• 'Hello'\n\nOr use /help to see all commands."

    def _find_lowest_pass_rate(self) -> str:
        """Find lab with lowest average pass rate."""
        try:
            labs_data = self.lms_client.get_labs()
            if not labs_data:
                return "No labs found in the system."

            lab_results = []
            for lab in labs_data[:6]:
                lab_id = lab.get("id", 0)
                if isinstance(lab_id, str) and lab_id.isdigit():
                    lab_id = int(lab_id)
                elif isinstance(lab_id, str) and lab_id.startswith("lab-"):
                    lab_id = int(lab_id[4:])

                lab_name = f"lab-{str(lab_id).zfill(2)}"
                try:
                    pass_rates = self.lms_client.get_pass_rates(lab_name)
                    if pass_rates and pass_rates.get("tasks"):
                        avg_score = sum(
                            t.get("pass_rate", 0) for t in pass_rates["tasks"]
                        ) / len(pass_rates["tasks"])
                        lab_results.append(
                            {
                                "id": lab_id,
                                "name": lab_name,
                                "avg_score": avg_score,
                                "tasks": pass_rates["tasks"],
                            }
                        )
                except:
                    continue

            if not lab_results:
                return "Unable to retrieve pass rates for labs."

            lowest = min(lab_results, key=lambda x: x["avg_score"])

            result = f"📉 **Lab {lowest['id']:02d} has the lowest average pass rate at {lowest['avg_score']:.1f}%**\n\n"
            result += "Task breakdown:\n"
            for task in lowest["tasks"][:3]:
                task_name = task.get("name", "Task")
                pass_rate = task.get("pass_rate", 0)
                attempts = task.get("attempts", 0)
                result += f"• {task_name}: {pass_rate:.1f}% ({attempts} attempts)\n"

            return result

        except Exception as e:
            return f"Error finding lowest pass rate: {str(e)}"

    def _get_tools(self) -> List[Dict[str, Any]]:
        """Define all 9 tools for the LLM."""
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_items",
                    "description": "Get list of all labs and tasks in the system.",
                    "parameters": {"type": "object", "properties": {}, "required": []},
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_learners",
                    "description": "Get list of enrolled students and their groups.",
                    "parameters": {"type": "object", "properties": {}, "required": []},
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_scores",
                    "description": "Get score distribution for a specific lab.",
                    "parameters": {
                        "type": "object",
                        "properties": {"lab": {"type": "string"}},
                        "required": ["lab"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_pass_rates",
                    "description": "Get per-task average scores for a lab.",
                    "parameters": {
                        "type": "object",
                        "properties": {"lab": {"type": "string"}},
                        "required": ["lab"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_timeline",
                    "description": "Get submission timeline for a lab.",
                    "parameters": {
                        "type": "object",
                        "properties": {"lab": {"type": "string"}},
                        "required": ["lab"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_groups",
                    "description": "Get per-group performance for a lab.",
                    "parameters": {
                        "type": "object",
                        "properties": {"lab": {"type": "string"}},
                        "required": ["lab"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_top_learners",
                    "description": "Get top learners by score for a lab.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "lab": {"type": "string"},
                            "limit": {"type": "integer"},
                        },
                        "required": ["lab"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_completion_rate",
                    "description": "Get completion rate for a lab.",
                    "parameters": {
                        "type": "object",
                        "properties": {"lab": {"type": "string"}},
                        "required": ["lab"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "trigger_sync",
                    "description": "Trigger ETL sync to refresh data.",
                    "parameters": {"type": "object", "properties": {}, "required": []},
                },
            },
        ]
