# barronaveia
aplicativo da escola de ceramica 
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Barro na Veia - Escola de Cerâmica</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {
            box-sizing: border-box;
        }
        
        .clay-gradient {
            background: linear-gradient(135deg, #556B2F 0%, #6B8E23 50%, #8FBC8F 100%);
        }
        
        .pottery-shadow {
            box-shadow: 0 8px 32px rgba(85, 107, 47, 0.3);
        }
        
        .slide-in {
            animation: slideIn 0.3s ease-out;
        }
        
        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        .fade-in {
            animation: fadeIn 0.5s ease-in;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .notification-badge {
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }
    </style>
</head>
<body class="bg-gradient-to-br from-amber-50 to-orange-100 min-h-screen">
    <!-- Header -->
    <header class="clay-gradient text-white shadow-lg">
        <div class="container mx-auto px-4 py-4">
            <div class="flex items-center justify-between">
                <div class="flex items-center space-x-3">
                    <div class="w-12 h-12 bg-white rounded-full flex items-center justify-center overflow-hidden">
                        <img id="schoolLogo" src="" alt="Logo Barro na Veia" class="w-full h-full object-cover hidden" onerror="this.style.display='none'; document.getElementById('defaultLogo').style.display='flex';">
                        <div id="defaultLogo" class="w-full h-full flex items-center justify-center">
                            <svg class="w-8 h-8 text-orange-600" fill="currentColor" viewBox="0 0 24 24">
                                <path d="M12 2C10.9 2 10 2.9 10 4V6H8C6.9 6 6 6.9 6 8V20C6 21.1 6.9 22 8 22H16C17.1 22 18 21.1 18 20V8C18 6.9 17.1 6 16 6H14V4C14 2.9 13.1 2 12 2ZM12 4V6H12V4ZM8 8H16V20H8V8ZM10 10V18H14V10H10Z"/>
                                <circle cx="12" cy="14" r="1"/>
                            </svg>
                        </div>
                    </div>
                    <div>
                        <h1 class="text-2xl font-bold">Barro na Veia</h1>
                        <p class="text-sm opacity-90">Escola de Cerâmica</p>
                    </div>
                </div>
                <div class="flex items-center space-x-4">
                    <button id="notificationBtn" class="relative p-2 hover:bg-white/20 rounded-full transition-colors">
                        <span class="text-xl">🔔</span>
                        <span class="notification-badge absolute -top-1 -right-1 bg-red-500 text-xs rounded-full w-5 h-5 flex items-center justify-center">3</span>
                    </button>
                    <div class="flex items-center space-x-2">
                        <div class="w-8 h-8 bg-white/20 rounded-full flex items-center justify-center">
                            <span class="text-sm">👩‍🎨</span>
                        </div>
                        <span class="text-sm">Maria Silva</span>
                    </div>
                </div>
            </div>
        </div>
    </header>

    <!-- Navigation -->
    <nav class="bg-white shadow-md sticky top-0 z-40">
        <div class="container mx-auto px-4">
            <div class="flex space-x-8 overflow-x-auto">
                <button class="nav-btn py-4 px-2 border-b-2 border-green-600 text-green-700 font-medium whitespace-nowrap" data-section="dashboard">
                    📊 Dashboard
                </button>
                <button class="nav-btn py-4 px-2 border-b-2 border-transparent text-gray-600 hover:text-green-600 transition-colors whitespace-nowrap" data-section="portfolio">
                    🎨 Meu Portfólio
                </button>
                <button class="nav-btn py-4 px-2 border-b-2 border-transparent text-gray-600 hover:text-green-600 transition-colors whitespace-nowrap" data-section="gallery">
                    🖼️ Galeria
                </button>
                <button class="nav-btn py-4 px-2 border-b-2 border-transparent text-gray-600 hover:text-green-600 transition-colors whitespace-nowrap" data-section="student-area">
                    🎓 Área do Aluno
                </button>
                <button class="nav-btn py-4 px-2 border-b-2 border-transparent text-gray-600 hover:text-green-600 transition-colors whitespace-nowrap" data-section="shop">
                    🛒 Loja
                </button>
                <button class="nav-btn py-4 px-2 border-b-2 border-transparent text-gray-600 hover:text-green-600 transition-colors whitespace-nowrap" data-section="financial">
                    💰 Financeiro
                </button>
                <button class="nav-btn py-4 px-2 border-b-2 border-transparent text-gray-600 hover:text-green-600 transition-colors whitespace-nowrap" data-section="chat">
                    💬 Chat da Turma
                </button>
                <button class="nav-btn py-4 px-2 border-b-2 border-transparent text-red-600 hover:text-red-700 transition-colors whitespace-nowrap" data-section="admin">
                    ⚙️ Admin
                </button>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <main class="container mx-auto px-4 py-8">
        <!-- Dashboard Section -->
        <section id="dashboard" class="section-content">
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
                <!-- Welcome Card -->
                <div class="lg:col-span-2 bg-white rounded-xl pottery-shadow p-6">
                    <div class="flex items-center justify-between mb-4">
                        <h2 class="text-2xl font-bold text-gray-800">Bem-vinda, Maria! 👋</h2>
                        <span class="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium">5ª-feira (tarde)</span>
                    </div>
                    <p class="text-gray-600 mb-4">Sua jornada na cerâmica está florescendo! Continue criando peças incríveis.</p>
                    <div class="grid grid-cols-2 gap-4">
                        <div class="text-center p-3 bg-green-50 rounded-lg">
                            <div class="text-2xl font-bold text-green-700">23</div>
                            <div class="text-sm text-gray-600">Peças Criadas</div>
                        </div>
                        <div class="text-center p-3 bg-blue-50 rounded-lg">
                            <div class="text-2xl font-bold text-blue-600">8</div>
                            <div class="text-sm text-gray-600">Meses no Ateliê</div>
                        </div>
                    </div>
                </div>

                <!-- Quick Actions -->
                <div class="bg-white rounded-xl pottery-shadow p-6">
                    <h3 class="text-lg font-semibold mb-4 text-gray-800">Ações Rápidas</h3>
                    <div class="space-y-3">
                        <button class="w-full bg-green-600 hover:bg-green-700 text-white py-2 px-4 rounded-lg transition-colors flex items-center justify-center space-x-2">
                            <span>📸</span>
                            <span>Adicionar Peça</span>
                        </button>
                        <button class="w-full bg-green-500 hover:bg-green-600 text-white py-2 px-4 rounded-lg transition-colors flex items-center justify-center space-x-2">
                            <span>🔥</span>
                            <span>Agendar Queima</span>
                        </button>
                        <button class="w-full bg-green-700 hover:bg-green-800 text-white py-2 px-4 rounded-lg transition-colors flex items-center justify-center space-x-2">
                            <span>🛒</span>
                            <span>Comprar Argila</span>
                        </button>
                    </div>
                </div>
            </div>

            <!-- Recent Activity -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div class="bg-white rounded-xl pottery-shadow p-6">
                    <h3 class="text-lg font-semibold mb-4 text-gray-800">Atividade Recente</h3>
                    <div class="space-y-4">
                        <div class="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
                            <span class="text-2xl">🏆</span>
                            <div>
                                <p class="font-medium">Sua tigela ganhou 15 curtidas!</p>
                                <p class="text-sm text-gray-600">Há 2 horas</p>
                            </div>
                        </div>
                        <div class="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
                            <span class="text-2xl">💬</span>
                            <div>
                                <p class="font-medium">Ana comentou na sua peça</p>
                                <p class="text-sm text-gray-600">Há 5 horas</p>
                            </div>
                        </div>
                        <div class="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
                            <span class="text-2xl">🔥</span>
                            <div>
                                <p class="font-medium">Queima concluída com sucesso</p>
                                <p class="text-sm text-gray-600">Ontem</p>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="bg-white rounded-xl pottery-shadow p-6">
                    <h3 class="text-lg font-semibold mb-4 text-gray-800">Próximos Eventos</h3>
                    <div class="space-y-4">
                        <div class="border-l-4 border-orange-500 pl-4 py-2">
                            <p class="font-medium">Aula de Esmaltação</p>
                            <p class="text-sm text-gray-600">Amanhã, 14:00</p>
                        </div>
                        <div class="border-l-4 border-blue-500 pl-4 py-2">
                            <p class="font-medium">Queima Coletiva</p>
                            <p class="text-sm text-gray-600">Sexta-feira, 09:00</p>
                        </div>
                        <div class="border-l-4 border-green-500 pl-4 py-2">
                            <p class="font-medium">Exposição Mensal</p>
                            <p class="text-sm text-gray-600">Próxima semana</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Portfolio Section -->
        <section id="portfolio" class="section-content hidden">
            <div class="flex justify-between items-center mb-6">
                <h2 class="text-3xl font-bold text-gray-800">Meu Portfólio</h2>
                <button id="addPieceBtn" class="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-lg transition-colors flex items-center space-x-2">
                    <span>➕</span>
                    <span>Adicionar Peça</span>
                </button>
            </div>

            <!-- Filter Tabs -->
            <div class="flex space-x-4 mb-6 overflow-x-auto">
                <button class="filter-btn bg-green-600 text-white px-4 py-2 rounded-lg whitespace-nowrap" data-filter="all">Todas</button>
                <button class="filter-btn bg-gray-200 text-gray-700 hover:bg-gray-300 px-4 py-2 rounded-lg transition-colors whitespace-nowrap" data-filter="tigelas">Tigelas</button>
                <button class="filter-btn bg-gray-200 text-gray-700 hover:bg-gray-300 px-4 py-2 rounded-lg transition-colors whitespace-nowrap" data-filter="vasos">Vasos</button>
                <button class="filter-btn bg-gray-200 text-gray-700 hover:bg-gray-300 px-4 py-2 rounded-lg transition-colors whitespace-nowrap" data-filter="pratos">Pratos</button>
                <button class="filter-btn bg-gray-200 text-gray-700 hover:bg-gray-300 px-4 py-2 rounded-lg transition-colors whitespace-nowrap" data-filter="esculturas">Esculturas</button>
            </div>

            <!-- Portfolio Grid -->
            <div id="portfolioGrid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <!-- Sample pieces -->
                <div class="piece-card bg-white rounded-xl pottery-shadow overflow-hidden" data-category="tigelas">
                    <div class="h-48 bg-gradient-to-br from-orange-200 to-orange-300 flex items-center justify-center">
                        <span class="text-6xl">🥣</span>
                    </div>
                    <div class="p-4">
                        <h3 class="font-semibold text-lg mb-2">Tigela Rústica</h3>
                        <p class="text-gray-600 text-sm mb-3">Técnica: Torno • Criada em: 15/03/2024</p>
                        <div class="flex items-center justify-between">
                            <div class="flex items-center space-x-1">
                                <span class="text-red-500">❤️</span>
                                <span class="text-sm">12</span>
                            </div>
                            <button class="text-blue-500 hover:text-blue-600 text-sm">Ver detalhes</button>
                        </div>
                    </div>
                </div>

                <div class="piece-card bg-white rounded-xl pottery-shadow overflow-hidden" data-category="vasos">
                    <div class="h-48 bg-gradient-to-br from-green-200 to-green-300 flex items-center justify-center">
                        <span class="text-6xl">🏺</span>
                    </div>
                    <div class="p-4">
                        <h3 class="font-semibold text-lg mb-2">Vaso Decorativo</h3>
                        <p class="text-gray-600 text-sm mb-3">Técnica: Modelagem • Criada em: 10/03/2024</p>
                        <div class="flex items-center justify-between">
                            <div class="flex items-center space-x-1">
                                <span class="text-red-500">❤️</span>
                                <span class="text-sm">8</span>
                            </div>
                            <button class="text-blue-500 hover:text-blue-600 text-sm">Ver detalhes</button>
                        </div>
                    </div>
                </div>

                <div class="piece-card bg-white rounded-xl pottery-shadow overflow-hidden" data-category="pratos">
                    <div class="h-48 bg-gradient-to-br from-blue-200 to-blue-300 flex items-center justify-center">
                        <span class="text-6xl">🍽️</span>
                    </div>
                    <div class="p-4">
                        <h3 class="font-semibold text-lg mb-2">Prato Artístico</h3>
                        <p class="text-gray-600 text-sm mb-3">Técnica: Placa • Criada em: 05/03/2024</p>
                        <div class="flex items-center justify-between">
                            <div class="flex items-center space-x-1">
                                <span class="text-red-500">❤️</span>
                                <span class="text-sm">15</span>
                            </div>
                            <button class="text-blue-500 hover:text-blue-600 text-sm">Ver detalhes</button>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Gallery Section -->
        <section id="gallery" class="section-content hidden">
            <div class="flex justify-between items-center mb-6">
                <h2 class="text-3xl font-bold text-gray-800">Galeria Coletiva</h2>
                <div class="flex items-center space-x-4">
                    <span class="bg-yellow-100 text-yellow-800 px-3 py-1 rounded-full text-sm font-medium">🏆 Votação 2024 Aberta</span>
                </div>
            </div>

            <!-- Gallery Grid -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <div class="bg-white rounded-xl pottery-shadow overflow-hidden">
                    <div class="h-48 bg-gradient-to-br from-purple-200 to-purple-300 flex items-center justify-center">
                        <span class="text-6xl">🏺</span>
                    </div>
                    <div class="p-4">
                        <div class="flex items-center justify-between mb-2">
                            <h3 class="font-semibold">Vaso Contemporâneo</h3>
                            <span class="bg-gold-100 text-yellow-700 px-2 py-1 rounded text-xs">🥇 1º Lugar</span>
                        </div>
                        <p class="text-gray-600 text-sm mb-3">Por: Ana Costa • 3ª-feira (noite)</p>
                        <div class="flex items-center justify-between">
                            <div class="flex items-center space-x-3">
                                <button class="vote-btn flex items-center space-x-1 text-red-500 hover:text-red-600">
                                    <span>❤️</span>
                                    <span class="text-sm">47</span>
                                </button>
                                <button class="text-blue-500 hover:text-blue-600 text-sm">💬 12</button>
                            </div>
                            <button class="text-gray-500 hover:text-gray-600 text-sm">Ver mais</button>
                        </div>
                    </div>
                </div>

                <div class="bg-white rounded-xl pottery-shadow overflow-hidden">
                    <div class="h-48 bg-gradient-to-br from-pink-200 to-pink-300 flex items-center justify-center">
                        <span class="text-6xl">🥣</span>
                    </div>
                    <div class="p-4">
                        <div class="flex items-center justify-between mb-2">
                            <h3 class="font-semibold">Conjunto de Tigelas</h3>
                            <span class="bg-gray-100 text-gray-700 px-2 py-1 rounded text-xs">🥈 2º Lugar</span>
                        </div>
                        <p class="text-gray-600 text-sm mb-3">Por: Carla Santos • 2ª-feira (manhã)</p>
                        <div class="flex items-center justify-between">
                            <div class="flex items-center space-x-3">
                                <button class="vote-btn flex items-center space-x-1 text-red-500 hover:text-red-600">
                                    <span>❤️</span>
                                    <span class="text-sm">35</span>
                                </button>
                                <button class="text-blue-500 hover:text-blue-600 text-sm">💬 8</button>
                            </div>
                            <button class="text-gray-500 hover:text-gray-600 text-sm">Ver mais</button>
                        </div>
                    </div>
                </div>

                <div class="bg-white rounded-xl pottery-shadow overflow-hidden">
                    <div class="h-48 bg-gradient-to-br from-teal-200 to-teal-300 flex items-center justify-center">
                        <span class="text-6xl">🍽️</span>
                    </div>
                    <div class="p-4">
                        <h3 class="font-semibold mb-2">Prato Decorativo</h3>
                        <p class="text-gray-600 text-sm mb-3">Por: Lucia Ferreira • 4ª-feira (manhã)</p>
                        <div class="flex items-center justify-between">
                            <div class="flex items-center space-x-3">
                                <button class="vote-btn flex items-center space-x-1 text-red-500 hover:text-red-600">
                                    <span>❤️</span>
                                    <span class="text-sm">28</span>
                                </button>
                                <button class="text-blue-500 hover:text-blue-600 text-sm">💬 5</button>
                            </div>
                            <button class="text-gray-500 hover:text-gray-600 text-sm">Ver mais</button>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Student Area Section -->
        <section id="student-area" class="section-content hidden">
            <h2 class="text-3xl font-bold text-gray-800 mb-6">Área do Aluno</h2>
            
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <!-- Payments -->
                <div class="bg-white rounded-xl pottery-shadow p-6">
                    <h3 class="text-xl font-semibold mb-4 flex items-center space-x-2">
                        <span>💳</span>
                        <span>Pagamentos</span>
                    </h3>
                    <div class="space-y-4">
                        <div class="flex items-center justify-between p-3 bg-green-50 rounded-lg border-l-4 border-green-500">
                            <div>
                                <p class="font-medium">Mensalidade Março</p>
                                <p class="text-sm text-gray-600">Vencimento: 05/04/2024</p>
                            </div>
                            <span class="bg-green-100 text-green-800 px-2 py-1 rounded text-sm">Pago</span>
                        </div>
                        <div class="flex items-center justify-between p-3 bg-yellow-50 rounded-lg border-l-4 border-yellow-500">
                            <div>
                                <p class="font-medium">Mensalidade Abril</p>
                                <p class="text-sm text-gray-600">Vencimento: 05/05/2024</p>
                            </div>
                            <button class="bg-yellow-500 hover:bg-yellow-600 text-white px-3 py-1 rounded text-sm transition-colors">Pagar</button>
                        </div>
                    </div>
                </div>

                <!-- Firings -->
                <div class="bg-white rounded-xl pottery-shadow p-6">
                    <h3 class="text-xl font-semibold mb-4 flex items-center space-x-2">
                        <span>🔥</span>
                        <span>Queimas</span>
                    </h3>
                    <div class="space-y-4">
                        <div class="p-3 bg-blue-50 rounded-lg">
                            <div class="flex items-center justify-between mb-2">
                                <p class="font-medium">Queima #234</p>
                                <span class="bg-blue-100 text-blue-800 px-2 py-1 rounded text-sm">Em andamento</span>
                            </div>
                            <p class="text-sm text-gray-600 mb-3">3 peças • Previsão: 2 dias</p>
                            
                            <!-- Student View - Pieces Details -->
                            <div class="bg-white rounded border p-3">
                                <h4 class="font-medium text-sm mb-2">Suas Peças nesta Queima:</h4>
                                <div class="space-y-2 text-sm">
                                    <div class="flex justify-between items-center py-1 border-b border-gray-100">
                                        <div>
                                            <span class="font-medium">Tigela Rústica</span>
                                            <span class="text-gray-500 ml-2">15×15×8 cm</span>
                                        </div>
                                        <span class="font-medium">R$ 18,00</span>
                                    </div>
                                    <div class="flex justify-between items-center py-1 border-b border-gray-100">
                                        <div>
                                            <span class="font-medium">Prato Decorativo</span>
                                            <span class="text-gray-500 ml-2">25×25×3 cm</span>
                                        </div>
                                        <span class="font-medium">R$ 19,00</span>
                                    </div>
                                    <div class="flex justify-between items-center py-1 border-b border-gray-100">
                                        <div>
                                            <span class="font-medium">Xícara Pequena</span>
                                            <span class="text-gray-500 ml-2">8×8×7 cm</span>
                                        </div>
                                        <span class="font-medium">R$ 9,00</span>
                                    </div>
                                </div>
                                <div class="flex justify-between items-center pt-2 mt-2 border-t border-gray-200 font-semibold">
                                    <span>Total:</span>
                                    <span class="text-green-700">R$ 46,00</span>
                                </div>
                            </div>
                        </div>
                        
                        <div class="p-3 bg-green-50 rounded-lg">
                            <div class="flex items-center justify-between mb-2">
                                <p class="font-medium">Queima #233</p>
                                <span class="bg-green-100 text-green-800 px-2 py-1 rounded text-sm">Concluída</span>
                            </div>
                            <p class="text-sm text-gray-600 mb-3">2 peças • Concluída ontem</p>
                            
                            <!-- Student View - Completed Pieces -->
                            <div class="bg-white rounded border p-3">
                                <h4 class="font-medium text-sm mb-2">Peças Prontas para Retirada:</h4>
                                <div class="space-y-2 text-sm">
                                    <div class="flex justify-between items-center py-1 border-b border-gray-100">
                                        <div>
                                            <span class="font-medium">Vaso Pequeno</span>
                                            <span class="text-gray-500 ml-2">10×10×15 cm</span>
                                        </div>
                                        <span class="font-medium">R$ 15,00</span>
                                    </div>
                                    <div class="flex justify-between items-center py-1 border-b border-gray-100">
                                        <div>
                                            <span class="font-medium">Pires</span>
                                            <span class="text-gray-500 ml-2">12×12×2 cm</span>
                                        </div>
                                        <span class="font-medium">R$ 6,00</span>
                                    </div>
                                </div>
                                <div class="flex justify-between items-center pt-2 mt-2 border-t border-gray-200 font-semibold">
                                    <span>Total Pago:</span>
                                    <span class="text-green-600">R$ 21,00</span>
                                </div>
                            </div>
                        </div>
                        

                    </div>
                </div>

                <!-- Clay Purchase History -->
                <div class="bg-white rounded-xl pottery-shadow p-6">
                    <div class="flex justify-between items-center mb-4">
                        <h3 class="text-xl font-semibold flex items-center space-x-2">
                            <span>🧱</span>
                            <span>Histórico de Compra de Argila</span>
                        </h3>
                        <button id="addClayPurchaseBtn" class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg transition-colors flex items-center space-x-2">
                            <span>➕</span>
                            <span>Nova Compra</span>
                        </button>
                    </div>
                    
                    <!-- Clay Purchase List -->
                    <div id="clayPurchasesList" class="space-y-3">
                        <div class="clay-purchase-item p-4 bg-gray-50 rounded-lg border">
                            <div class="flex justify-between items-start mb-2">
                                <div class="flex-1">
                                    <h4 class="font-medium text-gray-800">Argila Vermelha - 5kg</h4>
                                    <p class="text-sm text-gray-600">Fornecedor: Cerâmica São Paulo</p>
                                    <p class="text-xs text-gray-500">Compra em: 15/03/2024</p>
                                </div>
                                <div class="text-right">
                                    <p class="font-bold text-green-700">R$ 35,00</p>
                                    <span class="bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs">Pago</span>
                                </div>
                            </div>
                        </div>
                        
                        <div class="clay-purchase-item p-4 bg-gray-50 rounded-lg border">
                            <div class="flex justify-between items-start mb-2">
                                <div class="flex-1">
                                    <h4 class="font-medium text-gray-800">Argila Branca - 3kg</h4>
                                    <p class="text-sm text-gray-600">Fornecedor: Argilas do Vale</p>
                                    <p class="text-xs text-gray-500">Compra em: 08/03/2024</p>
                                </div>
                                <div class="text-right">
                                    <p class="font-bold text-green-700">R$ 28,00</p>
                                    <span class="bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs">Pago</span>
                                </div>
                            </div>
                        </div>
                        
                        <div class="clay-purchase-item p-4 bg-gray-50 rounded-lg border">
                            <div class="flex justify-between items-start mb-2">
                                <div class="flex-1">
                                    <h4 class="font-medium text-gray-800">Argila Grês - 2kg</h4>
                                    <p class="text-sm text-gray-600">Fornecedor: Cerâmica Artesanal</p>
                                    <p class="text-xs text-gray-500">Compra em: 01/03/2024</p>
                                </div>
                                <div class="text-right">
                                    <p class="font-bold text-orange-600">R$ 42,00</p>
                                    <span class="bg-yellow-100 text-yellow-800 px-2 py-1 rounded-full text-xs">Pendente</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Total Summary -->
                    <div class="mt-4 pt-4 border-t border-gray-200">
                        <div class="flex justify-between items-center">
                            <span class="font-semibold text-gray-800">Total a Pagar:</span>
                            <span class="text-xl font-bold text-green-700">R$ 42,00</span>
                        </div>
                        <p class="text-sm text-gray-600 mt-1">1 compra pendente</p>
                    </div>
                </div>

                <!-- Class Schedule -->
                <div class="bg-white rounded-xl pottery-shadow p-6">
                    <h3 class="text-xl font-semibold mb-4 flex items-center space-x-2">
                        <span>📅</span>
                        <span>Próximas Aulas</span>
                    </h3>
                    <div class="space-y-3">
                        <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                            <div>
                                <p class="font-medium">Técnicas de Esmaltação</p>
                                <p class="text-sm text-gray-600">Amanhã, 14:00 - 16:00</p>
                            </div>
                            <span class="text-green-500">✓</span>
                        </div>
                        <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                            <div>
                                <p class="font-medium">Modelagem Avançada</p>
                                <p class="text-sm text-gray-600">Quinta, 14:00 - 16:00</p>
                            </div>
                            <span class="text-green-500">✓</span>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Shop Section -->
        <section id="shop" class="section-content hidden">
            <div class="flex justify-between items-center mb-6">
                <h2 class="text-3xl font-bold text-gray-800">Loja Online</h2>
                <button id="cartBtn" class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg transition-colors flex items-center space-x-2">
                    <span>🛒</span>
                    <span>Carrinho (<span id="cartCount">0</span>)</span>
                </button>
            </div>

            <!-- Product Categories -->
            <div class="flex space-x-4 mb-6 overflow-x-auto">
                <button class="category-btn bg-green-600 text-white px-4 py-2 rounded-lg whitespace-nowrap" data-category="all">Todos</button>
                <button class="category-btn bg-gray-200 text-gray-700 hover:bg-gray-300 px-4 py-2 rounded-lg transition-colors whitespace-nowrap" data-category="clay">Argila</button>
                <button class="category-btn bg-gray-200 text-gray-700 hover:bg-gray-300 px-4 py-2 rounded-lg transition-colors whitespace-nowrap" data-category="tools">Ferramentas</button>
                <button class="category-btn bg-gray-200 text-gray-700 hover:bg-gray-300 px-4 py-2 rounded-lg transition-colors whitespace-nowrap" data-category="kits">Kits</button>
            </div>

            <!-- Products Grid -->
            <div id="productsGrid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <!-- Sample products -->
                <div class="product-card bg-white rounded-xl pottery-shadow overflow-hidden" data-category="clay">
                    <div class="h-48 bg-gradient-to-br from-amber-200 to-amber-300 flex items-center justify-center">
                        <span class="text-6xl">🧱</span>
                    </div>
                    <div class="p-4">
                        <h3 class="font-semibold text-lg mb-2">Argila Vermelha - 5kg</h3>
                        <p class="text-gray-600 text-sm mb-3">Argila de alta qualidade para modelagem</p>
                        <div class="flex items-center justify-between">
                            <span class="text-2xl font-bold text-green-700">R$ 35</span>
                            <button class="add-to-cart bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg transition-colors" data-product="Argila Vermelha 5kg" data-price="35">
                                Adicionar
                            </button>
                        </div>
                    </div>
                </div>

                <div class="product-card bg-white rounded-xl pottery-shadow overflow-hidden" data-category="tools">
                    <div class="h-48 bg-gradient-to-br from-blue-200 to-blue-300 flex items-center justify-center">
                        <span class="text-6xl">🔧</span>
                    </div>
                    <div class="p-4">
                        <h3 class="font-semibold text-lg mb-2">Kit Ferramentas Básico</h3>
                        <p class="text-gray-600 text-sm mb-3">5 ferramentas essenciais para cerâmica</p>
                        <div class="flex items-center justify-between">
                            <span class="text-2xl font-bold text-green-700">R$ 85</span>
                            <button class="add-to-cart bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg transition-colors" data-product="Kit Ferramentas Básico" data-price="85">
                                Adicionar
                            </button>
                        </div>
                    </div>
                </div>

                <div class="product-card bg-white rounded-xl pottery-shadow overflow-hidden" data-category="kits">
                    <div class="h-48 bg-gradient-to-br from-green-200 to-green-300 flex items-center justify-center">
                        <span class="text-6xl">📦</span>
                    </div>
                    <div class="p-4">
                        <h3 class="font-semibold text-lg mb-2">Kit Iniciante Completo</h3>
                        <p class="text-gray-600 text-sm mb-3">Argila + ferramentas + manual</p>
                        <div class="flex items-center justify-between">
                            <span class="text-2xl font-bold text-green-700">R$ 120</span>
                            <button class="add-to-cart bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg transition-colors" data-product="Kit Iniciante Completo" data-price="120">
                                Adicionar
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Financial Section -->
        <section id="financial" class="section-content hidden">
            <h2 class="text-3xl font-bold text-gray-800 mb-6">Controle Financeiro</h2>
            
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
                <!-- Balance Cards -->
                <div class="bg-white rounded-xl pottery-shadow p-6">
                    <div class="flex items-center justify-between mb-4">
                        <h3 class="text-lg font-semibold text-gray-800">Saldo Atual</h3>
                        <span class="text-2xl">💰</span>
                    </div>
                    <div class="text-3xl font-bold text-green-600">R$ 245,50</div>
                    <p class="text-sm text-gray-600 mt-2">Créditos disponíveis</p>
                </div>

                <div class="bg-white rounded-xl pottery-shadow p-6">
                    <div class="flex items-center justify-between mb-4">
                        <h3 class="text-lg font-semibold text-gray-800">Este Mês</h3>
                        <span class="text-2xl">📊</span>
                    </div>
                    <div class="text-3xl font-bold text-blue-600">R$ 180,00</div>
                    <p class="text-sm text-gray-600 mt-2">Total gasto</p>
                </div>

                <div class="bg-white rounded-xl pottery-shadow p-6">
                    <div class="flex items-center justify-between mb-4">
                        <h3 class="text-lg font-semibold text-gray-800">Próximo Vencimento</h3>
                        <span class="text-2xl">⏰</span>
                    </div>
                    <div class="text-3xl font-bold text-green-700">R$ 150,00</div>
                    <p class="text-sm text-gray-600 mt-2">Mensalidade - 05/05</p>
                </div>
            </div>

            <!-- Financial Chart -->
            <div class="bg-white rounded-xl pottery-shadow p-6 mb-6">
                <h3 class="text-xl font-semibold mb-4">Gastos dos Últimos 6 Meses</h3>
                <div class="h-64 flex items-end justify-between space-x-2">
                    <div class="flex flex-col items-center">
                        <div class="w-12 bg-blue-500 rounded-t" style="height: 120px;"></div>
                        <span class="text-xs mt-2">Nov</span>
                    </div>
                    <div class="flex flex-col items-center">
                        <div class="w-12 bg-blue-500 rounded-t" style="height: 150px;"></div>
                        <span class="text-xs mt-2">Dez</span>
                    </div>
                    <div class="flex flex-col items-center">
                        <div class="w-12 bg-blue-500 rounded-t" style="height: 100px;"></div>
                        <span class="text-xs mt-2">Jan</span>
                    </div>
                    <div class="flex flex-col items-center">
                        <div class="w-12 bg-blue-500 rounded-t" style="height: 180px;"></div>
                        <span class="text-xs mt-2">Fev</span>
                    </div>
                    <div class="flex flex-col items-center">
                        <div class="w-12 bg-blue-500 rounded-t" style="height: 160px;"></div>
                        <span class="text-xs mt-2">Mar</span>
                    </div>
                    <div class="flex flex-col items-center">
                        <div class="w-12 bg-orange-500 rounded-t" style="height: 140px;"></div>
                        <span class="text-xs mt-2">Abr</span>
                    </div>
                </div>
            </div>

            <!-- Transaction History -->
            <div class="bg-white rounded-xl pottery-shadow p-6">
                <h3 class="text-xl font-semibold mb-4">Histórico de Transações</h3>
                <div class="space-y-4">
                    <div class="flex items-center justify-between p-3 border-b">
                        <div class="flex items-center space-x-3">
                            <span class="text-2xl">💳</span>
                            <div>
                                <p class="font-medium">Mensalidade Março</p>
                                <p class="text-sm text-gray-600">15/03/2024</p>
                            </div>
                        </div>
                        <span class="text-red-600 font-semibold">-R$ 150,00</span>
                    </div>
                    <div class="flex items-center justify-between p-3 border-b">
                        <div class="flex items-center space-x-3">
                            <span class="text-2xl">🔥</span>
                            <div>
                                <p class="font-medium">Queima - 3 peças</p>
                                <p class="text-sm text-gray-600">12/03/2024</p>
                            </div>
                        </div>
                        <span class="text-red-600 font-semibold">-R$ 30,00</span>
                    </div>
                    <div class="flex items-center justify-between p-3 border-b">
                        <div class="flex items-center space-x-3">
                            <span class="text-2xl">🧱</span>
                            <div>
                                <p class="font-medium">Argila - 5kg</p>
                                <p class="text-sm text-gray-600">08/03/2024</p>
                            </div>
                        </div>
                        <span class="text-red-600 font-semibold">-R$ 35,00</span>
                    </div>
                </div>
            </div>
        </section>

        <!-- Chat Section -->
        <section id="chat" class="section-content hidden">
            <div class="bg-white rounded-xl pottery-shadow h-96 flex flex-col">
                <div class="p-4 border-b">
                    <h2 class="text-xl font-semibold flex items-center space-x-2">
                        <span>💬</span>
                        <span>Chat da Turma 5ª-feira (tarde)</span>
                        <span class="bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs">12 online</span>
                    </h2>
                </div>
                
                <div id="chatMessages" class="flex-1 p-4 overflow-y-auto space-y-4">
                    <div class="flex items-start space-x-3">
                        <div class="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center text-white text-sm">A</div>
                        <div class="flex-1">
                            <div class="flex items-center space-x-2 mb-1">
                                <span class="font-medium text-sm">Ana Costa</span>
                                <span class="text-xs text-gray-500">10:30</span>
                            </div>
                            <div class="bg-gray-100 rounded-lg p-3">
                                <p class="text-sm">Pessoal, alguém sabe qual a temperatura ideal para queima de grês?</p>
                            </div>
                        </div>
                    </div>

                    <div class="flex items-start space-x-3">
                        <div class="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center text-white text-sm">C</div>
                        <div class="flex-1">
                            <div class="flex items-center space-x-2 mb-1">
                                <span class="font-medium text-sm">Carla Santos</span>
                                <span class="text-xs text-gray-500">10:32</span>
                            </div>
                            <div class="bg-gray-100 rounded-lg p-3">
                                <p class="text-sm">Oi Ana! Geralmente entre 1200°C e 1300°C. Depende do tipo de grês 😊</p>
                            </div>
                        </div>
                    </div>

                    <div class="flex items-start space-x-3 flex-row-reverse">
                        <div class="w-8 h-8 bg-orange-500 rounded-full flex items-center justify-center text-white text-sm">M</div>
                        <div class="flex-1">
                            <div class="flex items-center space-x-2 mb-1 justify-end">
                                <span class="text-xs text-gray-500">10:35</span>
                                <span class="font-medium text-sm">Você</span>
                            </div>
                            <div class="bg-orange-500 text-white rounded-lg p-3">
                                <p class="text-sm">Obrigada, Carla! Vou testar na próxima queima 🏺</p>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="p-4 border-t">
                    <div class="flex space-x-2">
                        <input type="text" id="chatInput" placeholder="Digite sua mensagem..." class="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500">
                        <button id="sendMessage" class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg transition-colors">
                            Enviar
                        </button>
                    </div>
                </div>
            </div>
        </section>

        <!-- Admin Section -->
        <section id="admin" class="section-content hidden">
            <div class="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
                <div class="flex items-center space-x-2">
                    <span class="text-red-600">⚠️</span>
                    <span class="text-red-800 font-medium">Área Administrativa - Acesso Restrito</span>
                </div>
            </div>

            <h2 class="text-3xl font-bold text-gray-800 mb-6">Painel Administrativo</h2>
            
            <!-- Admin Stats -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                <div class="bg-white rounded-xl pottery-shadow p-6">
                    <div class="flex items-center justify-between mb-4">
                        <h3 class="text-lg font-semibold text-gray-800">Total de Alunas</h3>
                        <span class="text-2xl">👩‍🎨</span>
                    </div>
                    <div class="text-3xl font-bold text-blue-600">47</div>
                    <p class="text-sm text-gray-600 mt-2">+3 este mês</p>
                </div>

                <div class="bg-white rounded-xl pottery-shadow p-6">
                    <div class="flex items-center justify-between mb-4">
                        <h3 class="text-lg font-semibold text-gray-800">Receita Mensal</h3>
                        <span class="text-2xl">💰</span>
                    </div>
                    <div class="text-3xl font-bold text-green-600">R$ 7.050</div>
                    <p class="text-sm text-gray-600 mt-2">+12% vs mês anterior</p>
                </div>

                <div class="bg-white rounded-xl pottery-shadow p-6">
                    <div class="flex items-center justify-between mb-4">
                        <h3 class="text-lg font-semibold text-gray-800">Queimas Pendentes</h3>
                        <span class="text-2xl">🔥</span>
                    </div>
                    <div class="text-3xl font-bold text-orange-600">8</div>
                    <p class="text-sm text-gray-600 mt-2">23 peças aguardando</p>
                </div>

                <div class="bg-white rounded-xl pottery-shadow p-6">
                    <div class="flex items-center justify-between mb-4">
                        <h3 class="text-lg font-semibold text-gray-800">Pedidos Loja</h3>
                        <span class="text-2xl">📦</span>
                    </div>
                    <div class="text-3xl font-bold text-purple-600">12</div>
                    <p class="text-sm text-gray-600 mt-2">5 para entregar</p>
                </div>
            </div>

            <!-- Admin Tabs -->
            <div class="flex space-x-4 mb-6 overflow-x-auto">
                <button class="admin-tab-btn bg-red-500 text-white px-4 py-2 rounded-lg whitespace-nowrap" data-tab="students">👩‍🎨 Gestaõ de Alunas</button>
                <button class="admin-tab-btn bg-gray-200 text-gray-700 hover:bg-gray-300 px-4 py-2 rounded-lg transition-colors whitespace-nowrap" data-tab="firings">🔥 Controle de Queimas</button>
                <button class="admin-tab-btn bg-gray-200 text-gray-700 hover:bg-gray-300 px-4 py-2 rounded-lg transition-colors whitespace-nowrap" data-tab="payments">💳 Pagamentos</button>
                <button class="admin-tab-btn bg-gray-200 text-gray-700 hover:bg-gray-300 px-4 py-2 rounded-lg transition-colors whitespace-nowrap" data-tab="reports">📊 Relatórios</button>
                <button class="admin-tab-btn bg-gray-200 text-gray-700 hover:bg-gray-300 px-4 py-2 rounded-lg transition-colors whitespace-nowrap" data-tab="history">📋 Histórico</button>
                <button class="admin-tab-btn bg-gray-200 text-gray-700 hover:bg-gray-300 px-4 py-2 rounded-lg transition-colors whitespace-nowrap" data-tab="settings">⚙️ Configurações</button>
            </div>

            <!-- Students Management Tab -->
            <div id="admin-students" class="admin-tab-content">
                <div class="bg-white rounded-xl pottery-shadow p-6">
                    <div class="flex justify-between items-center mb-6">
                        <h3 class="text-xl font-semibold">Gestaõ de Alunas</h3>
                        <button id="addStudentBtn" class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg transition-colors">
                            ➕ Nova Aluna
                        </button>
                    </div>

                    <!-- Search and Filter -->
                    <div class="flex space-x-4 mb-6">
                        <input type="text" placeholder="Buscar aluna..." class="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500">
                        <select class="px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500">
                            <option value="">Todas as turmas</option>
                            <option value="2feira-manha">2ª-feira (manhã)</option>
                            <option value="2feira-tarde">2ª-feira (tarde)</option>
                            <option value="2feira-noite">2ª-feira (noite)</option>
                            <option value="3feira-manha">3ª-feira (manhã)</option>
                            <option value="3feira-tarde">3ª-feira (tarde)</option>
                            <option value="3feira-noite">3ª-feira (noite)</option>
                            <option value="4feira-manha">4ª-feira (manhã)</option>
                            <option value="4feira-tarde">4ª-feira (tarde)</option>
                            <option value="4feira-noite">4ª-feira (noite)</option>
                            <option value="5feira-manha">5ª-feira (manhã)</option>
                            <option value="5feira-tarde">5ª-feira (tarde)</option>
                            <option value="5feira-noite">5ª-feira (noite)</option>
                            <option value="6feira-manha">6ª-feira (manhã)</option>
                            <option value="6feira-tarde">6ª-feira (tarde)</option>
                            <option value="6feira-noite">6ª-feira (noite)</option>
                        </select>
                    </div>

                    <!-- Students Table -->
                    <div class="overflow-x-auto">
                        <table class="w-full">
                            <thead class="bg-gray-50">
                                <tr>
                                    <th class="px-4 py-3 text-left text-sm font-medium text-gray-700">Foto</th>
                                    <th class="px-4 py-3 text-left text-sm font-medium text-gray-700">Nome</th>
                                    <th class="px-4 py-3 text-left text-sm font-medium text-gray-700">Idade</th>
                                    <th class="px-4 py-3 text-left text-sm font-medium text-gray-700">Turma</th>
                                    <th class="px-4 py-3 text-left text-sm font-medium text-gray-700">Status</th>
                                    <th class="px-4 py-3 text-left text-sm font-medium text-gray-700">Ações</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-gray-200">
                                <tr>
                                    <td class="px-4 py-3">
                                        <div class="relative group">
                                            <div class="w-12 h-12 bg-gray-100 rounded-full flex items-center justify-center overflow-hidden">
                                                <img class="student-photo w-full h-full object-cover hidden" alt="Foto de Maria Silva" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
                                                <span class="text-gray-400 text-xs">👩‍🎨</span>
                                            </div>
                                            <input type="file" accept="image/*" class="student-photo-upload absolute inset-0 w-full h-full opacity-0 cursor-pointer" data-student="maria-silva">
                                            <div class="absolute inset-0 bg-black bg-opacity-50 rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity cursor-pointer">
                                                <span class="text-white text-xs">📷</span>
                                            </div>
                                        </div>
                                    </td>
                                    <td class="px-4 py-3">Maria Silva</td>
                                    <td class="px-4 py-3">34</td>
                                    <td class="px-4 py-3"><span class="bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs">5ª-feira (tarde)</span></td>
                                    <td class="px-4 py-3"><span class="bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs">Ativo</span></td>
                                    <td class="px-4 py-3">
                                        <button class="text-blue-600 hover:text-blue-800 mr-2">✏️</button>
                                        <button class="text-green-600 hover:text-green-800 mr-2">📊</button>
                                        <button class="text-red-600 hover:text-red-800">🗑️</button>
                                    </td>
                                </tr>
                                <tr>
                                    <td class="px-4 py-3">
                                        <div class="relative group">
                                            <div class="w-12 h-12 bg-gray-100 rounded-full flex items-center justify-center overflow-hidden">
                                                <img class="student-photo w-full h-full object-cover hidden" alt="Foto de Ana Costa" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
                                                <span class="text-gray-400 text-xs">👩‍🎨</span>
                                            </div>
                                            <input type="file" accept="image/*" class="student-photo-upload absolute inset-0 w-full h-full opacity-0 cursor-pointer" data-student="ana-costa">
                                            <div class="absolute inset-0 bg-black bg-opacity-50 rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity cursor-pointer">
                                                <span class="text-white text-xs">📷</span>
                                            </div>
                                        </div>
                                    </td>
                                    <td class="px-4 py-3">Ana Costa</td>
                                    <td class="px-4 py-3">28</td>
                                    <td class="px-4 py-3"><span class="bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs">3ª-feira (noite)</span></td>
                                    <td class="px-4 py-3"><span class="bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs">Ativo</span></td>
                                    <td class="px-4 py-3">
                                        <button class="text-blue-600 hover:text-blue-800 mr-2">✏️</button>
                                        <button class="text-green-600 hover:text-green-800 mr-2">📊</button>
                                        <button class="text-red-600 hover:text-red-800">🗑️</button>
                                    </td>
                                </tr>
                                <tr>
                                    <td class="px-4 py-3">
                                        <div class="relative group">
                                            <div class="w-12 h-12 bg-gray-100 rounded-full flex items-center justify-center overflow-hidden">
                                                <img class="student-photo w-full h-full object-cover hidden" alt="Foto de Carla Santos" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
                                                <span class="text-gray-400 text-xs">👩‍🎨</span>
                                            </div>
                                            <input type="file" accept="image/*" class="student-photo-upload absolute inset-0 w-full h-full opacity-0 cursor-pointer" data-student="carla-santos">
                                            <div class="absolute inset-0 bg-black bg-opacity-50 rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity cursor-pointer">
                                                <span class="text-white text-xs">📷</span>
                                            </div>
                                        </div>
                                    </td>
                                    <td class="px-4 py-3">Carla Santos</td>
                                    <td class="px-4 py-3">67</td>
                                    <td class="px-4 py-3"><span class="bg-purple-100 text-purple-800 px-2 py-1 rounded-full text-xs">2ª-feira (manhã)</span></td>
                                    <td class="px-4 py-3"><span class="bg-yellow-100 text-yellow-800 px-2 py-1 rounded-full text-xs">Pendente</span></td>
                                    <td class="px-4 py-3">
                                        <button class="text-blue-600 hover:text-blue-800 mr-2">✏️</button>
                                        <button class="text-green-600 hover:text-green-800 mr-2">📊</button>
                                        <button class="text-red-600 hover:text-red-800">🗑️</button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- Firings Management Tab -->
            <div id="admin-firings" class="admin-tab-content hidden">
                <div class="bg-white rounded-xl pottery-shadow p-6">
                    <div class="flex justify-between items-center mb-6">
                        <h3 class="text-xl font-semibold">Controle de Queimas</h3>
                        <div class="flex space-x-3">
                            <div class="flex items-center space-x-2">
                                <label class="text-sm font-medium">Multiplicador:</label>
                                <input type="number" id="firingMultiplier" value="1.0" step="0.1" min="0.1" max="2.0" class="w-16 px-2 py-1 border rounded focus:outline-none focus:ring-2 focus:ring-orange-500 text-sm">
                            </div>
                            <button id="newFiringBtn" class="bg-orange-500 hover:bg-orange-600 text-white px-4 py-2 rounded-lg transition-colors">
                                🔥 Nova Queima
                            </button>
                        </div>
                    </div>

                    <!-- Firing Status Cards -->
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                        <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                            <h4 class="font-semibold text-yellow-800 mb-2">Aguardando</h4>
                            <p class="text-2xl font-bold text-yellow-600">23 peças</p>
                            <p class="text-sm text-yellow-700">8 alunas</p>
                        </div>
                        <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
                            <h4 class="font-semibold text-blue-800 mb-2">Em Andamento</h4>
                            <p class="text-2xl font-bold text-blue-600">15 peças</p>
                            <p class="text-sm text-blue-700">Queima #234</p>
                        </div>
                        <div class="bg-green-50 border border-green-200 rounded-lg p-4">
                            <h4 class="font-semibold text-green-800 mb-2">Concluídas Hoje</h4>
                            <p class="text-2xl font-bold text-green-600">12 peças</p>
                            <p class="text-sm text-green-700">5 alunas</p>
                        </div>
                    </div>

                    <!-- Firings List -->
                    <div class="space-y-4">
                        <div class="border rounded-lg p-4">
                            <div class="flex justify-between items-center mb-3">
                                <h4 class="font-semibold">Queima #234</h4>
                                <span class="bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-sm">Em Andamento</span>
                            </div>
                            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm mb-4">
                                <div>
                                    <p class="text-gray-600">Peças: <span class="font-medium">15</span></p>
                                    <p class="text-gray-600">Alunas: <span class="font-medium">6</span></p>
                                </div>
                                <div>
                                    <p class="text-gray-600">Iniciada: <span class="font-medium">Hoje, 09:00</span></p>
                                    <p class="text-gray-600">Previsão: <span class="font-medium">Amanhã, 15:00</span></p>
                                </div>
                                <div class="flex space-x-2">
                                    <button class="bg-green-500 hover:bg-green-600 text-white px-3 py-1 rounded text-sm transition-colors">Finalizar</button>
                                    <button class="firing-details-btn bg-gray-500 hover:bg-gray-600 text-white px-3 py-1 rounded text-sm transition-colors" data-firing="234">Detalhes</button>
                                </div>
                            </div>
                            
                            <!-- Detailed Pieces List (Admin View) -->
                            <div class="firing-pieces-admin hidden bg-gray-50 rounded-lg p-4 mt-4">
                                <h5 class="font-semibold mb-3">Peças na Queima #234</h5>
                                <div class="overflow-x-auto">
                                    <table class="w-full text-sm">
                                        <thead class="bg-gray-100">
                                            <tr>
                                                <th class="px-3 py-2 text-left">Aluna</th>
                                                <th class="px-3 py-2 text-left">Peça</th>
                                                <th class="px-3 py-2 text-left">Medidas (C×L×A)</th>
                                                <th class="px-3 py-2 text-left">Volume</th>
                                                <th class="px-3 py-2 text-left">Multiplicador</th>
                                                <th class="px-3 py-2 text-left">Valor Final</th>
                                            </tr>
                                        </thead>
                                        <tbody class="divide-y divide-gray-200">
                                            <tr>
                                                <td class="px-3 py-2">Maria Silva</td>
                                                <td class="px-3 py-2">Tigela Rústica</td>
                                                <td class="px-3 py-2">15×15×8 cm</td>
                                                <td class="px-3 py-2">1.800 cm³</td>
                                                <td class="px-3 py-2">1.0</td>
                                                <td class="px-3 py-2">R$ 18,00</td>
                                            </tr>
                                            <tr>
                                                <td class="px-3 py-2">Maria Silva</td>
                                                <td class="px-3 py-2">Prato Decorativo</td>
                                                <td class="px-3 py-2">25×25×3 cm</td>
                                                <td class="px-3 py-2">1.875 cm³</td>
                                                <td class="px-3 py-2">1.0</td>
                                                <td class="px-3 py-2">R$ 19,00</td>
                                            </tr>
                                            <tr>
                                                <td class="px-3 py-2">Ana Costa</td>
                                                <td class="px-3 py-2">Vaso Contemporâneo</td>
                                                <td class="px-3 py-2">12×12×20 cm</td>
                                                <td class="px-3 py-2">2.880 cm³</td>
                                                <td class="px-3 py-2">1.0</td>
                                                <td class="px-3 py-2">R$ 29,00</td>
                                            </tr>
                                            <tr>
                                                <td class="px-3 py-2">Carla Santos</td>
                                                <td class="px-3 py-2">Conjunto Tigelas (3x)</td>
                                                <td class="px-3 py-2">10×10×6 cm cada</td>
                                                <td class="px-3 py-2">1.800 cm³ total</td>
                                                <td class="px-3 py-2">1.0</td>
                                                <td class="px-3 py-2">R$ 18,00</td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                                <div class="mt-3 text-right">
                                    <p class="font-semibold">Total da Queima: R$ 84,00</p>
                                </div>
                            </div>
                        </div>

                        <div class="border rounded-lg p-4">
                            <div class="flex justify-between items-center mb-3">
                                <h4 class="font-semibold">Queima #235 - Agendada</h4>
                                <span class="bg-yellow-100 text-yellow-800 px-2 py-1 rounded-full text-sm">Aguardando</span>
                            </div>
                            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm mb-4">
                                <div>
                                    <p class="text-gray-600">Peças: <span class="font-medium">23</span></p>
                                    <p class="text-gray-600">Alunas: <span class="font-medium">8</span></p>
                                </div>
                                <div>
                                    <p class="text-gray-600">Agendada: <span class="font-medium">Sexta, 09:00</span></p>
                                    <p class="text-gray-600">Duração: <span class="font-medium">30 horas</span></p>
                                </div>
                                <div class="flex space-x-2">
                                    <button class="bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded text-sm transition-colors">Iniciar</button>
                                    <button class="firing-details-btn bg-gray-500 hover:bg-gray-600 text-white px-3 py-1 rounded text-sm transition-colors" data-firing="235">Detalhes</button>
                                </div>
                            </div>
                            
                            <!-- Detailed Pieces List (Admin View) -->
                            <div class="firing-pieces-admin hidden bg-gray-50 rounded-lg p-4 mt-4">
                                <h5 class="font-semibold mb-3">Peças Agendadas - Queima #235</h5>
                                <div class="overflow-x-auto">
                                    <table class="w-full text-sm">
                                        <thead class="bg-gray-100">
                                            <tr>
                                                <th class="px-3 py-2 text-left">Aluna</th>
                                                <th class="px-3 py-2 text-left">Peça</th>
                                                <th class="px-3 py-2 text-left">Medidas (C×L×A)</th>
                                                <th class="px-3 py-2 text-left">Volume</th>
                                                <th class="px-3 py-2 text-left">Multiplicador</th>
                                                <th class="px-3 py-2 text-left">Valor Final</th>
                                            </tr>
                                        </thead>
                                        <tbody class="divide-y divide-gray-200">
                                            <tr>
                                                <td class="px-3 py-2">Lucia Ferreira</td>
                                                <td class="px-3 py-2">Escultura Abstrata</td>
                                                <td class="px-3 py-2">18×15×25 cm</td>
                                                <td class="px-3 py-2">6.750 cm³</td>
                                                <td class="px-3 py-2">0.8</td>
                                                <td class="px-3 py-2">R$ 54,00</td>
                                            </tr>
                                            <tr>
                                                <td class="px-3 py-2">Fernanda Lima</td>
                                                <td class="px-3 py-2">Jogo de Xícaras (6x)</td>
                                                <td class="px-3 py-2">8×8×7 cm cada</td>
                                                <td class="px-3 py-2">2.688 cm³ total</td>
                                                <td class="px-3 py-2">1.0</td>
                                                <td class="px-3 py-2">R$ 27,00</td>
                                            </tr>
                                            <tr>
                                                <td class="px-3 py-2">Patricia Souza</td>
                                                <td class="px-3 py-2">Vaso Grande</td>
                                                <td class="px-3 py-2">20×20×30 cm</td>
                                                <td class="px-3 py-2">12.000 cm³</td>
                                                <td class="px-3 py-2">0.8</td>
                                                <td class="px-3 py-2">R$ 96,00</td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                                <div class="mt-3 text-right">
                                    <p class="font-semibold">Total Previsto: R$ 177,00</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Payments Management Tab -->
            <div id="admin-payments" class="admin-tab-content hidden">
                <div class="bg-white rounded-xl pottery-shadow p-6">
                    <h3 class="text-xl font-semibold mb-6">Controle de Pagamentos</h3>

                    <!-- Payment Summary -->
                    <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                        <div class="bg-green-50 border border-green-200 rounded-lg p-4 text-center">
                            <p class="text-green-600 font-semibold">Recebido</p>
                            <p class="text-2xl font-bold text-green-700">R$ 6.450</p>
                        </div>
                        <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-4 text-center">
                            <p class="text-yellow-600 font-semibold">Pendente</p>
                            <p class="text-2xl font-bold text-yellow-700">R$ 600</p>
                        </div>
                        <div class="bg-red-50 border border-red-200 rounded-lg p-4 text-center">
                            <p class="text-red-600 font-semibold">Atrasado</p>
                            <p class="text-2xl font-bold text-red-700">R$ 300</p>
                        </div>
                        <div class="bg-blue-50 border border-blue-200 rounded-lg p-4 text-center">
                            <p class="text-blue-600 font-semibold">Total Mês</p>
                            <p class="text-2xl font-bold text-blue-700">R$ 7.350</p>
                        </div>
                    </div>

                    <!-- Payments Table -->
                    <div class="overflow-x-auto">
                        <table class="w-full">
                            <thead class="bg-gray-50">
                                <tr>
                                    <th class="px-4 py-3 text-left text-sm font-medium text-gray-700">Aluna</th>
                                    <th class="px-4 py-3 text-left text-sm font-medium text-gray-700">Tipo</th>
                                    <th class="px-4 py-3 text-left text-sm font-medium text-gray-700">Valor</th>
                                    <th class="px-4 py-3 text-left text-sm font-medium text-gray-700">Vencimento</th>
                                    <th class="px-4 py-3 text-left text-sm font-medium text-gray-700">Status</th>
                                    <th class="px-4 py-3 text-left text-sm font-medium text-gray-700">Ações</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-gray-200">
                                <tr>
                                    <td class="px-4 py-3">Maria Silva</td>
                                    <td class="px-4 py-3">Mensalidade</td>
                                    <td class="px-4 py-3">R$ 150,00</td>
                                    <td class="px-4 py-3">05/05/2024</td>
                                    <td class="px-4 py-3"><span class="bg-yellow-100 text-yellow-800 px-2 py-1 rounded-full text-xs">Pendente</span></td>
                                    <td class="px-4 py-3">
                                        <button class="text-green-600 hover:text-green-800 mr-2">✅</button>
                                        <button class="text-blue-600 hover:text-blue-800">📧</button>
                                    </td>
                                </tr>
                                <tr>
                                    <td class="px-4 py-3">Ana Costa</td>
                                    <td class="px-4 py-3">Queima</td>
                                    <td class="px-4 py-3">R$ 30,00</td>
                                    <td class="px-4 py-3">01/04/2024</td>
                                    <td class="px-4 py-3"><span class="bg-red-100 text-red-800 px-2 py-1 rounded-full text-xs">Atrasado</span></td>
                                    <td class="px-4 py-3">
                                        <button class="text-green-600 hover:text-green-800 mr-2">✅</button>
                                        <button class="text-blue-600 hover:text-blue-800">📧</button>
                                    </td>
                                </tr>
                                <tr>
                                    <td class="px-4 py-3">Carla Santos</td>
                                    <td class="px-4 py-3">Mensalidade</td>
                                    <td class="px-4 py-3">R$ 150,00</td>
                                    <td class="px-4 py-3">05/04/2024</td>
                                    <td class="px-4 py-3"><span class="bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs">Pago</span></td>
                                    <td class="px-4 py-3">
                                        <button class="text-gray-400">✅</button>
                                        <button class="text-blue-600 hover:text-blue-800 ml-2">📄</button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- Reports Tab -->
            <div id="admin-reports" class="admin-tab-content hidden">
                <div class="space-y-6">
                    <!-- Report Filters -->
                    <div class="bg-white rounded-xl pottery-shadow p-6">
                        <div class="flex justify-between items-center mb-4">
                            <h3 class="text-xl font-semibold">Relatórios e Análises</h3>
                            <div class="flex space-x-3">
                                <select id="reportPeriod" class="px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500">
                                    <option value="month">Este Mês</option>
                                    <option value="quarter">Último Trimestre</option>
                                    <option value="semester">Último Semestre</option>
                                    <option value="year">Este Ano</option>
                                    <option value="custom">Período Personalizado</option>
                                </select>
                                <button class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg transition-colors">
                                    📊 Gerar Relatório
                                </button>
                            </div>
                        </div>
                    </div>

                    <!-- Financial Report -->
                    <div class="bg-white rounded-xl pottery-shadow p-6">
                        <div class="flex justify-between items-center mb-4">
                            <h4 class="text-lg font-semibold flex items-center space-x-2">
                                <span>💰</span>
                                <span>Relatório Financeiro - Abril 2024</span>
                            </h4>
                            <button class="bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded text-sm transition-colors">
                                📥 Exportar PDF
                            </button>
                        </div>

                        <!-- Financial Summary -->
                        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                            <div class="bg-green-50 border border-green-200 rounded-lg p-4 text-center">
                                <p class="text-green-600 font-semibold">Receita Total</p>
                                <p class="text-2xl font-bold text-green-700">R$ 7.350</p>
                                <p class="text-xs text-green-600">+12% vs mês anterior</p>
                            </div>
                            <div class="bg-blue-50 border border-blue-200 rounded-lg p-4 text-center">
                                <p class="text-blue-600 font-semibold">Mensalidades</p>
                                <p class="text-2xl font-bold text-blue-700">R$ 6.580</p>
                                <p class="text-xs text-blue-600">47 alunas ativas</p>
                            </div>
                            <div class="bg-orange-50 border border-orange-200 rounded-lg p-4 text-center">
                                <p class="text-orange-600 font-semibold">Queimas</p>
                                <p class="text-2xl font-bold text-orange-700">R$ 450</p>
                                <p class="text-xs text-orange-600">45 peças queimadas</p>
                            </div>
                            <div class="bg-purple-50 border border-purple-200 rounded-lg p-4 text-center">
                                <p class="text-purple-600 font-semibold">Loja</p>
                                <p class="text-2xl font-bold text-purple-700">R$ 320</p>
                                <p class="text-xs text-purple-600">18 itens vendidos</p>
                            </div>
                        </div>

                        <!-- Payment Status -->
                        <div class="mb-6">
                            <h5 class="font-semibold mb-3">Status dos Pagamentos</h5>
                            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                                <div class="bg-gray-50 rounded-lg p-4">
                                    <div class="flex justify-between items-center mb-2">
                                        <span class="text-sm font-medium">Pagos</span>
                                        <span class="bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs">89%</span>
                                    </div>
                                    <p class="text-lg font-bold">42 alunas</p>
                                    <p class="text-sm text-gray-600">R$ 6.450,00</p>
                                </div>
                                <div class="bg-gray-50 rounded-lg p-4">
                                    <div class="flex justify-between items-center mb-2">
                                        <span class="text-sm font-medium">Pendentes</span>
                                        <span class="bg-yellow-100 text-yellow-800 px-2 py-1 rounded-full text-xs">8%</span>
                                    </div>
                                    <p class="text-lg font-bold">4 alunas</p>
                                    <p class="text-sm text-gray-600">R$ 600,00</p>
                                </div>
                                <div class="bg-gray-50 rounded-lg p-4">
                                    <div class="flex justify-between items-center mb-2">
                                        <span class="text-sm font-medium">Atrasados</span>
                                        <span class="bg-red-100 text-red-800 px-2 py-1 rounded-full text-xs">3%</span>
                                    </div>
                                    <p class="text-lg font-bold">1 aluna</p>
                                    <p class="text-sm text-gray-600">R$ 150,00</p>
                                </div>
                            </div>
                        </div>

                        <!-- Revenue Chart -->
                        <div class="bg-gray-50 rounded-lg p-4">
                            <h5 class="font-semibold mb-3">Receita dos Últimos 6 Meses</h5>
                            <div class="h-48 flex items-end justify-between space-x-2">
                                <div class="flex flex-col items-center">
                                    <div class="w-12 bg-blue-500 rounded-t" style="height: 80px;"></div>
                                    <span class="text-xs mt-1">Nov</span>
                                    <span class="text-xs text-gray-600">R$ 6.2k</span>
                                </div>
                                <div class="flex flex-col items-center">
                                    <div class="w-12 bg-blue-500 rounded-t" style="height: 100px;"></div>
                                    <span class="text-xs mt-1">Dez</span>
                                    <span class="text-xs text-gray-600">R$ 7.8k</span>
                                </div>
                                <div class="flex flex-col items-center">
                                    <div class="w-12 bg-blue-500 rounded-t" style="height: 60px;"></div>
                                    <span class="text-xs mt-1">Jan</span>
                                    <span class="text-xs text-gray-600">R$ 5.2k</span>
                                </div>
                                <div class="flex flex-col items-center">
                                    <div class="w-12 bg-blue-500 rounded-t" style="height: 120px;"></div>
                                    <span class="text-xs mt-1">Fev</span>
                                    <span class="text-xs text-gray-600">R$ 9.3k</span>
                                </div>
                                <div class="flex flex-col items-center">
                                    <div class="w-12 bg-blue-500 rounded-t" style="height: 110px;"></div>
                                    <span class="text-xs mt-1">Mar</span>
                                    <span class="text-xs text-gray-600">R$ 8.1k</span>
                                </div>
                                <div class="flex flex-col items-center">
                                    <div class="w-12 bg-green-500 rounded-t" style="height: 95px;"></div>
                                    <span class="text-xs mt-1">Abr</span>
                                    <span class="text-xs text-gray-600">R$ 7.4k</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Firing Report -->
                    <div class="bg-white rounded-xl pottery-shadow p-6">
                        <div class="flex justify-between items-center mb-4">
                            <h4 class="text-lg font-semibold flex items-center space-x-2">
                                <span>🔥</span>
                                <span>Relatório de Queimas - Abril 2024</span>
                            </h4>
                            <button class="bg-orange-500 hover:bg-orange-600 text-white px-3 py-1 rounded text-sm transition-colors">
                                📥 Exportar PDF
                            </button>
                        </div>

                        <!-- Firing Stats -->
                        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                            <div class="bg-orange-50 border border-orange-200 rounded-lg p-4 text-center">
                                <p class="text-orange-600 font-semibold">Total de Queimas</p>
                                <p class="text-2xl font-bold text-orange-700">8</p>
                                <p class="text-xs text-orange-600">+2 vs mês anterior</p>
                            </div>
                            <div class="bg-blue-50 border border-blue-200 rounded-lg p-4 text-center">
                                <p class="text-blue-600 font-semibold">Peças Queimadas</p>
                                <p class="text-2xl font-bold text-blue-700">156</p>
                                <p class="text-xs text-blue-600">Média: 19.5 por queima</p>
                            </div>
                            <div class="bg-green-50 border border-green-200 rounded-lg p-4 text-center">
                                <p class="text-green-600 font-semibold">Taxa de Sucesso</p>
                                <p class="text-2xl font-bold text-green-700">94%</p>
                                <p class="text-xs text-green-600">9 peças com defeito</p>
                            </div>
                            <div class="bg-purple-50 border border-purple-200 rounded-lg p-4 text-center">
                                <p class="text-purple-600 font-semibold">Receita Queimas</p>
                                <p class="text-2xl font-bold text-purple-700">R$ 1.560</p>
                                <p class="text-xs text-purple-600">R$ 10 por peça</p>
                            </div>
                        </div>

                        <!-- Firing Details -->
                        <div class="overflow-x-auto">
                            <table class="w-full text-sm">
                                <thead class="bg-gray-50">
                                    <tr>
                                        <th class="px-3 py-2 text-left font-medium text-gray-700">Queima</th>
                                        <th class="px-3 py-2 text-left font-medium text-gray-700">Data</th>
                                        <th class="px-3 py-2 text-left font-medium text-gray-700">Peças</th>
                                        <th class="px-3 py-2 text-left font-medium text-gray-700">Alunas</th>
                                        <th class="px-3 py-2 text-left font-medium text-gray-700">Duração</th>
                                        <th class="px-3 py-2 text-left font-medium text-gray-700">Sucesso</th>
                                        <th class="px-3 py-2 text-left font-medium text-gray-700">Receita</th>
                                    </tr>
                                </thead>
                                <tbody class="divide-y divide-gray-200">
                                    <tr>
                                        <td class="px-3 py-2">#234</td>
                                        <td class="px-3 py-2">15/04/2024</td>
                                        <td class="px-3 py-2">23</td>
                                        <td class="px-3 py-2">8</td>
                                        <td class="px-3 py-2">28h</td>
                                        <td class="px-3 py-2"><span class="bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs">100%</span></td>
                                        <td class="px-3 py-2">R$ 230</td>
                                    </tr>
                                    <tr>
                                        <td class="px-3 py-2">#233</td>
                                        <td class="px-3 py-2">10/04/2024</td>
                                        <td class="px-3 py-2">19</td>
                                        <td class="px-3 py-2">7</td>
                                        <td class="px-3 py-2">26h</td>
                                        <td class="px-3 py-2"><span class="bg-yellow-100 text-yellow-800 px-2 py-1 rounded-full text-xs">89%</span></td>
                                        <td class="px-3 py-2">R$ 190</td>
                                    </tr>
                                    <tr>
                                        <td class="px-3 py-2">#232</td>
                                        <td class="px-3 py-2">05/04/2024</td>
                                        <td class="px-3 py-2">21</td>
                                        <td class="px-3 py-2">9</td>
                                        <td class="px-3 py-2">30h</td>
                                        <td class="px-3 py-2"><span class="bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs">95%</span></td>
                                        <td class="px-3 py-2">R$ 210</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <!-- Shop Sales Report -->
                    <div class="bg-white rounded-xl pottery-shadow p-6">
                        <div class="flex justify-between items-center mb-4">
                            <h4 class="text-lg font-semibold flex items-center space-x-2">
                                <span>🛒</span>
                                <span>Relatório de Vendas - Abril 2024</span>
                            </h4>
                            <button class="bg-teal-500 hover:bg-teal-600 text-white px-3 py-1 rounded text-sm transition-colors">
                                📥 Exportar PDF
                            </button>
                        </div>

                        <!-- Sales Stats -->
                        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                            <div class="bg-teal-50 border border-teal-200 rounded-lg p-4 text-center">
                                <p class="text-teal-600 font-semibold">Pedidos</p>
                                <p class="text-2xl font-bold text-teal-700">24</p>
                                <p class="text-xs text-teal-600">+15% vs mês anterior</p>
                            </div>
                            <div class="bg-blue-50 border border-blue-200 rounded-lg p-4 text-center">
                                <p class="text-blue-600 font-semibold">Itens Vendidos</p>
                                <p class="text-2xl font-bold text-blue-700">67</p>
                                <p class="text-xs text-blue-600">Média: 2.8 por pedido</p>
                            </div>
                            <div class="bg-green-50 border border-green-200 rounded-lg p-4 text-center">
                                <p class="text-green-600 font-semibold">Receita Total</p>
                                <p class="text-2xl font-bold text-green-700">R$ 2.340</p>
                                <p class="text-xs text-green-600">Ticket médio: R$ 97,50</p>
                            </div>
                            <div class="bg-purple-50 border border-purple-200 rounded-lg p-4 text-center">
                                <p class="text-purple-600 font-semibold">Produto Top</p>
                                <p class="text-lg font-bold text-purple-700">Argila 5kg</p>
                                <p class="text-xs text-purple-600">18 unidades vendidas</p>
                            </div>
                        </div>

                        <!-- Top Products -->
                        <div class="mb-6">
                            <h5 class="font-semibold mb-3">Produtos Mais Vendidos</h5>
                            <div class="space-y-3">
                                <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                                    <div class="flex items-center space-x-3">
                                        <span class="text-2xl">🧱</span>
                                        <div>
                                            <p class="font-medium">Argila Vermelha 5kg</p>
                                            <p class="text-sm text-gray-600">18 unidades • R$ 35,00 cada</p>
                                        </div>
                                    </div>
                                    <div class="text-right">
                                        <p class="font-bold text-green-600">R$ 630,00</p>
                                        <p class="text-xs text-gray-500">27% das vendas</p>
                                    </div>
                                </div>
                                <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                                    <div class="flex items-center space-x-3">
                                        <span class="text-2xl">🔧</span>
                                        <div>
                                            <p class="font-medium">Kit Ferramentas Básico</p>
                                            <p class="text-sm text-gray-600">12 unidades • R$ 85,00 cada</p>
                                        </div>
                                    </div>
                                    <div class="text-right">
                                        <p class="font-bold text-green-600">R$ 1.020,00</p>
                                        <p class="text-xs text-gray-500">44% das vendas</p>
                                    </div>
                                </div>
                                <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                                    <div class="flex items-center space-x-3">
                                        <span class="text-2xl">📦</span>
                                        <div>
                                            <p class="font-medium">Kit Iniciante Completo</p>
                                            <p class="text-sm text-gray-600">6 unidades • R$ 120,00 cada</p>
                                        </div>
                                    </div>
                                    <div class="text-right">
                                        <p class="font-bold text-green-600">R$ 720,00</p>
                                        <p class="text-xs text-gray-500">31% das vendas</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Student Activity Report -->
                    <div class="bg-white rounded-xl pottery-shadow p-6">
                        <div class="flex justify-between items-center mb-4">
                            <h4 class="text-lg font-semibold flex items-center space-x-2">
                                <span>👩‍🎨</span>
                                <span>Relatório de Atividade das Alunas - Abril 2024</span>
                            </h4>
                            <button class="bg-pink-500 hover:bg-pink-600 text-white px-3 py-1 rounded text-sm transition-colors">
                                📥 Exportar PDF
                            </button>
                        </div>

                        <!-- Activity Stats -->
                        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                            <div class="bg-pink-50 border border-pink-200 rounded-lg p-4 text-center">
                                <p class="text-pink-600 font-semibold">Alunas Ativas</p>
                                <p class="text-2xl font-bold text-pink-700">47</p>
                                <p class="text-xs text-pink-600">+3 novas este mês</p>
                            </div>
                            <div class="bg-blue-50 border border-blue-200 rounded-lg p-4 text-center">
                                <p class="text-blue-600 font-semibold">Peças Criadas</p>
                                <p class="text-2xl font-bold text-blue-700">234</p>
                                <p class="text-xs text-blue-600">Média: 5 por aluna</p>
                            </div>
                            <div class="bg-green-50 border border-green-200 rounded-lg p-4 text-center">
                                <p class="text-green-600 font-semibold">Frequência Média</p>
                                <p class="text-2xl font-bold text-green-700">87%</p>
                                <p class="text-xs text-green-600">+5% vs mês anterior</p>
                            </div>
                            <div class="bg-orange-50 border border-orange-200 rounded-lg p-4 text-center">
                                <p class="text-orange-600 font-semibold">Turma Mais Ativa</p>
                                <p class="text-lg font-bold text-orange-700">5ª-feira (tarde)</p>
                                <p class="text-xs text-orange-600">92% de frequência</p>
                            </div>
                        </div>

                        <!-- Class Distribution -->
                        <div class="mb-6">
                            <h5 class="font-semibold mb-3">Distribuição por Turma</h5>
                            <div class="grid grid-cols-1 md:grid-cols-5 gap-4">
                                <div class="bg-gray-50 rounded-lg p-4">
                                    <div class="flex justify-between items-center mb-2">
                                        <span class="font-medium text-xs">2ª-feira</span>
                                        <span class="bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs">9 alunas</span>
                                    </div>
                                    <div class="w-full bg-gray-200 rounded-full h-2">
                                        <div class="bg-blue-500 h-2 rounded-full" style="width: 19%"></div>
                                    </div>
                                    <p class="text-xs text-gray-600 mt-1">19% do total</p>
                                </div>
                                <div class="bg-gray-50 rounded-lg p-4">
                                    <div class="flex justify-between items-center mb-2">
                                        <span class="font-medium text-xs">3ª-feira</span>
                                        <span class="bg-yellow-100 text-yellow-800 px-2 py-1 rounded-full text-xs">10 alunas</span>
                                    </div>
                                    <div class="w-full bg-gray-200 rounded-full h-2">
                                        <div class="bg-yellow-500 h-2 rounded-full" style="width: 21%"></div>
                                    </div>
                                    <p class="text-xs text-gray-600 mt-1">21% do total</p>
                                </div>
                                <div class="bg-gray-50 rounded-lg p-4">
                                    <div class="flex justify-between items-center mb-2">
                                        <span class="font-medium text-xs">4ª-feira</span>
                                        <span class="bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs">8 alunas</span>
                                    </div>
                                    <div class="w-full bg-gray-200 rounded-full h-2">
                                        <div class="bg-green-500 h-2 rounded-full" style="width: 17%"></div>
                                    </div>
                                    <p class="text-xs text-gray-600 mt-1">17% do total</p>
                                </div>
                                <div class="bg-gray-50 rounded-lg p-4">
                                    <div class="flex justify-between items-center mb-2">
                                        <span class="font-medium text-xs">5ª-feira</span>
                                        <span class="bg-purple-100 text-purple-800 px-2 py-1 rounded-full text-xs">12 alunas</span>
                                    </div>
                                    <div class="w-full bg-gray-200 rounded-full h-2">
                                        <div class="bg-purple-500 h-2 rounded-full" style="width: 26%"></div>
                                    </div>
                                    <p class="text-xs text-gray-600 mt-1">26% do total</p>
                                </div>
                                <div class="bg-gray-50 rounded-lg p-4">
                                    <div class="flex justify-between items-center mb-2">
                                        <span class="font-medium text-xs">6ª-feira</span>
                                        <span class="bg-pink-100 text-pink-800 px-2 py-1 rounded-full text-xs">8 alunas</span>
                                    </div>
                                    <div class="w-full bg-gray-200 rounded-full h-2">
                                        <div class="bg-pink-500 h-2 rounded-full" style="width: 17%"></div>
                                    </div>
                                    <p class="text-xs text-gray-600 mt-1">17% do total</p>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Export All Reports -->
                    <div class="bg-white rounded-xl pottery-shadow p-6 text-center">
                        <h4 class="text-lg font-semibold mb-4">Exportar Todos os Relatórios</h4>
                        <div class="flex justify-center space-x-4">
                            <button class="bg-red-500 hover:bg-red-600 text-white px-6 py-3 rounded-lg transition-colors">
                                📊 Relatório Completo (PDF)
                            </button>
                            <button class="bg-green-500 hover:bg-green-600 text-white px-6 py-3 rounded-lg transition-colors">
                                📈 Dados para Excel (CSV)
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- History Tab -->
            <div id="admin-history" class="admin-tab-content hidden">
                <div class="bg-white rounded-xl pottery-shadow p-6">
                    <div class="flex justify-between items-center mb-6">
                        <h3 class="text-xl font-semibold">Histórico de Alterações</h3>
                        <div class="flex space-x-2">
                            <select id="historyFilter" class="px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500">
                                <option value="all">Todas as ações</option>
                                <option value="student">Gestão de Alunas</option>
                                <option value="payment">Pagamentos</option>
                                <option value="firing">Queimas</option>
                                <option value="settings">Configurações</option>
                            </select>
                            <input type="date" id="historyDate" class="px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500">
                        </div>
                    </div>

                    <!-- History Timeline -->
                    <div id="historyTimeline" class="space-y-4 max-h-96 overflow-y-auto">
                        <div class="history-item flex items-start space-x-4 p-4 bg-gray-50 rounded-lg" data-type="payment">
                            <div class="w-10 h-10 bg-green-500 rounded-full flex items-center justify-center text-white text-sm">💳</div>
                            <div class="flex-1">
                                <div class="flex items-center justify-between mb-1">
                                    <p class="font-medium">Pagamento confirmado - Maria Silva</p>
                                    <span class="text-xs text-gray-500">Hoje, 14:30</span>
                                </div>
                                <p class="text-sm text-gray-600">Mensalidade de Abril (R$ 150,00) - Método: PIX</p>
                                <p class="text-xs text-gray-500">Por: Admin • IP: 192.168.1.100</p>
                            </div>
                        </div>

                        <div class="history-item flex items-start space-x-4 p-4 bg-gray-50 rounded-lg" data-type="firing">
                            <div class="w-10 h-10 bg-orange-500 rounded-full flex items-center justify-center text-white text-sm">🔥</div>
                            <div class="flex-1">
                                <div class="flex items-center justify-between mb-1">
                                    <p class="font-medium">Queima #234 finalizada</p>
                                    <span class="text-xs text-gray-500">Hoje, 12:15</span>
                                </div>
                                <p class="text-sm text-gray-600">15 peças de 6 alunas • Duração: 28h • Temperatura: 1250°C</p>
                                <p class="text-xs text-gray-500">Por: Admin • Sucesso: 100%</p>
                            </div>
                        </div>

                        <div class="history-item flex items-start space-x-4 p-4 bg-gray-50 rounded-lg" data-type="student">
                            <div class="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center text-white text-sm">👩‍🎨</div>
                            <div class="flex-1">
                                <div class="flex items-center justify-between mb-1">
                                    <p class="font-medium">Nova aluna cadastrada - Fernanda Lima</p>
                                    <span class="text-xs text-gray-500">Ontem, 16:45</span>
                                </div>
                                <p class="text-sm text-gray-600">Turma: Iniciante • Idade: 29 anos • Telefone: (11) 99999-9999</p>
                                <p class="text-xs text-gray-500">Por: Admin • Status: Ativo</p>
                            </div>
                        </div>

                        <div class="history-item flex items-start space-x-4 p-4 bg-gray-50 rounded-lg" data-type="settings">
                            <div class="w-10 h-10 bg-purple-500 rounded-full flex items-center justify-center text-white text-sm">⚙️</div>
                            <div class="flex-1">
                                <div class="flex items-center justify-between mb-1">
                                    <p class="font-medium">Valor de mensalidade alterado</p>
                                    <span class="text-xs text-gray-500">Ontem, 10:20</span>
                                </div>
                                <p class="text-sm text-gray-600">Turma Avançada: R$ 150,00 → R$ 160,00</p>
                                <p class="text-xs text-gray-500">Por: Admin • Motivo: Reajuste anual</p>
                            </div>
                        </div>

                        <div class="history-item flex items-start space-x-4 p-4 bg-gray-50 rounded-lg" data-type="payment">
                            <div class="w-10 h-10 bg-red-500 rounded-full flex items-center justify-center text-white text-sm">⚠️</div>
                            <div class="flex-1">
                                <div class="flex items-center justify-between mb-1">
                                    <p class="font-medium">Pagamento em atraso - Ana Costa</p>
                                    <span class="text-xs text-gray-500">2 dias atrás, 09:00</span>
                                </div>
                                <p class="text-sm text-gray-600">Mensalidade de Março (R$ 140,00) • Atraso: 5 dias</p>
                                <p class="text-xs text-gray-500">Sistema • Notificação enviada</p>
                            </div>
                        </div>

                        <div class="history-item flex items-start space-x-4 p-4 bg-gray-50 rounded-lg" data-type="firing">
                            <div class="w-10 h-10 bg-orange-500 rounded-full flex items-center justify-center text-white text-sm">🔥</div>
                            <div class="flex-1">
                                <div class="flex items-center justify-between mb-1">
                                    <p class="font-medium">Queima #233 iniciada</p>
                                    <span class="text-xs text-gray-500">3 dias atrás, 08:00</span>
                                </div>
                                <p class="text-sm text-gray-600">23 peças de 8 alunas • Previsão: 30h</p>
                                <p class="text-xs text-gray-500">Por: Admin • Status: Concluída</p>
                            </div>
                        </div>
                    </div>

                    <!-- Export History -->
                    <div class="mt-6 pt-4 border-t">
                        <button class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg transition-colors">
                            📥 Exportar Histórico (CSV)
                        </button>
                    </div>
                </div>
            </div>

            <!-- Settings Tab -->
            <div id="admin-settings" class="admin-tab-content hidden">
                <div class="space-y-6">
                    <!-- General Settings -->
                    <div class="bg-white rounded-xl pottery-shadow p-6">
                        <h3 class="text-xl font-semibold mb-4">Configurações Gerais</h3>
                        <div class="space-y-4">
                            <div>
                                <label class="block text-sm font-medium mb-2">Logo da Escola</label>
                                <div class="flex items-center space-x-4">
                                    <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center overflow-hidden">
                                        <img id="logoPreview" src="" alt="Preview do logo" class="w-full h-full object-cover hidden" onerror="this.style.display='none';">
                                        <span class="text-gray-400 text-xs text-center">Sem logo</span>
                                    </div>
                                    <div class="flex-1">
                                        <input type="file" id="logoUpload" accept="image/*" class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500">
                                        <p class="text-xs text-gray-500 mt-1">Formatos aceitos: JPG, PNG, SVG (máx. 2MB)</p>
                                    </div>
                                </div>
                            </div>
                            <div>
                                <label class="block text-sm font-medium mb-2">Nome da Escola</label>
                                <input type="text" value="Barro na Veia" class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500">
                            </div>
                            <div>
                                <label class="block text-sm font-medium mb-2">Valor da Queima (por peça)</label>
                                <input type="number" value="10" class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500">
                            </div>
                        </div>
                    </div>

                    <!-- Monthly Fee Management -->
                    <div class="bg-white rounded-xl pottery-shadow p-6">
                        <div class="flex justify-between items-center mb-4">
                            <h3 class="text-xl font-semibold">Gestão de Mensalidades</h3>
                            <button id="addFeeTypeBtn" class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg transition-colors flex items-center space-x-2">
                                <span>➕</span>
                                <span>Novo Tipo</span>
                            </button>
                        </div>
                        
                        <!-- Default Fee Types -->
                        <div class="space-y-4 mb-6">
                            <div class="bg-gray-50 rounded-lg p-4">
                                <h4 class="font-semibold mb-3">Tipos de Mensalidade Padrão</h4>
                                <div id="feeTypesList" class="space-y-3">
                                    <div class="fee-type-item flex items-center justify-between p-3 bg-white rounded border">
                                        <div class="flex-1">
                                            <input type="text" value="2ª-feira (manhã)" class="font-medium bg-transparent border-none focus:outline-none focus:ring-2 focus:ring-blue-500 rounded px-2 py-1">
                                        </div>
                                        <div class="flex items-center space-x-3">
                                            <span class="text-sm text-gray-600">R$</span>
                                            <input type="number" value="120" class="w-20 px-2 py-1 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500">
                                            <button class="text-red-500 hover:text-red-700">🗑️</button>
                                        </div>
                                    </div>
                                    <div class="fee-type-item flex items-center justify-between p-3 bg-white rounded border">
                                        <div class="flex-1">
                                            <input type="text" value="2ª-feira (tarde)" class="font-medium bg-transparent border-none focus:outline-none focus:ring-2 focus:ring-blue-500 rounded px-2 py-1">
                                        </div>
                                        <div class="flex items-center space-x-3">
                                            <span class="text-sm text-gray-600">R$</span>
                                            <input type="number" value="140" class="w-20 px-2 py-1 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500">
                                            <button class="text-red-500 hover:text-red-700">🗑️</button>
                                        </div>
                                    </div>
                                    <div class="fee-type-item flex items-center justify-between p-3 bg-white rounded border">
                                        <div class="flex-1">
                                            <input type="text" value="2ª-feira (noite)" class="font-medium bg-transparent border-none focus:outline-none focus:ring-2 focus:ring-blue-500 rounded px-2 py-1">
                                        </div>
                                        <div class="flex items-center space-x-3">
                                            <span class="text-sm text-gray-600">R$</span>
                                            <input type="number" value="160" class="w-20 px-2 py-1 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500">
                                            <button class="text-red-500 hover:text-red-700">🗑️</button>
                                        </div>
                                    </div>
                                    <div class="fee-type-item flex items-center justify-between p-3 bg-white rounded border">
                                        <div class="flex-1">
                                            <input type="text" value="3ª-feira (manhã)" class="font-medium bg-transparent border-none focus:outline-none focus:ring-2 focus:ring-blue-500 rounded px-2 py-1">
                                        </div>
                                        <div class="flex items-center space-x-3">
                                            <span class="text-sm text-gray-600">R$</span>
                                            <input type="number" value="120" class="w-20 px-2 py-1 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500">
                                            <button class="text-red-500 hover:text-red-700">🗑️</button>
                                        </div>
                                    </div>
                                    <div class="fee-type-item flex items-center justify-between p-3 bg-white rounded border">
                                        <div class="flex-1">
                                            <input type="text" value="3ª-feira (tarde)" class="font-medium bg-transparent border-none focus:outline-none focus:ring-2 focus:ring-blue-500 rounded px-2 py-1">
                                        </div>
                                        <div class="flex items-center space-x-3">
                                            <span class="text-sm text-gray-600">R$</span>
                                            <input type="number" value="140" class="w-20 px-2 py-1 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500">
                                            <button class="text-red-500 hover:text-red-700">🗑️</button>
                                        </div>
                                    </div>
                                    <div class="fee-type-item flex items-center justify-between p-3 bg-white rounded border">
                                        <div class="flex-1">
                                            <input type="text" value="3ª-feira (noite)" class="font-medium bg-transparent border-none focus:outline-none focus:ring-2 focus:ring-blue-500 rounded px-2 py-1">
                                        </div>
                                        <div class="flex items-center space-x-3">
                                            <span class="text-sm text-gray-600">R$</span>
                                            <input type="number" value="160" class="w-20 px-2 py-1 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500">
                                            <button class="text-red-500 hover:text-red-700">🗑️</button>
                                        </div>
                                    </div>
                                    <div class="fee-type-item flex items-center justify-between p-3 bg-white rounded border">
                                        <div class="flex-1">
                                            <input type="text" value="4ª-feira (manhã)" class="font-medium bg-transparent border-none focus:outline-none focus:ring-2 focus:ring-blue-500 rounded px-2 py-1">
                                        </div>
                                        <div class="flex items-center space-x-3">
                                            <span class="text-sm text-gray-600">R$</span>
                                            <input type="number" value="120" class="w-20 px-2 py-1 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500">
                                            <button class="text-red-500 hover:text-red-700">🗑️</button>
                                        </div>
                                    </div>
                                    <div class="fee-type-item flex items-center justify-between p-3 bg-white rounded border">
                                        <div class="flex-1">
                                            <input type="text" value="4ª-feira (tarde)" class="font-medium bg-transparent border-none focus:outline-none focus:ring-2 focus:ring-blue-500 rounded px-2 py-1">
                                        </div>
                                        <div class="flex items-center space-x-3">
                                            <span class="text-sm text-gray-600">R$</span>
                                            <input type="number" value="140" class="w-20 px-2 py-1 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500">
                                            <button class="text-red-500 hover:text-red-700">🗑️</button>
                                        </div>
                                    </div>
                                    <div class="fee-type-item flex items-center justify-between p-3 bg-white rounded border">
                                        <div class="flex-1">
                                            <input type="text" value="4ª-feira (noite)" class="font-medium bg-transparent border-none focus:outline-none focus:ring-2 focus:ring-blue-500 rounded px-2 py-1">
                                        </div>
                                        <div class="flex items-center space-x-3">
                                            <span class="text-sm text-gray-600">R$</span>
                                            <input type="number" value="160" class="w-20 px-2 py-1 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500">
                                            <button class="text-red-500 hover:text-red-700">🗑️</button>
                                        </div>
                                    </div>
                                    <div class="fee-type-item flex items-center justify-between p-3 bg-white rounded border">
                                        <div class="flex-1">
                                            <input type="text" value="5ª-feira (manhã)" class="font-medium bg-transparent border-none focus:outline-none focus:ring-2 focus:ring-blue-500 rounded px-2 py-1">
                                        </div>
                                        <div class="flex items-center space-x-3">
                                            <span class="text-sm text-gray-600">R$</span>
                                            <input type="number" value="120" class="w-20 px-2 py-1 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500">
                                            <button class="text-red-500 hover:text-red-700">🗑️</button>
                                        </div>
                                    </div>
                                    <div class="fee-type-item flex items-center justify-between p-3 bg-white rounded border">
                                        <div class="flex-1">
                                            <input type="text" value="5ª-feira (tarde)" class="font-medium bg-transparent border-none focus:outline-none focus:ring-2 focus:ring-blue-500 rounded px-2 py-1">
                                        </div>
                                        <div class="flex items-center space-x-3">
                                            <span class="text-sm text-gray-600">R$</span>
                                            <input type="number" value="140" class="w-20 px-2 py-1 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500">
                                            <button class="text-red-500 hover:text-red-700">🗑️</button>
                                        </div>
                                    </div>
                                    <div class="fee-type-item flex items-center justify-between p-3 bg-white rounded border">
                                        <div class="flex-1">
                                            <input type="text" value="5ª-feira (noite)" class="font-medium bg-transparent border-none focus:outline-none focus:ring-2 focus:ring-blue-500 rounded px-2 py-1">
                                        </div>
                                        <div class="flex items-center space-x-3">
                                            <span class="text-sm text-gray-600">R$</span>
                                            <input type="number" value="160" class="w-20 px-2 py-1 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500">
                                            <button class="text-red-500 hover:text-red-700">🗑️</button>
                                        </div>
                                    </div>
                                    <div class="fee-type-item flex items-center justify-between p-3 bg-white rounded border">
                                        <div class="flex-1">
                                            <input type="text" value="6ª-feira (manhã)" class="font-medium bg-transparent border-none focus:outline-none focus:ring-2 focus:ring-blue-500 rounded px-2 py-1">
                                        </div>
                                        <div class="flex items-center space-x-3">
                                            <span class="text-sm text-gray-600">R$</span>
                                            <input type="number" value="120" class="w-20 px-2 py-1 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500">
                                            <button class="text-red-500 hover:text-red-700">🗑️</button>
                                        </div>
                                    </div>
                                    <div class="fee-type-item flex items-center justify-between p-3 bg-white rounded border">
                                        <div class="flex-1">
                                            <input type="text" value="6ª-feira (tarde)" class="font-medium bg-transparent border-none focus:outline-none focus:ring-2 focus:ring-blue-500 rounded px-2 py-1">
                                        </div>
                                        <div class="flex items-center space-x-3">
                                            <span class="text-sm text-gray-600">R$</span>
                                            <input type="number" value="140" class="w-20 px-2 py-1 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500">
                                            <button class="text-red-500 hover:text-red-700">🗑️</button>
                                        </div>
                                    </div>
                                    <div class="fee-type-item flex items-center justify-between p-3 bg-white rounded border">
                                        <div class="flex-1">
                                            <input type="text" value="6ª-feira (noite)" class="font-medium bg-transparent border-none focus:outline-none focus:ring-2 focus:ring-blue-500 rounded px-2 py-1">
                                        </div>
                                        <div class="flex items-center space-x-3">
                                            <span class="text-sm text-gray-600">R$</span>
                                            <input type="number" value="160" class="w-20 px-2 py-1 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500">
                                            <button class="text-red-500 hover:text-red-700">🗑️</button>
                                        </div>
                                    </div>
                                    <div class="fee-type-item flex items-center justify-between p-3 bg-white rounded border">
                                        <div class="flex-1">
                                            <input type="text" value="Aula Particular" class="font-medium bg-transparent border-none focus:outline-none focus:ring-2 focus:ring-blue-500 rounded px-2 py-1">
                                        </div>
                                        <div class="flex items-center space-x-3">
                                            <span class="text-sm text-gray-600">R$</span>
                                            <input type="number" value="200" class="w-20 px-2 py-1 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500">
                                            <button class="text-red-500 hover:text-red-700">🗑️</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Individual Student Fees -->
                        <div class="bg-gray-50 rounded-lg p-4">
                            <div class="flex justify-between items-center mb-3">
                                <h4 class="font-semibold">Mensalidades Personalizadas por Aluna</h4>
                                <button id="addCustomFeeBtn" class="bg-green-500 hover:bg-green-600 text-white px-3 py-1 rounded text-sm transition-colors">
                                    ➕ Personalizar
                                </button>
                            </div>
                            <div id="customFeesList" class="space-y-3">
                                <div class="custom-fee-item flex items-center justify-between p-3 bg-white rounded border">
                                    <div class="flex-1 grid grid-cols-2 gap-3">
                                        <select class="px-2 py-1 border rounded focus:outline-none focus:ring-2 focus:ring-green-500">
                                            <option value="">Selecionar aluna...</option>
                                            <option value="maria" selected>Maria Silva</option>
                                            <option value="ana">Ana Costa</option>
                                            <option value="carla">Carla Santos</option>
                                        </select>
                                        <input type="text" value="Desconto especial" placeholder="Motivo (opcional)" class="px-2 py-1 border rounded focus:outline-none focus:ring-2 focus:ring-green-500 text-sm">
                                    </div>
                                    <div class="flex items-center space-x-3 ml-3">
                                        <span class="text-sm text-gray-600">R$</span>
                                        <input type="number" value="130" class="w-20 px-2 py-1 border rounded focus:outline-none focus:ring-2 focus:ring-green-500">
                                        <button class="text-red-500 hover:text-red-700">🗑️</button>
                                    </div>
                                </div>
                                <div class="custom-fee-item flex items-center justify-between p-3 bg-white rounded border">
                                    <div class="flex-1 grid grid-cols-2 gap-3">
                                        <select class="px-2 py-1 border rounded focus:outline-none focus:ring-2 focus:ring-green-500">
                                            <option value="">Selecionar aluna...</option>
                                            <option value="maria">Maria Silva</option>
                                            <option value="ana">Ana Costa</option>
                                            <option value="carla" selected>Carla Santos</option>
                                        </select>
                                        <input type="text" value="Aposentada" placeholder="Motivo (opcional)" class="px-2 py-1 border rounded focus:outline-none focus:ring-2 focus:ring-green-500 text-sm">
                                    </div>
                                    <div class="flex items-center space-x-3 ml-3">
                                        <span class="text-sm text-gray-600">R$</span>
                                        <input type="number" value="100" class="w-20 px-2 py-1 border rounded focus:outline-none focus:ring-2 focus:ring-green-500">
                                        <button class="text-red-500 hover:text-red-700">🗑️</button>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Fee Summary -->
                        <div class="mt-6 bg-blue-50 rounded-lg p-4">
                            <h4 class="font-semibold mb-3 text-blue-800">Resumo de Mensalidades</h4>
                            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                                <div class="text-center">
                                    <p class="text-2xl font-bold text-blue-600">47</p>
                                    <p class="text-blue-700">Total de Alunas</p>
                                </div>
                                <div class="text-center">
                                    <p class="text-2xl font-bold text-green-600">R$ 6.580</p>
                                    <p class="text-green-700">Receita Mensal Prevista</p>
                                </div>
                                <div class="text-center">
                                    <p class="text-2xl font-bold text-orange-600">R$ 140</p>
                                    <p class="text-orange-700">Valor Médio</p>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Notification Settings -->
                    <div class="bg-white rounded-xl pottery-shadow p-6">
                        <h3 class="text-xl font-semibold mb-4">Configurações de Notificação</h3>
                        <div class="space-y-4">
                            <div class="flex items-center justify-between">
                                <span>Lembrete de pagamento (3 dias antes)</span>
                                <input type="checkbox" checked class="w-5 h-5 text-red-600">
                            </div>
                            <div class="flex items-center justify-between">
                                <span>Notificação de queima concluída</span>
                                <input type="checkbox" checked class="w-5 h-5 text-red-600">
                            </div>
                            <div class="flex items-center justify-between">
                                <span>Mensagens poéticas semanais</span>
                                <input type="checkbox" checked class="w-5 h-5 text-red-600">
                            </div>
                        </div>
                    </div>

                    <!-- Backup & Security -->
                    <div class="bg-white rounded-xl pottery-shadow p-6">
                        <h3 class="text-xl font-semibold mb-4">Backup e Segurança</h3>
                        <div class="space-y-4">
                            <button class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg transition-colors">
                                📥 Fazer Backup dos Dados
                            </button>
                            <button class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg transition-colors">
                                🔄 Restaurar Backup
                            </button>
                            <button class="bg-orange-500 hover:bg-orange-600 text-white px-4 py-2 rounded-lg transition-colors">
                                🔑 Alterar Senha Admin
                            </button>
                        </div>
                    </div>

                    <!-- Save Button -->
                    <div class="text-center">
                        <button class="bg-red-500 hover:bg-red-600 text-white px-8 py-3 rounded-lg transition-colors font-semibold">
                            💾 Salvar Todas as Configurações
                        </button>
                    </div>
                </div>
            </div>
        </section>
    </main>

    <!-- Modals -->
    <!-- Add Piece Modal -->
    <div id="addPieceModal" class="fixed inset-0 bg-black bg-opacity-50 hidden items-center justify-center z-50">
        <div class="bg-white rounded-xl p-6 w-full max-w-md mx-4">
            <h3 class="text-xl font-semibold mb-4">Adicionar Nova Peça</h3>
            <form id="addPieceForm" class="space-y-4">
                <div>
                    <label class="block text-sm font-medium mb-2">Nome da Peça</label>
                    <input type="text" class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500" required>
                </div>
                <div>
                    <label class="block text-sm font-medium mb-2">Técnica</label>
                    <select class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500" required>
                        <option value="">Selecione...</option>
                        <option value="torno">Torno</option>
                        <option value="modelagem">Modelagem</option>
                        <option value="placa">Placa</option>
                        <option value="escultura">Escultura</option>
                    </select>
                </div>
                <div>
                    <label class="block text-sm font-medium mb-2">Categoria</label>
                    <select class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500" required>
                        <option value="">Selecione...</option>
                        <option value="tigelas">Tigelas</option>
                        <option value="vasos">Vasos</option>
                        <option value="pratos">Pratos</option>
                        <option value="esculturas">Esculturas</option>
                    </select>
                </div>
                <div>
                    <label class="block text-sm font-medium mb-2">Foto da Peça</label>
                    <input type="file" accept="image/*" class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500">
                </div>
                <div class="flex space-x-3 pt-4">
                    <button type="button" id="cancelAddPiece" class="flex-1 bg-gray-300 hover:bg-gray-400 text-gray-700 py-2 px-4 rounded-lg transition-colors">
                        Cancelar
                    </button>
                    <button type="submit" class="flex-1 bg-green-600 hover:bg-green-700 text-white py-2 px-4 rounded-lg transition-colors">
                        Adicionar
                    </button>
                </div>
            </form>
        </div>
    </div>

    <!-- Cart Modal -->
    <div id="cartModal" class="fixed inset-0 bg-black bg-opacity-50 hidden items-center justify-center z-50">
        <div class="bg-white rounded-xl p-6 w-full max-w-md mx-4">
            <h3 class="text-xl font-semibold mb-4">Carrinho de Compras</h3>
            <div id="cartItems" class="space-y-3 mb-4">
                <!-- Cart items will be added here -->
            </div>
            <div class="border-t pt-4">
                <div class="flex justify-between items-center mb-4">
                    <span class="font-semibold">Total:</span>
                    <span id="cartTotal" class="text-xl font-bold text-orange-600">R$ 0,00</span>
                </div>
                <div class="flex space-x-3">
                    <button id="closeCart" class="flex-1 bg-gray-300 hover:bg-gray-400 text-gray-700 py-2 px-4 rounded-lg transition-colors">
                        Continuar Comprando
                    </button>
                    <button id="checkout" class="flex-1 bg-orange-500 hover:bg-orange-600 text-white py-2 px-4 rounded-lg transition-colors">
                        Finalizar Pedido
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- Notifications Modal -->
    <div id="notificationsModal" class="fixed inset-0 bg-black bg-opacity-50 hidden items-center justify-center z-50">
        <div class="bg-white rounded-xl p-6 w-full max-w-md mx-4">
            <h3 class="text-xl font-semibold mb-4">Notificações</h3>
            <div class="space-y-3">
                <div class="p-3 bg-blue-50 rounded-lg border-l-4 border-blue-500">
                    <p class="font-medium text-sm">Lembrete: Aula amanhã</p>
                    <p class="text-xs text-gray-600">Técnicas de esmaltação às 14:00</p>
                </div>
                <div class="p-3 bg-green-50 rounded-lg border-l-4 border-green-500">
                    <p class="font-medium text-sm">Queima concluída!</p>
                    <p class="text-xs text-gray-600">Suas 3 peças estão prontas para retirada</p>
                </div>
                <div class="p-3 bg-purple-50 rounded-lg border-l-4 border-purple-500">
                    <p class="font-medium text-sm">Mensagem da Professora</p>
                    <p class="text-xs text-gray-600">"A arte nasce das mãos que moldam com amor" ✨</p>
                </div>
            </div>
            <button id="closeNotifications" class="w-full mt-4 bg-orange-500 hover:bg-orange-600 text-white py-2 px-4 rounded-lg transition-colors">
                Fechar
            </button>
        </div>
    </div>

    <!-- Add Clay Purchase Modal -->
    <div id="addClayPurchaseModal" class="fixed inset-0 bg-black bg-opacity-50 hidden items-center justify-center z-50">
        <div class="bg-white rounded-xl p-6 w-full max-w-md mx-4">
            <h3 class="text-xl font-semibold mb-4">Nova Compra de Argila</h3>
            <form id="addClayPurchaseForm" class="space-y-4">
                <div>
                    <label class="block text-sm font-medium mb-2">Tipo de Argila</label>
                    <select id="clayTypeSelect" class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500">
                        <option value="">Selecione ou digite novo tipo...</option>
                        <option value="Argila Vermelha">Argila Vermelha</option>
                        <option value="Argila Branca">Argila Branca</option>
                        <option value="Argila Grês">Argila Grês</option>
                        <option value="Argila Refratária">Argila Refratária</option>
                        <option value="Argila Chamote">Argila Chamote</option>
                        <option value="custom">➕ Outro tipo (digitar)</option>
                    </select>
                    <input type="text" id="customClayType" placeholder="Digite o tipo de argila..." class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 mt-2 hidden">
                </div>
                <div>
                    <label class="block text-sm font-medium mb-2">Quantidade (kg)</label>
                    <input type="number" id="clayQuantity" step="0.1" min="0.1" class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500" required>
                </div>
                <div>
                    <label class="block text-sm font-medium mb-2">Fornecedor</label>
                    <select id="supplierSelect" class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500">
                        <option value="">Selecione ou digite novo fornecedor...</option>
                        <option value="Cerâmica São Paulo">Cerâmica São Paulo</option>
                        <option value="Argilas do Vale">Argilas do Vale</option>
                        <option value="Cerâmica Artesanal">Cerâmica Artesanal</option>
                        <option value="Fornecedor Regional">Fornecedor Regional</option>
                        <option value="Casa da Cerâmica">Casa da Cerâmica</option>
                        <option value="custom">➕ Outro fornecedor (digitar)</option>
                    </select>
                    <input type="text" id="customSupplier" placeholder="Digite o nome do fornecedor..." class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 mt-2 hidden">
                </div>
                <div>
                    <label class="block text-sm font-medium mb-2">Valor Total (R$)</label>
                    <input type="number" id="clayValue" step="0.01" min="0" class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500" required>
                </div>
                <div>
                    <label class="block text-sm font-medium mb-2">Status do Pagamento</label>
                    <select id="paymentStatus" class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500" required>
                        <option value="Pendente">Pendente</option>
                        <option value="Pago">Pago</option>
                    </select>
                </div>
                <div class="flex space-x-3 pt-4">
                    <button type="button" id="cancelClayPurchase" class="flex-1 bg-gray-300 hover:bg-gray-400 text-gray-700 py-2 px-4 rounded-lg transition-colors">
                        Cancelar
                    </button>
                    <button type="submit" class="flex-1 bg-green-600 hover:bg-green-700 text-white py-2 px-4 rounded-lg transition-colors">
                        Adicionar
                    </button>
                </div>
            </form>
        </div>
    </div>

    <script>
        // Global state
        let cart = [];
        let cartTotal = 0;

        // Navigation functionality
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const section = btn.dataset.section;
                
                // Update active nav button
                document.querySelectorAll('.nav-btn').forEach(b => {
                    b.classList.remove('border-orange-500', 'text-orange-600');
                    b.classList.add('border-transparent', 'text-gray-600');
                });
                btn.classList.remove('border-transparent', 'text-gray-600');
                btn.classList.add('border-orange-500', 'text-orange-600');
                
                // Show selected section
                document.querySelectorAll('.section-content').forEach(s => {
                    s.classList.add('hidden');
                });
                document.getElementById(section).classList.remove('hidden');
                document.getElementById(section).classList.add('fade-in');
            });
        });

        // Portfolio filtering
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const filter = btn.dataset.filter;
                
                // Update active filter button
                document.querySelectorAll('.filter-btn').forEach(b => {
                    b.classList.remove('bg-orange-500', 'text-white');
                    b.classList.add('bg-gray-200', 'text-gray-700');
                });
                btn.classList.remove('bg-gray-200', 'text-gray-700');
                btn.classList.add('bg-orange-500', 'text-white');
                
                // Filter pieces
                document.querySelectorAll('.piece-card').forEach(card => {
                    if (filter === 'all' || card.dataset.category === filter) {
                        card.style.display = 'block';
                    } else {
                        card.style.display = 'none';
                    }
                });
            });
        });

        // Shop category filtering
        document.querySelectorAll('.category-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const category = btn.dataset.category;
                
                // Update active category button
                document.querySelectorAll('.category-btn').forEach(b => {
                    b.classList.remove('bg-orange-500', 'text-white');
                    b.classList.add('bg-gray-200', 'text-gray-700');
                });
                btn.classList.remove('bg-gray-200', 'text-gray-700');
                btn.classList.add('bg-orange-500', 'text-white');
                
                // Filter products
                document.querySelectorAll('.product-card').forEach(card => {
                    if (category === 'all' || card.dataset.category === category) {
                        card.style.display = 'block';
                    } else {
                        card.style.display = 'none';
                    }
                });
            });
        });

        // Add to cart functionality
        document.querySelectorAll('.add-to-cart').forEach(btn => {
            btn.addEventListener('click', () => {
                const product = btn.dataset.product;
                const price = parseFloat(btn.dataset.price);
                
                cart.push({ product, price });
                cartTotal += price;
                
                updateCartDisplay();
                
                // Show success message
                btn.textContent = 'Adicionado!';
                btn.classList.add('bg-green-500');
                setTimeout(() => {
                    btn.textContent = 'Adicionar';
                    btn.classList.remove('bg-green-500');
                }, 1000);
            });
        });

        function updateCartDisplay() {
            document.getElementById('cartCount').textContent = cart.length;
            document.getElementById('cartTotal').textContent = `R$ ${cartTotal.toFixed(2).replace('.', ',')}`;
            
            const cartItems = document.getElementById('cartItems');
            cartItems.innerHTML = '';
            
            cart.forEach((item, index) => {
                const itemDiv = document.createElement('div');
                itemDiv.className = 'flex justify-between items-center p-2 bg-gray-50 rounded';
                itemDiv.innerHTML = `
                    <span class="text-sm">${item.product}</span>
                    <div class="flex items-center space-x-2">
                        <span class="text-sm font-medium">R$ ${item.price.toFixed(2).replace('.', ',')}</span>
                        <button class="text-red-500 hover:text-red-700 text-sm" onclick="removeFromCart(${index})">✕</button>
                    </div>
                `;
                cartItems.appendChild(itemDiv);
            });
        }

        function removeFromCart(index) {
            cartTotal -= cart[index].price;
            cart.splice(index, 1);
            updateCartDisplay();
        }

        // Modal functionality
        function showModal(modalId) {
            document.getElementById(modalId).classList.remove('hidden');
            document.getElementById(modalId).classList.add('flex');
        }

        function hideModal(modalId) {
            document.getElementById(modalId).classList.add('hidden');
            document.getElementById(modalId).classList.remove('flex');
        }

        // Add piece modal
        document.getElementById('addPieceBtn').addEventListener('click', () => {
            showModal('addPieceModal');
        });

        document.getElementById('cancelAddPiece').addEventListener('click', () => {
            hideModal('addPieceModal');
        });

        document.getElementById('addPieceForm').addEventListener('submit', (e) => {
            e.preventDefault();
            // Here you would normally send the data to a server
            alert('Peça adicionada com sucesso!');
            hideModal('addPieceModal');
        });

        // Cart modal
        document.getElementById('cartBtn').addEventListener('click', () => {
            showModal('cartModal');
        });

        document.getElementById('closeCart').addEventListener('click', () => {
            hideModal('cartModal');
        });

        document.getElementById('checkout').addEventListener('click', () => {
            if (cart.length === 0) {
                alert('Seu carrinho está vazio!');
                return;
            }
            alert('Pedido finalizado com sucesso! Você receberá um email de confirmação.');
            cart = [];
            cartTotal = 0;
            updateCartDisplay();
            hideModal('cartModal');
        });

        // Notifications modal
        document.getElementById('notificationBtn').addEventListener('click', () => {
            showModal('notificationsModal');
        });

        document.getElementById('closeNotifications').addEventListener('click', () => {
            hideModal('notificationsModal');
        });

        // Chat functionality
        document.getElementById('sendMessage').addEventListener('click', () => {
            const input = document.getElementById('chatInput');
            const message = input.value.trim();
            
            if (message) {
                const chatMessages = document.getElementById('chatMessages');
                const messageDiv = document.createElement('div');
                messageDiv.className = 'flex items-start space-x-3 flex-row-reverse';
                messageDiv.innerHTML = `
                    <div class="w-8 h-8 bg-orange-500 rounded-full flex items-center justify-center text-white text-sm">M</div>
                    <div class="flex-1">
                        <div class="flex items-center space-x-2 mb-1 justify-end">
                            <span class="text-xs text-gray-500">${new Date().toLocaleTimeString('pt-BR', {hour: '2-digit', minute: '2-digit'})}</span>
                            <span class="font-medium text-sm">Você</span>
                        </div>
                        <div class="bg-orange-500 text-white rounded-lg p-3">
                            <p class="text-sm">${message}</p>
                        </div>
                    </div>
                `;
                
                chatMessages.appendChild(messageDiv);
                chatMessages.scrollTop = chatMessages.scrollHeight;
                input.value = '';
            }
        });

        document.getElementById('chatInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                document.getElementById('sendMessage').click();
            }
        });

        // Vote functionality
        document.querySelectorAll('.vote-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const countSpan = btn.querySelector('span:last-child');
                let count = parseInt(countSpan.textContent);
                count++;
                countSpan.textContent = count;
                
                // Add animation
                btn.style.transform = 'scale(1.2)';
                setTimeout(() => {
                    btn.style.transform = 'scale(1)';
                }, 200);
            });
        });

        // Admin tab functionality
        document.querySelectorAll('.admin-tab-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const tab = btn.dataset.tab;
                
                // Update active tab button
                document.querySelectorAll('.admin-tab-btn').forEach(b => {
                    b.classList.remove('bg-red-500', 'text-white');
                    b.classList.add('bg-gray-200', 'text-gray-700');
                });
                btn.classList.remove('bg-gray-200', 'text-gray-700');
                btn.classList.add('bg-red-500', 'text-white');
                
                // Show selected tab content
                document.querySelectorAll('.admin-tab-content').forEach(content => {
                    content.classList.add('hidden');
                });
                document.getElementById(`admin-${tab}`).classList.remove('hidden');
            });
        });

        // Admin functionality
        document.getElementById('addStudentBtn')?.addEventListener('click', () => {
            alert('Funcionalidade de adicionar aluna será implementada aqui!');
        });

        document.getElementById('newFiringBtn')?.addEventListener('click', () => {
            alert('Funcionalidade de nova queima será implementada aqui!');
        });

        // Firing details functionality
        document.querySelectorAll('.firing-details-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const firingContainer = btn.closest('.border');
                const detailsSection = firingContainer.querySelector('.firing-pieces-admin');
                
                if (detailsSection.classList.contains('hidden')) {
                    detailsSection.classList.remove('hidden');
                    btn.textContent = 'Ocultar';
                } else {
                    detailsSection.classList.add('hidden');
                    btn.textContent = 'Detalhes';
                }
            });
        });

        // Firing multiplier functionality
        document.getElementById('firingMultiplier')?.addEventListener('change', function() {
            const multiplier = parseFloat(this.value);
            
            // Update all firing calculations in real-time
            document.querySelectorAll('.firing-pieces-admin tbody tr').forEach(row => {
                const volumeCell = row.cells[3];
                const multiplierCell = row.cells[4];
                const valueCell = row.cells[5];
                
                if (volumeCell && multiplierCell && valueCell) {
                    const volume = parseFloat(volumeCell.textContent.replace(/[^\d.]/g, ''));
                    const currentMultiplier = parseFloat(multiplierCell.textContent);
                    
                    // Calculate new value based on volume and multiplier
                    // Assuming R$ 0.01 per cm³ as base rate
                    const baseValue = volume * 0.01;
                    const finalValue = baseValue * multiplier;
                    
                    multiplierCell.textContent = multiplier.toFixed(1);
                    valueCell.textContent = `R$ ${finalValue.toFixed(2).replace('.', ',')}`;
                }
            });
            
            // Recalculate totals
            document.querySelectorAll('.firing-pieces-admin').forEach(section => {
                let total = 0;
                section.querySelectorAll('tbody tr').forEach(row => {
                    const valueCell = row.cells[5];
                    if (valueCell) {
                        const value = parseFloat(valueCell.textContent.replace(/[^\d,]/g, '').replace(',', '.'));
                        total += value;
                    }
                });
                
                const totalElement = section.querySelector('.text-right p');
                if (totalElement) {
                    totalElement.innerHTML = totalElement.innerHTML.replace(/R\$ [\d,]+/, `R$ ${total.toFixed(2).replace('.', ',')}`);
                }
            });
            
            logActivity('settings', 'Multiplicador de queima alterado', `Novo valor: ${multiplier}`);
        });

        // Fee management functionality
        document.getElementById('addFeeTypeBtn')?.addEventListener('click', () => {
            const feeTypesList = document.getElementById('feeTypesList');
            const newFeeType = document.createElement('div');
            newFeeType.className = 'fee-type-item flex items-center justify-between p-3 bg-white rounded border';
            newFeeType.innerHTML = `
                <div class="flex-1">
                    <input type="text" placeholder="Nome do tipo de mensalidade" class="font-medium bg-transparent border-none focus:outline-none focus:ring-2 focus:ring-blue-500 rounded px-2 py-1 w-full">
                </div>
                <div class="flex items-center space-x-3">
                    <span class="text-sm text-gray-600">R$</span>
                    <input type="number" placeholder="0" class="w-20 px-2 py-1 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500">
                    <button class="text-red-500 hover:text-red-700" onclick="this.parentElement.parentElement.remove()">🗑️</button>
                </div>
            `;
            feeTypesList.appendChild(newFeeType);
            newFeeType.querySelector('input[type="text"]').focus();
        });

        document.getElementById('addCustomFeeBtn')?.addEventListener('click', () => {
            const customFeesList = document.getElementById('customFeesList');
            const newCustomFee = document.createElement('div');
            newCustomFee.className = 'custom-fee-item flex items-center justify-between p-3 bg-white rounded border';
            newCustomFee.innerHTML = `
                <div class="flex-1 grid grid-cols-2 gap-3">
                    <select class="px-2 py-1 border rounded focus:outline-none focus:ring-2 focus:ring-green-500">
                        <option value="">Selecionar aluna...</option>
                        <option value="maria">Maria Silva</option>
                        <option value="ana">Ana Costa</option>
                        <option value="carla">Carla Santos</option>
                        <option value="lucia">Lucia Ferreira</option>
                    </select>
                    <input type="text" placeholder="Motivo (opcional)" class="px-2 py-1 border rounded focus:outline-none focus:ring-2 focus:ring-green-500 text-sm">
                </div>
                <div class="flex items-center space-x-3 ml-3">
                    <span class="text-sm text-gray-600">R$</span>
                    <input type="number" placeholder="0" class="w-20 px-2 py-1 border rounded focus:outline-none focus:ring-2 focus:ring-green-500">
                    <button class="text-red-500 hover:text-red-700" onclick="this.parentElement.parentElement.remove()">🗑️</button>
                </div>
            `;
            customFeesList.appendChild(newCustomFee);
            newCustomFee.querySelector('select').focus();
        });

        // Add delete functionality to existing fee items
        document.addEventListener('click', (e) => {
            if (e.target.textContent === '🗑️' && (e.target.closest('.fee-type-item') || e.target.closest('.custom-fee-item'))) {
                if (confirm('Tem certeza que deseja remover este item?')) {
                    e.target.closest('.fee-type-item, .custom-fee-item').remove();
                }
            }
        });

        // Logo upload functionality
        document.getElementById('logoUpload')?.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                // Validate file size (2MB max)
                if (file.size > 2 * 1024 * 1024) {
                    alert('O arquivo é muito grande. Tamanho máximo: 2MB');
                    this.value = ''; // Clear the input
                    return;
                }
                
                // Validate file type
                const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp'];
                if (!validTypes.includes(file.type)) {
                    alert('Formato não suportado. Use JPG, PNG, GIF ou WebP');
                    this.value = ''; // Clear the input
                    return;
                }
                
                const reader = new FileReader();
                reader.onload = function(e) {
                    const logoUrl = e.target.result;
                    
                    // Update header logo
                    const schoolLogo = document.getElementById('schoolLogo');
                    const defaultLogo = document.getElementById('defaultLogo');
                    
                    if (schoolLogo && defaultLogo) {
                        schoolLogo.src = logoUrl;
                        schoolLogo.style.display = 'block';
                        schoolLogo.classList.remove('hidden');
                        defaultLogo.style.display = 'none';
                        
                        // Remove error handler temporarily to avoid conflicts
                        schoolLogo.onerror = null;
                        
                        // Add new error handler
                        schoolLogo.onerror = function() {
                            console.error('Erro ao carregar logo no header');
                            this.style.display = 'none';
                            defaultLogo.style.display = 'flex';
                        };
                    }
                    
                    // Update preview in settings
                    const logoPreview = document.getElementById('logoPreview');
                    if (logoPreview) {
                        logoPreview.src = logoUrl;
                        logoPreview.style.display = 'block';
                        logoPreview.classList.remove('hidden');
                        
                        // Hide the "Sem logo" text
                        const noLogoText = logoPreview.parentElement.querySelector('span');
                        if (noLogoText) {
                            noLogoText.style.display = 'none';
                        }
                        
                        logoPreview.onerror = function() {
                            console.error('Erro ao carregar logo no preview');
                            this.style.display = 'none';
                            if (noLogoText) {
                                noLogoText.style.display = 'block';
                            }
                        };
                    }
                    
                    // Store in localStorage for persistence
                    try {
                        localStorage.setItem('barroNaVeiaLogo', logoUrl);
                        console.log('Logo salvo no localStorage');
                    } catch (error) {
                        console.error('Erro ao salvar logo:', error);
                        alert('Erro ao salvar logo. Tente uma imagem menor.');
                    }
                };
                
                reader.onerror = function() {
                    alert('Erro ao ler o arquivo. Tente novamente.');
                };
                
                reader.readAsDataURL(file);
            }
        });
        
        // Load saved logo on page load
        window.addEventListener('DOMContentLoaded', function() {
            const savedLogo = localStorage.getItem('barroNaVeiaLogo');
            if (savedLogo) {
                const schoolLogo = document.getElementById('schoolLogo');
                const defaultLogo = document.getElementById('defaultLogo');
                const logoPreview = document.getElementById('logoPreview');
                
                if (schoolLogo && defaultLogo) {
                    schoolLogo.src = savedLogo;
                    schoolLogo.style.display = 'block';
                    schoolLogo.classList.remove('hidden');
                    defaultLogo.style.display = 'none';
                    
                    schoolLogo.onerror = function() {
                        console.error('Logo salvo está corrompido, removendo...');
                        localStorage.removeItem('barroNaVeiaLogo');
                        this.style.display = 'none';
                        defaultLogo.style.display = 'flex';
                    };
                }
                
                if (logoPreview) {
                    logoPreview.src = savedLogo;
                    logoPreview.style.display = 'block';
                    logoPreview.classList.remove('hidden');
                    
                    const noLogoText = logoPreview.parentElement.querySelector('span');
                    if (noLogoText) {
                        noLogoText.style.display = 'none';
                    }
                    
                    logoPreview.onerror = function() {
                        console.error('Logo salvo está corrompido no preview');
                        this.style.display = 'none';
                        if (noLogoText) {
                            noLogoText.style.display = 'block';
                        }
                    };
                }
            }
        });

        // History filtering functionality
        document.getElementById('historyFilter')?.addEventListener('change', function() {
            const filterValue = this.value;
            const historyItems = document.querySelectorAll('.history-item');
            
            historyItems.forEach(item => {
                if (filterValue === 'all' || item.dataset.type === filterValue) {
                    item.style.display = 'flex';
                } else {
                    item.style.display = 'none';
                }
            });
        });

        // History date filtering
        document.getElementById('historyDate')?.addEventListener('change', function() {
            const selectedDate = new Date(this.value);
            const historyItems = document.querySelectorAll('.history-item');
            
            if (this.value) {
                historyItems.forEach(item => {
                    const timeSpan = item.querySelector('.text-xs.text-gray-500');
                    const itemText = timeSpan.textContent;
                    
                    // Simple date matching - in a real app, you'd parse the actual dates
                    if (itemText.includes('Hoje') || itemText.includes(selectedDate.toLocaleDateString('pt-BR'))) {
                        item.style.display = 'flex';
                    } else {
                        item.style.display = 'none';
                    }
                });
            } else {
                // Show all items if no date selected
                historyItems.forEach(item => {
                    item.style.display = 'flex';
                });
            }
        });

        // Report generation functionality
        document.querySelector('[data-tab="reports"] button')?.addEventListener('click', function() {
            const period = document.getElementById('reportPeriod')?.value || 'month';
            
            // Simulate report generation
            this.textContent = '⏳ Gerando...';
            this.disabled = true;
            
            setTimeout(() => {
                this.textContent = '📊 Gerar Relatório';
                this.disabled = false;
                alert(`Relatório do período "${period}" gerado com sucesso!`);
            }, 2000);
        });

        // Export functionality for reports
        document.querySelectorAll('button[class*="bg-blue-500"], button[class*="bg-orange-500"], button[class*="bg-teal-500"], button[class*="bg-pink-500"]').forEach(btn => {
            if (btn.textContent.includes('Exportar PDF')) {
                btn.addEventListener('click', function() {
                    const reportType = this.closest('.bg-white').querySelector('h4').textContent;
                    
                    this.textContent = '⏳ Exportando...';
                    this.disabled = true;
                    
                    setTimeout(() => {
                        this.textContent = '📥 Exportar PDF';
                        this.disabled = false;
                        alert(`${reportType} exportado com sucesso!`);
                    }, 1500);
                });
            }
        });

        // Export complete reports functionality
        document.querySelectorAll('button').forEach(btn => {
            if (btn.textContent.includes('Relatório Completo (PDF)')) {
                btn.addEventListener('click', function() {
                    this.textContent = '⏳ Gerando PDF...';
                    this.disabled = true;
                    
                    setTimeout(() => {
                        this.textContent = '📊 Relatório Completo (PDF)';
                        this.disabled = false;
                        alert('Relatório completo exportado com sucesso! Arquivo salvo como "relatorio_completo_abril_2024.pdf"');
                    }, 3000);
                });
            }
            
            if (btn.textContent.includes('Dados para Excel (CSV)')) {
                btn.addEventListener('click', function() {
                    this.textContent = '⏳ Gerando CSV...';
                    this.disabled = true;
                    
                    setTimeout(() => {
                        this.textContent = '📈 Dados para Excel (CSV)';
                        this.disabled = false;
                        alert('Dados exportados com sucesso! Arquivo salvo como "dados_atelie_abril_2024.csv"');
                    }, 2000);
                });
            }
        });

        // Export history functionality
        document.querySelector('#admin-history button')?.addEventListener('click', function() {
            if (this.textContent.includes('Exportar Histórico')) {
                this.textContent = '⏳ Exportando...';
                this.disabled = true;
                
                setTimeout(() => {
                    this.textContent = '📥 Exportar Histórico (CSV)';
                    this.disabled = false;
                    alert('Histórico exportado com sucesso! Arquivo salvo como "historico_alteracoes.csv"');
                }, 1500);
            }
        });

        // Add logging functionality to track changes
        function logActivity(type, description, details = '') {
            const timestamp = new Date().toLocaleString('pt-BR');
            const historyTimeline = document.getElementById('historyTimeline');
            
            if (historyTimeline) {
                const newItem = document.createElement('div');
                newItem.className = 'history-item flex items-start space-x-4 p-4 bg-gray-50 rounded-lg';
                newItem.dataset.type = type;
                
                const iconMap = {
                    'payment': '💳',
                    'firing': '🔥',
                    'student': '👩‍🎨',
                    'settings': '⚙️',
                    'shop': '🛒'
                };
                
                const colorMap = {
                    'payment': 'bg-green-500',
                    'firing': 'bg-orange-500',
                    'student': 'bg-blue-500',
                    'settings': 'bg-purple-500',
                    'shop': 'bg-teal-500'
                };
                
                newItem.innerHTML = `
                    <div class="w-10 h-10 ${colorMap[type] || 'bg-gray-500'} rounded-full flex items-center justify-center text-white text-sm">${iconMap[type] || '📝'}</div>
                    <div class="flex-1">
                        <div class="flex items-center justify-between mb-1">
                            <p class="font-medium">${description}</p>
                            <span class="text-xs text-gray-500">${timestamp}</span>
                        </div>
                        <p class="text-sm text-gray-600">${details}</p>
                        <p class="text-xs text-gray-500">Por: Admin • Sistema</p>
                    </div>
                `;
                
                historyTimeline.insertBefore(newItem, historyTimeline.firstChild);
            }
        }

        // Track fee changes
        document.addEventListener('change', function(e) {
            if (e.target.closest('#feeTypesList') && e.target.type === 'number') {
                const feeTypeName = e.target.closest('.fee-type-item').querySelector('input[type="text"]').value;
                const newValue = e.target.value;
                logActivity('settings', `Valor de mensalidade alterado - ${feeTypeName}`, `Novo valor: R$ ${newValue},00`);
            }
            
            if (e.target.closest('#customFeesList') && e.target.type === 'number') {
                const studentSelect = e.target.closest('.custom-fee-item').querySelector('select');
                const studentName = studentSelect.options[studentSelect.selectedIndex].text;
                const newValue = e.target.value;
                logActivity('settings', `Mensalidade personalizada alterada - ${studentName}`, `Novo valor: R$ ${newValue},00`);
            }
        });

        // Student photo upload functionality
        document.querySelectorAll('.student-photo-upload').forEach(input => {
            input.addEventListener('change', function(e) {
                const file = e.target.files[0];
                if (file) {
                    // Validate file size (2MB max)
                    if (file.size > 2 * 1024 * 1024) {
                        alert('O arquivo é muito grande. Tamanho máximo: 2MB');
                        this.value = '';
                        return;
                    }
                    
                    // Validate file type
                    const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp'];
                    if (!validTypes.includes(file.type)) {
                        alert('Formato não suportado. Use JPG, PNG, GIF ou WebP');
                        this.value = '';
                        return;
                    }
                    
                    const reader = new FileReader();
                    const studentId = this.dataset.student;
                    const photoContainer = this.parentElement;
                    const photoImg = photoContainer.querySelector('.student-photo');
                    const defaultIcon = photoContainer.querySelector('span');
                    
                    reader.onload = function(e) {
                        const photoUrl = e.target.result;
                        
                        // Update photo display
                        photoImg.src = photoUrl;
                        photoImg.style.display = 'block';
                        photoImg.classList.remove('hidden');
                        defaultIcon.style.display = 'none';
                        
                        // Store in localStorage
                        try {
                            localStorage.setItem(`studentPhoto_${studentId}`, photoUrl);
                            console.log(`Foto do aluno ${studentId} salva`);
                        } catch (error) {
                            console.error('Erro ao salvar foto:', error);
                            alert('Erro ao salvar foto. Tente uma imagem menor.');
                        }
                        
                        // Log activity
                        logActivity('student', `Foto atualizada`, `Aluno: ${studentId}`);
                    };
                    
                    reader.onerror = function() {
                        alert('Erro ao ler o arquivo. Tente novamente.');
                    };
                    
                    reader.readAsDataURL(file);
                }
            });
        });

        // Load saved student photos on page load
        window.addEventListener('DOMContentLoaded', function() {
            document.querySelectorAll('.student-photo-upload').forEach(input => {
                const studentId = input.dataset.student;
                const savedPhoto = localStorage.getItem(`studentPhoto_${studentId}`);
                
                if (savedPhoto) {
                    const photoContainer = input.parentElement;
                    const photoImg = photoContainer.querySelector('.student-photo');
                    const defaultIcon = photoContainer.querySelector('span');
                    
                    photoImg.src = savedPhoto;
                    photoImg.style.display = 'block';
                    photoImg.classList.remove('hidden');
                    defaultIcon.style.display = 'none';
                    
                    photoImg.onerror = function() {
                        console.error(`Foto do aluno ${studentId} está corrompida, removendo...`);
                        localStorage.removeItem(`studentPhoto_${studentId}`);
                        this.style.display = 'none';
                        defaultIcon.style.display = 'flex';
                    };
                }
            });
        });

        // Clay purchase modal functionality
        document.getElementById('addClayPurchaseBtn')?.addEventListener('click', () => {
            showModal('addClayPurchaseModal');
        });

        document.getElementById('cancelClayPurchase')?.addEventListener('click', () => {
            hideModal('addClayPurchaseModal');
        });

        // Clay type select functionality
        document.getElementById('clayTypeSelect')?.addEventListener('change', function() {
            const customInput = document.getElementById('customClayType');
            if (this.value === 'custom') {
                customInput.classList.remove('hidden');
                customInput.required = true;
                customInput.focus();
            } else {
                customInput.classList.add('hidden');
                customInput.required = false;
                customInput.value = '';
            }
        });

        // Supplier select functionality
        document.getElementById('supplierSelect')?.addEventListener('change', function() {
            const customInput = document.getElementById('customSupplier');
            if (this.value === 'custom') {
                customInput.classList.remove('hidden');
                customInput.required = true;
                customInput.focus();
            } else {
                customInput.classList.add('hidden');
                customInput.required = false;
                customInput.value = '';
            }
        });

        // Add clay purchase form submission
        document.getElementById('addClayPurchaseForm')?.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const clayTypeSelect = document.getElementById('clayTypeSelect');
            const customClayType = document.getElementById('customClayType');
            const clayQuantity = document.getElementById('clayQuantity');
            const supplierSelect = document.getElementById('supplierSelect');
            const customSupplier = document.getElementById('customSupplier');
            const clayValue = document.getElementById('clayValue');
            const paymentStatus = document.getElementById('paymentStatus');
            
            // Get clay type
            let clayType = clayTypeSelect.value;
            if (clayType === 'custom') {
                clayType = customClayType.value;
            }
            
            // Get supplier
            let supplier = supplierSelect.value;
            if (supplier === 'custom') {
                supplier = customSupplier.value;
            }
            
            // Validate required fields
            if (!clayType || !clayQuantity.value || !supplier || !clayValue.value) {
                alert('Por favor, preencha todos os campos obrigatórios.');
                return;
            }
            
            // Create new clay purchase item
            const clayPurchasesList = document.getElementById('clayPurchasesList');
            const newPurchase = document.createElement('div');
            newPurchase.className = 'clay-purchase-item p-4 bg-gray-50 rounded-lg border';
            
            const currentDate = new Date().toLocaleDateString('pt-BR');
            const statusClass = paymentStatus.value === 'Pago' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800';
            const valueClass = paymentStatus.value === 'Pago' ? 'text-green-700' : 'text-orange-600';
            
            newPurchase.innerHTML = `
                <div class="flex justify-between items-start mb-2">
                    <div class="flex-1">
                        <h4 class="font-medium text-gray-800">${clayType} - ${clayQuantity.value}kg</h4>
                        <p class="text-sm text-gray-600">Fornecedor: ${supplier}</p>
                        <p class="text-xs text-gray-500">Compra em: ${currentDate}</p>
                    </div>
                    <div class="text-right">
                        <p class="font-bold ${valueClass}">R$ ${parseFloat(clayValue.value).toFixed(2).replace('.', ',')}</p>
                        <span class="${statusClass} px-2 py-1 rounded-full text-xs">${paymentStatus.value}</span>
                    </div>
                </div>
            `;
            
            // Add to the top of the list
            clayPurchasesList.insertBefore(newPurchase, clayPurchasesList.firstChild);
            
            // Update total
            updateClayPurchaseTotal();
            
            // Reset form
            this.reset();
            document.getElementById('customClayType').classList.add('hidden');
            document.getElementById('customSupplier').classList.add('hidden');
            
            // Close modal
            hideModal('addClayPurchaseModal');
            
            // Show success message
            alert('Compra de argila adicionada com sucesso!');
            
            // Log activity
            logActivity('student', 'Nova compra de argila registrada', `${clayType} - ${clayQuantity.value}kg - ${supplier} - R$ ${clayValue.value}`);
        });

        // Function to update clay purchase total
        function updateClayPurchaseTotal() {
            const clayPurchaseItems = document.querySelectorAll('.clay-purchase-item');
            let totalPending = 0;
            let pendingCount = 0;
            
            clayPurchaseItems.forEach(item => {
                const statusSpan = item.querySelector('span[class*="px-2"]');
                const valueP = item.querySelector('p[class*="font-bold"]');
                
                if (statusSpan && statusSpan.textContent.trim() === 'Pendente' && valueP) {
                    const value = parseFloat(valueP.textContent.replace(/[^\d,]/g, '').replace(',', '.'));
                    totalPending += value;
                    pendingCount++;
                }
            });
            
            // Update total display
            const totalElement = document.querySelector('.text-xl.font-bold.text-green-700');
            const countElement = document.querySelector('.text-sm.text-gray-600');
            
            if (totalElement) {
                totalElement.textContent = `R$ ${totalPending.toFixed(2).replace('.', ',')}`;
            }
            
            if (countElement) {
                countElement.textContent = `${pendingCount} compra${pendingCount !== 1 ? 's' : ''} pendente${pendingCount !== 1 ? 's' : ''}`;
            }
        }

        // Close modals when clicking outside
        document.querySelectorAll('[id$="Modal"]').forEach(modal => {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    hideModal(modal.id);
                }
            });
        });
    </script>
<script>(function(){function c(){var b=a.contentDocument||a.contentWindow.document;if(b){var d=b.createElement('script');d.innerHTML="window.__CF$cv$params={r:'98981776445bcaee',t:'MTc1OTYxNjY4OS4wMDAwMDA='};var a=document.createElement('script');a.nonce='';a.src='/cdn-cgi/challenge-platform/scripts/jsd/main.js';document.getElementsByTagName('head')[0].appendChild(a);";b.getElementsByTagName('head')[0].appendChild(d)}}if(document.body){var a=document.createElement('iframe');a.height=1;a.width=1;a.style.position='absolute';a.style.top=0;a.style.left=0;a.style.border='none';a.style.visibility='hidden';document.body.appendChild(a);if('loading'!==document.readyState)c();else if(window.addEventListener)document.addEventListener('DOMContentLoaded',c);else{var e=document.onreadystatechange||function(){};document.onreadystatechange=function(b){e(b);'loading'!==document.readyState&&(document.onreadystatechange=e,c())}}}})();</script></body>
</html>
