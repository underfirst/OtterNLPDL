import json
import subprocess
from random import randint
from time import sleep, time


class ScheduleByGPUStatus:
    def __init__(self, nvidia_smi_path="nvidia-smi"):
        self.default_attributes = (
            'index',
            'uuid',
            'name',
            'timestamp',
            'memory.total',
            'memory.free',
            'memory.used',
            'utilization.gpu',
            'utilization.memory'
        )
        self.nvidia_smi_path = nvidia_smi_path

    def get_gpu_info(self, keys=None, no_units=True):
        if keys is None:
            keys = self.default_attributes
        nu_opt = '' if not no_units else ',nounits'

        cmd = '%s --query-gpu=%s --format=csv,noheader%s' % (self.nvidia_smi_path, ','.join(keys), nu_opt)
        output = subprocess.check_output(cmd, shell=True)
        lines = output.decode().split('\n')
        lines = [line.strip() for line in lines if line.strip() != '']

        return [{k: v for k, v in zip(keys, line.split(', '))} for line in lines]

    def wait_untill_free(self, gpu_idx):
        start = time()
        hour_num = 0
        while True:
            try:
                info = self.get_gpu_info()
                for item in info:
                    if item["index"] == gpu_idx and int(item["memory.used"]) < 1000:
                        return True
            except:
                pass
            if time() - start > hour_num * 60 * 60:
                hour_num += 1
                print(f"Wait about {hour_num} hour")
            sleep(randint(0, 60))

if __name__ == '__main__':
    scheduler = ScheduleByGPUStatus()
    info = scheduler.get_gpu_info()
    print(info)
