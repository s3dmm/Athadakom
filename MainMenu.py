<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>حرب الألوان 3D</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Cairo', sans-serif; touch-action: manipulation; overflow: hidden; }
        #canvas-container { width: 100%; height: 60vh; max-height: 550px; cursor: pointer; border: 2px solid #4a5568; border-radius: 0.5rem; margin: auto; background-color: #1f2937; }
        canvas { display: block; }
        .color-box { width: 2rem; height: 2rem; border: 2px solid white; transition: transform 0.2s; }
        .color-box.selected { transform: scale(1.2); border: 3px solid #6366F1; }
        .btn-primary { @apply bg-indigo-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-opacity-50 transition-colors duration-300 disabled:bg-gray-600 disabled:text-gray-400 disabled:cursor-not-allowed; }
        .card { @apply bg-gray-800 p-6 rounded-xl shadow-2xl border border-gray-700; }
        .player-list-item { @apply flex items-center gap-3 p-2 bg-gray-700 rounded-md; }
        .input-field { @apply text-sm rounded-lg focus:ring-indigo-500 focus:border-indigo-500 block w-full p-2.5 text-center; }
    </style>
</head>
<body class="bg-gray-900 text-white flex items-center justify-center min-h-screen">

    <div id="app" class="container mx-auto p-4 max-w-4xl text-center">

        <div id="game-setup" class="card">
            <h1 class="text-4xl font-bold mb-2 text-indigo-400">حرب الألوان 3D</h1>
            <p class="text-gray-400 mb-6">سيطر على المكعبات بلونك الخاص!</p>
            
            <div class="mb-4 max-w-sm mx-auto">
                <label for="player-name-input" class="block mb-2 text-sm font-medium text-gray-300">اسمك في اللعبة</label>
                <input type="text" id="player-name-input" class="input-field" style="background-color: #4B5563; color: #FFFFFF; border: 1px solid #6B7280;" placeholder="اكتب اسمك هنا" maxlength="12">
            </div>

            <div class="mb-4 max-w-sm mx-auto">
                 <label class="block mb-2 text-sm font-medium text-gray-300">اختر لونك</label>
                 <div id="color-picker" class="flex justify-center gap-2"></div>
            </div>

            <div class="space-y-4 max-w-sm mx-auto">
                <button id="create-game-btn" class="btn-primary w-full" disabled>🚀 إنشاء لعبة جديدة</button>
                <div class="flex items-center">
                    <hr class="w-full border-gray-600"><span class="p-2 text-gray-500">أو</span><hr class="w-full border-gray-600">
                </div>
                <input type="text" id="join-game-id-input" class="input-field" placeholder="أدخل معرّف اللعبة هنا" style="background-color: #4B5563; color: #FFFFFF; border: 1px solid #6B7280;">
                <button id="join-game-btn" class="btn-primary w-full" disabled>🤝 انضمام إلى لعبة</button>
            </div>
             <p id="auth-status" class="text-xs text-yellow-400 mt-4 h-4">جاري الاتصال بالخادم...</p>
        </div>

        <div id="game-lobby" class="hidden card">
            <h2 class="text-3xl font-bold text-indigo-400 mb-4">غرفة الانتظار</h2>
            <p class="text-gray-400 mb-2">شارك هذا المعرّف مع أصدقائك للانضمام:</p>
            <p id="lobby-game-id" class="text-4xl font-mono p-3 bg-gray-900 rounded-lg cursor-pointer mb-6" title="اضغط للنسخ"></p>
            <h3 class="text-xl font-bold text-gray-300 mb-3">اللاعبون المنضمون (<span id="player-count">0</span>):</h3>
            <div id="lobby-players-list" class="space-y-2 text-left max-w-md mx-auto mb-8 min-h-[5rem]"></div>
            <button id="start-game-btn" class="btn-primary w-full max-w-md mx-auto hidden">🚀 بدء اللعبة</button>
            <p id="lobby-waiting-msg" class="text-gray-400 mt-4">في انتظار المضيف لبدء اللعبة...</p>
        </div>

        <div id="game-board" class="hidden">
            <div class="card mb-4">
                <div class="flex flex-col sm:flex-row justify-between items-center gap-4">
                    <div><p class="text-sm text-gray-400">معرّف اللعبة:</p><p id="game-id-display" class="text-2xl font-bold font-mono text-indigo-400"></p></div>
                    <div id="timer-display" class="text-5xl font-bold">05:00</div>
                    <div><p class="text-sm text-gray-400">لونك:</p><div id="player-color-box" class="color-box rounded-md mx-auto"></div></div>
                </div>
                 <div id="status-message" class="mt-4 text-yellow-400 h-6"></div>
            </div>
            <div id="canvas-container"></div>
            <div id="scoreboard" class="card mt-4">
                <h3 class="text-xl font-bold mb-2">لوحة النتائج</h3><div id="scores-container" class="grid grid-cols-2 sm:grid-cols-4 gap-4"></div>
            </div>
        </div>

        <div id="winner-modal" class="hidden fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50">
            <div class="card text-center">
                <h2 id="winner-title" class="text-3xl font-bold mb-4"></h2>
                <p id="winner-message" class="text-lg mb-6"></p>
                <button id="play-again-btn" class="btn-primary">العب مرة أخرى</button>
            </div>
        </div>
    
    <script async src="https://unpkg.com/es-module-shims@1.6.3/dist/es-module-shims.js"></script>
    <script type="importmap">{ "imports": { "three": "https://cdn.jsdelivr.net/npm/three@0.155.0/build/three.module.js", "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.155.0/examples/jsm/" } }</script>
    <script type="module">
        import { initializeApp } from "https://www.gstatic.com/firebasejs/11.6.1/firebase-app.js";
        import { getAuth, signInAnonymously, signInWithCustomToken, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/11.6.1/firebase-auth.js";
        import { getFirestore, doc, getDoc, setDoc, onSnapshot, updateDoc, arrayUnion, runTransaction } from "https://www.gstatic.com/firebasejs/11.6.1/firebase-firestore.js";
        import * as THREE from 'three';
        import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
        import { firebaseConfig } from './firebase-config.js';

        const GRID_SIZE = 15, GAME_DURATION_SECONDS = 300, PIXEL_CLICK_COOLDOWN = 250;
        const PLAYER_COLORS = ["#FF5733", "#33FF57", "#3357FF", "#FF33A1", "#A133FF", "#33FFA1", "#FFD700", "#00FFFF"];
        
        const appId = typeof __app_id !== 'undefined' ? __app_id : 'default-color-wars-3d';
        const DB_PATH = `artifacts/${appId}/public/data/color-wars-3d-games`;

... (300 lines left)
Collapse
