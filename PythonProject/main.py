from graphviz import Digraph

# Создаем диаграмму вариантов использования
dot = Digraph(format='png')

# Определяем стили
dot.attr('node', shape='ellipse', fontname='Arial', fontsize='12')
dot.attr('edge', fontname='Arial', fontsize='10')

# Актёры
dot.node('Guest', 'Гость', shape='actor')
dot.node('FreeUser', 'Пользователь (бесплатный)', shape='actor')
dot.node('Subscriber', 'Пользователь (подписка)', shape='actor')
dot.node('Admin', 'Администратор', shape='actor')

# Варианты использования для гостя
dot.node('ViewParkingMap', 'Просмотр карты парковок')
dot.node('ViewParkingPrice', 'Просмотр стоимости парковки')
dot.node('FilterParking', 'Фильтрация парковок')
dot.node('NavigateToParking', 'Навигация до парковки')
dot.node('PayViaERIP', 'Оплата через ЕРИП')

dot.edge('Guest', 'ViewParkingMap')
dot.edge('Guest', 'ViewParkingPrice')
dot.edge('Guest', 'FilterParking')
dot.edge('Guest', 'NavigateToParking')
dot.edge('Guest', 'PayViaERIP')

# Варианты использования для бесплатного пользователя
dot.node('Register', 'Регистрация и создание аккаунта')
dot.node('ViewHistory', 'Просмотр истории парковок')
dot.node('FilterParkingFree', 'Фильтрация парковок по параметрам')
dot.node('PayInApp', 'Оплата парковки через приложение')
dot.node('ReceiveNotifications', 'Получение уведомлений')

dot.edge('FreeUser', 'Register')
dot.edge('FreeUser', 'ViewHistory')
dot.edge('FreeUser', 'FilterParkingFree')
dot.edge('FreeUser', 'PayInApp')
dot.edge('FreeUser', 'ReceiveNotifications')

# Варианты использования для подписчиков
dot.node('ViewAvailableSpots', 'Просмотр свободных мест')
dot.node('SaveFavorite', 'Сохранение "любимых" парковок')
dot.node('Heatmap', 'Просмотр heatmap загруженности')
dot.node('PersonalRecommendations', 'Персонализированные рекомендации')
dot.node('OfflineMaps', 'Использование офлайн-карт')
dot.node('BestParkingTime', 'Лучшее время для парковки')
dot.node('AccessClosedParkings', 'Доступ к закрытым парковкам')

dot.edge('Subscriber', 'ViewAvailableSpots')
dot.edge('Subscriber', 'SaveFavorite')
dot.edge('Subscriber', 'Heatmap')
dot.edge('Subscriber', 'PersonalRecommendations')
dot.edge('Subscriber', 'OfflineMaps')
dot.edge('Subscriber', 'BestParkingTime')
dot.edge('Subscriber', 'AccessClosedParkings')

# Варианты использования для администратора
dot.node('AddParking', 'Добавление новой парковки')
dot.node('EditParking', 'Редактирование парковки')
dot.node('DeleteParking', 'Удаление парковки')
dot.node('MonitorOccupancy', 'Мониторинг занятости')
dot.node('AnalyzeStats', 'Анализ статистики')
dot.node('ManageUsers', 'Управление пользователями')
dot.node('IntegratePayments', 'Интеграция платежных систем')
dot.node('UpdateSecurity', 'Обновление системы безопасности')

dot.edge('Admin', 'AddParking')
dot.edge('Admin', 'EditParking')
dot.edge('Admin', 'DeleteParking')
dot.edge('Admin', 'MonitorOccupancy')
dot.edge('Admin', 'AnalyzeStats')
dot.edge('Admin', 'ManageUsers')
dot.edge('Admin', 'IntegratePayments')
dot.edge('Admin', 'UpdateSecurity')

# Сохранение файла
file_path = "/mnt/data/use_case_diagram"
dot.render(file_path)

file_path + ".png"
