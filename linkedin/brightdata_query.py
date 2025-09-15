import requests
import json
import time
import pandas as pd
from IPython.display import display

# --- Configuration ---
API_KEY = "5edee3b2-e38f-4a19-9f00-30915fad054d"
DATASET_ID = "gd_l1viktl72bvl7bjuj0"

# --- API Endpoint Definitions ---
FILTER_API_URL = "https://api.brightdata.com/datasets/filter"
SNAPSHOTS_BASE_URL = "https://api.brightdata.com/datasets/snapshots"


# --- Common Search Parameters ---
BAY_AREA_CITIES = [
    "San Francisco", "Palo Alto", "Mountain View", "San Jose",
    "Oakland", "Berkeley", "Sunnyvale", "Menlo Park", "Cupertino",
    "Santa Clara", "Bay Area"
]

# UPDATED: Added seniority levels to capture leadership roles
POSITION_TITLES = [
    "Product Marketing", "PMM", "Technical Marketing"#, "Lead", "Head","Senior", "Manager"
]

AI_KEYWORDS = [
    "AI", "Machine Learning", "MLOps", "Developer Tools", "Data Platform",
    "SaaS", "PaaS", "LLM", "Generative AI", "Data-centric", "RAG",
    # Tier 1: Core Product & Technical Keywords
    "Private LLM", "LLM Training", "Model Training", "Fine-tuning", "AI Platform", "On-premise AI", "On-prem", "Enterprise AI",
    # Tier 3: Broader AI & Developer Ecosystem Keywords
    "AI Infrastructure", "Developer Tools", "API Marketing", "SDK", "AI Framework", "Observability", "AI Evaluation", "Data Privacy", "AI Security"
]

STARTUP_KEYWORDS = [
    "0 to 1", "0-to-1", "Zero to One", "go-to-market", "GTM", "product launch", "early stage","seed stage", "zero to one",
    "Founder", "Founding Team", "Head of Marketing",
    # Tier 2: Go-to-Market & Business Function Keywords
    "Product Marketing", "Go-to-Market", "Developer Marketing", "Technical Product Marketing", 
    "Product Launch", "Community-led Growth", "B2B SaaS","Developer Relations", "DevRel", 
]

TARGET_COMPANIES = [
    "Scale AI", "Hugging Face", "Weights & Biases", "Databricks",
    "Labelbox", "Snorkel AI", "Roboflow", "Arize AI", "WhyLabs",
    "OpenAI", "Anthropic", "Cohere",
    "Arize AI", "OctoML", 
    "Tecton", # A San Francisco-based company founded in 2019, Tecton is a leader in the feature store category for machine learning.9 Their product marketing is centered on the "data-for-AI" narrative, requiring PMMs who can articulate the value of robust data infrastructure in building high-performance AI systems. This experience is directly relevant to marketing a platform for training private LLMs, which relies on high-quality, proprietary data.
    "Snorkel AI", # Founded in May 2019 and located in Redwood City, Snorkel AI pioneered the concept of programmatic data labeling and weak supervision.12 Their GTM motion is aimed at sophisticated ML teams and requires a deep understanding of the data-centric AI development lifecycle. PMMs from Snorkel are adept at communicating a novel, highly technical approach to a core ML problem.
    "Modular", # A Palo Alto-based startup founded in 2022, Modular is building a next-generation AI developer platform designed to unify the fragmented AI/ML infrastructure stack.28 Their core product is a fast, scalable inference platform that includes the Mojo programming language, positioned as a high-performance alternative to Python that avoids CUDA lock-in.30 Their GTM is centered on marketing a challenger platform technology focused on speed and cost-efficiency, making their talent pool a prime target for Preseen.
    "LangChain", #Founded in 2022 in San Francisco, LangChain has quickly become the dominant open-source framework for developing applications powered by LLMs.31 The framework provides abstractions and tools that simplify the process of building context-aware, reasoning applications.34 Their GTM is the epitome of modern, community-led, developer-first growth. Sourcing talent from LangChain would be a grand slam, as their PMMs are marketing the essential toolkit for Preseen's core developer audience.
    "Arize AI", #Founded in January 2020 and headquartered in Berkeley, Arize AI is a leader in the ML observability and model monitoring market.2 Their marketing must address complex, high-stakes technical issues, requiring PMMs who can build a narrative around trust and control in production AI systems. Their competitor landscape is rich with similar, recently founded companies, indicating a vibrant talent pool in this domain.42
    "Aporia", #Founded in 2019/2020 with a US office, Aporia is a direct competitor to Arize AI in the ML observability space.46 The company was recently acquired by Coralogix, a move that often makes early-stage talent more receptive to new opportunities.48 Aporia's product messaging, which emphasizes guardrails against hallucinations, data leakage, and prompt attacks, aligns perfectly with the security and reliability narrative essential for marketing private LLMs.4
    "Confident AI", #An extremely high-value and recent target, Confident AI was founded in San Francisco in 2024.51 It is an LLM evaluation platform built by the creators of the popular open-source DeepEval framework.53 Their entire GTM is centered on enabling developers to test, evaluate, and deploy LLMs with 
    "Cohere", # With operations in San Francisco and Toronto, Cohere was founded in 2019 with a specific focus on providing enterprise-grade LLMs.19 This enterprise-first orientation means their PMMs have deep experience in B2B messaging, vertical-specific use cases, and communicating the value of data privacy and security in the context of LLMs.
    "Perplexity AI", # Founded in San Francisco in 2022, Perplexity AI has built a popular AI-native search engine.56 While its primary product is consumer-facing, the company's rapid growth demonstrates a strong product and engineering culture. Their recent expansion into enterprise knowledge search, allowing users to query internal documents, makes their talent increasingly relevant to B2B AI challenges.
    "Inflection AI", # Founded in Palo Alto in 2022, Inflection AI developed the "Pi" personal AI chatbot before its core team was "acqui-hired" by Microsoft in March 2024.62 This event creates a unique, time-sensitive opportunity to source top-tier talent who built a product from 0-to-1 and may now be seeking a return to a startup environment. Their focus on "personal intelligence" and human-centered AI aligns well with the bespoke nature of private LLMs.
    "Glean", #  A Palo Alto-based company founded in 2019, Glean uses AI to power a unified enterprise search experience across all of a company's applications.22 Backed by top-tier VCs like Sequoia, Glean has built a powerful B2B marketing engine and maintains a high bar for talent.23 Their PMMs are skilled at selling a high-value AI solution into the enterprise.
    "Adept AI", # ● Founded in San Francisco in January 2022, Adept AI is building an "AI teammate" designed to automate complex enterprise workflows by interacting with existing software tools.25 Their marketing challenge involves selling a new paradigm of human-computer interaction to businesses, requiring PMMs who can craft visionary and compelling narratives.
    "Sierra", # Founded in 2023 by Bret Taylor (former co-CEO of Salesforce) and Clay Bavor (former head of Google's VR efforts), Sierra is a conversational AI platform for customer service.64 This is a top-tier target. Their GTM is focused on selling AI agents that can be personalized to embody a company's brand, voice, and policies—a direct parallel to Preseen's value proposition of private, customized LLMs.68
    "Harvey AI" # A leader in AI for legal and professional services, Harvey AI was founded in San Francisco in January 2022.24 Their product marketers must be adept at selling to a risk-averse, highly specialized vertical, demonstrating a sophisticated ability to build trust and articulate value. The burgeoning "Legal AI" space, with competitors like Aline and CoCounsel, indicates a growing pool of talent with this specialized skill set.70
    "Pika", # Founded in Palo Alto in 2023, Pika is a generative AI platform for video creation.73 While focused on a different modality (video vs. text), their rapid, product-led growth in a competitive new category makes their early marketing talent valuable.76 A PMM from Pika would possess invaluable experience in modern user acquisition strategies and building a brand from scratch in a noisy market.
    "Confident AI", # Most recent founding date; GTM is centered on trust and reliability, a perfect parallel for private LLMs.5
    "Aline", # Aline is a legal AI company that provides a platform for legal research and analysis.
    "Sierra", # Sierra is a conversational AI platform for customer service.
    "Run.ai", # Acquired by Nvidia for $700 million; An AI infrastructure management startup that provided a Kubernetes-based platform for managing and orchestrating AI workloads. This $700 million acquisition highlights the critical importance of AI infrastructure. Talent from Run.ai is expert in the technical nuts and bolts of deploying AI at scale, a crucial skill set for marketing a private LLM platform.
    "CoCounsel", # CoCounsel is a legal AI company that provides a platform for legal research and analysis.
    "Dazz", # Acquired by Wiz, A cloud remediation and cybersecurity startup focused on application security and threat management.Acquired for a reported $450 million, Dazz's team is skilled in selling high-stakes security solutions to enterprises, a GTM motion that requires building significant trust and technical credibility.
    "Alcion", # Acquired by Veeam; Alcion is a A very recent startup whose team has experience building and marketing AI solutions that address core enterprise needs for data security and resilience.
    "Definitive Intelligence", # An AI solutions provider that built business-oriented tools, including AI chatbots, data visualization, and autonomous analytics. The team was acquired to build and lead GroqCloud, the developer-facing platform for Groq's high-speed inference chips. This talent is now at the forefront of developer marketing for a cutting-edge AI infrastructure company.
    "Tenyx", # A developer of AI-powered voice agents that create natural and engaging conversational experiences for customer service. This team specializes in building and marketing human-like voice AI for enterprise use cases. Their expertise in voice and conversational AI is highly relevant for any platform aiming to create natural user interactions.
    "Aporia", # An ML observability platform focused on monitoring models in production to detect drift, bias, and performance issues. Talent from Aporia is expert in marketing the concepts of trust, reliability, and control for AI systems—a narrative that aligns perfectly with the value proposition of a private LLM platform.   
    "Ghost Autonomy", # Developed autonomous driving software, initially for consumer kits and later pivoting to crash prevention technology. After raising nearly $220 million, the company shut down due to the inability to secure further funding. Its team of ~100 employees has deep experience in building and marketing a highly complex, safety-critical AI system.
    "Modal Labs" # 主打云原生、Serverless 的模型部署与推理，其 PMM 极度理解开发者需求和云基础设施。
    "Baseten", # 为 ML 团队提供模型部署和应用构建的基础设施，目标用户与我们高度重叠。
    "Pinecone", "Weaviate",  "Chroma", #向量数据库的“三巨头”。他们的 PMM 是将抽象的“向量搜索”概念成功推向市场的专家，对 RAG 场景的理解极其深刻。
    "MotherDuck", # 基于 DuckDB 的 Serverless 数据分析平台，其 GTM 策略在开发者社区中非常成功，值得关注。
    "Replicate",# 让开发者通过 API 轻松运行和微调开源模型，其 PMM 非常擅长降低复杂技术的上手门槛。
    "Determined AI", # (被 HPE 收购): 开源的深度学习训练平台，其早期团队对 MLOps 和模型训练有深刻理解。"
    'Primer AI', # (近期战略调整): NLP 领域的早期独角兽，经历过市场从 NLP 到 LLM 的转变，相关人才经验宝贵。'
]

# --- Helper Functions ---


def display_profiles_as_table(records):
    """Converts a list of profile records into a pandas DataFrame and displays it."""
    if not records:
        print("No records to display.")
        return
    df = pd.DataFrame(records)
    relevant_columns = [
        'name', 'position', 'current_company_name', 'city', 'about',
        'experience', 'url'
    ]
    display_columns = [col for col in relevant_columns if col in df.columns]
    if not display_columns:
        print("Could not find standard columns. Displaying all available columns.")
        display(df)
        return
    pd.set_option('display.max_rows', 100)
    pd.set_option('display.max_colwidth', 150)
    print("\n--- Candidate Profiles ---")
    display(df[display_columns])


# --- Search Strategy Payload Creation ---

def create_strategy_1_payload():
    """Strategy 1: The Broad Net (Core Profile)."""
    return {
        "dataset_id": DATASET_ID,
        "filter": {
            "operator": "and",
            "filters": [
                {"name": "position", "value": POSITION_TITLES, "operator": "includes"},
                {"name": "city", "value": BAY_AREA_CITIES, "operator": "includes"},
            ]
        }
    }

def create_strategy_2_payload():
    """Strategy 2: The AI & Startup Focus (High-Relevance)."""
    return {
        "dataset_id": DATASET_ID,
        "filter": {
            "operator": "and",
            "filters": [
                {"name": "position", "value": POSITION_TITLES, "operator": "includes"},
                {"name": "city", "value": BAY_AREA_CITIES, "operator": "includes"},
                {'operator': 'or', 'filters': [
                    {"name": "about", "value": AI_KEYWORDS, "operator": "includes"},
                    {"name": "experience", "value": AI_KEYWORDS, "operator": "includes"}
                ]},
                {'operator': 'or', 'filters': [
                    {"name": "about", "value": STARTUP_KEYWORDS, "operator": "includes"},
                    {"name": "experience", "value": STARTUP_KEYWORDS, "operator": "includes"}
                ]},
                {"name": "experience", "value": TARGET_COMPANIES, "operator": "includes"},
            ]
        }
    }

def create_strategy_3_payload():
    """Strategy 3: The Ecosystem Poach (Targeted)."""
    return {
        "dataset_id": DATASET_ID,
        "filter": {
            "operator": "and",
            "filters": [
                {"name": "position", "value": POSITION_TITLES, "operator": "includes"},
                {"name": "city", "value": BAY_AREA_CITIES, "operator": "includes"},
                {"name": "experience", "value": TARGET_COMPANIES, "operator": "includes"},
                {"name": "current_company_name", "value": TARGET_COMPANIES, "operator": "includes"}
            ]
        }
    }

# --- Query Visualization and Execution ---

def _parse_filter_recursive(filter_obj, indent_level=0):
    """Recursively parses a filter object and returns a human-readable description."""
    indent = "  " * indent_level
    
    # Handle field filters (leaf nodes)
    if "name" in filter_obj and "operator" in filter_obj and "value" in filter_obj:
        field_name = filter_obj["name"]
        operator = filter_obj["operator"]
        value = filter_obj["value"]
        
        # Format field names for better readability
        field_display_names = {
            "position": "Position title",
            "city": "Location",
            "about": "About section",
            "experience": "Experience section",
            "current_company_name": "Current company"
        }
        
        field_display = field_display_names.get(field_name, field_name)
        
        # Format values for display
        if isinstance(value, list):
            if len(value) <= 5:
                value_str = str(value)
            else:
                value_str = f"{value[:3]}... and {len(value)-3} more"
        else:
            value_str = str(value)
        
        # Format operator descriptions
        operator_descriptions = {
            "=": "equals",
            "!=": "does not equal",
            "<": "is less than",
            "<=": "is less than or equal to",
            ">": "is greater than",
            ">=": "is greater than or equal to",
            "in": "is one of",
            "not_in": "is not one of",
            "includes": "contains any of",
            "not_includes": "does not contain any of",
            "array_includes": "includes",
            "not_array_includes": "does not include",
            "is_null": "is null",
            "is_not_null": "is not null"
        }
        
        operator_desc = operator_descriptions.get(operator, operator)
        return f"{indent}- {field_display} {operator_desc}: {value_str}"
    
    # Handle filter groups (non-leaf nodes)
    elif "operator" in filter_obj and "filters" in filter_obj:
        operator = filter_obj["operator"]
        filters = filter_obj["filters"]
        
        if operator == "and":
            if indent_level == 0:
                # Top-level AND - just process each filter
                results = []
                for f in filters:
                    result = _parse_filter_recursive(f, indent_level + 1)
                    if result:
                        results.append(result)
                return results
            else:
                # Nested AND - show as "AND" condition
                results = [f"{indent}- ALL of the following:"]
                for f in filters:
                    result = _parse_filter_recursive(f, indent_level + 1)
                    if result:
                        results.append(result)
                return results
                
        elif operator == "or":
            # OR condition
            results = [f"{indent}- ANY of the following:"]
            for f in filters:
                result = _parse_filter_recursive(f, indent_level + 1)
                if result:
                    results.append(result)
            return results
    
    return None

def _flatten_results(results):
    """Flattens nested list results into a single list of strings."""
    flattened = []
    if isinstance(results, list):
        for result in results:
            if isinstance(result, list):
                flattened.extend(_flatten_results(result))
            else:
                flattened.append(result)
    else:
        flattened.append(results)
    return flattened

def view_query_in_natural_language(payload, strategy_name):
    """Translates the JSON payload into a human-readable format using recursive parsing."""
    print(f"--- {strategy_name} ---")
    print("This search will find candidates where:")
    
    filter_obj = payload.get("filter", {})
    if not filter_obj:
        print("  - No filters specified")
        return
    
    # Parse the filter recursively
    parsed_results = _parse_filter_recursive(filter_obj)
    
    # Flatten and display results
    flattened_results = _flatten_results(parsed_results)
    for result in flattened_results:
        if result:  # Only print non-empty results
            print(result)

    print("-" * (len(strategy_name) + 6))


def run_search(payload, poll_interval=15, timeout=300):
    """
    Executes the full asynchronous search workflow with a confirmation step,
    robust polling, and handles partitioned snapshot downloads.
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    print("\n--- Search Execution ---")
    print("Payload to be sent:")
    print(json.dumps(payload, indent=2))
    print("----------------------------")
    
    # confirm = input("The vendor charges per row of data returned. Do you want to execute this search? (y/n): ")
    # if confirm.lower() not in ['y', 'yes']:
    #     print("Search aborted by user.")
    #     return

    print("\n--- Initiating Filter Job... ---")
    init_response = requests.post(FILTER_API_URL, headers=headers, json=payload)
    
    if not init_response.ok:
        print(f"Failed to initiate job. Status: {init_response.status_code}, Response: {init_response.text}")
        return

    snapshot_id = init_response.json().get('snapshot_id')
    if not snapshot_id:
        print(f"Error: 'snapshot_id' not found in initiation response. Full response: {init_response.json()}")
        return
    print(f"Successfully initiated job. Snapshot ID: {snapshot_id}")

    start_time = time.time()
    snapshot_meta_url = f"{SNAPSHOTS_BASE_URL}/{snapshot_id}"
    snapshot_data = {}
    
    while time.time() - start_time < timeout:
        print(f"Polling for snapshot status...")
        meta_response = requests.get(snapshot_meta_url, headers=headers)
        
        if not meta_response.ok:
            print(f"Failed to poll status. Status: {meta_response.status_code}")
            time.sleep(poll_interval)
            continue
            
        snapshot_data = meta_response.json()
        status = snapshot_data.get('status')
        print(f"Current job status: '{status}'")

        if status in ['ready', 'failed']:
            break
        
        time.sleep(poll_interval)
    else:
        print(f"Timeout: Job did not complete within {timeout} seconds.")
        return

    if status == 'failed':
        print("\n--- Search Complete: Job Failed ---")
        print(f"Warning from API: {snapshot_data.get('warning')}")
        return

    record_count = snapshot_data.get('records_count')
    if record_count is None:
        print(f"Could not determine record count. Final metadata: {snapshot_data}")
        return
    
    print(f"\nJob complete. Found {record_count} matching profiles.")

    if record_count > 0:
        all_records = []
        parts_count = snapshot_data.get('parts_count', 1)

        if parts_count > 1:
            print(f"Snapshot is split into {parts_count} parts. Downloading each part...")
            for i in range(1, parts_count + 1):
                part_url = f"{snapshot_meta_url}/parts/{i}"
                print(f"  - Downloading part {i}/{parts_count}...")
                part_response = requests.get(part_url, headers=headers, stream=True)
                if part_response.ok:
                    try:
                        records = [json.loads(line) for line in part_response.text.strip().split('\n')]
                        all_records.extend(records)
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON from part {i}: {e}")
                else:
                    print(f"Failed to download part {i}. Status: {part_response.status_code}")
        else:
            download_url = f"{snapshot_meta_url}/download"
            print(f"Downloading single snapshot file...")
            download_response = requests.get(download_url, headers=headers)
            if download_response.ok:
                try:
                    all_records = [json.loads(line) for line in download_response.text.strip().split('\n')]
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON from snapshot: {e}")
            else:
                print(f"Failed to download data. Status: {download_response.status_code}")
        
        display_profiles_as_table(all_records)
    else:
        print("No profiles found matching the criteria.")






# --- Main Execution for Notebook ---
if __name__ == "__main__":
    # --- STAGE 1: Define and View All Queries ---
    payload_1 = create_strategy_1_payload()
    payload_2 = create_strategy_2_payload()
    payload_3 = create_strategy_3_payload()
    
    print("="*40)
    print("      PREVIEW OF SEARCH STRATEGIES")
    print("="*40)
    view_query_in_natural_language(payload_1, "Strategy 1: Broad Search")
    print("\n")
    view_query_in_natural_language(payload_2, "Strategy 2: Focused Search (AI or Startup)")
    print("\n")
    view_query_in_natural_language(payload_3, "Strategy 3: Targeted Search (Competitors)")
    
    
    # --- STAGE 2: Execute a Specific Query ---
    # INSTRUCTIONS: Uncomment the line for the strategy you wish to run.
    print("\nTo execute a search, uncomment one of the following lines and run this script/cell:")
    # run_search(payload_1)
    run_search(payload_2) # Recommended starting point
    # run_search(payload_3)