import os
import signal
from datetime import datetime
import psutil
from redis.client import Redis

from common.utilities import logger
from rtmp.docker_manager import DockerManager
from rtmp.rtmp_models import RtmpServerImages


def kill_all_prev_ffmpeg_procs():
    all_process_list = psutil.process_iter()
    for proc in all_process_list:
        if proc.name() == "ffmpeg":
            try:
                os.kill(proc.pid, signal.SIGKILL)
                logger.warn(f'a previous FFmpeg process was detected and killed - {proc.pid} at {datetime.now()}')
            except BaseException as e:
                logger.error(f'an error occurred during killing a previous FFmpeg process, ex: {e} at {datetime.now()}')


def reset_rtmp_container_ports(connection_main: Redis):
    connection_main.hset('rtmpports', 'ports_count', 0)


def remove_all_prev_rtmp_containers(connection_main: Redis):
    docker_manager = DockerManager(connection_main)
    containers = docker_manager.get_all_containers()
    image_names = {RtmpServerImages.OSSRS.value: True, RtmpServerImages.LIVEGO.value: True, RtmpServerImages.NMS.value: True}
    for container in containers:
        image_name = docker_manager.parse_image_name(container)
        if image_name not in image_names:
            continue
        try:
            docker_manager.stop_container(container)
            logger.warn(f'an unstopped rtmp server container has been detected and stopped, container name: {container.name}')
        except BaseException as e:
            logger.error(f'an error occurred during stopping a leaked rtmp server container ({container.name}), ex: {e} at {datetime.now()}')