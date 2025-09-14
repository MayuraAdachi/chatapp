# 管理者・開発者向けルーティング

from flask import Blueprint, render_template, jsonify
from app.controllers import admin_dashboard_controller
from app.services.admin_service import AdminService
from app.utils.decorators import require_role

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# 統計・分析

def detailed_statistics():
    user_stats = AdminService.get_user_statistics()
    room_stats = AdminService.get_room_statistics()
    message_stats = AdminService.get_message_statistics()
    return render_template('admin/statistics.html',
                            user_stats=user_stats,
                            room_stats=room_stats,
                            message_stats=message_stats)

def system_logs():
    logs = AdminService.get_system_logs(limit=100)
    activities = AdminService.get_recent_activities(limit=30)
    return render_template('admin/logs.html',
                            logs=logs,
                            activities=activities)

def api_statistics():
    user_stats = AdminService.get_user_statistics()
    room_stats = AdminService.get_room_statistics()
    message_stats = AdminService.get_message_statistics()
    return jsonify({
        'users': user_stats,
        'rooms': room_stats,
        'messages': message_stats
    })

admin_bp.route('/dashboard')(admin_dashboard_controller.dashboard)
admin_bp.route('/system-info')(admin_dashboard_controller.system_info)
admin_bp.route('/users')(admin_dashboard_controller.user_management)
admin_bp.route('/users/update-role', methods=['POST'])(admin_dashboard_controller.update_user_role)
admin_bp.route('/password-reset', methods=['GET', 'POST'])(admin_dashboard_controller.password_reset_tool)
admin_bp.route('/statistics')(detailed_statistics)
admin_bp.route('/developer-tools')(admin_dashboard_controller.developer_tools)
admin_bp.route('/logs')(system_logs)
admin_bp.route('/api/stats')(api_statistics)

admin_blueprints = [admin_bp]
