import json
import re
from sqlalchemy import create_engine
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_community.utilities import SQLDatabase
from langchain.agents import create_sql_agent


class PolicyChecker:
    def __init__(self):
        """Initialize PolicyChecker with fixed config inside the class."""

        # 🔑 Static configuration (your values live here)
        self.db_path = "my_database.db"
        self.policy_path = "/home/arshad-ahmed/Documents/Agents/companypolicies.json"
        self.llm_model = "qwen/qwen3-coder-480b-a35b-instruct"
        self.api_key = ""

        # Load policies
        with open(self.policy_path, "r") as f:
            self.policy = json.load(f)

        # Create agent
        self.agent_executor = self._create_agent()

    def _create_agent(self):
        """Create and return a LangChain SQL agent connected to DuckDB."""
        # LLM
        llm = ChatNVIDIA(
            model=self.llm_model,
            api_key=self.api_key,
        )

        # DuckDB engine
        engine = create_engine(f"duckdb:///{self.db_path}")
        db = SQLDatabase(engine=engine)

        print("Available tables:", db.get_usable_table_names())

        return create_sql_agent(
            llm=llm,
            db=db,
            verbose=True,
            handle_parsing_errors=True
        )

    def run_policy_check(self, output_file: str = "report.json") -> dict:
        """Run policy analysis with the agent and save result as JSON file."""
        prompt = f"""
        You are an excellent assistant employed to check whether the given table in the DB 
        violates the company policies below:

        {json.dumps(self.policy, indent=2)}

        Return your analysis strictly as JSON with the following structure:
        {{
          "summary_report": {{
            "general_description": "string",
            "total_records": "int",
            "policy_violations": ["list of violations"],
            "data_quality_issues": ["list of issues"],
            "overall_assessment": "string"
          }}
        }}
        """

        parsed_json = {}

        try:
            result = self.agent_executor.invoke(prompt)
            raw_output = str(result)

            # Try extracting JSON
            match = re.search(r"(\{.*\})", raw_output, re.DOTALL)
            if match:
                parsed_json = json.loads(match.group(1))
            else:
                parsed_json = {"error": "No JSON found in agent output."}

        except ValueError as e:
            print(f"❌ Agent execution failed: {e}")
            match = re.search(r"(\{.*\})", str(e), re.DOTALL)
            if match:
                try:
                    parsed_json = json.loads(match.group(1))
                except json.JSONDecodeError:
                    parsed_json = {"error": "Failed to decode JSON from ValueError."}
            else:
                parsed_json = {"error": "No JSON found in ValueError."}

        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            parsed_json = {"error": str(e)}

        # Save JSON report
        with open(output_file, "w") as f:
            json.dump(parsed_json, f, indent=2)

        print(f"📄 JSON report saved to {output_file}")
        return parsed_json
