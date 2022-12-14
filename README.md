# Bot tests [![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/izveigor/bot-tests/blob/main/LICENSE) ![Tests](https://github.com/izveigor/bot-tests/actions/workflows/tests.yml/badge.svg)
![3](https://user-images.githubusercontent.com/68601180/186197495-51627433-ee85-4243-87cb-4e59a4ddb2f6.JPG)

(Ссылка на аватар бота - https://ru.wikipedia.org/wiki/HAL_9000#/media/%D0%A4%D0%B0%D0%B9%D0%BB:HAL9000.svg)

Телеграм бот, создающий тесты.

## Описание
Бот создан для создания и отображения тестов разных тематик. Любой пользователь может создать свой собственный тест, загрузив оформленный по правилам json-файл.

В возможностях бота входят:
- Отображение описания теста (допускается использование цифровых изображений с помощью url адреса)
- Возможность начать решение теста
- Отображение вопроса теста (допускается использование цифровых изображений с помощью url адреса)
- Возможность ответить на вопрос с помощью следующих элементов интерфейса:

| Название элемента интерфейса | Назначение | Внешний вид |
| --------------------| ----------------------------------- | --- |
| Поле редактирования | Стандартное поле ввода в Телеграме  | ![input](https://user-images.githubusercontent.com/68601180/186197721-ebb357f4-add1-42da-b0b6-6d687842d18c.JPG)|
| Кнопка              | Кнопка с текстовым значением ответа | ![button](https://user-images.githubusercontent.com/68601180/186197585-6e7a057e-41be-42e7-b977-41d836dc72b9.JPG)|
| Флаговая кнопка     | Можно выбрать несколько ответов     | ![checkbox](https://user-images.githubusercontent.com/68601180/186197709-829defad-3e5d-43fd-b91e-92cc34ed6345.JPG)|

- Отображение результата теста пользователю (количество и процент правильных ответов, описание результата теста)
- Возможность преждевременно закончить тест
- Возможность создать свой тест с помощью json-документа
- Проверка правильности json-файла, оповещение пользователю о проблемах с файлом.
- Возможность удалить тест.
- Просмотр инструкции по командам бота и созданию своего первого теста
- Последовательное создание теста

## Запуск
Для того чтобы запустить бота, необходимо выполнить поэтапную инструкцию:
1) Скачать исходник кода (с помощью приложения или сайта Github или с помощью команды git clone)
2) Зайти в файл config/.prod.env и изменить значение TELEGRAM_TOKEN на свой токен (см. https://core.telegram.org/bots/api)
```
TELEGRAM_TOKEN=Токен
```
3) В главной папке запустить docker-compose
```
$ docker-compose up --build
```
4) Зайти в телеграм, найти своего бота и начать беседу

## Как создать тест с помощью последовательных операций
Пропишите команду /create и отвечайте на вопросы, который задал вам бот. После того, как вы ответили на все вопросы, бот автоматически создаст тест.

## Как создать тест с помощью json (Пример)
Ниже написана поэтапная инструкция с примером по созданию теста. В качестве примера создадим исторический тест по первым правителям Руси.
1) Заходим в любой редактор кода и создаем файл с любым именем с разрешением json (В нашем примере файл будет иметь название history.json)
2) Заходим в код и начинаем заполнять первое поле "command"

history.json:
```
{
    "command": "/test_FirstRussianRulers",
}
```

Поле "command" определяет команду Телеграм бота, с помощью которой можно посмотреть описание теста и начать его. У команды есть обязательный префикс "/test_", благодаря этому префиксу бот сможет различить тест от другой команды. После префикса вводится латинские буквы алфавита и другие символы.

3) Далее, мы должны придумать название теста. Для этого заполним поле "name".

history.json
```
{
    "command": "/test_FirstRussianRulers",
    "name": "Первые правители России",
}
```

4) Пользователь пока что ничего не знает о нашем тесте, и нам необходимо заинтересовать его. Для этого используем поле "description" для описания нашего теста:

history.json
```
{
    ...
    "name": "Первые правители России",
    "description": {
        "text": "В этом тесте продемонстрированы вопросы касательно раннего существования древнерусского государства в период правления от Рюрика до Ярослава Мудрого. Вопросы и ответы теста полностью соответсвуют историческому документу \"Повесть временных лет\" монаха Нестора Печерского. Этот тест поможет вам запомнить даты и события, полезные для уроков истории.",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/14_2_List_of_Radzivill_Chron.jpg/800px-14_2_List_of_Radzivill_Chron.jpg"
    },
}
```

Обратите внимание, что поле "description" в действительности отличается от предыдущих полей. Связано это с тем, что это поле представлено в виде словаря с двумя ключами: text и url. "text" представляет из себя тестовое содержание описания теста, тогда как "url" показывает нам интересную картинку.

5) Начинаем заполнять самую главную деталь в любом тесте - вопросы. Поле "questions" представляет собой массив из словарей, в которых содержатся необходимые элемента для представления вопроса.

history.json
```
    ...
    "description": {
        "text": "В этом тесте продемонстрированы вопросы касательно раннего существования древнерусского государства в период правления от Рюрика до Ярослава Мудрого. Вопросы и ответы теста полностью соответсвуют историческому документу \"Повесть временных лет\" монаха Нестора Печерского. Этот тест поможет вам запомнить даты и события, полезные для уроков истории.",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/14_2_List_of_Radzivill_Chron.jpg/800px-14_2_List_of_Radzivill_Chron.jpg"
    }
    "questions": [
        // Все вопросы мы будем заполнять здесь
    ],
```

6) Начинаем создавать наш вопрос, и первое, что необходимо сделать, это написать описание вопроса. Для этого, как и для поля "description" можно добавить картинку с текстом. Воспользуемся полем "body":

history.json
```
    ...
    "questions": [
        {
            "body": {
                "text": "В каком году произошло событие \"Призвание варягов\"?",
                "url": "https://upload.wikimedia.org/wikipedia/commons/6/69/Radzivill_chronicle_015.jpg"
            },
        }
    ]
```

7) Теперь выберем необходимый элемент интерфейса, который подходит для нашего вопроса. Здесь нам подойдет интерфейс "input" (поле редактирования).

history.json
```
            "body": {
                "text": "В каком году произошло событие \"Призвание варягов\"?",
                "url": "https://upload.wikimedia.org/wikipedia/commons/6/69/Radzivill_chronicle_015.jpg"
            },
            "widget": {
                "type": "input"
            },
```
8) После введения пользователем своего ответа, сервер должен проверить его правильность. Для этого воспользуемся полем "answer" и напишем правильный ответ.

history.json
```
            ...
            "widget": {
                "type": "input"
            },
            "answer": "862",
```

9) После того, как пользователь ввел ответ, он наверняка хотел бы узнать его разъяснение (это может пригодиться не только в тех случаях, когда он ввел неправильный ответ). Заполним поле "answer_explanation" информацией о событиях 862 года.
```
            "answer": "862",
            "answer_explanation": "В 862 году произошло знаменитое событие \"Призвание варягов\", которое ознаменовало появление нового могущественного государства в средневековой Европе - Руси. На территорию современной России прибыли княжить три брата - Рюрик, Синеус и Трувор. Потомки Рюрика по мужской линии правили Русским государством до 1610 года."
```

10) Создадим Еще один вопрос, но изменим пользовательский интерфейс на кнопку:

history.json
```
            ...
        },
        {
            "body": "Выберите имя следующего правителя России после Рюрика:",
            "widget": {
                "type": "button",
                "body": [
                    "Игорь",
                    "Олег",
                    "Ольга",
                    "Владимир"
                ]
            },
            "answer": 2,
            "answer_explanation": {
                "text": "После Рюрика правил его соплеменник - Олег Вещий. Это было связано с тем фактом, что единственный сын Рюрика - Игорь - был малолетнего возраста и не смог сам управлять государством. Олег правил Россией с 879 по 912 год.",
                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/%D0%9F%D1%80%D0%B8%D0%BD%D0%BE%D1%88%D0%B5%D0%BD%D0%B8%D0%B5_%D0%BA%D0%BD%D1%8F%D0%B7%D1%8E_%D0%9E%D0%BB%D0%B5%D0%B3%D1%83_%D0%B4%D0%B0%D0%BD%D0%B8_%D0%BF%D0%BE%D0%BA%D0%BE%D1%80%D0%B5%D0%BD%D0%BD%D1%8B%D0%BC%D0%B8_%D0%BD%D0%B0%D1%80%D0%BE%D0%B4%D0%B0%D0%BC%D0%B8.jpg/1920px-%D0%9F%D1%80%D0%B8%D0%BD%D0%BE%D1%88%D0%B5%D0%BD%D0%B8%D0%B5_%D0%BA%D0%BD%D1%8F%D0%B7%D1%8E_%D0%9E%D0%BB%D0%B5%D0%B3%D1%83_%D0%B4%D0%B0%D0%BD%D0%B8_%D0%BF%D0%BE%D0%BA%D0%BE%D1%80%D0%B5%D0%BD%D0%BD%D1%8B%D0%BC%D0%B8_%D0%BD%D0%B0%D1%80%D0%BE%D0%B4%D0%B0%D0%BC%D0%B8.jpg"
            }
        },
```

Добавление элемента интерфейса "Кнопка" немного отличается от поля редактирования. Внутри поля "widget" присутствует два ключа: "type" и "body".
Первый ключ представлюет собой тип элемента интерфейса, тогда как второй добавляет варианты ответа на вопрос. Значение поля "answer" должен принадлежать целочисленному типу данных, где число отождествляет себя с порядковым значением правильного ответа (в нашем случае правильный ответом является 2-я кнопка с текстовым значением "Олег").

11) Создадим последний вопрос нашего теста с элементом интерфейса "checkbox" (флаговая кнопка). Создание этого элемента интерфейса аналогично с созданием "Кнопки". Вся разница состоит в том, что ответом на вопрос является несколько правильных утверждений, поэтому поле "answer" является массивом, состоящего из целочисленных чисел (порядковых номеров правильных ответов).

history.json
```
            ...
        },
        {
            "body": "Выберите города, которые существовали в конце X века:",
            "widget": {
                "type": "checkbox",
                "body": [
                    "Великий Новгород",
                    "Киев",
                    "Москва",
                    "Ростов"
                ]
            },
            "answer": [1, 2, 4],
            "answer_explanation": {
                "text": "Москва была основана в 1147 году ростово-суздальским князем Юрием Долгоруким. Остальные города были основаны до начала XI века"
            }
        }
    ],
```

12) Мы создали все вопросы теста. Напоследок нам необходимо объяснить пользователю его результат: похвалить пользователя за его обширные знания в истории образования Русского государства или посоветовать ему прочитать дополнительную литературу для улучшения своего результата. Для достижения этой цели мы заполним поле "result_explanation":

```
    "questions": [
        // Все вопросы, которые мы написали сверху
    ],
    "result_explanation": {
        "0": "Вам необходимо поучить историю образования Руси, вот статьи из Википедии, которые введут вас в курс дела:\n- Статья о Рюрике: https://ru.wikipedia.org/wiki/%D0%A0%D1%8E%D1%80%D0%B8%D0%BA\n- Статья об Игоре: https://ru.wikipedia.org/wiki/%D0%98%D0%B3%D0%BE%D1%80%D1%8C_%D0%A0%D1%8E%D1%80%D0%B8%D0%BA%D0%BE%D0%B2%D0%B8%D1%87\n- Статья об Ольге: https://ru.wikipedia.org/wiki/%D0%9E%D0%BB%D1%8C%D0%B3%D0%B0_(%D0%BA%D0%BD%D1%8F%D0%B3%D0%B8%D0%BD%D1%8F_%D0%BA%D0%B8%D0%B5%D0%B2%D1%81%D0%BA%D0%B0%D1%8F)\n- Статья о Святославе: https://ru.wikipedia.org/wiki/%D0%A1%D0%B2%D1%8F%D1%82%D0%BE%D1%81%D0%BB%D0%B0%D0%B2_%D0%98%D0%B3%D0%BE%D1%80%D0%B5%D0%B2%D0%B8%D1%87\n- Статья о Владимире: https://ru.wikipedia.org/wiki/%D0%92%D0%BB%D0%B0%D0%B4%D0%B8%D0%BC%D0%B8%D1%80_%D0%A1%D0%B2%D1%8F%D1%82%D0%BE%D1%81%D0%BB%D0%B0%D0%B2%D0%B8%D1%87",
        "2": {
            "text": "Вы замечательно знаете историю образования Руси!",
            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Olga_and_emperor_Konstantin_%28Sofia_of_Kiev_cathedral%29_2.jpg/411px-Olga_and_emperor_Konstantin_%28Sofia_of_Kiev_cathedral%29_2.jpg"
        }
    }
}
```

Вам может показаться непонятным цифры в качестве ключей, но на самом деле они обозначают интервалы выдачи объяснений по количеству правильных ответов. Цифра "0" обозначает, что описание результата соответствующее цифре выдается, если пользователь набрал от 0 баллов. Верхняя граница этого значения служит следующая цифра в сортированном порядке - цифра "2". При наступлении количества правильных ответов больше или равных 2 нам выдается объяснение уже этой цифры.

13) На этом этапе создание json-файла подошло к концу. Сохраните его и сжайте его в zip-файл (в zip-файле должен быть только json-файл). Далее зайдите в Телеграм в разделе бота с тестами и нажмите на "скрепку" (отправка медии боту). После этого загрузите ваш файл и отправьте сообщение (caption) "/create" боту. Подождав несколько секунд, у вас должно появиться сообщение об успешности загрузки теста(если у вас появилась ошибка, то сверьте свой json-файл с нашим, полный текст json-файла смотрите внизу). Далее, пропишите команду "/my_tests" и убедитесь, что ваш тест был полностью загружен на сервер.

На этом этапе создание теста подошло к концу. Если вы хотите начать тест, то пропишите команду "/test_FirstRussianRulers", после которой вам высветится описание теста, далее нажмите или пропишите команду "/start_test", и после этого у вас будут появляться вопросы этого теста.

Результат:

![1](https://user-images.githubusercontent.com/68601180/186197441-e6d1e22e-aa35-4b98-972f-2695643aff2c.JPG)
![2](https://user-images.githubusercontent.com/68601180/186197480-ffec0a0b-b5ec-413f-a940-0449ebe9305b.JPG)
![3](https://user-images.githubusercontent.com/68601180/186197495-51627433-ee85-4243-87cb-4e59a4ddb2f6.JPG)
![4](https://user-images.githubusercontent.com/68601180/186197505-dc8377d6-c06a-44ba-b50f-5a1b6e29995e.JPG)
![5](https://user-images.githubusercontent.com/68601180/186197532-235f6bbe-dc0c-4fda-a68d-7dda5636f0a8.JPG)

Ниже представлен полный текст json-файла, написанного в примере:

history.json
```
{
    "command": "/test_FirstRussianRulers",
    "name": "Первые правители России",
    "description": {
        "text": "В этом тесте продемонстрированы вопросы касательно раннего существования древнерусского государства в период правления от Рюрика до Ярослава Мудрого. Вопросы и ответы теста полностью соответсвуют историческому документу \"Повесть временных лет\" монаха Нестора Печерского. Этот тест поможет вам запомнить даты и события, полезные для уроков истории.",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/14_2_List_of_Radzivill_Chron.jpg/800px-14_2_List_of_Radzivill_Chron.jpg"
    },
    "questions": [
        {
            "body": {
                "text": "В каком году произошло событие \"Призвание варягов\"?",
                "url": "https://upload.wikimedia.org/wikipedia/commons/6/69/Radzivill_chronicle_015.jpg"
            },
            "widget": {
                "type": "input"
            },
            "answer": "862",
            "answer_explanation": "В 862 году произошло знаменитое событие \"Призвание варягов\", которое ознаменовало появление нового могущественного государства в средневековой Европе - Руси. На территорию современной России прибыли княжить три брата - Рюрик, Синеус и Трувор. Потомки Рюрика по мужской линии правили Русским государством до 1610 года."
        },
        {
            "body": "Выберите имя следующего правителя России после Рюрика:",
            "widget": {
                "type": "button",
                "body": [
                    "Игорь",
                    "Олег",
                    "Ольга",
                    "Владимир"
                ]
            },
            "answer": 2,
            "answer_explanation": {
                "text": "После Рюрика правил его соплеменник - Олег Вещий. Это было связано с тем фактом, что единственный сын Рюрика - Игорь - был малолетнего возраста и не смог сам управлять государством. Олег правил Россией с 879 по 912 год.",
                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/%D0%9F%D1%80%D0%B8%D0%BD%D0%BE%D1%88%D0%B5%D0%BD%D0%B8%D0%B5_%D0%BA%D0%BD%D1%8F%D0%B7%D1%8E_%D0%9E%D0%BB%D0%B5%D0%B3%D1%83_%D0%B4%D0%B0%D0%BD%D0%B8_%D0%BF%D0%BE%D0%BA%D0%BE%D1%80%D0%B5%D0%BD%D0%BD%D1%8B%D0%BC%D0%B8_%D0%BD%D0%B0%D1%80%D0%BE%D0%B4%D0%B0%D0%BC%D0%B8.jpg/1920px-%D0%9F%D1%80%D0%B8%D0%BD%D0%BE%D1%88%D0%B5%D0%BD%D0%B8%D0%B5_%D0%BA%D0%BD%D1%8F%D0%B7%D1%8E_%D0%9E%D0%BB%D0%B5%D0%B3%D1%83_%D0%B4%D0%B0%D0%BD%D0%B8_%D0%BF%D0%BE%D0%BA%D0%BE%D1%80%D0%B5%D0%BD%D0%BD%D1%8B%D0%BC%D0%B8_%D0%BD%D0%B0%D1%80%D0%BE%D0%B4%D0%B0%D0%BC%D0%B8.jpg"
            }
        },
        {
            "body": "Выберите города, которые существовали в конце X века:",
            "widget": {
                "type": "checkbox",
                "body": [
                    "Великий Новгород",
                    "Киев",
                    "Москва",
                    "Ростов"
                ]
            },
            "answer": [1, 2, 4],
            "answer_explanation": {
                "text": "Москва была основана в 1147 году ростово-суздальским князем Юрием Долгоруким. Остальные города были основаны до начала XI века"
            }
        }
    ],
    "result_explanation": {
        "0": "Вам необходимо поучить историю образования Руси, вот статьи из Википедии, которые введут вас в курс дела:\n- Статья о Рюрике: https://ru.wikipedia.org/wiki/%D0%A0%D1%8E%D1%80%D0%B8%D0%BA\n- Статья об Игоре: https://ru.wikipedia.org/wiki/%D0%98%D0%B3%D0%BE%D1%80%D1%8C_%D0%A0%D1%8E%D1%80%D0%B8%D0%BA%D0%BE%D0%B2%D0%B8%D1%87\n- Статья об Ольге: https://ru.wikipedia.org/wiki/%D0%9E%D0%BB%D1%8C%D0%B3%D0%B0_(%D0%BA%D0%BD%D1%8F%D0%B3%D0%B8%D0%BD%D1%8F_%D0%BA%D0%B8%D0%B5%D0%B2%D1%81%D0%BA%D0%B0%D1%8F)\n- Статья о Святославе: https://ru.wikipedia.org/wiki/%D0%A1%D0%B2%D1%8F%D1%82%D0%BE%D1%81%D0%BB%D0%B0%D0%B2_%D0%98%D0%B3%D0%BE%D1%80%D0%B5%D0%B2%D0%B8%D1%87\n- Статья о Владимире: https://ru.wikipedia.org/wiki/%D0%92%D0%BB%D0%B0%D0%B4%D0%B8%D0%BC%D0%B8%D1%80_%D0%A1%D0%B2%D1%8F%D1%82%D0%BE%D1%81%D0%BB%D0%B0%D0%B2%D0%B8%D1%87",
        "2": {
            "text": "Вы замечательно знаете историю образования Руси!",
            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Olga_and_emperor_Konstantin_%28Sofia_of_Kiev_cathedral%29_2.jpg/411px-Olga_and_emperor_Konstantin_%28Sofia_of_Kiev_cathedral%29_2.jpg"
        }
    }
}
```
