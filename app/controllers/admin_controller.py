# app/controllers/admin_controller.py
# 管理者機能（言語管理など）

from flask import render_template, request, redirect, url_for, flash, jsonify
from app.services.translation_service import TranslationService

def language_admin():
    """言語管理画面"""
    data = TranslationService.get_language_admin_data()
    return render_template('admin/language_admin.html',
                         languages=data['languages'],
                         status=data['status'])

def add_translation():
    """翻訳追加"""
    if request.method == 'POST':
        lang = request.form.get('language')
        key = request.form.get('key')
        value = request.form.get('value')

        success, message = TranslationService.add_translation(lang, key, value)
        flash(message, 'success' if success else 'error')

    return redirect(url_for('admin.language_admin'))

def export_translations():
    """翻訳データをJSON形式でエクスポート"""
    lang = request.args.get('lang', 'en')

    result = TranslationService.export_translations(lang)

    if result['success']:
        return jsonify(result['data'])
    else:
        return jsonify({'error': result['error']}), result['status_code']
