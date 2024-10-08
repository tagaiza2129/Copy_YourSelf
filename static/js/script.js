document.addEventListener('DOMContentLoaded', function() {
    const title = document.getElementById('title');
    const menuToggle = document.getElementById('menu-toggle');
    const sideMenu = document.getElementById('side-menu');
    const profileToggle = document.getElementById('profile-toggle');
    const profileModal = document.getElementById('profile-modal');
    const closeProfileModal = document.querySelector('.modal .close-btn');
    const closeSideMenuButton = document.querySelector('#side-menu .close-btn');
    const profileMenuButton = document.getElementById('profile-menu-button');
    const saveProfileButton = document.getElementById('save-profile');
    const profileImageUpload = document.getElementById('profile-image-upload');
    const profileImage = document.getElementById('profile-image');
    const profileIcon = document.getElementById('profile-icon');
    const profileNameInput = document.getElementById('profile-name');
    const sendMessageButton = document.getElementById('send-message');
    const messageInput = document.querySelector('input[type="text"]');
    const messagesContainer = document.querySelector('.messages-container');
    const appContainer = document.querySelector('.app-container'); // 追加
    const fileUploadButton = document.getElementById('file-upload-button'); // 追加
    const fileUploadInput = document.getElementById('file-upload'); // 追加
    const fileListContainer = document.getElementById('file-list'); // 追加

    fileUploadButton.addEventListener('click', function() {
        fileUploadInput.click();
    });

    document.addEventListener('DOMContentLoaded', function() {
    // ページの要素を取得
    const loginPage = document.getElementById('login-page');
    const settingsPage = document.getElementById('settings-page');
    const errorPage = document.getElementById('error-page');
    const loginForm = document.getElementById('login-form');
    const redirectButton = document.getElementById('redirect-button');
    const backToMainButton = document.getElementById('back-to-main');

    // 初期画面としてログインページを表示
    loginPage.style.display = 'flex';

    // ログインフォームの送信イベントを監視
    loginForm.addEventListener('submit', function(event) {
        event.preventDefault();
        // ログイン成功時の処理（仮に成功とする）
        loginPage.style.display = 'none';
        settingsPage.style.display = 'block';
    });

    // ユーザー設定ページの戻るボタン
    backToMainButton.addEventListener('click', function() {
        settingsPage.style.display = 'none';
        loginPage.style.display = 'flex';
    });

    // エラーページのリダイレクトボタン
    redirectButton.addEventListener('click', function() {
        window.location.href = '/'; // ホームにリダイレクトする例
    });

    // エラーページの表示（エラー発生時に呼び出す関数）
    function showErrorPage() {
        loginPage.style.display = 'none';
        settingsPage.style.display = 'none';
        errorPage.style.display = 'block';
    }

    // 例：何らかのエラーが発生したとき
    // showErrorPage();
});


    menuToggle.addEventListener('click', function() {
        sideMenu.classList.toggle('active');
        appContainer.classList.toggle('menu-active'); // 追加
    });

    closeSideMenuButton.addEventListener('click', function() {
        sideMenu.classList.remove('active');
        appContainer.classList.remove('menu-active'); // 追加
    });

    profileToggle.addEventListener('click', function() {
        profileModal.style.display = 'block';
    });

    profileMenuButton.addEventListener('click', function() {
        profileModal.style.display = 'block';
        sideMenu.classList.remove('active');
        appContainer.classList.remove('menu-active'); // 追加
    });

    closeProfileModal.addEventListener('click', function() {
        profileModal.style.display = 'none';
    });

    window.addEventListener('click', function(event) {
        if (event.target === profileModal) {
            profileModal.style.display = 'none';
        }
    });

    saveProfileButton.addEventListener('click', function() {
        const profileName = profileNameInput.value.trim();
        if (profileName) {
            // ここでプロフィール名を保存する処理を追加できます
        }
        profileModal.style.display = 'none';
    });

    profileImageUpload.addEventListener('change', function(event) {
        const file = event.target.files[0];
        if (file && (file.type === 'image/png' || file.type === 'image/jpeg')) {
            const reader = new FileReader();
            reader.onload = function(e) {
                profileImage.src = e.target.result;
                profileIcon.src = e.target.result;
            };
            reader.readAsDataURL(file);
        }
    });

    function sendMessage() {
        const messageText = messageInput.value.trim();
        if (messageText !== "") {
            const messageElement = document.createElement('div');
            messageElement.classList.add('message');
            messageElement.textContent = messageText;
            messagesContainer.appendChild(messageElement);
            messageInput.value = "";
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
            fetch("inference", {
                method: 'POST',
                body: JSON.stringify({
                    message: messageText,
                    max_length: 10,
                    device_type: "NVIDIA",
                    device_id: 0,
                    len_nutral: 800,
                    len_vector: 300,
                    num_layers: 1,
                    bidirectional: true,
                    dropout: "0.0",
                    clip: 100
                }),
                headers: {'Content-Type': 'application/json'}
            })
            .then(response => response.json())
            .then(data => {
                console.log('AI:', data.map(item => item.message));
                const resultElement = document.createElement('div');
                resultElement.textContent = 'AI: ' + data;
                messagesContainer.appendChild(resultElement);
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            })
            .catch(error => {
                console.error('AI:', error);
                alert('AI processing failed.');
            });
        }
    }

    sendMessageButton.addEventListener('click', sendMessage);

    messageInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });

    // ファイルアップロードのロジックを追加
    fileUploadInput.addEventListener('change', function(event) {
        const files = Array.from(event.target.files);
        if (files.length > 3) {
            alert('ファイルは3つまで選択できます。');
            fileUploadInput.value = ''; // 選択をリセット
            return;
        }

        fileListContainer.innerHTML = ''; // 既存のリストをクリア
        files.forEach(file => {
            const fileItem = document.createElement('div');
            fileItem.classList.add('file-item');

            const fileIcon = document.createElement('img');
            fileIcon.src = 'file-icon.png'; // アイコン画像へのパスを設定
            fileItem.appendChild(fileIcon);

            const fileName = document.createElement('span');
            fileName.textContent = file.name;
            fileItem.appendChild(fileName);

            const fileDetails = document.createElement('span');
            const fileExtension = file.name.split('.').pop().toUpperCase(); // 拡張子を取得
            const fileSize = `${(file.size / 1024).toFixed(2)} KB`;
            fileDetails.textContent = `${fileExtension} - ${fileSize}`;
            fileDetails.classList.add('file-details');
            fileItem.appendChild(fileDetails);

            fileListContainer.appendChild(fileItem);
        });

        const existingFiles = fileListContainer.children.length;
        if (existingFiles >= 3) {
            fileUploadInput.disabled = true;
            fileUploadButton.style.opacity = 0.5; // ボタンを無効化して視覚的に認識
        } else {
            fileUploadInput.disabled = false;
            fileUploadButton.style.opacity = 1;
        }
    });


    // ファイル送信機能の追加
    sendMessageButton.addEventListener('click', function() {
        const files = fileUploadInput.files;

        if (files.length === 0) {
            alert('送信するファイルを選択してください。');
            return;
        }

        const formData = new FormData();
        for (let i = 0; i < files.length; i++) {
            formData.append('file' + i, files[i]);
        }

        // サーバーにファイルを送信するリクエスト
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log('ファイルが送信されました:', data);
            alert('ファイルが送信されました！');
            fileListContainer.innerHTML = ''; // 送信後にファイルリストをクリア
            fileUploadInput.value = ''; // ファイル入力をリセット
            fileUploadInput.disabled = false;
            fileUploadButton.style.opacity = 1;
        })
        .catch(error => {
            console.error('ファイル送信に失敗しました:', error);
            alert('ファイル送信に失敗しました。');
        });
    });

    function fetchChatList() {
        fetch('/models', { method: 'GET' })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                const names = data.map(item => item.name);
                const paths = data.map(item => item.path);
                return names,paths;
            })
            .catch(error => {
                console.error('モデルのリストの取得に失敗しました:', error);
            });
    }
    const chatList = document.querySelector('.chat-list');

    function addChatItem(text) {
        const chatItem = document.createElement('li');
        chatItem.textContent = text;
        chatList.appendChild(chatItem);
    }

    fetchChatList().then(names,paths => {
        for (let i = 0; i < names.length; i++) {
            addChatItem(data[i]);
        }
    });
});
