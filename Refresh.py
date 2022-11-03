import subprocess
import sys

command_arg = ("--timeout 30s --contimeout 10s "
               "--low-level-retries 100 "
               "--retries 30 --retries-sleep 1s")

Driver1 = "gd_team1_lizkes:"
Driver2 = "od_lizkes_backup_root:"
Driver3 = "od_lizkes2_backup_root:"

refesh_commands = [
    f"rclone about {Driver1} {command_arg}",
    f"rclone about {Driver2} {command_arg}",
    f"rclone about {Driver3} {command_arg}",
]

for command in refesh_commands:
  print(f"运行指令：{command}", flush=True)

  try:
    process = subprocess.run(
        command,
        shell=True,
        stdout=sys.stdout,
        stderr=sys.stderr,
        text=True,
        check=True)
  except subprocess.CalledProcessError:
    sys.exit("子进程发生了一个错误，停止运行运行 :(")

  print(f"指令完成：{command}", flush=True)
