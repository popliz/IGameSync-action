import subprocess
import sys
import NotifyWorkflow
import time

command_arg = ("--multi-thread-streams=8 --multi-thread-cutoff=256M "
               "--buffer-size=256M --onedrive-chunk-size 10Mi "
               "--log-level INFO --stats 30s "
               "--low-level-retries 100 --retries 30 --retries-sleep 1s "
               "--create-empty-src-dirs --check-first")

Driver1 = "gd_team1_lizkes:"
Driver2 = "od_lizkes_backup_root:"
Driver3 = "od_lizkes2_backup_root:"
Driver4 = "od_lizkes2_backup_sp1:"

sync_commands = [
    # 同步
    f"rclone sync {Driver2}/IGame {Driver3}/IGame {command_arg}",
    # 备份到SP
    f"rclone sync {Driver2}/IGame {Driver4}/IGame {command_arg}",
    f"rclone sync {Driver2}/H {Driver4}/个人/视频/H {command_arg}",
    # 备份到谷歌盘
    f"rclone sync {Driver4}/ {Driver1}/OneDrive {command_arg}",
]

limit_time = 5 * 3600
start_time = time.time()

for sync_command in sync_commands:
  print(f"运行指令：{sync_command}", flush=True)

  process_timeout = limit_time - int(time.time() - start_time)
  try:
    process = subprocess.run(
        sync_command,
        shell=True,
        stdout=sys.stdout,
        stderr=sys.stderr,
        text=True,
        check=True,
        timeout=process_timeout)
  except subprocess.TimeoutExpired:
    print(f"任务超过限制时间：{process_timeout}秒，运行下一班车 :)", flush=True)
    NotifyWorkflow.notify(sys.argv[1], sys.argv[2], sys.argv[3])
    sys.exit(0)
  except subprocess.CalledProcessError:
    sys.exit("子进程发生了一个错误，停止运行运行 :(")

  print(f"指令完成：{sync_command}\n用时{int(time.time() - start_time)}秒", flush=True)
