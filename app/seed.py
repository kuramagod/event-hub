from datetime import datetime, timedelta
from app.db import db_session
from app.models import Category, City, Event, User, Role


def seed_database():        
    categories_data = {
        'Концерты': '#918FFF',
        'Спорт': '#FF6B9D',
        'Театр и кино': '#4ECDC4',
        'Выставки': '#FFD93D',
        'Конференции': '#4A7CF7',
    }
    
    categories = []
    for cat_name, cat_color in categories_data.items():
        if not db_session.query(Category).filter_by(name=cat_name).first():
            category = Category(name=cat_name, color=cat_color)
            db_session.add(category)
            categories.append(category)
    
    db_session.commit()
    
    cities_data = [
        'Москва',
        'Санкт-Петербург',
        'Казань',
        'Екатеринбург',
        'Волгоград'
    ]
    
    cities = []
    for city_name in cities_data:
        if not db_session.query(City).filter_by(name=city_name).first():
            city = City(name=city_name)
            db_session.add(city)
            cities.append(city)
    
    db_session.commit()

    roles_data = [
        'Админ',
        'Пользователь'
    ]
    
    for role_name in roles_data:
        if not db_session.query(Role).filter_by(name=role_name).first():
            role = Role(name=role_name)
            db_session.add(role)
    
    db_session.commit()
    
    demo_user = db_session.query(User).filter_by(email='demo@example.com').first()
    if not demo_user:
        demo_user = User(
            fullname='Demo User',
            email='demo@example.com',
            phone='79991234567',
            role_id=1
        )
        demo_user.set_password('demo123')
        db_session.add(demo_user)
        db_session.commit()
    
    events_data = [
        {
            'name': 'Концерт Кисс',
            'slug': 'slug1',
            'image_url': 'https://i.pinimg.com/1200x/08/13/c8/0813c8aaa0ffbd0aa6fb58d1e2b5d101.jpg',
            'category_idx': 0,
            'city_idx': 0,
            'address': 'ул. Арбат, 12',
            'price': '1500',
            'description': 'Грандиозный концерт популярного исполнителя',
            'days_offset': 5
        },
        {
            'name': 'Чемпионат по футзалу',
            'slug': 'slug2',
            'image_url': 'https://i.pinimg.com/736x/b9/8f/ba/b98fba31a105d2c6640ddeaa6c66aca1.jpg',
            'category_idx': 1,
            'city_idx': 0,
            'address': 'Спортивный комплекс "Динамо"',
            'price': '500',
            'description': 'Региональный чемпионат по мини-футболу',
            'days_offset': 7
        },
        {
            'name': 'Спектакль "Гамлет"',
            'slug': 'slug3',
            'image_url': 'https://i.pinimg.com/736x/57/ff/da/57ffdab4bafbb5b7f85ea61161e56aea.jpg',
            'category_idx': 2,
            'city_idx': 1,
            'address': 'Александринский театр',
            'price': '2000',
            'description': 'Классическая постановка пьесы Шекспира',
            'days_offset': 10
        },
        {
            'name': 'Выставка современного искусства',
            'slug': 'slug4',
            'image_url': 'https://i.pinimg.com/736x/31/23/a5/3123a59a11cfc624d434a5bc7ec88ded.jpg',
            'category_idx': 3,
            'city_idx': 1,
            'address': 'Музей современного искусства',
            'price': '300',
            'description': 'Выставка работ молодых художников России',
            'days_offset': 3
        },
        {
            'name': 'IT Конференция "DevFest 2026"',
            'slug': 'slug5',
            'image_url': 'https://i.pinimg.com/1200x/b9/77/2b/b9772b2c9d32862033bd3cb6a7d3cb36.jpg',
            'category_idx': 4,
            'city_idx': 2,
            'address': 'Центр высоких технологий',
            'price': '1000',
            'description': 'Конференция для разработчиков и IT-специалистов',
            'days_offset': 14
        },
        {
            'name': 'Концерт "Симфоническая ночь"',
            'slug': 'slug6',
            'image_url': 'https://i.pinimg.com/736x/70/d1/b8/70d1b8569f8639c35406d11c461744af.jpg',
            'category_idx': 0,
            'city_idx': 3,
            'address': 'Концертный зал "Свердловск"',
            'price': '800',
            'description': 'Вечер классической музыки под руководством маэстро',
            'days_offset': 8
        },
        {
            'name': 'Марафон "Бегите со мной"',
            'slug': 'slug7',
            'image_url': 'https://i.pinimg.com/736x/bf/95/1a/bf951a0f653b5ad3c7f26c2a8d5120b3.jpg',
            'category_idx': 1,
            'city_idx': 4,
            'address': 'Центральный парк',
            'price': '200',
            'description': 'Благотворительный забег на 10 км',
            'days_offset': 12
        },
        {
            'name': 'Кинопремьера "Звёздные войны"',
            'slug': 'slug8',
            'image_url': 'https://i.pinimg.com/736x/11/b4/82/11b482983d71b7cec0a3cca0f1a49330.jpg',
            'category_idx': 2,
            'city_idx': 0,
            'address': 'Кинотеатр "Киносфера"',
            'price': '350',
            'description': 'Премьера долгожданного фильма с красной дорожкой',
            'days_offset': 6
        },
        {
            'name': 'Экспозиция "Золото древних цивилизаций"',
            'slug': 'slug9',
            'image_url': 'https://i.pinimg.com/736x/94/7c/f0/947cf043accdf30ff6ef8cf4f1455b2e.jpg',
            'category_idx': 3,
            'city_idx': 2,
            'address': 'Национальный музей Республики Татарстан',
            'price': '400',
            'description': 'Редкие артефакты из коллекций мировых музеев',
            'days_offset': 9
        },
        {
            'name': 'Семинар "Основы криптовалют"',
            'slug': 'slug10',
            'image_url': 'https://i.pinimg.com/1200x/a5/f9/e2/a5f9e2f443a895d1c28a697110ac81fd.jpg',
            'category_idx': 4,
            'city_idx': 3,
            'address': 'Бизнес-центр "Уральский"',
            'price': '600',
            'description': 'Обучающий семинар для начинающих инвесторов',
            'days_offset': 11
        }
    ]
    
    for event_data in events_data:
        existing_event = db_session.query(Event).filter_by(name=event_data['name']).first()
        if not existing_event:
            event_date = datetime.now().replace(second=0, microsecond=0) + timedelta(days=event_data['days_offset'])
            
            event = Event(
                name=event_data['name'],
                slug=event_data['slug'],
                category_id=categories[event_data['category_idx']].id,
                city_id=cities[event_data['city_idx']].id,
                address=event_data['address'],
                price=event_data['price'],
                date=event_date,
                description=event_data['description'],
                image_url=event_data['image_url'],
                user_id=demo_user.id,
            )
            db_session.add(event)
    
    db_session.commit()