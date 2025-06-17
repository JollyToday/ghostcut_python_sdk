
- 安装uv
    参考官方文档，最好不要使用pip安装，否则会安装到对应python的bin里，而不是全局的python无关的路径
    国内安装比较慢

- 克隆项目到本地，切换到review分支

- 同步环境，会创建虚拟环境，安装相关依赖
    ```bash
    cd ghostcut_python_sdk
    uv sync
    ```

- 开发者模式安装项目到虚拟环境
    ```bash
    uv pip install -e .
    ```
