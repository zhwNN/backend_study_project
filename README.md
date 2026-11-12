# 待办任务 API

基于 **Flask + SQLite** 的 RESTful 待办事项后端服务，采用分层结构（入口 / 路由 / 数据库）组织代码，支持任务的增删改查与数据持久化。

## 功能特性

- ✅ 任务的创建、查询、更新、删除（CRUD）
- ✅ 数据持久化：使用 SQLite，服务重启后数据不丢失
- ✅ 中文友好的 JSON 响应
- ✅ 分层结构：`app.py`（入口）、`tasks.py`（路由）、`db.py`（数据库）
- ✅ 使用 Flask Blueprint 组织路由，便于后续扩展

## 技术栈

| 技术 | 版本 | 说明 |
|---|---|---|
| Python | 3.12 | 编程语言 |
| Flask | 3.1 | Web 框架 |
| SQLite | 内置 | 嵌入式数据库 |
| Werkzeug | 3.1 | Flask 底层 WSGI 工具 |

## 项目结构

```
backend_study_project/
├── app.py            # 入口：创建应用、注册蓝图、启动
├── tasks.py          # 任务路由（Flask Blueprint）
├── db.py             # 数据库：连接 + 建表
├── requirements.txt  # 依赖清单
├── README.md         # 项目说明
└── database.db       # SQLite 数据库（首次运行自动生成）
```

## 快速开始

### 1. 创建并激活虚拟环境（推荐）

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 启动服务

```bash
python app.py
```

服务默认运行在 **http://127.0.0.1:5000**。首次启动会自动创建 `database.db` 和 `tasks` 表。

## API 接口

### 统一响应格式

大多数接口返回：

```json
{
  "mes": "提示信息",
  "data": {}
}
```

### 1. 获取所有任务

```
GET /tasks
```

**响应示例（200）**

```json
{
  "mes": "获取任务列表成功",
  "data": [
    { "id": 1, "title": "学习 Flask", "done": 0 },
    { "id": 2, "title": "写 README", "done": 1 }
  ]
}
```

### 2. 获取单个任务

```
GET /tasks/<id>
```

- 成功：`200`
- 任务不存在：`404`

**响应示例（200）**

```json
{
  "mes": "ok",
  "data": { "id": 1, "title": "学习 Flask", "done": 0 }
}
```

### 3. 新建任务

```
POST /tasks
Content-Type: application/json

{ "title": "学习 SQLite" }
```

- 成功：`201`，返回新任务对象
- `title` 为空：`400`

**响应示例（201）**

```json
{ "id": 3, "title": "学习 SQLite", "done": 0 }
```

### 4. 更新任务

```
PUT /tasks/<id>
Content-Type: application/json

{ "title": "学习 SQLite", "done": 1 }
```

- 成功：`200`
- `title` 为空：`400`

**响应示例（200）**

```json
{ "mes": "修改成功", "data": [] }
```

### 5. 删除任务

```
DELETE /tasks/<id>
```

- 成功：`200`

**响应示例（200）**

```json
{ "mes": "删除成功", "data": [] }
```

## 数据库结构

表名：`tasks`

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | INTEGER | 主键，自增 |
| `title` | TEXT | 任务标题，非空 |
| `done` | INTEGER | 是否完成（0 = 未完成，1 = 已完成） |

建表语句在程序启动时自动执行（`CREATE TABLE IF NOT EXISTS`），因此无需手动初始化数据库。

## 状态码约定

| 状态码 | 含义 | 使用场景 |
|---|---|---|
| 200 | 成功 | 查询、更新、删除成功 |
| 201 | 创建成功 | 新建任务成功 |
| 400 | 请求参数错误 | `title` 为空 |
| 404 | 资源不存在 | 查询不存在的任务 |
| 500 | 服务器错误 | 数据库异常等 |

## 已知可优化点

- [ ] 统一响应格式（POST 成功时也包一层 `{mes, data}`）
- [ ] 删除/更新不存在的任务时返回 `404` 而非 `500`
- [ ] 支持按 `done` 状态过滤任务列表
- [ ] 增加分页
- [ ] 编写单元测试（pytest）
- [ ] 部署上线（Render / Railway / 云服务器）

## 开发备注

- 数据库文件 `database.db` 是本地运行产物，已加入 `.gitignore`，不应提交到仓库。
- 修改代码后，Flask 在 `debug=True` 模式下会自动重启。
