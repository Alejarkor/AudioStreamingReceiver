#!/usr/bin/env python3
"""Low latency stereo video streaming receiver using GStreamer."""

import argparse
import sys

from gi.repository import Gst, GLib


def build_pipeline(url: str) -> Gst.Pipeline:
    """Create a GStreamer pipeline for low latency video and stereo audio."""
    pipeline_description = (
        f"rtspsrc location={url} latency=0 ! "
        "decodebin name=dec "
        "dec. ! queue leaky=2 max-size-buffers=5 ! videoconvert ! autovideosink sync=false "
        "dec. ! queue leaky=2 max-size-buffers=5 ! audioconvert ! audioresample ! audio/x-raw,channels=2 ! autoaudiosink sync=false"
    )
    return Gst.parse_launch(pipeline_description)


def main() -> int:
    parser = argparse.ArgumentParser(description="Receive low latency stereo video stream")
    parser.add_argument("url", help="RTSP URL of the stream")
    args = parser.parse_args()

    Gst.init(None)
    pipeline = build_pipeline(args.url)

    loop = GLib.MainLoop()

    def on_message(bus, message):
        t = message.type
        if t == Gst.MessageType.EOS:
            loop.quit()
        elif t == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            print(f"Error: {err}", debug, file=sys.stderr)
            loop.quit()
        return True

    bus = pipeline.get_bus()
    bus.add_signal_watch()
    bus.connect("message", on_message)

    pipeline.set_state(Gst.State.PLAYING)
    try:
        loop.run()
    finally:
        pipeline.set_state(Gst.State.NULL)
    return 0


if __name__ == "__main__":
    sys.exit(main())
