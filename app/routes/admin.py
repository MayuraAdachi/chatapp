# 管理者・開発者向けルーティング

from flask import Blueprint, render_template, jsonify
from app.controllers import admin_dashboard_controller
from app.services.admin_service import AdminService
from app.utils.decorators import require_role

# =============================================================================
# 管理者・開発者共通ルート (/admin)
# =============================================================================
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# ダッシュボード・基本機能
@admin_bp.route('/dashboard')
@require_role('admin')
def dashboard():
    """管理者・開発者共通ダッシュボード"""
    return admin_dashboard_controller.dashboard()

@admin_bp.route('/system-info')
@require_role('admin')
def system_info():
    """システム情報表示"""
    return admin_dashboard_controller.system_info()

# =============================================================================
# 管理者専用機能
# =============================================================================

# ユーザー管理
@admin_bp.route('/users')
@require_role('admin')
def user_management():
    """ユーザー管理（管理者専用）"""
    return admin_dashboard_controller.user_management()

@admin_bp.route('/users/update-role', methods=['POST'])
@require_role('admin')
def update_user_role():
    """ユーザーロール変更（管理者専用）"""
    return admin_dashboard_controller.update_user_role()

# パスワード管理
@admin_bp.route('/password-reset', methods=['GET', 'POST'])
@require_role('admin')
def password_reset_tool():
    """パスワードリセットツール（管理者専用）"""
    return admin_dashboard_controller.password_reset_tool()

# 統計・分析
@admin_bp.route('/statistics')
@require_role('admin')
def detailed_statistics():
    """詳細統計ページ（管理者専用）"""
    user_stats = AdminService.get_user_statistics()
    room_stats = AdminService.get_room_statistics()
    message_stats = AdminService.get_message_statistics()

    return render_template('admin/statistics.html',
                         user_stats=user_stats,
                         room_stats=room_stats,
                         message_stats=message_stats)

# =============================================================================
# 開発者専用機能
# =============================================================================

@admin_bp.route('/developer-tools')
@require_role('developer')
def developer_tools():
    """開発者ツール（開発者専用）"""
    return admin_dashboard_controller.developer_tools()

@admin_bp.route('/logs')
@require_role('developer')
def system_logs():
    """システムログ表示（開発者専用）"""
    logs = AdminService.get_system_logs(limit=100)
    activities = AdminService.get_recent_activities(limit=30)

    return render_template('admin/logs.html',
                         logs=logs,
                         activities=activities)

# =============================================================================
# API エンドポイント
# =============================================================================

@admin_bp.route('/api/stats')
@require_role('admin')
def api_statistics():
    """統計情報のAPI（AJAX用）"""
    user_stats = AdminService.get_user_statistics()
    room_stats = AdminService.get_room_statistics()
    message_stats = AdminService.get_message_statistics()

    return jsonify({
        'users': user_stats,
        'rooms': room_stats,
        'messages': message_stats
    })

# 将来的に追加予定の管理機能
# @admin_bp.route('/rooms')
# @require_role('admin')
# def room_management():
#     """ルーム管理"""
#     pass

# @admin_bp.route('/maintenance')
# @require_role('developer')
# def maintenance_mode():
#     """メンテナンスモード切り替え"""
#     pass

# =============================================================================
# 管理者Blueprint一覧
# =============================================================================
admin_blueprints = [admin_bp]
