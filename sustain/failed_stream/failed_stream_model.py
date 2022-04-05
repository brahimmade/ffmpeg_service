from enum import Enum

from common.data.source_model import SourceModel


class WatchDogOperations(str, Enum):
    check_rtmp_container = 'check_rtmp_container'
    check_rtmp_feeder_process = 'check_rtmp_feeder_process'
    check_hls_process = 'check_hls_process'
    check_ffmpeg_reader_process = 'check_ffmpeg_reader_process'
    check_record_process = 'check_record_process'
    check_snapshot_process = 'check_snapshot_process'
    check_record_stuck_process = 'check_record_stuck_process'


class FailedStreamModel:
    def __init__(self):
        self.id: str = ''
        self.brand: str = ''
        self.name: str = ''
        self.address: str = ''

        self.watch_dog_interval: float = .0

        self.rtmp_container_failed_count: int = 0
        self.rtmp_feeder_failed_count: int = 0
        self.hls_failed_count: int = 0
        self.ffmpeg_reader_failed_count: int = 0
        self.record_failed_count: int = 0
        self.snapshot_failed_count: int = 0
        self.record_stuck_process_count: int = 0

    def map_from_source(self, source: SourceModel):
        self.id = source.id
        self.brand = source.brand
        self.name = source.name
        self.address = source.address
        return self

    def set_failed_count(self, op: WatchDogOperations):
        if op == WatchDogOperations.check_rtmp_container:
            self.rtmp_container_failed_count += 1
        elif op == WatchDogOperations.check_rtmp_feeder_process:
            self.rtmp_feeder_failed_count += 1
        elif op == WatchDogOperations.check_hls_process:
            self.hls_failed_count += 1
        elif op == WatchDogOperations.check_record_process:
            self.record_failed_count += 1
        elif op == WatchDogOperations.check_ffmpeg_reader_process:
            self.ffmpeg_reader_failed_count += 1
        elif op == WatchDogOperations.check_record_process:
            self.record_failed_count += 1
        elif op == WatchDogOperations.check_snapshot_process:
            self.snapshot_failed_count += 1
        elif op == WatchDogOperations.check_record_stuck_process:
            self.record_stuck_process_count += 1
        else:
            raise NotImplementedError(op.value)