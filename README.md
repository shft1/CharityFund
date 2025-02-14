# _**QRKot**_ (новая версия)
[прошлая версия проекта (без гугл-отчета)](https://github.com/shft1/CatCharityFund)

## **QRKot** - это приложение для Благотворительного фонда поддержки котов.

Описание: Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.

#### **Проекты**    
В Фонде QRKot может быть открыто несколько целевых проектов. У каждого проекта есть название, описание и сумма, которую планируется собрать. После того, как нужная сумма собрана — проект закрывается. Пожертвования в проекты поступают по принципу First In, First Out: все пожертвования идут в проект, открытый раньше других; когда этот проект набирает необходимую сумму и закрывается — пожертвования начинают поступать в следующий проект.  
#### **Пожертвования**  
Каждый пользователь может сделать пожертвование и сопроводить его комментарием. Пожертвования не целевые: они вносятся в фонд, а не в конкретный проект. Каждое полученное пожертвование автоматически добавляется в первый открытый проект, который ещё не набрал нужную сумму. Если пожертвование больше нужной суммы или же в Фонде нет открытых проектов — оставшиеся деньги ждут открытия следующего проекта. При создании нового проекта все неинвестированные пожертвования автоматически вкладываются в новый проект.  
#### **Пользователи**  
Целевые проекты создаются администраторами сайта. 
Любой пользователь может видеть список всех проектов, включая требуемые и уже внесенные суммы. Это касается всех проектов — и открытых, и закрытых.
Зарегистрированные пользователи могут отправлять пожертвования и просматривать список своих пожертвований.
#### **Отчет в гугл-таблицу**
Пользователю доступен отчет (отсортированный список со всеми закрытыми проектами по количеству времени) в гугл-таблице, сохраненный на его гугл-диске.

---

Как запустить проект ?  
1. Создайте виртуальное окружение:
   
    ```
    python3 -m venv venv
    ```
2. Активируете виртуальное окружение:  
   * Если у вас Linux/macOS
   	```
    source venv/bin/activate
    ```
	* Если у вас windows  
    ```
    source venv/scripts/activate
    ```
3. В активированное виртуальное окружение установите зависимости:
   ```
   pip install -r requirements.txt
   ```
4. Как заполнить .env
   - ENV_DATABASE_URL - адрес БД, в адресе необходимо указать асинхронный драйвер  
      (по умолчанию приложение работает на SQLite, с именем `fastapi.db` в корне проекта)
   - ENV_SECRET - секретный ключ, необходимый для генерации токена (можно указать любую строку)
   - ENV_FIRST_SUPERUSER_EMAIL - e-mail первого суперпользователя
   - ENV_FIRST_SUPERUSER_PASSWORD - пароль первого суперпользователя
   - TYPE, PROJECT_ID, PRIVATE_KEY_ID, PRIVATE_KEY, CLIENT_EMAIL, CLIENT_ID, AUTH_URI, TOKEN_URI, AUTH_PROVIDER_X509_CERT_URL, CLIENT_X509_CERT_URL, EMAIL - данные сервисного акканута в Google Cloud
5. Дабы удостовериться в корректной работе приложения, нужно, из корня проекта, запустить тесты:
   ```
   pytest
   ```
6. Применяем миграции:
   ```
   alembic upgrade head
   ```
6. Запуск приложения (после запуска приложения, будет автоматически создан первый суперпользователь с e-mail и password, указанным ранее:
   ```
   uvicorn app.main:app
   ```
7. Для получения ссылки на отчет нужно обратиться на адрес:
   ```
   .../google
   ```
