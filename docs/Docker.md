# Dockerの使い方

## 古いやつ

コマンドのテンプレート
```shell
# 起動:
# {/path/to/host/project/top/}は各位のdockerホストのプロジェクトディレクトリの絶対パス.
# {/path/to/container/mount_dir/}は各位のdocker containerのマウントしたいパス.
# {container name}は各位好きなコンテナ名.
# --rm でとりあえずcuda:10.1が動くやつなら何でもええ.
nvidia-docker run -it -v {/path/to/host/project/top/}:{/path/to/container/mount_dir/} --name="{container name}" --rm pytorch/pytorch:1.7.1-cuda11.0-cudnn8-runtime /bin/bash
# shell login:
nvidia-docker exec -it {container name} /bin/bash
# プロセス確認? プロセス終了? 気合いでkill. (人に聞いてくり)
```

コマンド例
```shell
nvidia-docker run -it -v `pwd`:/data --name=otter_festival --rm pytorch/pytorch:1.7.1-cuda11.0-cudnn8-runtime /bin/bash 
nvidia-docker exec -it otter_festival /bin/bash
```

## 新しいやつ

コマンドのテンプレート
```shell
# 起動:
# {/path/to/host/project/top/}は各位のdockerホストのプロジェクトディレクトリの絶対パス.
# {/path/to/container/mount_dir/}は各位のdocker containerのマウントしたいパス.
# {container name}は各位好きなコンテナ名.
# --gpus: 使用したいgpuのid. とりあえず全部使えるようにしとけ. それが人生.
# --rm でとりあえずcuda:10.1が動くやつなら何でもええ.
docker run -it -v {/path/to/host/project/top/}:{/path/to/container/mount_dir/} --name="{container name}" --rm pytorch/pytorch:1.7.1-cuda11.0-cudnn8-runtime /bin/bash
# shell login:
docker exec -it {container name} /bin/bash
# プロセス確認? プロセス終了? 気合いでkill. (人に聞いてくり)
```

コマンド例
```shell
docker run -it -v `pwd`:/data --name=otter_festival --rm pytorch/pytorch:1.7.1-cuda11.0-cudnn8-runtime /bin/bash 
docker exec -it otter_festival /bin/bash
```
