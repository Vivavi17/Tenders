  # Tenders avito

Приложение для работы с тендерами.

### Перед запуском

Убедитесь что БД существует и содержит сущности:

Пользователь (User):
 

    CREATE TABLE employee (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50) UNIQUE NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );


Организация (Organization):

    CREATE TYPE organization_type AS ENUM (
    'IE',
    'LLC',
    'JSC'
    );

organization

    CREATE TABLE organization (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    type organization_type,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

organization_responsible

    CREATE TABLE organization_responsible (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID REFERENCES organization(id) ON DELETE CASCADE,
    user_id UUID REFERENCES employee(id) ON DELETE CASCADE
    );


### Переменные окружения
 
 Создать **.env** по примеру файла **.env-example**,  если файла нет, он создастся автоматически.
 
  ### Запуск приложения

Создание образа `make build`

Запуск контейнера `make run`