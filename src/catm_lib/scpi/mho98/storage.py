from __future__ import annotations

from pathlib import Path

import h5py
import numpy as np

from acquisition import WaveformRecord


class ScopeHDF5Writer:
    """
    1 レコード = 1 trigger x 1 channel
    可変長配列として time_us, voltage_mV を保存する。
    """

    def __init__(self, path: str) -> None:
        self.path = Path(path)
        self.h5 = h5py.File(self.path, "w")

        dt_i64 = np.int64
        dt_f64 = np.float64
        dt_vlen_f64 = h5py.vlen_dtype(dt_f64)

        self.ds_trigger = self.h5.create_dataset(
            "trigger_index",
            shape=(0,),
            maxshape=(None,),
            dtype=dt_i64,
            chunks=True,
        )
        self.ds_channel = self.h5.create_dataset(
            "channel_index",
            shape=(0,),
            maxshape=(None,),
            dtype=dt_i64,
            chunks=True,
        )
        self.ds_time = self.h5.create_dataset(
            "time_us",
            shape=(0,),
            maxshape=(None,),
            dtype=dt_vlen_f64,
            chunks=True,
        )
        self.ds_voltage = self.h5.create_dataset(
            "voltage_mV",
            shape=(0,),
            maxshape=(None,),
            dtype=dt_vlen_f64,
            chunks=True,
        )

        # preamble も個別に保存
        self.ds_points = self.h5.create_dataset(
            "preamble_points",
            shape=(0,),
            maxshape=(None,),
            dtype=dt_i64,
            chunks=True,
        )
        self.ds_x_inc = self.h5.create_dataset(
            "preamble_x_inc_s",
            shape=(0,),
            maxshape=(None,),
            dtype=dt_f64,
            chunks=True,
        )
        self.ds_x_ori = self.h5.create_dataset(
            "preamble_x_ori_s",
            shape=(0,),
            maxshape=(None,),
            dtype=dt_f64,
            chunks=True,
        )
        self.ds_y_inc = self.h5.create_dataset(
            "preamble_y_inc_v_per_count",
            shape=(0,),
            maxshape=(None,),
            dtype=dt_f64,
            chunks=True,
        )
        self.ds_y_ori = self.h5.create_dataset(
            "preamble_y_ori_v",
            shape=(0,),
            maxshape=(None,),
            dtype=dt_f64,
            chunks=True,
        )
        self.ds_y_ref = self.h5.create_dataset(
            "preamble_y_ref",
            shape=(0,),
            maxshape=(None,),
            dtype=dt_f64,
            chunks=True,
        )

    def _append_one(self, ds, value) -> None:
        n = len(ds)
        ds.resize((n + 1,))
        ds[n] = value

    def append(self, record: WaveformRecord) -> None:
        self._append_one(self.ds_trigger, int(record.trigger_index))
        self._append_one(self.ds_channel, int(record.channel_index))
        self._append_one(self.ds_time, np.asarray(record.time_us, dtype=np.float64))
        self._append_one(self.ds_voltage, np.asarray(record.voltage_mV, dtype=np.float64))

        p = record.preamble
        self._append_one(self.ds_points, int(p["points"]))
        self._append_one(self.ds_x_inc, float(p["x_inc"]))
        self._append_one(self.ds_x_ori, float(p["x_ori"]))
        self._append_one(self.ds_y_inc, float(p["y_inc"]))
        self._append_one(self.ds_y_ori, float(p["y_ori"]))
        self._append_one(self.ds_y_ref, float(p["y_ref"]))

        self.h5.flush()

    def append_many(self, records: list[WaveformRecord]) -> None:
        for record in records:
            self.append(record)

    def close(self) -> None:
        self.h5.close()