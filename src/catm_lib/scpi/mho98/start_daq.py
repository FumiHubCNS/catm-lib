from __future__ import annotations

import argparse
import sys

from acquisition import RigolScope
from storage import ScopeHDF5Writer
from viewer import launch_scope_viewer, queue_waveform


def parse_args():
    parser = argparse.ArgumentParser(
        description="Acquire triggered scope waveforms from all channels, save to HDF5, and optionally plot live."
    )
    parser.add_argument(
        "-ip", 
        "--ip", 
        # required=True,
        type=str,
        default="172.16.206.60",
        help="Oscilloscope IP address"
        )
    
    parser.add_argument(
        "-n",
        "--num-triggers",
        type=int,
        default=10,
        help="Number of triggers to acquire",
    )

    parser.add_argument(
        "-of",
        "--output-file",
        default="scope_data.h5",
        help="Output HDF5 filename",
    )

    parser.add_argument(
        "-ch",
        "--channels",
        nargs="+",
        type=int,
        default=[1, 2, 3, 4],
        help="Channels to acquire, e.g. -ch 1 2 3 4",
    )

    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="Single-trigger wait timeout in seconds",
    )

    parser.add_argument(
        "--points",
        type=int,
        default=1000,
        help="Waveform points to request in NORMal mode",
    )

    parser.add_argument(
        "--no-viewer",
        action="store_true",
        help="Disable live viewer",
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print SCPI commands and responses",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    scope = RigolScope(
        ip=args.ip,
        timeout_ms=10000,
        backend="@py",
        verbose=args.verbose,
    )

    writer = ScopeHDF5Writer(args.output_file)

    viewer_proc = None
    viewer_queue = None
    if not args.no_viewer:
        viewer_proc, viewer_queue = launch_scope_viewer(interval_ms=50)

    try:
        scope.connect()
        print("Connected to:", scope.get_idn())

        # 表示範囲波形
        scope.setup_waveform_transfer(
            points=args.points,
            mode="NORMal",
            fmt="BYTE",
        )

        for trig_idx in range(args.num_triggers):
            print(f"Waiting trigger {trig_idx} ...")
            records = scope.acquire_one_trigger_all_channels(
                trigger_index=trig_idx,
                channels=args.channels,
                timeout_s=args.timeout,
            )

            writer.append_many(records)

            for record in records:
                print(
                    f"Saved trigger={record.trigger_index}, "
                    f"ch={record.channel_index}, "
                    f"points={len(record.time_us)}"
                )

                if viewer_queue is not None:
                    queue_waveform(
                        viewer_queue,
                        trigger_index=record.trigger_index,
                        channel_index=record.channel_index,
                        time_us=record.time_us,
                        voltage_mV=record.voltage_mV,
                    )

        print(f"Done. Data saved to {args.output_file}")
        return 0

    except KeyboardInterrupt:
        print("Interrupted by user.")
        return 130

    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    finally:
        try:
            scope.close()
        finally:
            writer.close()
            if viewer_queue is not None:
                viewer_queue.put(None)
            if viewer_proc is not None:
                viewer_proc.join(timeout=1.0)


if __name__ == "__main__":
    raise SystemExit(main())