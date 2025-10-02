#!/usr/bin/env python3
"""
Batch Query Processor for Apllos Assistant.

Overview
--------
Process multiple queries from a YAML file and generate a comprehensive report
with all responses, classifications, and metadata. Useful for testing the
system with multiple queries at once.

Design
------
1) Load queries from YAML file (queries + optional attachments)
2) Process each query through the assistant API
3) Generate formatted output with clear separation between queries
4) Include input, agent classification, confidence, reason, and full response

Integration
-----------
- Uses the same API endpoint as query_assistant.py
- Supports both text queries and file attachments
- Generates human-readable output file with all results

Usage
-----
$ python scripts/batch_query.py --input queries.yaml --output results.txt
$ python scripts/batch_query.py --input test_queries.yaml --output batch_results.md
"""

import argparse
import asyncio
import json
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import httpx
import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def load_queries(yaml_file: Path) -> List[Dict[str, Any]]:
    """Load queries from YAML file."""
    try:
        with open(yaml_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        queries = data.get('queries', [])
        if not queries:
            raise ValueError("No 'queries' section found in YAML file")
        
        return queries
    except Exception as e:
        print(f"Error loading YAML file: {e}")
        sys.exit(1)


async def process_query(
    client: httpx.AsyncClient,
    query_data: Dict[str, Any],
    query_index: int
) -> Dict[str, Any]:
    """Process a single query through the assistant API."""
    
    query_text = query_data.get('query', '')
    attachment = query_data.get('attachment', '')
    description = query_data.get('description', '')
    
    try:
        # Prepare input data like query_assistant.py
        input_data = {}
        
        if query_text:
            input_data["query"] = query_text
        
        # Handle attachment if provided
        if attachment:
            attachment_path = Path(attachment)
            if attachment_path.exists():
                try:
                    with open(attachment_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    input_data["attachment"] = {
                        "filename": attachment_path.name,
                        "content": content,
                        "type": "text/plain"
                    }
                except Exception as e:
                    print(f"Warning: Could not read attachment {attachment}: {e}")
            else:
                print(f"Warning: Attachment file not found: {attachment}")
        
        if not input_data:
            return {
                "query_index": query_index,
                "input": query_data,
                "error": "No query or attachment provided",
                "success": False
            }
        
        # Create empty thread (like query_assistant.py)
        response = await client.post(
            "http://localhost:2024/threads",
            json={},
            timeout=120.0
        )
        
        if response.status_code != 200:
            return {
                "query_index": query_index,
                "input": query_data,
                "error": f"Thread creation HTTP {response.status_code}: {response.text}",
                "success": False
            }
        
        thread_data = response.json()
        thread_id = thread_data.get("thread_id")
        
        if not thread_id:
            return {
                "query_index": query_index,
                "input": query_data,
                "error": "No thread_id in response",
                "success": False
            }
        
        # Create and start a run with input data
        run_data = {
            "assistant_id": "assistant",
            "input": input_data
        }
        response = await client.post(
            f"http://localhost:2024/threads/{thread_id}/runs",
            json=run_data,
            timeout=120.0
        )
        
        if response.status_code != 200:
            return {
                "query_index": query_index,
                "input": query_data,
                "error": f"Run HTTP {response.status_code}: {response.text}",
                "success": False
            }
        
        run_response = response.json()
        run_id = run_response.get("run_id")
        
        # Wait for completion
        max_attempts = 30
        for attempt in range(max_attempts):
            state_response = await client.get(
                f"http://localhost:2024/threads/{thread_id}/state",
                timeout=60.0
            )
            
            if state_response.status_code != 200:
                continue
                
            state_data = state_response.json()
            values = state_data.get("values", {})
            
            # Check if processing is complete (has answer)
            if values.get("answer"):
                break
                
            await asyncio.sleep(1)
        else:
            return {
                "query_index": query_index,
                "input": query_data,
                "error": "Timeout waiting for response",
                "success": False
            }
        
        # Extract response data
        answer = values.get("answer", {})
        router_decision = values.get("router_decision", {})
        agent = values.get("agent", "unknown")
        
        return {
            "query_index": query_index,
            "input": query_data,
            "thread_id": thread_id,
            "agent": agent,
            "confidence": router_decision.get("confidence", "N/A"),
            "reason": router_decision.get("reason", "N/A"),
            "answer": answer,
            "success": True
        }
        
    except Exception as e:
        if files:
            files["attachment"].close()
        return {
            "query_index": query_index,
            "input": query_data,
            "error": str(e),
            "success": False
        }


def format_output(results: List[Dict[str, Any]], output_file: Path) -> None:
    """Format and write results to output file."""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        # Header
        f.write("# Batch Query Results\n\n")
        
        # Summary section
        f.write("## Summary\n\n")
        f.write(f"- **Generated:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"- **Total Queries:** {len(results)}\n")
        
        successful = sum(1 for r in results if r.get('success', False))
        failed = len(results) - successful
        f.write(f"- **Successful:** {successful}\n")
        f.write(f"- **Failed:** {failed}\n\n")
        
        # Table of Contents
        f.write("<a id=\"table-of-contents\"></a>\n")
        f.write("## 📋 Table of Contents\n\n")
        for i, result in enumerate(results, 1):
            input_data = result.get('input', {})
            query_text = input_data.get('query', 'N/A')
            # Truncate long queries for TOC
            if len(query_text) > 60:
                query_text = query_text[:60] + "..."
            
            # Get agent classification if available
            agent = "Unknown"
            if result.get('success', False):
                agent = result.get('agent', 'Unknown')
            
            f.write(f"{i}. [{query_text}](#query-{i}) - `{agent}`\n")
        
        f.write("\n")
        
        # Results section
        f.write("---\n\n")
        f.write("## Results\n\n")
        
        for i, result in enumerate(results, 1):
            f.write(f"<a id=\"query-{i}\"></a>\n")
            f.write(f"### Query {i}\n\n")
            
            # Input section
            input_data = result.get('input', {})
            f.write("#### 📝 Input\n\n")
            f.write(f"- **Query:** {input_data.get('query', 'N/A')}\n")
            
            if input_data.get('attachment'):
                f.write(f"- **Attachment:** `{input_data.get('attachment')}`\n")
            
            f.write("\n")
            
            # Check if query was successful
            if not result.get('success', False):
                f.write("#### ❌ Error\n\n")
                f.write("```\n")
                f.write(f"{result.get('error', 'Unknown error')}\n")
                f.write("```\n\n")
                # Back to top link for errors
                f.write("**[⬆️ Back to Top](#table-of-contents)**\n\n")
                f.write("---\n\n")
                continue
            
            # Classification section
            f.write("#### 🎯 Classification\n\n")
            f.write(f"- **Agent:** `{result.get('agent', 'N/A')}`\n")
            f.write(f"- **Confidence:** {result.get('confidence', 'N/A')}\n")
            f.write(f"- **Reason:** {result.get('reason', 'N/A')}\n")
            f.write(f"- **Thread ID:** `{result.get('thread_id', 'N/A')}`\n\n")
            
            # Response section
            answer = result.get('answer', {})
            f.write("#### 💬 Response\n\n")
            
            response_text = answer.get('text', 'No response text')
            f.write("```\n")
            f.write(f"{response_text}\n")
            f.write("```\n\n")
            
            # Citations if available
            citations = answer.get('citations', [])
            if citations:
                f.write("#### 📚 Citations\n\n")
                for j, citation in enumerate(citations, 1):
                    title = citation.get('title', 'No title')
                    f.write(f"{j}. `{title}`\n")
                f.write("\n")
            
            # Chunks if available (full content)
            chunks = answer.get('chunks', [])
            if chunks:
                f.write("#### 📄 Document Chunks\n\n")
                for j, chunk in enumerate(chunks, 1):
                    title = chunk.get('title', f'Chunk {j}')
                    content = chunk.get('content', 'No content')
                    # Truncate very long chunks for readability
                    if len(content) > 500:
                        content = content[:500] + "..."
                    f.write(f"**{j}. {title}**\n\n")
                    f.write("```\n")
                    f.write(f"{content}\n")
                    f.write("```\n\n")
                f.write("\n")
            
            # Metadata if available
            meta = answer.get('meta', {})
            if meta:
                f.write("#### 📊 Metadata\n\n")
                for key, value in meta.items():
                    f.write(f"- **{key}:** {value}\n")
                f.write("\n")
            
            # Back to top link
            f.write("**[⬆️ Back to Top](#table-of-contents)**\n\n")
            f.write("---\n\n")


async def main():
    parser = argparse.ArgumentParser(description="Process batch queries for Apllos Assistant")
    parser.add_argument("--input", "-i", required=True, help="Input YAML file with queries")
    parser.add_argument("--output", "-o", help="Output file for results (default: input filename with .md extension)")
    parser.add_argument("--concurrent", "-c", type=int, default=3, help="Max concurrent requests")
    
    args = parser.parse_args()
    
    input_file = Path(args.input)
    
    # Auto-generate output filename if not provided
    if args.output:
        output_file = Path(args.output)
    else:
        output_file = input_file.with_suffix('.md')
    
    if not input_file.exists():
        print(f"Error: Input file not found: {input_file}")
        sys.exit(1)
    
    print(f"Loading queries from: {input_file}")
    queries = load_queries(input_file)
    print(f"Found {len(queries)} queries to process")
    
    print("Processing queries...")
    
    # Process queries with limited concurrency
    semaphore = asyncio.Semaphore(args.concurrent)
    
    async def process_with_semaphore(client, query_data, index):
        async with semaphore:
            print(f"Processing query {index + 1}/{len(queries)}: {query_data.get('query', '')[:50]}...")
            return await process_query(client, query_data, index)
    
    async with httpx.AsyncClient() as client:
        tasks = [
            process_with_semaphore(client, query_data, i)
            for i, query_data in enumerate(queries)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Handle any exceptions
    processed_results = []
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            processed_results.append({
                "query_index": i,
                "input": queries[i],
                "error": str(result),
                "success": False
            })
        else:
            processed_results.append(result)
    
    print(f"Writing results to: {output_file}")
    format_output(processed_results, output_file)
    
    successful = sum(1 for r in processed_results if r.get('success', False))
    failed = len(processed_results) - successful
    
    print(f"\nBatch processing complete!")
    print(f"Total queries: {len(processed_results)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Results saved to: {output_file}")


if __name__ == "__main__":
    asyncio.run(main())
