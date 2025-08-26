# 管理者・開発者用ダッシュボードコントローラー
from flask import render_template, request, redirect, url_for, session, flash
from app.services.admin_service import AdminService

# ビュー関数
def dashboard():
    """管理者・開発者共通ダッシュボード"""
    user_id = session.get('user_id')

    # 権限チェック
    has_permission, error_message = AdminService.check_admin_or_developer_permission(user_id)
    if not has_permission:
        flash(error_message, 'error')
        return redirect(url_for('auth.login') if 'ログイン' in error_message else url_for('room.index'))

    user, is_admin, is_developer = AdminService.get_user_and_permissions(user_id)
    stats = AdminService.get_dashboard_stats()

    return render_template('admin/dashboard.html',
                            user=user,
                            stats=stats,
                            is_admin=is_admin,
                            is_developer=is_developer)

def system_info():
    """システム情報表示"""
    user_id = session.get('user_id')

    # 権限チェック
    has_permission, error_message = AdminService.check_admin_or_developer_permission(user_id)
    if not has_permission:
        flash(error_message, 'error')
        return redirect(url_for('auth.login') if 'ログイン' in error_message else url_for('room.index'))

    user, is_admin, is_developer = AdminService.get_user_and_permissions(user_id)
    stats = AdminService.get_dashboard_stats()

    return render_template('admin/system_info.html',
                            user=user,
                            stats=stats,
                            is_admin=is_admin,
                            is_developer=is_developer)

def developer_tools():
    """開発者ツール（管理者・開発者共用）"""
    user_id = session.get('user_id')

    # 権限チェック
    has_permission, error_message = AdminService.check_admin_or_developer_permission(user_id)
    if not has_permission:
        flash(error_message, 'error')
        return redirect(url_for('auth.login') if 'ログイン' in error_message else url_for('room.index'))

    user, is_admin, is_developer = AdminService.get_user_and_permissions(user_id)

    return render_template('admin/developer_tools.html',
                            user=user,
                            is_admin=is_admin,
                            is_developer=is_developer)

def user_management():
    """ユーザー管理（管理者専用）"""
    user_id = session.get('user_id')

    # 管理者権限チェック
    has_permission, error_message = AdminService.check_admin_permission(user_id)
    if not has_permission:
        flash(error_message, 'error')
        return redirect(url_for('auth.login') if 'ログイン' in error_message else url_for('room.index'))

    page = request.args.get('page', 1, type=int)
    users = AdminService.get_users_paginated(page)

    return render_template('admin/user_management.html', users=users)

def update_user_role():
    """ユーザーロール変更（管理者専用）"""
    user_id = session.get('user_id')

    # 管理者権限チェック
    has_permission, error_message = AdminService.check_admin_permission(user_id)
    if not has_permission:
        flash(error_message, 'error')
        return redirect(url_for('auth.login') if 'ログイン' in error_message else url_for('room.index'))

    if request.method == 'POST':
        target_user_id = request.form.get('user_id')
        new_role = request.form.get('role')

        success, message = AdminService.update_user_role(target_user_id, new_role)
        flash(message, 'success' if success else 'error')

    return redirect(url_for('admin.user_management'))

def password_reset_tool():
    """パスワードリセットツール（管理者専用）"""
    user_id = session.get('user_id')

    # 管理者権限チェック
    has_permission, error_message = AdminService.check_admin_permission(user_id)
    if not has_permission:
        flash(error_message, 'error')
        return redirect(url_for('auth.login') if 'ログイン' in error_message else url_for('room.index'))

    if request.method == 'POST':
        username = request.form.get('username')
        new_password = request.form.get('new_password')

        success, message = AdminService.reset_user_password(username, new_password)
        flash(message, 'success' if success else 'error')

    return render_template('admin/password_reset.html')
