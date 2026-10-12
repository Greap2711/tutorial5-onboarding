from flask import Flask, request, jsonify, render_template_string
import pyodbc
from datetime import datetime

app = Flask(__name__)

# Kết nối SQL Server tự động bằng tài khoản Windows của máy bạn
def get_db_connection():
    drivers = [
        '{ODBC Driver 17 for SQL Server}',
        '{ODBC Driver 18 for SQL Server}',
        '{SQL Server}'
    ]
    for driver in drivers:
        try:
            conn = pyodbc.connect(
                f"DRIVER={driver};SERVER=localhost;DATABASE=onboarding_db;Trusted_Connection=yes;TrustServerCertificate=yes;"
            )
            return conn
        except Exception:
            continue
    raise Exception("Không tìm thấy Driver kết nối SQL Server!")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Employee Onboarding Tasks</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f4f6f9; }
        .card { background: white; padding: 25px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        h2 { color: #333; margin-top: 0; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        th { background-color: #007bff; color: white; }
        select { padding: 6px; border-radius: 4px; border: 1px solid #ccc; font-size: 14px; }
        .badge { padding: 5px 10px; border-radius: 4px; font-weight: bold; font-size: 12px; }
        .pending { background: #ffeeba; color: #856404; }
        .in_progress { background: #b8daff; color: #004085; }
        .completed { background: #c3e6cb; color: #155724; }
        #alert { margin-top: 15px; padding: 10px; background: #d4edda; color: #155724; border-radius: 4px; display: none; }
    </style>
</head>
<body>
    <div class="card">
        <h2>Onboarding Tasks - User 1 (Tran Hoang Minh)</h2>
        <div id="alert"></div>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Tên nhiệm vụ</th>
                    <th>Trạng thái hiện tại</th>
                    <th>Thao tác đổi trạng thái</th>
                </tr>
            </thead>
            <tbody id="task-body"></tbody>
        </table>
    </div>

    <script>
        async function loadTasks() {
            const res = await fetch('/api/employee-tasks');
            const data = await res.json();
            const tbody = document.getElementById('task-body');
            tbody.innerHTML = '';
            data.forEach(t => {
                tbody.innerHTML += `
                    <tr>
                        <td>${t.id}</td>
                        <td>${t.title}</td>
                        <td><span class="badge ${t.status}">${t.status}</span></td>
                        <td>
                            <select onchange="changeStatus(${t.id}, this.value)">
                                <option value="pending" ${t.status === 'pending' ? 'selected' : ''}>pending</option>
                                <option value="in_progress" ${t.status === 'in_progress' ? 'selected' : ''}>in_progress</option>
                                <option value="completed" ${t.status === 'completed' ? 'selected' : ''}>completed</option>
                            </select>
                        </td>
                    </tr>
                `;
            });
        }

        async function changeStatus(id, newStatus) {
            const res = await fetch(`/api/employee-tasks/${id}/status`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ status: newStatus })
            });
            const result = await res.json();
            if (res.ok) {
                const alertBox = document.getElementById('alert');
                alertBox.innerText = `Thành công: Cập nhật task ${id} sang '${newStatus}'!`;
                alertBox.style.display = 'block';
                loadTasks();
            } else {
                alert(result.error);
            }
        }
        loadTasks();
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/employee-tasks', methods=['GET'])
def get_tasks():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT et.id, ot.title, et.status, et.completed_at
        FROM employee_tasks et
        JOIN onboarding_tasks ot ON et.task_id = ot.id
        WHERE et.user_id = 1
    """)
    rows = cursor.fetchall()
    tasks = [{'id': r[0], 'title': r[1], 'status': r[2], 'completed_at': str(r[3])} for r in rows]
    conn.close()
    return jsonify(tasks)

@app.route('/api/employee-tasks/<int:id>/status', methods=['PUT'])
def update_status(id):
    data = request.get_json() or {}
    new_status = data.get('status')

    valid_statuses = ['pending', 'in_progress', 'completed']
    if new_status not in valid_statuses:
        return jsonify({'error': "Status must be 'pending', 'in_progress', or 'completed'"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM employee_tasks WHERE id = ?", (id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({'error': 'Task ID does not exist'}), 404

    completed_at = datetime.now() if new_status == 'completed' else None
    cursor.execute(
        "UPDATE employee_tasks SET status = ?, completed_at = ? WHERE id = ?",
        (new_status, completed_at, id)
    )
    conn.commit()
    conn.close()

    return jsonify({'message': 'Status updated successfully', 'task_id': id, 'new_status': new_status}), 200

if __name__ == '__main__':
    print("Server đang chạy tại http://127.0.0.1:5000")
    app.run(debug=True, port=5000)