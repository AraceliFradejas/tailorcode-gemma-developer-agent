"""Opt-in single public task evaluation on an already provisioned Linux GPU host.

Follows the organizer's getting-started notebook (September 27, 2026).
Does not install packages, download inputs, allocate cloud compute, or submit.
This integration has not yet been exercised against a running model.
"""
import argparse
import asyncio
import hashlib
import json
import os
import shutil
from pathlib import Path

from check_smoke_environment import inspect_environment
from prepare_evaluation import select_tasks

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-root', type=Path, required=True)
    parser.add_argument('--model-path', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--task-id', default='fastapi_14786',
                        choices=['fastapi_14786', 'rich_4077', 'requests_6592'])
    parser.add_argument('--run-agent', action='store_true',
                        help='Explicitly start model inference on the current host')
    args = parser.parse_args()
    if not args.run_agent:
        parser.exit(2, 'Stopped: inference requires --run-agent after runtime/cost approval.\n')
    report = inspect_environment(args.data_root, args.model_path, args.task_id)
    if report['blockers']:
        print(json.dumps(report, indent=2))
        parser.exit(1, 'Environment is not ready. No model started.\n')
    suite = json.loads((ROOT / 'evaluation/smoke-suite.json').read_text())
    suite['tasks'] = [t for t in suite['tasks'] if t['instance_id'] == args.task_id]
    selected = select_tasks(args.data_root / 'tasks.jsonl', suite)
    args.output.mkdir(parents=True, exist_ok=False)
    task_path = args.output / 'tasks.jsonl'
    task_path.write_text(json.dumps(selected[0]) + '\n')
    agent_dir = args.output / 'agent'
    shutil.copytree(ROOT / 'agents/baseline', agent_dir)
    report.update(status='starting', inference='pending', max_time_minutes=5,
                  max_tool_calls=50, max_turns=100,
                  agent_files_sha256={str(p.relative_to(agent_dir)): hashlib.sha256(p.read_bytes()).hexdigest()
                                      for p in sorted(agent_dir.rglob('*.yaml'))})
    report_path = args.output / 'run.json'

    def save_report():
        report_path.write_text(json.dumps(report, indent=2, default=str) + '\n')

    save_report()
    for key, value in {
        'LITELLM_LOCAL_MODEL_COST_MAP': 'True', 'TRANSFORMERS_NO_TF': '1',
        'VLLM_WORKER_MULTIPROC_METHOD': 'spawn', 'VLLM_ENGINE_READY_TIMEOUT_S': '1200',
        'VLLM_MEMORY_PROFILER_ESTIMATE_CUDAGRAPHS': '1', 'VLLM_NO_USAGE_STATS': '1',
        'OTEL_SDK_DISABLED': 'true', 'PYTORCH_CUDA_ALLOC_CONF': 'expandable_segments:True',
    }.items():
        os.environ[key] = value
    server = None
    try:
        import litellm
        import torch
        from adk_submission import VllmConfig, VllmServer, discover_adapters
        from google.adk.agents.context_cache_config import ContextCacheConfig
        from google.adk.apps._configs import EventsCompactionConfig
        from swegemma.config import ALLOWED_ADAPTER_EXTENSIONS, EvalConfig, build_submission_limits
        from swegemma.evaluate import Evaluator
        from swegemma.models import load_tasks
        from swegemma.models.discovery import validate_single_declared_model

        litellm.drop_params = True
        declared_model = validate_single_declared_model(agent_dir)
        adapters = discover_adapters(str(agent_dir), adapter_extensions=ALLOWED_ADAPTER_EXTENSIONS)
        gpu_count = torch.cuda.device_count()
        if not torch.cuda.is_available() or gpu_count < 1:
            raise RuntimeError('PyTorch cannot use a CUDA GPU')
        config = VllmConfig(
            model=str(args.model_path), host='127.0.0.1', port=8000,
            tool_call_parser='gemma4', reasoning_parser='gemma4',
            default_chat_template_kwargs={'enable_thinking': True},
            max_model_len=32768, dtype='bfloat16' if torch.cuda.is_bf16_supported() else 'auto',
            gpu_memory_utilization=0.90, enable_auto_tool_choice=True,
            enable_lora=True, max_loras=8, max_lora_rank=128,
            tensor_parallel_size=4 if gpu_count >= 4 else (2 if gpu_count >= 2 else 1),
            startup_timeout=1200,
        )
        server = VllmServer(config, adapter_manifest=adapters)
        server.start()
        models = server.create_model_registry(aliases=[declared_model],
                                              model_prefix='openai/', api_key='EMPTY')
        limits, constraints = build_submission_limits()
        evaluation = EvalConfig(
            tasks_path=task_path, snapshots_dir=args.data_root / 'snapshots',
            results_dir=args.output / 'results', submission_dir=agent_dir,
            models=models, sandbox='subprocess', timeout_seconds=300,
            max_time_minutes=5.0, max_tool_calls=50, max_turns=100,
            limits=limits, generation_constraints=constraints, adapter_manifest=adapters,
            context_cache_config=ContextCacheConfig(min_tokens=2048, ttl_seconds=1800, cache_intervals=10),
            events_compaction_config=EventsCompactionConfig(
                compaction_interval=15, overlap_size=2, token_threshold=14336, event_retention_size=5),
            graph_dir=str(args.data_root / 'graphs'), embeddings_dir=str(args.data_root / 'embeddings'),
            wheels_dir=args.data_root / 'wheels', verbose=False,
        )
        report.update(status='evaluating', inference='started')
        save_report()
        result = asyncio.run(Evaluator(evaluation).evaluate_task(
            task=load_tasks(task_path)[0], task_index=1, total_tasks=1))
        (args.output / 'agent.patch').write_text(result.agent_patch or '')
        report.update(status='completed', inference='completed', resolved=result.resolved,
                      test_exit_code=result.test_exit_code, tool_calls=result.tool_calls,
                      duration_seconds=result.duration_seconds)
        print(json.dumps(report, indent=2, default=str))
    except BaseException as exc:
        report.update(status='failed', error=f'{type(exc).__name__}: {exc}')
        raise
    finally:
        try:
            if server is not None:
                server.stop()
        finally:
            save_report()
            print('Model cleanup attempted. Disconnect/delete the cloud runtime separately to stop credit use.')


if __name__ == '__main__':
    main()
