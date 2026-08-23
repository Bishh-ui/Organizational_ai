import argparse

from config_reader import load_config
from pipeline_runner import run_pipeline


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser("data-pipeline")
    p.add_argument("command", choices=["run"], help="Command to run")
    p.add_argument(
        "--config",
        default="config/pipeline_config.yaml",
        help="Pipeline config YAML",
    )
    p.add_argument("--input", help="Input PDF/TXT file or directory (overrides config)")
    p.add_argument("--output", help="Output JSON file (overrides config)")
    return p


def main():
    parser = build_parser()
    args = parser.parse_args()

    cfg1 = load_config(args.config)
    cfg2 = load_config("config/model_config.yaml")
    cfg = (cfg1 or {}) | (cfg2 or {})

    input_path = args.input or cfg.get("input_path", "")
    out_file = args.output or cfg.get("output_file", "data/output/results.json")

    if not input_path:
        parser.error("No input path provided. Use --input or set input_path in config.")

    run_pipeline(input_path, out_file, cfg)


if __name__ == "__main__":
    main()
