#!/usr/bin/env python3
"""プロンプト自動最適化ツール

Usage:
    python optimize_prompt.py "最適化したいプロンプト"
    python optimize_prompt.py -f prompt.txt
    echo "プロンプト" | python optimize_prompt.py
"""
import sys
import argparse
import anthropic


def optimize_prompt(original_prompt: str) -> str:
    client = anthropic.Anthropic()
    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        system="あなたはプロンプトエンジニアリングの専門家です。与えられたプロンプトをより明確・効果的・簡潔になるよう改善してください。改善後のプロンプトのみを返してください。",
        messages=[
            {"role": "user", "content": f"以下のプロンプトを最適化してください:\n\n{original_prompt}"}
        ],
    )
    return response.content[0].text


def main():
    parser = argparse.ArgumentParser(description="プロンプト自動最適化ツール")
    parser.add_argument("prompt", nargs="?", help="最適化したいプロンプト")
    parser.add_argument("-f", "--file", help="プロンプトを読み込むファイル")
    args = parser.parse_args()

    if args.file:
        with open(args.file) as f:
            prompt = f.read().strip()
    elif args.prompt:
        prompt = args.prompt
    elif not sys.stdin.isatty():
        prompt = sys.stdin.read().strip()
    else:
        parser.error("プロンプトを引数、-f ファイル、またはパイプで渡してください")

    result = optimize_prompt(prompt)
    print(result)


if __name__ == "__main__":
    main()
