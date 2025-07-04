self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open('tetris-cache').then((cache) => {
            return cache.addAll([
                '/',
                '/tetris.py',
                '/assets/sfx/land.wav',
                '/assets/sfx/clear.wav',
                '/assets/sfx/gameover.wav',
                'https://cdn.jsdelivr.net/pyodide/v0.23.4/full/pyodide.js',
                'https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css'
            ]);
        })
    );
});

self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request).then((response) => {
            return response || fetch(event.request);
        })
    );
});
