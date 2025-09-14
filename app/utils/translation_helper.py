# app/utils/translation_helper.py
# 翻訳辞書を管理するヘルパーファイル
import os

# デバッグ出力を制御するフラグ
DEBUG_TRANSLATION = os.getenv('DEBUG_MODE', 'False').lower() in ['true', '1', 'yes']

# 基本翻訳辞書
BASIC_TRANSLATIONS = {
    'en': {
        # 基本UI
        'login': 'Login',
        'register': 'Register',
        'logout': 'Logout',
        'username': 'Username',
        'email': 'Email Address',
        'password': 'Password',
        'confirm_password': 'Confirm Password',
        'back': 'Back',
        'cancel': 'Cancel',
        'submit': 'Submit',
        'save': 'Save',
        'edit': 'Edit',
        'delete': 'Delete',
        'create': 'Create',
        'update': 'Update',
        'search': 'Search',
        'next': 'Next',
        'previous': 'Previous',
        'home': 'Home',
        'settings': 'Settings',
        'profile': 'Profile',
        'dashboard': 'Dashboard',

        # ナビゲーション・メニュー
        'chat_room': 'Chat Room',
        'room_list': 'Room List',
        'room_create': 'Create Room',
        'join_room': 'Join Room',
        'leave_room': 'Leave Room',
        'room_name': 'Room Name',
        'room_description': 'Room Description',
        'members': 'Members',
        'online': 'Online',
        'offline': 'Offline',

        # メッセージ・チャット関連
        'message': 'Message',
        'send_message': 'Send Message',
        'type_message': 'Type your message...',
        'chat_history': 'Chat History',
        'no_messages': 'No messages yet.',
        'message_sent': 'Message sent successfully.',
        'message_failed': 'Failed to send message.',

        # 認証・アカウント関連
        'login_title': 'Login to Chat App',
        'register_title': 'Create Account',
        'login_required': 'Please log in to access this page.',
        'login_failed': 'Login failed. Please check your credentials.',
        'registration_success': 'Account created successfully.',
        'registration_failed': 'Registration failed. Please try again.',
        'already_have_account': 'Already have an account?',
        'dont_have_account': 'Don\'t have an account?',
        'forgot_password': 'Forgot Password?',
        'reset_password': 'Reset Password',

        # フォームバリデーション
        'required_field': 'This field is required.',
        'invalid_email': 'Please enter a valid email address.',
        'password_too_short': 'Password must be at least 8 characters long.',
        'passwords_dont_match': 'Passwords do not match.',
        'username_taken': 'This username is already taken.',
        'email_taken': 'This email address is already registered.',

        # エラー・成功メッセージ
        'error_occurred': 'An error occurred.',
        'success': 'Operation completed successfully.',
        'not_found': 'Page not found.',
        'access_denied': 'Access denied.',
        'server_error': 'Server error occurred.',

        # チャットアプリ固有
        'welcome_message': 'Welcome to the Chat App!',
        'room_created': 'Room created successfully.',
        'room_joined': 'You have joined the room.',
        'room_left': 'You have left the room.',
        'user_joined': '{user} has joined the room.',
        'user_left': '{user} has left the room.',

        # 確認・修正ページ
        'confirm_registration': 'Confirm Registration',
        'registration_info': 'Please confirm your registration information:',
        'correct_info': 'Correct',
        'modify_info': 'Modify',
        'registration_complete': 'Registration Complete!',
        'go_to_login': 'Go to Login',

        # 言語関連
        'language': 'Language',
        'change_language': 'Change Language',
        'current_language': 'Current Language',

        # ログインページ固有
        'ユーザー名またはメールアドレスとパスワードを入力してログインしてください。': 'Please enter your username or email address and password to log in.',
        'ユーザー名またはメールアドレス': 'Username or Email Address',
        'ログイン': 'Login',
        'パスワード': 'Password',
        'または': 'Or',
        'アカウントを作成': 'Create Account',
        'トップへ戻る': 'Back to Top',
        'その他': 'Others',

        # トップページ固有
        'トップ': 'Top',
        'チャットアプリへようこそ': 'Welcome to Chat App',
        'アカウントでログインするか、新規登録してご利用ください。': 'Please log in with your account or register as a new user.',
        'アカウント登録なしでも匿名でご参加いただけます。': 'You can also join anonymously without account registration.',
        '既にアカウントをお持ちの方': 'For those who already have an account',
        '新規でアカウントを作成する方': 'For those who want to create a new account',
        'ニックネーム（匿名参加）': 'Nickname (Anonymous)',
        '匿名で参加': 'Join Anonymously',
        'アカウント登録なしで参加': 'Join without account registration',
    },
    'ja': {
        # 基本UI
        'login': 'ログイン',
        'register': '新規登録',
        'logout': 'ログアウト',
        'username': 'ユーザー名',
        'email': 'メールアドレス',
        'password': 'パスワード',
        'confirm_password': 'パスワード確認',
        'back': '戻る',
        'cancel': 'キャンセル',
        'submit': '送信',
        'save': '保存',
        'edit': '編集',
        'delete': '削除',
        'create': '作成',
        'update': '更新',
        'search': '検索',
        'next': '次へ',
        'previous': '前へ',
        'home': 'ホーム',
        'settings': '設定',
        'profile': 'プロフィール',
        'dashboard': 'ダッシュボード',

        # ナビゲーション・メニュー
        'chat_room': 'チャットルーム',
        'room_list': 'ルーム一覧',
        'room_create': 'ルーム作成',
        'join_room': 'ルーム参加',
        'leave_room': 'ルーム退出',
        'room_name': 'ルーム名',
        'room_description': 'ルーム説明',
        'members': 'メンバー',
        'online': 'オンライン',
        'offline': 'オフライン',

        # メッセージ・チャット関連
        'message': 'メッセージ',
        'send_message': 'メッセージ送信',
        'type_message': 'メッセージを入力してください...',
        'chat_history': 'チャット履歴',
        'no_messages': 'まだメッセージがありません。',
        'message_sent': 'メッセージが正常に送信されました。',
        'message_failed': 'メッセージの送信に失敗しました。',

        # 認証・アカウント関連
        'login_title': 'チャットアプリにログイン',
        'register_title': 'アカウント作成',
        'login_required': 'このページにアクセスするにはログインが必要です。',
        'login_failed': 'ログインに失敗しました。認証情報を確認してください。',
        'registration_success': 'アカウントが正常に作成されました。',
        'registration_failed': '登録に失敗しました。もう一度お試しください。',
        'already_have_account': 'すでにアカウントをお持ちですか？',
        'dont_have_account': 'アカウントをお持ちでないですか？',
        'forgot_password': 'パスワードを忘れましたか？',
        'reset_password': 'パスワードリセット',

        # フォームバリデーション
        'required_field': 'この項目は必須です。',
        'invalid_email': '正しいメールアドレスを入力してください。',
        'password_too_short': 'パスワードは8文字以上で入力してください。',
        'passwords_dont_match': 'パスワードが一致しません。',
        'username_taken': 'このユーザー名は既に使用されています。',
        'email_taken': 'このメールアドレスは既に登録されています。',

        # エラー・成功メッセージ
        'error_occurred': 'エラーが発生しました。',
        'success': '操作が正常に完了しました。',
        'not_found': 'ページが見つかりません。',
        'access_denied': 'アクセスが拒否されました。',
        'server_error': 'サーバーエラーが発生しました。',

        # チャットアプリ固有
        'welcome_message': 'チャットアプリへようこそ！',
        'room_created': 'ルームが正常に作成されました。',
        'room_joined': 'ルームに参加しました。',
        'room_left': 'ルームから退出しました。',
        'user_joined': '{user}がルームに参加しました。',
        'user_left': '{user}がルームから退出しました。',

        # 確認・修正ページ
        'confirm_registration': '登録確認',
        'registration_info': '登録情報をご確認ください：',
        'correct_info': '確定',
        'modify_info': '修正する',
        'registration_complete': '登録完了！',
        'go_to_login': 'ログインページへ',

        # 言語関連
        'language': '言語',
        'change_language': '言語を変更',
        'current_language': '現在の言語',

        # ログインページ固有
        'ユーザー名またはメールアドレスとパスワードを入力してログインしてください。': 'ユーザー名またはメールアドレスとパスワードを入力してログインしてください。',
        'ユーザー名またはメールアドレス': 'ユーザー名またはメールアドレス',
        'ログイン': 'ログイン',
        'パスワード': 'パスワード',
        'または': 'または',
        'アカウントを作成': 'アカウントを作成',
        'トップへ戻る': 'トップへ戻る',
        'その他': 'その他',

        # トップページ固有
        'トップ': 'ホーム',
        'チャットアプリへようこそ': '채팅 앱에 오신 것을 환영합니다',
        'アカウントでログインするか、新規登録してご利用ください。': '계정으로 로그인하거나 새로 등록해 주세요.',
        'アカウント登録なしでも匿名でご参加いただけます。': '계정 등록 없이도 익명으로 참여하실 수 있습니다.',
        '既にアカウントをお持ちの方': '이미 계정이 있는 분',
        '新規でアカウントを作成する方': '새로운 계정을 만들고 싶은 분',
        'ニックネーム（匿名参加）': '닉네임（익명）',
        '匿名で参加': '익명으로 참여',
        'アカウント登録なしで参加': '계정 등록 없이 참여',
    },
    'zh': {
        # 基本UI
        'login': '登录',
        'register': '注册',
        'logout': '登出',
        'username': '用户名',
        'email': '邮箱地址',
        'password': '密码',
        'confirm_password': '确认密码',
        'back': '返回',
        'cancel': '取消',
        'submit': '提交',
        'save': '保存',
        'edit': '编辑',
        'delete': '删除',
        'create': '创建',
        'update': '更新',
        'search': '搜索',
        'next': '下一个',
        'previous': '上一个',
        'home': '首页',
        'settings': '设置',
        'profile': '个人资料',
        'dashboard': '仪表板',

        # ナビゲーション・メニュー
        'chat_room': '聊天室',
        'room_list': '房间列表',
        'room_create': '创建房间',
        'join_room': '加入房间',
        'leave_room': '退出房间',
        'room_name': '房间名称',
        'room_description': '房间描述',
        'members': '成员',
        'online': '在线',
        'offline': '离线',

        # メッセージ・チャット関連
        'message': '消息',
        'send_message': '发送消息',
        'type_message': '请输入您的消息...',
        'chat_history': '聊天记录',
        'no_messages': '暂无消息。',
        'message_sent': '消息发送成功。',
        'message_failed': '消息发送失败。',

        # 認証・アカウント関連
        'login_title': '登录聊天应用',
        'register_title': '创建账户',
        'login_required': '请登录以访问此页面。',
        'login_failed': '登录失败。请检查您的凭据。',
        'registration_success': '账户创建成功。',
        'registration_failed': '注册失败。请重试。',
        'already_have_account': '已有账户？',
        'dont_have_account': '还没有账户？',
        'forgot_password': '忘记密码？',
        'reset_password': '重置密码',

        # フォームバリデーション
        'required_field': '此字段为必填项。',
        'invalid_email': '请输入有效的邮箱地址。',
        'password_too_short': '密码至少需要8个字符。',
        'passwords_dont_match': '密码不匹配。',
        'username_taken': '此用户名已被使用。',
        'email_taken': '此邮箱地址已被注册。',

        # エラー・成功メッセージ
        'error_occurred': '发生错误。',
        'success': '操作成功完成。',
        'not_found': '页面未找到。',
        'access_denied': '访问被拒绝。',
        'server_error': '服务器错误。',

        # チャットアプリ固有
        'welcome_message': '欢迎使用聊天应用！',
        'room_created': '房间创建成功。',
        'room_joined': '您已加入房间。',
        'room_left': '您已退出房间。',
        'user_joined': '{user} 已加入房间。',
        'user_left': '{user} 已退出房间。',

        # 確認・修正ページ
        'confirm_registration': '确认注册',
        'registration_info': '请确认您的注册信息：',
        'correct_info': '正确',
        'modify_info': '修改',
        'registration_complete': '注册完成！',
        'go_to_login': '前往登录',

        # 言語関連
        'language': '语言',
        'change_language': '更改语言',
        'current_language': '当前语言',

        # ログインページ固有
        'ユーザー名またはメールアドレスとパスワードを入力してログインしてください。': '请输入您的用户名或邮箱地址和密码进行登录。',
        'ユーザー名またはメールアドレス': '用户名或邮箱地址',
        'ログイン': '登录',
        'パスワード': '密码',
        'または': '或者',
        'アカウントを作成': '创建账户',
        'トップへ戻る': '返回首页',
        'その他': '其他',

        # トップページ固有
        'トップ': '首页',
        'チャットアプリへようこそ': '欢迎使用聊天应用',
        'アカウントでログインするか、新規登録してご利用ください。': '请使用您的账户登录或注册为新用户。',
        'アカウント登録なしでも匿名でご参加いただけます。': '您也可以不注册账户匿名参与。',
        '既にアカウントをお持ちの方': '已有账户的用户',
        '新規でアカウントを作成する方': '想要创建新账户的用户',
        'ニックネーム（匿名参加）': '昵称（匿名）',
        '匿名で参加': '匿名参与',
        'アカウント登録なしで参加': '不注册账户参与',
    },
    'ko': {
        # 基本UI
        'login': '로그인',
        'register': '회원가입',
        'logout': '로그아웃',
        'username': '사용자명',
        'email': '이메일 주소',
        'password': '비밀번호',
        'confirm_password': '비밀번호 확인',
        'back': '뒤로',
        'cancel': '취소',
        'submit': '제출',
        'save': '저장',
        'edit': '편집',
        'delete': '삭제',
        'create': '생성',
        'update': '업데이트',
        'search': '검색',
        'next': '다음',
        'previous': '이전',
        'home': '홈',
        'settings': '설정',
        'profile': '프로필',
        'dashboard': '대시보드',

        # ナビゲーション・メニュー
        'chat_room': '채팅방',
        'room_list': '방 목록',
        'room_create': '방 만들기',
        'join_room': '방 참여',
        'leave_room': '방 나가기',
        'room_name': '방 이름',
        'room_description': '방 설명',
        'members': '멤버',
        'online': '온라인',
        'offline': '오프라인',

        # メッセージ・チャット関連
        'message': '메시지',
        'send_message': '메시지 보내기',
        'type_message': '메시지를 입력하세요...',
        'chat_history': '채팅 기록',
        'no_messages': '아직 메시지가 없습니다.',
        'message_sent': '메시지가 성공적으로 전송되었습니다.',
        'message_failed': '메시지 전송에 실패했습니다.',

        # 認証・アカウント関連
        'login_title': '채팅 앱에 로그인',
        'register_title': '계정 만들기',
        'login_required': '이 페이지에 액세스하려면 로그인이 필요합니다.',
        'login_failed': '로그인에 실패했습니다. 자격 증명을 확인하세요.',
        'registration_success': '계정이 성공적으로 생성되었습니다.',
        'registration_failed': '등록에 실패했습니다. 다시 시도하세요.',
        'already_have_account': '이미 계정이 있으신가요?',
        'dont_have_account': '계정이 없으신가요?',
        'forgot_password': '비밀번호를 잊으셨나요?',
        'reset_password': '비밀번호 재설정',

        # フォームバリデーション
        'required_field': '이 필드는 필수입니다.',
        'invalid_email': '유효한 이메일 주소를 입력하세요.',
        'password_too_short': '비밀번호는 최소 8자 이상이어야 합니다.',
        'passwords_dont_match': '비밀번호가 일치하지 않습니다.',
        'username_taken': '이 사용자명은 이미 사용 중입니다.',
        'email_taken': '이 이메일 주소는 이미 등록되어 있습니다.',

        # エラー・成功メッセージ
        'error_occurred': '오류가 발생했습니다.',
        'success': '작업이 성공적으로 완료되었습니다.',
        'not_found': '페이지를 찾을 수 없습니다.',
        'access_denied': '액세스가 거부되었습니다.',
        'server_error': '서버 오류가 발생했습니다.',

        # チャットアプリ固有
        'welcome_message': '채팅 앱에 오신 것을 환영합니다!',
        'room_created': '방이 성공적으로 생성되었습니다.',
        'room_joined': '방에 참여했습니다.',
        'room_left': '방에서 나갔습니다.',
        'user_joined': '{user}님이 방에 참여했습니다.',
        'user_left': '{user}님이 방에서 나갔습니다.',

        # 確認・修正ページ
        'confirm_registration': '등록 확인',
        'registration_info': '등록 정보를 확인하세요:',
        'correct_info': '정확함',
        'modify_info': '수정',
        'registration_complete': '등록 완료!',
        'go_to_login': '로그인 페이지로',

        # 言語関連
        'language': '언어',
        'change_language': '언어 변경',
        'current_language': '현재 언어',

        # ログインページ固有
        'ユーザー名またはメールアドレスとパスワードを入力してログインしてください。': '로그인하려면 사용자명 또는 이메일 주소와 비밀번호를 입력하세요.',
        'ユーザー名またはメールアドレス': '사용자명 또는 이메일 주소',
        'ログイン': '로그인',
        'パスワード': '비밀번호',
        'または': '또는',
        'アカウントを作成': '계정 만들기',
        'トップへ戻る': '처음으로 돌아가기',
        'その他': '기타',

        # トップページ固有
        'トップ': '홈',
        'チャットアプリへようこそ': '채팅 앱에 오신 것을 환영합니다',
        'アカウントでログインするか、新規登録してご利用ください。': '계정으로 로그인하거나 새로 등록해 주세요.',
        'アカウント登録なしでも匿名でご参加いただけます。': '계정 등록 없이도 익명으로 참여하실 수 있습니다.',
        '既にアカウントをお持ちの方': '이미 계정이 있는 분',
        '新規でアカウントを作成する方': '새로운 계정을 만들고 싶은 분',
        'ニックネーム（匿名参加）': '닉네임（익명）',
        '匿名で参加': '익명으로 참여',
        'アカウント登録なしで参加': '계정 등록 없이 참여',
    },
    'es': {
        # 基本UI
        'login': 'Iniciar sesión',
        'register': 'Registrarse',
        'logout': 'Cerrar sesión',
        'username': 'Nombre de usuario',
        'email': 'Dirección de correo electrónico',
        'password': 'Contraseña',
        'confirm_password': 'Confirmar contraseña',
        'back': 'Atrás',
        'cancel': 'Cancelar',
        'submit': 'Enviar',
        'save': 'Guardar',
        'edit': 'Editar',
        'delete': 'Eliminar',
        'create': 'Crear',
        'update': 'Actualizar',
        'search': 'Buscar',
        'next': 'Siguiente',
        'previous': 'Anterior',
        'home': 'Inicio',
        'settings': 'Configuración',
        'profile': 'Perfil',
        'dashboard': 'Panel de control',

        # ナビゲーション・メニュー
        'chat_room': 'Sala de chat',
        'room_list': 'Lista de salas',
        'room_create': 'Crear sala',
        'join_room': 'Unirse a sala',
        'leave_room': 'Salir de sala',
        'room_name': 'Nombre de la sala',
        'room_description': 'Descripción de la sala',
        'members': 'Miembros',
        'online': 'En línea',
        'offline': 'Desconectado',

        # メッセージ・チャット関連
        'message': 'Mensaje',
        'send_message': 'Enviar mensaje',
        'type_message': 'Escribe tu mensaje...',
        'chat_history': 'Historial de chat',
        'no_messages': 'Aún no hay mensajes.',
        'message_sent': 'Mensaje enviado correctamente.',
        'message_failed': 'Error al enviar el mensaje.',

        # 認証・アカウント関連
        'login_title': 'Iniciar sesión en Chat App',
        'register_title': 'Crear cuenta',
        'login_required': 'Por favor inicie sesión para acceder a esta página.',
        'login_failed': 'Error de inicio de sesión. Verifique sus credenciales.',
        'registration_success': 'Cuenta creada correctamente.',
        'registration_failed': 'Error en el registro. Inténtelo de nuevo.',
        'already_have_account': '¿Ya tienes una cuenta?',
        'dont_have_account': '¿No tienes una cuenta?',
        'forgot_password': '¿Olvidaste tu contraseña?',
        'reset_password': 'Restablecer contraseña',

        # 確認・修正ページ
        'confirm_registration': 'Confirmar registro',
        'registration_info': 'Por favor confirme su información de registro:',
        'correct_info': 'Correcto',
        'modify_info': 'Modificar',
        'registration_complete': '¡Registro completo!',
        'go_to_login': 'Ir al login',

        # 言語関連
        'language': 'Idioma',
        'change_language': 'Cambiar idioma',
        'current_language': 'Idioma currente',

        # ログインページ固有
        'ユーザー名またはメールアドレスとパスワードを入力してログインしてください。': 'Por favor, ingrese su nombre de usuario o dirección de correo electrónico y contraseña para iniciar sesión.',
        'ユーザー名またはメールアドレス': 'Nombre de usuario o dirección de correo electrónico',
        'ログイン': 'Iniciar sesión',
        'パスワード': 'Contraseña',
        'または': 'O',
        'アカウントを作成': 'Crear cuenta',
        'トップへ戻る': 'Volver al inicio',
        'その他': 'Otros',

        # トップページ固有
        'トップ': 'Inicio',
        'チャットアプリへようこそ': 'Bienvenido a la aplicación de chat',
        'アカウントでログインするか、新規登録してご利用ください。': 'Por favor inicie sesión con su cuenta o regístrese como nuevo usuario.',
        'アカウント登録なしでも匿名でご参加いただけます。': 'También puede unirse de forma anónima sin registrar una cuenta.',
        '既にアカウントをお持ちの方': 'Para aquellos que ya tienen una cuenta',
        '新規でアカウントを作成する方': 'Para aquellos que quieren crear una nueva cuenta',
        'ニックネーム（匿名参加）': 'Apodo (Anónimo)',
        '匿名で参加': 'Unirse anónimamente',
        'アカウント登録なしで参加': 'Unirse sin registro de cuenta',
    },
    'fr': {
        # 基本UI
        'login': 'Se connecter',
        'register': 'S\'inscrire',
        'logout': 'Se déconnecter',
        'username': 'Nom d\'utilisateur',
        'email': 'Adresse e-mail',
        'password': 'Mot de passe',
        'confirm_password': 'Confirmer le mot de passe',
        'back': 'Retour',
        'cancel': 'Annuler',
        'submit': 'Envoyer',
        'save': 'Enregistrer',
        'edit': 'Modifier',
        'delete': 'Supprimer',
        'create': 'Créer',
        'update': 'Mettre à jour',
        'search': 'Rechercher',
        'next': 'Suivant',
        'previous': 'Précédent',
        'home': 'Accueil',
        'settings': 'Paramètres',
        'profile': 'Profil',
        'dashboard': 'Tableau de bord',

        # ナビゲーション・メニュー
        'chat_room': 'Salon de discussion',
        'room_list': 'Liste des salons',
        'room_create': 'Créer un salon',
        'join_room': 'Rejoindre le salon',
        'leave_room': 'Quitter le salon',
        'room_name': 'Nom du salon',
        'room_description': 'Description du salon',
        'members': 'Membres',
        'online': 'En ligne',
        'offline': 'Hors ligne',

        # メッセージ・チャット関連
        'message': 'Message',
        'send_message': 'Envoyer un message',
        'type_message': 'Tapez votre message...',
        'chat_history': 'Historique du chat',
        'no_messages': 'Aucun message pour le moment.',
        'message_sent': 'Message envoyé avec succès.',
        'message_failed': 'Échec de l\'envoi du message.',

        # 認証・アカウント関連
        'login_title': 'Connexion à Chat App',
        'register_title': 'Créer un compte',
        'login_required': 'Veuillez vous connecter pour accéder à cette page.',
        'login_failed': 'Échec de la connexion. Vérifiez vos identifiants.',
        'registration_success': 'Compte créé avec succès.',
        'registration_failed': 'Échec de l\'inscription. Veuillez réessayer.',
        'already_have_account': 'Vous avez déjà un compte?',
        'dont_have_account': 'Vous n\'avez pas de compte?',
        'forgot_password': 'Mot de passe oublié?',
        'reset_password': 'Réinitialiser le mot de passe',

        # 確認・修正ページ
        'confirm_registration': 'Confirmer l\'inscription',
        'registration_info': 'Veuillez confirmer vos informations d\'inscription:',
        'correct_info': 'Correct',
        'modify_info': 'Modifier',
        'registration_complete': 'Inscription terminée!',
        'go_to_login': 'Aller à la connexion',

        # 言語関連
        'language': 'Langue',
        'change_language': 'Changer de langue',
        'current_language': 'Langue actuelle',

        # ログインページ固有
        'ユーザー名またはメールアドレスとパスワードを入力してログインしてください。': 'Veuillez saisir votre nom d\'utilisateur ou adresse e-mail et mot de passe pour vous connecter.',
        'ユーザー名またはメールアドレス': 'Nom d\'utilisateur ou adresse e-mail',
        'ログイン': 'Se connecter',
        'パスワード': 'Mot de passe',
        'または': 'Ou',
        'アカウントを作成': 'Créer un compte',
        'トップへ戻る': 'Retour à l\'accueil',
        'その他': 'Autres',

        # トップページ固有
        'トップ': 'Accueil',
        'チャットアプリへようこそ': 'Bienvenue dans l\'application de chat',
        'アカウントでログインするか、新規登録してご利用ください。': 'Veuillez vous connecter avec votre compte ou vous inscrire en tant que nouvel utilisateur.',
        'アカウント登録なしでも匿名でご参加いただけます。': 'Vous pouvez également vous joindre de manière anonyme sans enregistrer de compte.',
        '既にアカウントをお持ちの方': 'Pour ceux qui ont déjà un compte',
        '新規でアカウントを作成する方': 'Pour ceux qui veulent créer un nouveau compte',
        'ニックネーム（匿名参加）': 'Surnom (Anonyme)',
        '匿名で参加': 'Rejoindre anonymement',
        'アカウント登録なしで参加': 'Rejoindre sans enregistrement de compte',
    },
    'de': {
        # 基本UI
        'login': 'Anmelden',
        'register': 'Registrieren',
        'logout': 'Abmelden',
        'username': 'Benutzername',
        'email': 'E-Mail-Adresse',
        'password': 'Passwort',
        'confirm_password': 'Passwort bestätigen',
        'back': 'Zurück',
        'cancel': 'Abbrechen',
        'submit': 'Senden',
        'save': 'Speichern',
        'edit': 'Bearbeiten',
        'delete': 'Löschen',
        'create': 'Erstellen',
        'update': 'Aktualisieren',
        'search': 'Suchen',
        'next': 'Weiter',
        'previous': 'Zurück',
        'home': 'Startseite',
        'settings': 'Einstellungen',
        'profile': 'Profil',
        'dashboard': 'Dashboard',

        # ナビゲーション・メニュー
        'chat_room': 'Chatraum',
        'room_list': 'Raumliste',
        'room_create': 'Raum erstellen',
        'join_room': 'Raum beitreten',
        'leave_room': 'Raum verlassen',
        'room_name': 'Raumname',
        'room_description': 'Raumbeschreibung',
        'members': 'Mitglieder',
        'online': 'Online',
        'offline': 'Offline',

        # メッセージ・チャット関連
        'message': 'Nachricht',
        'send_message': 'Nachricht senden',
        'type_message': 'Geben Sie Ihre Nachricht ein...',
        'chat_history': 'Chat-Verlauf',
        'no_messages': 'Noch keine Nachrichten.',
        'message_sent': 'Nachricht erfolgreich gesendet.',
        'message_failed': 'Nachricht konnte nicht gesendet werden.',

        # 認証・アカウント関連
        'login_title': 'Bei Chat App anmelden',
        'register_title': 'Konto erstellen',
        'login_required': 'Bitte melden Sie sich an, um auf diese Seite zuzugreifen.',
        'login_failed': 'Anmeldung fehlgeschlagen. Überprüfen Sie Ihre Anmeldedaten.',
        'registration_success': 'Konto erfolgreich erstellt.',
        'registration_failed': 'Registrierung fehlgeschlagen. Bitte versuchen Sie es erneut.',
        'already_have_account': 'Haben Sie bereits ein Konto?',
        'dont_have_account': 'Haben Sie noch kein Konto?',
        'forgot_password': 'Passwort vergessen?',
        'reset_password': 'Passwort zurücksetzen',

        # 確認・修正ページ
        'confirm_registration': 'Registrierung bestätigen',
        'registration_info': 'Bitte bestätigen Sie Ihre Registrierungsdaten:',
        'correct_info': 'Korrekt',
        'modify_info': 'Ändern',
        'registration_complete': 'Registrierung abgeschlossen!',
        'go_to_login': 'Zur Anmeldung',

        # 言語関連
        'language': 'Sprache',
        'change_language': 'Sprache ändern',
        'current_language': 'Aktuelle Sprache',

        # ログインページ固有
        'ユーザー名またはメールアドレスとパスワードを入力してログインしてください。': 'Bitte geben Sie Ihren Benutzernamen oder Ihre E-Mail-Adresse und Ihr Passwort ein, um sich anzumelden.',
        'ユーザー名またはメールアドレス': 'Benutzername oder E-Mail-Adresse',
        'ログイン': 'Anmelden',
        'パスワード': 'Passwort',
        'または': 'Oder',
        'アカウントを作成': 'Konto erstellen',
        'トップへ戻る': 'Zurück zur Startseite',
        'その他': 'Andere',
    },
    'pt': {
        # 基本UI
        'login': 'Entrar',
        'register': 'Registrar',
        'logout': 'Sair',
        'username': 'Nome de usuário',
        'email': 'Endereço de e-mail',
        'password': 'Senha',
        'confirm_password': 'Confirmar senha',
        'back': 'Voltar',
        'cancel': 'Cancelar',
        'submit': 'Enviar',
        'save': 'Salvar',
        'edit': 'Editar',
        'delete': 'Excluir',
        'create': 'Criar',
        'update': 'Atualizar',
        'search': 'Pesquisar',
        'next': 'Próximo',
        'previous': 'Anterior',
        'home': 'Início',
        'settings': 'Configurações',
        'profile': 'Perfil',
        'dashboard': 'Painel',

        # ナビゲーション・メニュー
        'chat_room': 'Sala de chat',
        'room_list': 'Lista de salas',
        'room_create': 'Criar sala',
        'join_room': 'Entrar na sala',
        'leave_room': 'Sair da sala',
        'room_name': 'Nome da sala',
        'room_description': 'Descrição da sala',
        'members': 'Membros',
        'online': 'Online',
        'offline': 'Offline',

        # メッセージ・チャット関連
        'message': 'Mensagem',
        'send_message': 'Enviar mensagem',
        'type_message': 'Digite sua mensagem...',
        'chat_history': 'Histórico do chat',
        'no_messages': 'Ainda não há mensagens.',
        'message_sent': 'Mensagem enviada com sucesso.',
        'message_failed': 'Falha ao enviar mensagem.',

        # 認証・アカウント関連
        'login_title': 'Entrar no Chat App',
        'register_title': 'Criar conta',
        'login_required': 'Por favor, faça login para acessar esta página.',
        'login_failed': 'Falha no login. Verifique suas credenciais.',
        'registration_success': 'Conta criada com sucesso.',
        'registration_failed': 'Falha no registro. Tente novamente.',
        'already_have_account': 'Já tem uma conta?',
        'dont_have_account': 'Não tem uma conta?',
        'forgot_password': 'Esqueceu a senha?',
        'reset_password': 'Redefinir senha',

        # 確認・修正ページ
        'confirm_registration': 'Confirmar registro',
        'registration_info': 'Por favor, confirme suas informações de registro:',
        'correct_info': 'Correto',
        'modify_info': 'Modificar',
        'registration_complete': 'Registro completo!',
        'go_to_login': 'Ir para login',

        # 言語関連
        'language': 'Idioma',
        'change_language': 'Alterar idioma',
        'current_language': 'Idioma atual',

        # ログインページ固有
        'ユーザー名またはメールアドレスとパスワードを入力してログインしてください。': 'Por favor, insira seu nome de usuário ou endereço de e-mail e senha para fazer login.',
        'ユーザー名またはメールアドレス': 'Nome de usuário ou endereço de e-mail',
        'ログイン': 'Entrar',
        'パスワード': 'Senha',
        'または': 'Ou',
        'アカウントを作成': 'Criar conta',
        'トップへ戻る': 'Voltar ao início',
        'その他': 'Outros',
    },
}

def get_translation(text, lang='ja'):
    """指定された言語でテキストを翻訳する"""
    if DEBUG_TRANSLATION:
        print(f"get_translation: text='{text}', lang='{lang}'")

    # 指定された言語の翻訳辞書を取得
    translations = BASIC_TRANSLATIONS.get(lang, {})
    translated = translations.get(text, text)  # 翻訳がない場合は元のテキストを返す

    if DEBUG_TRANSLATION:
        print(f"get_translation: result='{translated}'")

    return translated

def get_available_languages():
    """利用可能な言語のリストを返す"""
    return list(BASIC_TRANSLATIONS.keys())

def add_translation(lang, key, value):
    """新しい翻訳を追加する（管理画面用）"""
    if lang not in BASIC_TRANSLATIONS:
        BASIC_TRANSLATIONS[lang] = {}

    BASIC_TRANSLATIONS[lang][key] = value

    if DEBUG_TRANSLATION:
        print(f"Translation added: {lang}.{key} = '{value}'")

def get_language_translations(lang):
    """指定された言語のすべての翻訳を取得する"""
    return BASIC_TRANSLATIONS.get(lang, {})

def export_translations_to_json():
    """翻訳辞書をJSON形式で出力する（管理画面用）"""
    import json
    return json.dumps(BASIC_TRANSLATIONS, ensure_ascii=False, indent=2)
