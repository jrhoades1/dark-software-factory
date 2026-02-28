#!/usr/bin/env python3
"""Extract transcripts from YouTube videos given video IDs or URLs."""

import argparse
import json
import re
import sys
from datetime import datetime, timezone

try:
    from youtube_transcript_api import YouTubeTranscriptApi
    from youtube_transcript_api._errors import (
        NoTranscriptFound,
        TranscriptsDisabled,
        VideoUnavailable,
    )
except ImportError:
    print(
        json.dumps({
            "success": False,
            "error": "youtube-transcript-api not installed. Run: pip install youtube-transcript-api",
        }),
        file=sys.stderr,
    )
    sys.exit(1)


def extract_video_id(url_or_id):
    """Extract video ID from a YouTube URL or return as-is if already an ID."""
    # Already a plain ID (11 chars, alphanumeric + dash + underscore)
    if re.match(r"^[a-zA-Z0-9_-]{11}$", url_or_id):
        return url_or_id

    # Standard watch URL
    match = re.search(r"[?&]v=([a-zA-Z0-9_-]{11})", url_or_id)
    if match:
        return match.group(1)

    # Short URL (youtu.be/ID)
    match = re.search(r"youtu\.be/([a-zA-Z0-9_-]{11})", url_or_id)
    if match:
        return match.group(1)

    # Embed URL
    match = re.search(r"embed/([a-zA-Z0-9_-]{11})", url_or_id)
    if match:
        return match.group(1)

    return url_or_id  # Return as-is and let the API handle the error


def fetch_transcript(video_id):
    """Fetch transcript for a single video. Returns (transcript_text, language, is_generated) or raises."""
    ytt_api = YouTubeTranscriptApi()

    # Try the simple fetch first (prefers manual EN, falls back to auto-generated EN)
    try:
        snippets = ytt_api.fetch(video_id, languages=["en"])
        text = " ".join(s.text for s in snippets)
        return text, "en", False
    except NoTranscriptFound:
        pass

    # Fall back: list all transcripts and take whatever is available
    transcript_list = ytt_api.list(video_id)
    for transcript in transcript_list:
        snippets = transcript.fetch()
        text = " ".join(s.text for s in snippets)
        return text, transcript.language_code, transcript.is_generated

    raise NoTranscriptFound(video_id, ["en"], transcript_list)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--video-ids",
        help="Comma-separated list of YouTube video IDs",
    )
    group.add_argument(
        "--urls",
        help="Comma-separated list of YouTube video URLs",
    )
    parser.add_argument(
        "--output",
        help="Output JSON file path (default: stdout)",
    )
    args = parser.parse_args()

    # Parse input
    if args.video_ids:
        raw_ids = [v.strip() for v in args.video_ids.split(",") if v.strip()]
    else:
        raw_ids = [v.strip() for v in args.urls.split(",") if v.strip()]

    video_ids = [extract_video_id(v) for v in raw_ids]

    transcripts = []
    failures = []

    for video_id in video_ids:
        try:
            text, language, is_generated = fetch_transcript(video_id)
            word_count = len(text.split())
            transcripts.append({
                "video_id": video_id,
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "transcript_text": text,
                "word_count": word_count,
                "language": language,
                "is_generated": is_generated,
            })
        except TranscriptsDisabled:
            failures.append({"video_id": video_id, "reason": "TranscriptsDisabled"})
        except VideoUnavailable:
            failures.append({"video_id": video_id, "reason": "VideoUnavailable"})
        except NoTranscriptFound:
            failures.append({"video_id": video_id, "reason": "NoTranscriptFound"})
        except Exception as e:
            failures.append({"video_id": video_id, "reason": str(e)})

    result = {
        "run_date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "videos_processed": len(transcripts),
        "videos_failed": len(failures),
        "transcripts": transcripts,
        "failures": failures,
    }

    output = json.dumps(result, indent=2)
    if args.output:
        from pathlib import Path
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"Output saved to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
